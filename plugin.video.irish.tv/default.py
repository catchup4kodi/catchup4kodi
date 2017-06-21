import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os

import json
import htmlcleaner

ADDON = xbmcaddon.Addon(id='plugin.video.irish.tv')

art = xbmc.translatePath(os.path.join(ADDON.getAddonInfo('path'),'resources','media/'))

TVTHREELIVE='rtmpe://fml.5011.edgecastcdn.net/205011/live playpath=mp4:tv3.mp4 app=205011/live pageURL=http://www.tv3.ie/3player/live/ swfUrl=http://www.tv3.ie/player/assets/flowplayer/flash/flowplayer.commercial-3.2.7.swf swfVfy=true live=true'

def CATEGORIES():
    addDir('Live','url',20,art+'RTE_Live.jpg','')
    addDir('Catchup','url',21,'','')
     

def CATEGORIES_LIVE():
    addDir('RTE 1','rte1',201,art+'RTE_One.jpg','')
    addDir('RTE 2','rte2',201,art+'RTE_Two.jpg','')
    addDir('RTE News','newsnow',201,art+'RTE_NewsNow.jpg','') 
    addDir('RTE Junior','rsw5',201,art+'rsw5.jpg','')
    addDir('3e','whatver',203,art+'3hd.png','')
    addLink('TV3',TVTHREELIVE,art+'TV3.jpg')
    try:
        GetTG4('url')
    except:pass    

    
def CATEGORIES_CATCHUP():
    addDir('RTE Player','rte1',4,art+'RTE.jpg','')
    addDir('TV3 Player','url',10,art+'TV3.jpg','')
    addDir('TG4 Player','url',9,art+'TG4.jpg','')

def TVTHREE():
    addDir('A to Z','url',8,art+'TV3.jpg','')
    addDir('Date Picker','url',13,art+'TV3.jpg','')



def char_range(c1, c2):
    
    for c in xrange(ord(c1), ord(c2)+1):
        yield chr(c)



def datepicker():
    import datetime,time

    a = datetime.datetime.today()
    numdays = 30
    dateList = []
    dateName = []
    for x in range (0, numdays):
        dateString =a - datetime.timedelta(days = x)
        dateList.append(dateString.strftime("%d-%m-%Y"))
        dateName.append(dateString.strftime("%a %d %b"))

    return dateList[xbmcgui.Dialog().select('Please Select', dateName)]


def TVTHREE_DAYPICKER(name,url):
 
    url='http://www.tv3.ie/3player/byday/tv3/'+str(datepicker())
 
    link=OPEN_URL(url)  
    match=re.compile('data-focus-h="844">.+?<a href=".+?"><img src="(.+?)" alt="(.+?)"',re.DOTALL).findall(link)
    for iconimage ,NAME in match:
        URL=iconimage.replace('http://content.tv3.ie','http://wpc.5011.edgecastcdn.net/805011/origin').split('_preview')[0]+'.mp4'
        if not 'div>' in NAME:
            addLink(NAME,URL,iconimage)
            
        
def TVTHREE_CATCHUP(name):
    nameurl=[]
    urlurl=[]
    for name in char_range('A', 'Z'):
        nameurl.append(name)
        urlurl.append(name.lower())    
    url='http://www.tv3.ie/3player/a-z/%s/' % (urlurl[xbmcgui.Dialog().select('Please Select', nameurl)])
    link=OPEN_URL(url)  
    match=re.compile('<a href="(.+?)">(.+?)</a>.+?<span>(.+?)</span>',re.DOTALL).findall(link)
    for URL ,name , episode in match:
        name= name +' - ' +episode
        if 'Episode' in episode:
            addDir(name,'http://www.tv3.ie'+URL,11,iconimage,'')

            
            
