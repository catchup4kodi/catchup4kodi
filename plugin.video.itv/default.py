import urllib.request, urllib.parse, urllib.error,urllib.request,urllib.error,urllib.parse,re,sys,socket,os,datetime,xbmcplugin,xbmcgui, xbmcaddon,json
from hashlib import md5
import codecs

# external libs
sys.path.insert(0, xbmc.translatePath(os.path.join('special://home/addons/plugin.video.itv', 'lib')))
import utils, httplib2, http.client, logging, time
import datetime
import time

PLUGIN='plugin.video.itv'
ADDON = xbmcaddon.Addon(id=PLUGIN)
icon = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.itv', 'icon.png'))
foricon = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.itv', ''))
from bs4 import BeautifulSoup

# setup cache dir
__scriptname__  = 'ITV'
__scriptid__ = "plugin.video.itv"
__addoninfo__ = utils.get_addoninfo(__scriptid__)
__addon__ = __addoninfo__["addon"]
__settings__   = xbmcaddon.Addon(id=__scriptid__)



DIR_USERDATA   = xbmc.translatePath(__addoninfo__["profile"])
SUBTITLES_DIR  = os.path.join(DIR_USERDATA, 'Subtitles')
IMAGE_DIR      = os.path.join(DIR_USERDATA, 'Images')
favorites      = os.path.join(DIR_USERDATA, 'favorites')

if not os.path.isdir(DIR_USERDATA):
    os.makedirs(DIR_USERDATA)
if not os.path.isdir(SUBTITLES_DIR):
    os.makedirs(SUBTITLES_DIR)
