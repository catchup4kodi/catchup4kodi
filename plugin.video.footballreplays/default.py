# -*- coding: utf-8 -*-
import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os
import datetime
import time
import net
net=net.Net()

PLUGIN='plugin.video.footballreplays'
ADDON = xbmcaddon.Addon(id='plugin.video.footballreplays')
maxVideoQuality = ADDON.getSetting("maxVideoQuality")
xbmc.log('maxVideoQuality: %s'%maxVideoQuality,2)
qual = ["480p", "720p", "1080p"]
maxVideoQuality = qual[int(maxVideoQuality)]
xbmc.log('maxVideoQuality: %s'%maxVideoQuality,2)

datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
cookie_path = os.path.join(datapath, 'cookies')
cookie_jar = os.path.join(cookie_path, "football.lwp")
    
VERSION = "1.0.2"
PATH = "Football Replays"            
UATRACK="UA-35537758-1"  
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
cookie_path = os.path.join(datapath, 'cookies')
cookie_jar = os.path.join(cookie_path, "football.lwp")

if os.path.exists(cookie_path) == False:
        os.makedirs(cookie_path)
        net.save_cookies(cookie_jar)
        
def CATEGORIES():
    addDir('Full Matches','url',3,'','1')
    # addDir('Search Team','url',4,'','1')
    addDir('Highlights','url',5 ,'','1')
    setView('movies', 'main') 
       #setView is setting the automatic view.....first is what section "movies"......second is what you called it in the settings xml  
 
    
def CATEGORIES2():
    link=OPEN_URL('http://livefootballvideo.com/fullmatch')
    r='<div class="cover"><a href="(.+?)" rel="bookmark" title="(.+?)".+?<img src="(.+?)".+? longdate" rel=".+?">(.+?)/(.+?)/(.+?)</p>'
    match=re.compile(r,re.DOTALL).findall(link)
  
    for url,name,iconimage,month,day,year in match:
        _date='%s/%s/%s'%(day,month,year)
        _name='%s-[COLOR yellow][%s][/COLOR]'%(name,_date)    
        addDir(_name,url,1,iconimage,'')
    addDir('Next Page >>','url',2,'','1')
    setView('movies', 'main') 
       #setView is setting the automatic view.....first is what section "movies"......second is what you called it in the settings xml  
       
def NEXTPAGE(page):
    pagenum=int(page) +1
    link=OPEN_URL('http://livefootballvideo.com/fullmatch/page/'+str(pagenum))
    r='<div class="cover"><a href="(.+?)" rel="bookmark" title="(.+?)">.+?<img src="(.+?)".+?<p class="postmetadata longdate" rel=".+?">(.+?)/(.+?)/(.+?)</p>'
    match=re.compile(r,re.DOTALL).findall(link)
    print match
    for url,name,iconimage,month,day,year in match:
        _date='%s/%s/%s'%(day,month,year)  
        _name='%s-[COLOR yellow][%s][/COLOR]'%(name,_date)    
        addDir(_name,url,1,iconimage,'')
    addDir('Next Page >>','url',2,'','1')
    setView('movies', 'main') 
                                                                      