def TVTHREE_PLAY(name,url):
    SHOW=url.split('show/')[1]
    link=OPEN_URL(url)
    CHECKER=url.split('tv3.ie/')[1]
    NAME=re.compile('meta property="og:title".+?content="(.+?)"').findall(link)[0]
    iconimage=re.compile('<meta property="og:image".+?content="(.+?)"').findall(link)[0]
    URL=iconimage.replace('http://content.tv3.ie','http://wpc.5011.edgecastcdn.net/805011/origin').split('_preview')[0]+'.mp4'
    if '-' in NAME:
        NAME=NAME.split('- ')[1]
        addLink(NAME,URL,iconimage)
    try:
        match=re.compile('<img src="(.+?)".+?<a href="(.+?)">(.+?)</a>',re.DOTALL).findall(link)
        for iconimage ,checkme, NAME in match:
            if CHECKER in checkme:
                URL=iconimage.replace('http://content.tv3.ie','http://wpc.5011.edgecastcdn.net/805011/origin').split('_preview')[0]+'.mp4'
                addLink(NAME,URL,iconimage)
    except:pass

    try:    
        amount= name.split(' - ')[1]
        amount=amount.split('Episode')[0]
        amount =int(amount)
        if amount > 6:
            n=6
            while n<amount:
                if n%6==0:
                  
                    OPENME='http://www.tv3.ie/player_2015/assets/ajax/video_page_load_more.php?showID=%s&offset=%s&type=all' % (SHOW,str(n))
           
                    link=OPEN_URL(OPENME)
                    match=re.compile('<img src="(.+?)".+?href=".+?">(.+?)</a>',re.DOTALL).findall(link)
                 
                    for iconimage , NAME in match:
                        URL=iconimage.replace('http://content.tv3.ie','http://wpc.5011.edgecastcdn.net/805011/origin').split('_preview')[0]+'.mp4'
                        addLink(NAME,URL,iconimage)
                n=n+1
    except:pass                
    
def GetRTE_CATEGORIES(url):
    addDir('Most Popular','http://www.rte.ie/player/gb/most-popular',5,art+'RTE_MostPopular.jpg','')    
    addDir('Latest','http://www.rte.ie/player/gb/date/latest',5,art+'RTE_Latest.jpg','')
    addDir('Categories','http://www.rte.ie/player/gb/categories',5,art+'RTE_Categories.jpg','')
    #addDir('Classics','http://www.rte.ie/player/gb/classics',5,'','')
    addDir('A to Z','http://www.rte.ie/player/gb/a-z/',6,art+'RTE_AtoZ.jpg','') 


def GetRTE_CATEGORIES_LINKS(name,url):
     genre=name

     link=OPEN_URL(url)
     select=[]
     returned=[]
     if 'Categories' in name:
         LINKS=link.split('thumbnail-module')
         for p in LINKS:
             try:
                 id=re.compile('href="(.+?)"').findall(p)[0]
                 name=re.compile('thumbnail-title">(.+?)</span>').findall(p)[0]
                 select.append(name)
                 returned.append('http://www.rte.ie'+id)
             except:pass
         link=OPEN_URL(returned[xbmcgui.Dialog().select('Please Select', select)])
     LINKS=link.split('thumbnail-module')
     uniques=[]
     for p in LINKS:
         try:
             id=re.compile('href=".+?/show/(.+?)/"').findall(p)[0]
             if 'popular' in url:name=re.compile('class="thumbnail-title">(.+?)<').findall(p)[0].strip()
             else:name=re.compile('img alt="(.+?)"').findall(p)[0]
             if 'Latest' in genre:
                 date=re.compile('thumbnail-date">(.+?)</span>',re.DOTALL).findall(p)[0]
             iconimage=re.compile('src="(.+?)"').findall(p)[0]
             NAME='[COLOR white]%s[/COLOR]'%name
             id=id.split('/')[1]
             if 'Latest' in genre:

                 addDir(NAME+' - '+date ,'http://feeds.rasset.ie/rteavgen/player/playlist?type=iptv&showId='+id,201,iconimage,'')                
             else:
                 if NAME not in uniques:
                     uniques.append(NAME)
                     addDir(NAME,'http://www.rte.ie/player/gb/show/'+id,7,iconimage,'')
         except:pass


              

def GetRTE_CATEGORIES_LINKS_AZ(url):    
     html=OPEN_URL(url)
     select=['A']
     returned=['http://www.rte.ie/player/gb/a-z/a/']
     match=re.compile('<td class=""><a href="(.+?)">(.+?)</a></td>').findall(html)
     for URL , TITLE in match:
         select.append(TITLE)
         returned.append('http://www.rte.ie'+URL)
         
     link=OPEN_URL(returned[xbmcgui.Dialog().select('Please Select', select)])
     LINKS=link.split('thumbnail-module')
     for p in LINKS:
         try:
             id=re.compile('href=".+?/show/(.+?)/"').findall(p)[0]
             name=re.compile('img alt="(.+?)"').findall(p)[0]
             iconimage=re.compile('src="(.+?)"').findall(p)[0]
             NAME='[COLOR white]%s[/COLOR]'%name
             id=id.split('/')[1]

             addDir(NAME,'http://www.rte.ie/player/gb/show/'+id,7,iconimage,'')
         except:pass