if not os.path.isdir(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

def get_httplib():
    return httplib2.Http()

http = get_httplib()
       
# what OS?        
environment = os.environ.get( "OS", "xbox" )

def download_subtitles_HLS(url, offset):

    logging.info('subtitles at =%s' % url)
    outfile = os.path.join(SUBTITLES_DIR, 'itv.srt')
    fw = codecs.open(outfile, 'w', encoding='utf-8')
    
    if not url:
        fw.write("1\n0:00:00,001 --> 0:01:00,001\nNo subtitles available\n\n")
        fw.close()
        return outfile

    try:
        txt = OPEN_URL(url).decode('utf-8')
    
    except:
        fw.write("1\n0:00:00,001 --> 0:01:00,001\nNo subtitles available\n\n")
        fw.close()
        return outfile
    # print txt

    # get styles
    styles = []
    match = re.search(r'<styling>(.+?)</styling>', txt, re.DOTALL)
    if match:
        match = re.findall(r'<style(.*?)>', match.group(1), re.DOTALL)
        if match:
            for style_line in match:
                match = re.search(r'id="(.*?)"', style_line, re.DOTALL)
                id = None
                if match:
                    id = match.group(1)
                color = None
                match = re.search(r'color="(.*?)"', style_line, re.DOTALL)
                if match:
                    # Some of the subtitle files use #ffffff color coding, others use plain text.
                    if match.group(1).startswith('#'):
                        styles.append((id, match.group(1)[0:7]))
                    else:
                        styles.append((id, match.group(1)))
                    # span_replacer = make_span_replacer(styles)
    # print "Retrieved styles"
    # print styles

    # get body
    body = []
    body = re.search(r'<body.*?>(.+?)</body>', txt, re.DOTALL)
    if body:
        # print "Located body"
        # print body.group(1).encode('utf-8')
        frames = re.findall(r'<p(.*?)>(.*?)</p>', body.group(1), re.DOTALL)
        # frames = re.findall(r'<p.*?begin=\"(.*?)".*?end=\"(.*?)".*?style="(.*?)".*?>(.*?)</p>', body.group(1), re.DOTALL)
        if frames:
            index = 1
            # print "Found %s frames"%len(frames)
            # print frames
            for formatting, content in frames:
                start = ''
                match = re.search(r'begin=\"(.*?)"', formatting, re.DOTALL)
                if match:
                    # begin="00:00:27:00"
                    start = match.group(1)
                    start_value = start[0:8] + "," + start[9:11] + '0'
                end = ''
                match = re.search(r'end=\"(.*?)"', formatting, re.DOTALL)
                if match:
                    #      0123456789
                    # end="00:00:29:06"
                    end = match.group(1)
                    end_value = end[0:8] + "," + end[9:11] + '0'
                style = None
                match = re.search(r'style=\"(.*?)"', formatting, re.DOTALL)
                if match:
                    style = match.group(1)
                else:
                    style = False
                start_split = re.split('\.',start)
                # print start_split
                if(len(start_split)>1):
                    start_mil_f = start_split[1].ljust(3, '0')
                else:
                    start_mil_f = "000"
                end_split = re.split('\.',end)
                if(len(end_split)>1):
                    end_mil_f = end_split[1].ljust(3, '0')
                else:
                    end_mil_f = "000"

                spans = []
                text = ''
                spans = re.findall(r'<span.*?tts:color="(.*?)">(.*?)<\/span>', content, re.DOTALL)
                if (spans):
                    num_spans = len(spans)
                    for num, (substyle, line) in enumerate(spans):
                        if num >0:
                            text = text+'\n'
                        # print substyle, color, line.encode('utf-8')
                        text = text+'<font color="%s">%s</font>' %  (substyle, line)
                else:
                    if style:
                        color = [value for (style_id, value) in styles if style == style_id]
                        text = text+'<font color="%s">%s</font>' %  (color[0], content)
                    else:
                         text = text+content
                    # print substyle, color, line.encode('utf-8')
                entry = "%d\n%s --> %s\n%s\n\n" % (index, start_value, end_value, text)
                if entry:
                    fw.write(entry)
                    index += 1

    fw.close()
    return outfile

def CATS():
        if os.path.exists(favorites)==True:
            addDir('[COLOR yellow]Favorites[/COLOR]','url',12,'')
            
        addDir('Shows','http://www.itv.com/hub/shows',1,icon,isFolder=True)
        # addDir('Categories','cats',205,icon,isFolder=True)
        # addDir('Live','Live',206,icon,isFolder=True)
        setView('tvshows', 'default')
                        
def LIVE():
    addDir('ITV1','https://www.itv.com/hub/itv',8,foricon+'art/1.png',isFolder=False)
    addDir('ITV2','https://www.itv.com/hub/itv2',8,foricon+'art/2.png',isFolder=False)
    addDir('ITV3','https://www.itv.com/hub/itv3',8,foricon+'art/3.png',isFolder=False)
    addDir('ITV4','https://www.itv.com/hub/itv4',8,foricon+'art/4.png',isFolder=False)
    addDir('ITVBe','https://www.itv.com/hub/itvbe',8,foricon+'art/8.jpg',isFolder=False)
    addDir('CITV','https://www.itv.com/hub/citv',8,foricon+'art/7.png',isFolder=False)

def CATEGORIES():
        CATS= [('children', 'Children'),
               ('comedy', 'Comedy'),
               ('entertainment', 'Entertainment'),
               ('drama-soaps', 'Drama & Soaps'),
               ('factual', 'Factual'),
               ('films', 'Films'),
               ('news', 'News'),
               ('sport', 'Sport')]

        for url, title in CATS:
            
            addDir(title,'https://www.itv.com/hub/categories/%s'%url,1,icon,isFolder=True)
        
        setView('tvshows', 'default')

def SHOWS(url):
    f = urllib.request.urlopen(url)
    buf = f.read().decode('utf-8')
    buf=re.sub('&amp;','&',buf)
    buf=re.sub('&middot;','',buf)
    #print "BUF %s" % buf
    f.close()
    buf = buf.split('grid-list__item width--one-half width--custard--one-third')
    for p in buf:
        try:
            linkurl= re.compile('href="(.+?)"').findall (p)[0]
            #print linkurl
            image= re.compile('srcset="(.+?)"').findall (p)[0]
            if '?' in image:
                image=image.split('?')[0] +'?w=512&h=288'
            #print image
            name= re.compile('"tout__title complex-link__target theme__target">(.+?)</h3',re.DOTALL).findall (p)[0].strip()
            #print name
            episodes = re.compile('"tout__meta theme__meta">(.+?)</p',re.DOTALL).findall (p)[0].strip()
            if 'mins' in episodes:
               episodes = re.compile('>(.+?)</',re.DOTALL).findall (episodes)[0].strip() 
            #print episodes
            if 'day left' in episodes or 'days left' in episodes or episodes=='1 episode' or 'mins' in episodes:
                if not 'mins' in episodes:
                    linkurl = linkurl+'##'
                addDir2(name+' - [COLOR orange]%s[/COLOR]'%episodes,linkurl,3,'', '',image,'',isFolder=False)
            else:
                if not 'no episodes' in episodes.lower():
                    addDir(name+' - [COLOR orange]%s[/COLOR]'%episodes,linkurl,2,image)
        except:pass        
    setView('tvshows', 'show') 
            
            
def getFavorites():
        import json
        try:
            with open(favorites) as f:
                a = f.read()
        except:
            pass
        try:
            for i in json.loads(a):
                name = i[0]
                url = i[1]
                iconimage = i[2]
                addDir(name,url,204,iconimage)
        except:
            pass

            
def addFavorite(name,url,iconimage):
        iconimage='http://mercury.itv.com/browser/production/image?q=80&format=jpg&w=800&h=450&productionId='+iconimage
        import json
        favList = []
        if os.path.exists(favorites)==False:
            print ('Making Favorites File')
            favList.append((name.split(' -')[0],url,iconimage))
            a = open(favorites, "w")
            a.write(json.dumps(favList))
            a.close()
        else:
            print ('Appending Favorites')
            with open(favorites) as f:
                a = f.read()
            try:
                data = json.loads(a)
                data.append((name.split(' -')[0],url,iconimage))
                b = open(favorites, "w")
                b.write(json.dumps(data))
                b.close()
            except:
                favList.append((name.split(' -')[0],url,iconimage))
                a = open(favorites, "w")
                a.write(json.dumps(favList))
                a.close()

def rmFavorite(name):
        import json
        print ('Remove Favorite')
        with open(favorites) as f:
            a = f.read()
        data = json.loads(a)
        print(len(data))
        for index in range(len(data)):
            try:
                if data[index][0]==name:
                    del data[index]
                    b = open(favorites, "w")
                    b.write(json.dumps(data))
                    b.close()
                if (len(data))<1:
                    os.remove(favorites)
            except:
                pass


def parse_Date(date_string,format,thestrip):
    try:
        DATE = datetime.datetime.strptime(date_string, format).strftime(thestrip)
    except TypeError:
        DATE = datetime.datetime(*(time.strptime(date_string, format)[0:6])).strftime(thestrip)
    return DATE    
    
def EPS(name,url):

    f = urllib.request.urlopen(url)
    buf = f.read().decode('utf-8')
    buf=re.sub('&amp;','&',buf)
    buf=re.sub('&middot;','',buf)
    buf=re.sub('&#039;','\'',buf)
    f.close()
    buf = buf.split('more-episodes')[1]
    buf = buf.split('<div id="')[0]
    buf = buf.split('grid-list__item width--one-half width--custard--one-third')
    NAME=name.split('-')[0]
    uniques=[]
    for p in buf:
       
        try:
            linkurl= re.compile('href="(.+?)"').findall (p)[0]
          
            image= re.compile('srcset="(.+?)"').findall (p)[0]
            if '?' in image:
                image=image.split('?')[0] +'?w=512&h=288'
            name= re.compile('"tout__title complex-link__target theme__target.+?>(.+?)</h',re.DOTALL).findall (p)[0].strip()
            
            if 'datetime' in name:
                name=NAME
            #episodes = re.compile('"tout__meta theme__meta">(.+?)</p',re.DOTALL).findall (p)[0].strip()
            try:description = re.compile('tout__summary theme__subtle">(.+?)</p',re.DOTALL).findall (p)[0].strip()
            except: description = ''
            #print description

            date = re.compile('datetime="(.+?)">',re.DOTALL).findall (p)[0]
            try:
                TIME= parse_Date(str(date), '%Y-%m-%dT%H:%MZ','%H:%M')
                DATE= parse_Date(str(date), '%Y-%m-%dT%H:%MZ','%d/%m/%Y')
                ADDDATE= '%s %s' % (DATE,TIME)
            except Exception as e:
               ADDDATE= ''
        
            NAME = name
            
            #if ADDDATE not in uniques:
                #uniques.append(ADDDATE)
            addDir2(NAME + ' - ' + ADDDATE,linkurl,3,date, name,image,description,isFolder=False)
        except:pass  
                                

    setView('tvshows', 'episode') 

def OPEN_URL(url):
    req = urllib.request.Request(url, headers={'User-Agent' : "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G34 Safari/601.1"}) 
    con = urllib.request.urlopen( req )
    link= con.read()
    return link

def PLAY_STREAM_HLS_LIVE(name,url,iconimage):
    ENDING=''
    xbmc.log("URL to fetch: %s" % url)

    buf = OPEN_URL(url).decode('utf-8')

    TITLE=re.compile('data-video-title="(.+?)"').findall(buf)[0]
    POSTURL=re.compile('data-html5-playlist="(.+?)"').findall(buf)[0]
    hmac=re.compile('data-video-hmac="(.+?)"').findall(buf)[0]

    data  = {"user": {"itvUserId": "", "entitlements": [], "token": ""}, "device": {"manufacturer": "Safari", "model": "5", "os": {"name": "Windows NT", "version": "6.1", "type": "desktop"}}, "client": {"version": "4.1", "id": "browser"}, "variantAvailability": {"featureset": {"min": ["hls", "aes"], "max": ["hls", "aes"]}, "platformTag": "youview"}}

    req = urllib.request.Request(POSTURL)
    jsondata = json.dumps(data)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes

    req.add_header('Host','simulcast.itv.com')
    req.add_header('Accept','application/vnd.itv.vod.playlist.v2+json')
    req.add_header('Proxy-Connection','keep-alive')
    req.add_header('Accept-Language','en-gb')
    req.add_header('Accept-Encoding','gzip, deflate')
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    req.add_header('Origin','http://www.itv.com')
    req.add_header('Connection','keep-alive')
    req.add_header('User-Agent','Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G34 Safari/601.1')       
    req.add_header('Referer',url)
    req.add_header('hmac',hmac)
    req.add_header('Content-Length', len(jsondataasbytes))

    xbmc.log("Attempting to fetch: %s" % url)
    xbmc.log("With data: %s" % data)
    xbmc.log("with HMAC: %s" % hmac)

    with urllib.request.urlopen(req,jsondataasbytes) as f:
        content = f.read()

    link=json.loads(content)

    BEG = link['Playlist']['Video']['Base']
    bb= link['Playlist']['Video']['MediaFiles']
    try:
        SUBLINK = link['Playlist']['Video']['Subtitles'][0]['Href']
        subtitles_exist = 1
    except:
        subtitles_exist = 0
        there_are_subtitles=0
        
    for k in bb:
        END = bb[0]['Href']

    if __settings__.getSetting('subtitles_control') == 'true':
        if subtitles_exist == 1:
            subtitles_file = download_subtitles_HLS(SUBLINK, '')
            print ("Subtitles at ", subtitles_file)
            there_are_subtitles=1
        
    STREAM =  BEG+END
    
    liz = xbmcgui.ListItem(TITLE)
    liz.setArt({'icon' : 'DefaultVideo.png', 'thumb' : iconimage})
    try:
        if there_are_subtitles == 1:
            liz.setSubtitles([subtitles_file])
    except:pass     
    liz.setInfo(type='Video', infoLabels={'Title':TITLE})
    liz.setProperty("IsPlayable","true")
    liz.setPath(STREAM+ENDING)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

def HLS(url,iconimage):
    xbmc.log("URL to fetch: %s" % url)
    #xbmc.log(str(url))  
    if url.endswith('##'):
        url=url.split('##')[0]
        buf = OPEN_URL(url).decode('utf-8')
            
        link=buf.split('data-episode-current')[1]
        url=re.compile('href="(.+?)"').findall(link)[0]
    
    #xbmc.log(str(url))            
    ENDING=''
    buf = OPEN_URL(url).decode('utf-8')

    TITLE=re.compile('data-video-title="(.+?)"').findall(buf)[0]
    POSTURL=re.compile('data-video-id="(.+?)"').findall(buf)[0]
    hmac=re.compile('data-video-hmac="(.+?)"').findall(buf)[0]

    data  = {"user": {"itvUserId": "", "entitlements": [], "token": ""}, "device": {"manufacturer": "Safari", "model": "5", "os": {"name": "Windows NT", "version": "6.1", "type": "desktop"}}, "client": {"version": "4.1", "id": "browser"}, "variantAvailability": {"featureset": {"min": ["hls", "aes", "outband-webvtt"], "max": ["hls", "aes", "outband-webvtt"]}, "platformTag": "youview"}}

    req = urllib.request.Request(POSTURL)
    jsondata = json.dumps(data)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes

    req.add_header('Host','magni.itv.com')
    req.add_header('hmac',hmac)
    req.add_header('Accept','application/vnd.itv.vod.playlist.v2+json')
    req.add_header('Proxy-Connection','keep-alive')
    req.add_header('Accept-Language','en-gb')
    req.add_header('Accept-Encoding','gzip, deflate')
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    req.add_header('Origin','http://www.itv.com')
    req.add_header('Connection','keep-alive')
    req.add_header('User-Agent','Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G34 Safari/601.1')       
    req.add_header('Referer',url)
    req.add_header('Content-Length', len(jsondataasbytes))

    xbmc.log("Attempting to fetch: %s" % POSTURL)
    xbmc.log("With data: %s" % data)
    xbmc.log("HMAC: %s" % hmac)
    xbmc.log("Refer: %s" % url)

    with urllib.request.urlopen(req,jsondataasbytes) as f:
        content = f.read()

    link=json.loads(content)

    BEG = link['Playlist']['Video']['Base']
    bb= link['Playlist']['Video']['MediaFiles']
    try:
        SUBLINK = link['Playlist']['Video']['Subtitles'][0]['Href']
        subtitles_exist = 1
    except:
        subtitles_exist = 0
        there_are_subtitles=0
        
    for k in bb:
        END = bb[0]['Href']

    if __settings__.getSetting('subtitles_control') == 'true':
        if subtitles_exist == 1:
            subtitles_file = download_subtitles_HLS(SUBLINK, '')
            print ("Subtitles at ", subtitles_file)
            there_are_subtitles=1
        
    STREAM =  BEG+END
    
    liz = xbmcgui.ListItem(TITLE)
    liz.setArt({'icon' : 'DefaultVideo.png', 'thumb' : iconimage})
    try:
        if there_are_subtitles == 1:
            liz.setSubtitles([subtitles_file])
    except:pass     
    liz.setInfo(type='Video', infoLabels={'Title':TITLE})
    liz.setProperty("IsPlayable","true")
    liz.setPath(STREAM+ENDING)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    
def setView(content, viewType):
        # set content type so library shows more views and info
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
                
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

def addDir(name,url,mode,iconimage,plot='',isFolder=True):
    
        try:
            PID = iconimage.split('episode/')[1].split('?')[0]
        except:pass    
        u=sys.argv[0]+"?url="+urllib.parse.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.parse.quote_plus(name)+"&iconimage="+urllib.parse.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name)
        liz.setArt({'icon' : 'DefaultVideo.png', 'thumb' : iconimage})
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot } )
        liz.setProperty('Fanart_Image', iconimage.replace('w=512&h=288','w=1280&h=720'))
        menu=[]
        if mode == 2:
            menu.append(('[COLOR yellow]Add To Favourites[/COLOR]','RunPlugin(%s?mode=13&url=%s&name=%s&iconimage=%s)'% (sys.argv[0],url,name,PID)))
        if mode == 204:
            menu.append(('[COLOR yellow]Remove Favourite[/COLOR]','RunPlugin(%s?mode=14&url=%s&name=%s&iconimage=%s)'% (sys.argv[0],url,name,iconimage)))
        liz.addContextMenuItems(items=menu, replaceItems=False)    
        if mode==3:
            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_DATE)
        if isFolder==False:
            liz.setProperty("IsPlayable","true")
            liz.setProperty('mimetype', 'application/x-mpegURL')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
        return ok