def GETLINKS(name,url):#  cause mode is empty in this one it will go back to first directory
    xbmc.log('GETLINKS: %s'%url)
    links=OPEN_URL(url)
    links= links.split("class='heading-more open'><span>")
    xbmc.log('LINK LEN: %s'%len(links))
    for link in links:
        # try:
            language=link.split('<')[0]
            if len(language)>1:
                addDir ('[COLOR green]%s[/COLOR]'%language, url , 200 , '', '' )
                xbmc.log('LANGUAGE URL: %s'%url)
            if "proxy.link=lfv*" in link :
                import base64
                import decrypter
                match = re.compile('proxy\.link=lfv\*(.+?)&').findall(link)
                match = uniqueList(match)
                match = [decrypter.decrypter(198,128).decrypt(i,base64.urlsafe_b64decode('Y0ZNSENPOUhQeHdXbkR4cWJQVlU='),'ECB').split('\0')[0] for i in match]
                print match
                for url in match:

                    url = replaceHTMLCodes(url)
                    if url.startswith('//') : url = 'http:' + url
                    url = url.encode('utf-8')  
                    _name=url.split('://')[1] 
                    _name=_name.split('/')[0].upper()
                    addDir( name+' - [COLOR red]%s[/COLOR]'%_name , url , 200 , '' , '' )
            if "www.youtube.com/embed/" in link :
                r = 'youtube.com/embed/(.+?)"'
                match = re.compile(r,re.DOTALL).findall(link)
                yt= match[0]
                iconimage = 'http://i.ytimg.com/vi/%s/0.jpg' % yt.replace('?rel=0','')
                url = 'plugin://plugin.video.youtube/play/?video_id=%s' % yt.replace('?rel=0','')
                addDir( name+' - [COLOR red]YOUTUBE[/COLOR]' , url , 200 , iconimage , '' )
            if "dailymotion.com" in link :
                r = 'src="//www.dailymotion.com/embed/video/(.+?)"'
                match = re.compile(r,re.DOTALL).findall(link)
                xbmc.log('MATCH: %s'%match)
                for url in match :
                    addDir ( name+' - [COLOR red]DAILYMOTION[/COLOR]' , url , 200 , GETTHUMB(url), '' )
            if "streamable.com" in link :
                # r = 'src="https://streamable.com/s/.+?/(.+?)\?.+?"></iframe>'
                r = '<iframe src="(.+?)"'
                match = re.compile(r,re.DOTALL).findall(link)
                for url in match:
                    if 'streamable' in url:
                        addDir ( name+' - [COLOR red]STREAMABLE[/COLOR]' , url , 200 , GETTHUMB(url), '' )
            if "http://videa" in link :
                r = 'http://videa.+?v=(.+?)"'
                match = re.compile(r,re.DOTALL).findall(link)
                for url in match :
                    addDir (name+' - [COLOR red]VIDEA[/COLOR]',url,200,'', '' )
                    
            if "rutube.ru" in link :
                r = 'ttp://rutube.ru/video/embed/(.+?)\?'
                match = re.compile(r,re.DOTALL).findall(link)
                print match
                for url in match :
                    addDir (name+' - [COLOR red]RUTUBE[/COLOR]',url,200,'', '' )
            if 'cdn.playwire.com' in link :
                r = 'data-config="(.+?)"'
                match = re.compile(r,re.DOTALL).findall(link)
                for vid in match :
                    if not 'http' in vid:
                            vid='http:'+vid
                    url=vid.replace('zeus.json','manifest.f4m')
                    addDir (name+' - [COLOR red]PLAYWIRE[/COLOR]',url,200,'', '' )
            if "vk.com" in link :
                r = 'vk.com/(.+?)"'
                match = re.compile(r,re.DOTALL).findall(link)
                for url in match :
                    addDir (name+' - [COLOR red]VK.COM[/COLOR]','http://vk.com/'+url,200,'', '' )
            if "mail.ru" in link :
                r = 'http://videoapi.my.mail.ru/videos/embed/(.+?)\.html'
                match = re.compile(r,re.DOTALL).findall(link)
                for url in match :
                    addDir (name+' - [COLOR red]MAIL.RU[/COLOR]','http://videoapi.my.mail.ru/videos/%s.json'%url,200,'', '' )
            if "openload.co" in link :
                r = 'data-lazy-src="(.+?)"'
                match = re.compile(r,re.DOTALL).findall(link)
                for url in match :
                    addDir (name+' - [COLOR red]OPENLOAD.CO[/COLOR]',url,200,'', '' )
                r = 'iframe src="(.+?)"'
                match = re.compile(r,re.DOTALL).findall(link)
                for url in match :
                    if 'openload' in url:
                        addDir (name+' - [COLOR red]OPENLOAD.CO[/COLOR]',url,200,'', '' )
            if "//player.footballfullmatch" in link :
                r = 'src="(.+?player.footballfullmatch.com.+?)"'
                match = re.compile(r,re.DOTALL).findall(link)
                for url in match :
                    addDir (name+' - [COLOR red]FOOTBALLFULLMATCH.COM[/COLOR]',url,200,'', '' )
        # except:pass


                
def uniqueList(name):
    uniques = []
    for n in name:
        if n not in uniques:
            uniques.append(n)
    return uniques                     

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
        
def HIGHLIGHTS():
    link=OPEN_URL('http://livefootballvideo.com/highlights')
    r= '<div class="team home column">(.+?)&nbsp;.+?<a href="(.+?)" class="score">(.+?)</a>.+?">&nbsp;(.+?)</div>'
    match = re.compile ( r , re.DOTALL).findall (link)
    for team_a ,url,score,  team_b  in match :
        xbmc.log(score)
        if score.startswith('<span'):
            score = score.split('/span>')[1]
        if score.endswith('</span>'):
            score = score.split('<span')[0]
        name = '[COLOR white]%s[/COLOR] [COLOR yellow]%s[/COLOR] [COLOR white]%s[/COLOR]' % ( team_a ,score, team_b )
        iconimage = 'http://livefootballvideo.com'
        addDir(name,url,7,iconimage,'')
    addDir('Next Page >>' , 'url' , 6 , '' , '1' )
    setView('movies', 'default') 
    