def GetRTE_CATEGORIES_LINKS_TO_PLAY(name,url,iconimage):

     ICON=iconimage
     TITLE=name.lower()
     TITLE=TITLE.replace('[color white]','').replace('[/color]','').strip()
     try:
         TITLE=TITLE.split(' -')[0]
     except:pass    
     link=OPEN_URL(url)
     LINKS=link.split('thumbnail-module')     
     for p in LINKS:
         try:
             id=re.compile('href=".+?/show/(.+?)/"').findall(p)[0]
             name=re.compile('img alt="(.+?)"').findall(p)[0]
             try:
                 date=re.compile('thumbnail-date">(.+?)<').findall(p)[0]
             except:date=re.compile('thumbnail-title">(.+?)<').findall(p)[0]
             iconimage=re.compile('src="(.+?)"').findall(p)[0]
             NAME='[COLOR white]%s[/COLOR]'%name
             id=id.split('/')[1]
             if name.lower().strip() in TITLE:
                 if 'episode' in date:
                     if '1 episode ' in date:
                         addDir(NAME+' - '+date,'http://feeds.rasset.ie/rteavgen/player/playlist?type=iptv&showId='+id,201,iconimage,'')
                     else:
                         addDir(NAME+' - '+date,'http://www.rte.ie/player/gb/show/'+id,7,iconimage,'')
                 else:
                     addDir(NAME+' - '+date,'http://feeds.rasset.ie/rteavgen/player/playlist?type=iptv&showId='+id,201,iconimage,'')
             else:
                 
                 #addDir('[COLOR white]%s[/COLOR]'%TITLE.title(),'http://feeds.rasset.ie/rteavgen/player/playlist?type=iptv&showId='+url.split('show/')[1],201,ICON,'')
                 break
         except:pass

         
        
    
def PLAY_RTE(name,url,iconimage):
    name=htmlcleaner.cleanUnicode(name)
    if 'feeds' in url:
        
        link=OPEN_URL(url)
        URL=re.compile('media:content url="(.+?)"').findall(link)[0]
        import F4MProxy
        player=F4MProxy.f4mProxyHelper()
        player.playF4mLink(URL, name,iconimage)
                     

    else:
        if 'f4m' in url:
            import F4MProxy
            player=F4MProxy.f4mProxyHelper()
            player.playF4mLink(url, name,iconimage)
        else:
            select=[]
            returned=[]
            r='http://www.rte.ie/manifests/%s.f4m'%url
            html=OPEN_URL(r)
            match=re.compile('href=".+?-(.+?)\.f4m"').findall(html)
            for i in match:
                select.append(i+'P')
                returned.append(i)
                
            link=(returned[xbmcgui.Dialog().select('Please Select', select)])
            stream='http://cdn.rasset.ie/hls-live/_definst_/%s/%s-%s.m3u8' %(url,url,link)
            liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
            liz.setInfo(type='Video', infoLabels={'Title':name})
            liz.setProperty("IsPlayable","true")
            liz.setPath(stream)
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

def replaceHTMLCodes(txt):
    import HTMLParser

    # Fix missing ; in &#<number>;
    txt = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", makeUTF8(txt))

    txt = HTMLParser.HTMLParser().unescape(txt)
    txt = txt.replace("&amp;", "&")
    return txt    
    
def makeUTF8(data):
    return data
    try:
        return data.decode('utf8', 'xmlcharrefreplace') # was 'ignore'
    except:
        s = u""
        for i in data:
            try:
                i.decode("utf8", "xmlcharrefreplace") 
            except:
                log("Can't convert character", 4)
                continue
            else:
                s += i
        return s  

                                                                      
def GetTG4(url):

        new_url='http://www.tg4.ie/ga/beo/baile'
        response=MOBILE_URL(new_url)
        match=re.compile("url = \'(.+?)'").findall(response)[0]
              
        addLink('TG4',match,art+'TG4.jpg')