def addDir2(name,url,mode,date, episode,iconimage,plot='',isFolder=True):
        u=sys.argv[0]+"?url="+urllib.parse.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.parse.quote_plus(name)+"&iconimage="+urllib.parse.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name)
        liz.setArt({'icon' : 'DefaultVideo.png', 'thumb' : iconimage})
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot,'Premiered' : date,'Episode' : episode } )
        liz.setProperty('Fanart_Image', iconimage.replace('w=512&h=288','w=1280&h=720'))
        menu = []
        if isFolder==False:
            liz.setProperty("IsPlayable","true")        
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
        return ok


params=get_params()
url=None
name=None
iconimage=None
mode=None

try:
        url=urllib.parse.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.parse.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.parse.unquote_plus(params["iconimage"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

if mode==None or url==None or len(url)<1:
        CATS()
elif mode==1:
        SHOWS(url)
elif mode==2:
        EPS(name,url)
elif mode==3:
        HLS(url,iconimage)
elif mode==8:
        PLAY_STREAM_HLS_LIVE(name,url,iconimage)        
elif mode==12:
    getFavorites()
elif mode==13:
    addFavorite(name,url,iconimage)
elif mode==14:
    rmFavorite(name)
elif mode==204:
    EPS(name,url)
elif mode==205:
    CATEGORIES()
elif mode==206:
    LIVE()   
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))