def HIGHLIGHTS_NEXTPAGE( page ) :
    page_num =int ( page ) + 1
    link=OPEN_URL( 'http://livefootballvideo.com/highlights/page/' + str ( page_num ) )
    r= '<div class="team home column">(.+?)&nbsp;.+?<a href="(.+?)" class="score">(.+?)</a>.+?">&nbsp;(.+?)</div>'
    match = re.compile ( r , re.DOTALL).findall (link)
    for team_a ,url,score,  team_b  in match :
        name = '[COLOR white]%s[/COLOR] [COLOR yellow]%s[/COLOR] [COLOR white]%s[/COLOR]' % ( team_a ,score, team_b )
        iconimage = 'http://livefootballvideo.com'
        addDir(name,url,7,iconimage,'')
    addDir('Next Page >>' , 'url' , 6 , '' , '1' )
    setView('movies', 'default')    
    
def HIGHLIGHTS_LINKS(name,url):
    GETLINKS(name,url)
           
def Search():
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, 'Search Football Replays')
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText() .replace(' ','+')  # sometimes you need to replace spaces with + or %20#
            if search_entered == None:
                return False
        link=OPEN_MAGIC('https://cse.google.co.uk/cse?cx=partner-pub-9069051203647610:8413886168&ie=UTF-8&q=%s&sa=Search&ref=&gws_rd=cr&ei=GHF4WeipBdCjUPbqsIAN#gsc.tab=0&gsc.q=%s&gsc.page=1'%(search_entered,search_entered))
        xbmc.log('### LINK: %s'%link)
        match=re.compile('" href="(.+?)" onmousedown=".+?">(.+?)</a>').findall(link)
        for url,dirtyname in match: 
            import HTMLParser
            cleanname= HTMLParser.HTMLParser().unescape(dirtyname)
            name= cleanname.replace('<b>','').replace('</b>','')
            addDir(name,url,1,'','')
        setView('movies', 'default') 
              
def GETTHUMB(url):
    try:
        import json
        content = OPEN_URL('https://api.dailymotion.com/video/%s?fields=thumbnail_large_url'%url)
        data = json.loads(content)
        icon=data['thumbnail_large_url']
        return icon
    except:
        return ''   
        
def GrabRu(id):
    print id
    link = OPEN_URL('http://rutube.ru/api/play/trackinfo/%s/?format=xml'%str(id))
    r = '<m3u8>(.+?)</m3u8>'
    match = re.compile(r,re.DOTALL).findall(link)
    return match[0]

def getData(url,headers={}):
    net.save_cookies(cookie_jar)
    req = urllib2.Request(url)
    req.add_header('User-Agent', USER_AGENT)
    response = urllib2.urlopen(req)
    data=response.read()
    response.close()
    return data

def GrabMailRu(url):
    print 'RESOLVING VIDEO.MAIL.RU VIDEO API LINK'
      
    import json
    items = []
    quality = "???"
    data = getData(url)
    cookie = net.get_cookies()
    for x in cookie:

         for y in cookie[x]:

              for z in cookie[x][y]:
                   
                   l= (cookie[x][y][z])
    name=[]
    url=[]
    r = '"key":"(.+?)","url":"(.+?)"'
    match = re.compile(r,re.DOTALL).findall(data)
    for quality,stream in match:
        name.append(quality.title())
        test = str(l)
        test = test.replace('<Cookie ','')
        test = test.replace(' for .my.mail.ru/>','')
        url.append(stream +'|Cookie='+test)

    return url[xbmcgui.Dialog().select('Please Select Resolution', name)]
  
def GrabVidea(id):
    link = OPEN_URL('http://videa.hu/flvplayer_get_video_xml.php?v=%s&m=0'%str(id))
    name=[]
    url=[]
    r = 'version quality="(.+?)" video_url="(.+?)"'
    match = re.compile(r,re.DOTALL).findall(link)
    for quality,stream in match:
        name.append(quality.title())
        url.append(stream)
    return url[xbmcgui.Dialog().select('Please Select Resolution', name)]

def GrabVK(url):
    if not 'http:' in url:
            url='http:'+url
    print url.replace('amp;','')
    url=url.replace('amp;','')
    if 'ext.php' in url:
        html=OPEN_URL(url)
        r      ='"url(\d+)":"(.+?)"'
        name=[]
        url=[]
        match = re.compile(r,re.DOTALL).findall(html)
        for quality,stream in match:
            name.append(quality.replace('\\','')+'p')
            url.append(stream.replace('\/','/'))
        return url[xbmcgui.Dialog().select('Please Select Resolution', name)]
    
    else:
        try:
            dp = xbmcgui.DialogProgress()
            dp.create("Football Replays", '','Please Wait Trying to Resolve', '')
            if ADDON.getSetting('use_vk')== 'true':
                    number=ADDON.getSetting('vk_user')
                    password=ADDON.getSetting('vk_password')
                    
            else:
                    p=OPEN_URL('https://xunitytalk-repository.googlecode.com/svn/addons/plugin.video.footballreplays/accounts.txt')
                    from random import randint
                    match=re.compile('user=(.+?)pass=(.+?)"').findall (p)
                    b = int(randint(0,len(match)-1))
                    number= match[b][0]
                    password= match[b][1]
            html=LOGIN_VK(number,password,url)
            r      ='"url(\d+)":"(.+?)"'
            name=[]
            url=[]
            match = re.compile(r,re.DOTALL).findall(html)
            for quality,stream in match:
                name.append(quality.replace('\\','')+'p')
                url.append(stream.replace('\/','/'))
            return url[xbmcgui.Dialog().select('Please Select Resolution', name)]
            dp.close()
        except:
            dialog = xbmcgui.Dialog()
            dialog.ok("Football Replays", '','Sorry Video Is Private', '')
        