def TG4_CATCHUP(name):

    link= OPEN_URL('http://www.tg4.ie/wp-content/themes/tg4-starter/assets/json/tg4data.json')#.encode('utf8')
    #print link.encode('ascii','ignore')
    import json
    data=json.loads(link)

    uniques=[]
    for field in data:
        id= field['id']
        iconimage=field['videoStillURL']
        description=htmlcleaner.cleanUnicode(field['shortDescription'])
        name=htmlcleaner.cleanUnicode(field['customFields']['seriestitle'])
        
        if name not in uniques:
            uniques.append(name)
            try:addDir(name,'url',12,iconimage,description)
            except:pass
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)


def TG4_PLAY(name,url):
    _NAME_ = name
    link= OPEN_URL('http://www.tg4.ie/wp-content/themes/tg4-starter/assets/json/tg4data.json')
    data=json.loads(link)
    
    uniques=[]
    for field in data:
        try:
            id= field['id']
            iconimage=field['videoStillURL']
            description=htmlcleaner.cleanUnicode(field['shortDescription'])
            name=htmlcleaner.cleanUnicode(field['customFields']['seriestitle'])
            Name =htmlcleaner.cleanUnicode(field['name'])
            date=field['customFields']['episode']
            if not 'Anois / Now' in date:
                if name in _NAME_ :

                    addDir(Name,str(id),202,iconimage,description)
        except:pass
    setView('episodes', '50')


def TG4_PLAY_LINK(name,url,iconimage):
    vid=url
    pubid=iconimage.split('pubId=')[1]
    stream_url='http://c.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId=%s&pubId=%s'% (vid,pubid)
    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title':name})
    liz.setProperty("IsPlayable","true")
    liz.setPath(stream_url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

    
        
def threeE(name,url,iconimage):
    import time
    TIME=str(time.time())
    TIME=TIME.split('.')[0]
    stream_url='http://csm-e.cds1.yospace.com/csm/extlive/tv3ie01,tv3-prd.m3u8?yo.ac=true&yo.sl=3&yo.po=5&yo.ls=1,2,3&unique='+ TIME
    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title':name})
    liz.setProperty("IsPlayable","true")
    liz.setPath(stream_url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)



 
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link


def MOBILE_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link    
    
    



   
    
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

def addDir(name,url,mode,iconimage,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        name=replaceHTMLCodes(name)
        name=name.strip()
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
        menu = []
        if mode ==200 or mode ==201 or mode ==202 or mode ==203:
            if not 'feeds' in url:
                if not 'f4m' in url:
                    if 'm3u8' in url:
                        liz.setProperty('mimetype', 'application/x-mpegURL')
                        liz.setProperty('mimetype', 'video/MP2T')
                    liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)          
        else:
            menu.append(('Play All Videos','XBMC.RunPlugin(%s?name=%s&mode=2001&iconimage=None&url=%s)'% (sys.argv[0],name,url)))
            liz.addContextMenuItems(items=menu, replaceItems=False)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
        
def addLink(name,url,iconimage):
        name=replaceHTMLCodes(name.strip())
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        
 
        
def setView(content, viewType):
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
                      
               
params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
   
        
#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        GetRTE(url)

elif mode==3:
        print ""+url
        GetTG4(url)

elif mode==4:
        print ""+url
        GetRTE_CATEGORIES(url)

elif mode==5:
        print ""+url
        GetRTE_CATEGORIES_LINKS(name,url)

elif mode==6:
        print ""+url
        GetRTE_CATEGORIES_LINKS_AZ(url)

elif mode==7:
        print ""+url
        GetRTE_CATEGORIES_LINKS_TO_PLAY(name,url,iconimage)

elif mode==8:
        print ""+url
        TVTHREE_CATCHUP(name)


elif mode==9:
        print ""+url
        TG4_CATCHUP(name)        

elif mode==10:
        print ""+url
        TVTHREE()

elif mode==11:
        print ""+url
        TVTHREE_PLAY(name,url)


elif mode==12:
        print ""+url
        TG4_PLAY(name,url)

elif mode==13:
        print ""+url
        TVTHREE_DAYPICKER(name,url)   

elif mode==20:
        CATEGORIES_LIVE()

elif mode==21:
        CATEGORIES_CATCHUP()
        
elif mode==200:

        PLAY_STREAM(name,url,iconimage)

elif mode==201:

        PLAY_RTE(name,url,iconimage)


elif mode==202:
        print ""+url
        TG4_PLAY_LINK(name,url,iconimage)

elif mode==203:
        print ""+url
        threeE(name,url,iconimage)         

elif mode==2001:

        playall(name,url)        
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