def LOGIN_VK(number,password,GET_URL):
    headers = {}
    headers.update({'Content-Type': 'application/x-www-form-urlencoded', 'Connection': 'keep-alive',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Encoding': 'gzip,deflate,sdch', 'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36'})
    
    html = net.http_GET('http://vk.com') 
    ip_h = re.search(r'ip_h\"\svalue=\"(.*?)\"', html.content, re.I)
    html = net.http_POST('https://login.vk.com/?act=login', {'act':'login','role':'al_frame','expire':'',
                                                             'captcha_sid':'','_origin':'http://vk.com','ip_h':ip_h.group(1),
                                                             'email':str(number),'pass':str(password)})
    if os.path.exists(cookie_path) == False:
        os.makedirs(cookie_path)
    net.save_cookies(cookie_jar)
    net.set_cookies(cookie_jar)  
    html = net.http_GET(GET_URL).content.replace('\\','')
    return html
     
def PLAYSTREAM(name,url,iconimage):
        if 'YOUTUBE' in name:
            link = str(url)
        elif 'VIDEA' in name:
            try:
                url=url.split('-')[1]
            except:
                url=url
            link = GrabVidea(url)
        elif 'VK.COM' in name:
            link = GrabVK(url)

        elif 'MAIL.RU' in name:
            link = GrabMailRu(url)
      
        elif 'RUTUBE' in name:
            try:
                html = 'http://rutube.ru/api/play/trackinfo/%s/?format=xml'% url.replace('_ru','')
                print html
                link = OPEN_URL(html)
                r = '<m3u8>(.+?)</m3u8>'
                match = re.compile(r,re.DOTALL).findall(link)
                if match:
                    link=match[0]
                else:
                    dialog = xbmcgui.Dialog()
                    dialog.ok("Football Replays", '','Sorry Video Is Private', '')
                    return
            except:
                dialog = xbmcgui.Dialog()
                dialog.ok("Football Replays", '','Sorry Video Is Private', '')
                return
        elif 'PLAYWIRE' in name:
            link = OPEN_URL(url)
            r = '<baseURL>(.+?)</baseURL>'
            base=  re.compile(r,re.DOTALL).findall(link)[0]
            h='media url="(.+?)"'
            files = re.compile(h,re.DOTALL).findall(link)[0]

            if base:
                link=base+'/'+files         
                
        elif 'DAILYMOTION' in name:
            import urlresolver
            link = 'http://www.dailymotion.com/embed/video/'+url
            link=urlresolver.resolve(str(link))

        elif 'FOOTBALLFULLMATCH.COM' in name:
            link = OPEN_URL(url).replace("'",'"')
            r = '"file": "(.+?)"'
            link=  re.compile(r,re.DOTALL).findall(link)[0]
  
        else:
            import urlresolver
            link=urlresolver.resolve(str(url))
        try:
            liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
            liz.setInfo( type="Video", infoLabels={ "Title": name} )
            liz.setProperty("IsPlayable","true")
            liz.setPath(link)
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
        except:pass
        
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
def OPEN_MAGIC(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent' , "Magic Browser")
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
 
# this is the listing of the items        
def addDir(name,url,mode,iconimage,page):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&page="+str(page)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name} )
        if mode == 200:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

# same as above but this is addlink this is where you pass your playable content so you dont use addDir you use addLink "url" is always the playable content         
def addLink(name,url,iconimage,description):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok 
        
# below tells plugin about the views                
def setView(content, viewType):
        # set content type so library shows more views and info
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
                            
params=get_params()
url=None
name=None
mode=None
iconimage=None
page=None


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
        page=int(params["page"])
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
        GETLINKS(name,url)
        
elif mode==2:
        NEXTPAGE(page)
        
elif mode==3:
        CATEGORIES2()
        
elif mode==4:
        Search()
        
elif mode==5:
        HIGHLIGHTS()
        
elif mode == 6 :
    HIGHLIGHTS_NEXTPAGE(page)
        
elif mode == 7 :
    HIGHLIGHTS_LINKS(name,url)
        
elif mode==200:
        PLAYSTREAM(name,url,iconimage)
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
