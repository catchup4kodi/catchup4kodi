import urllib.request, urllib.parse, urllib.error,urllib.request,urllib.error,urllib.parse,re,sys,socket,os,datetime,xbmcplugin,xbmcgui, xbmcaddon,json
from hashlib import md5


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
datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
favorites = os.path.join(datapath, 'favorites')
#if os.path.exists(favorites)==True:
    #FAV = open(favorites).read()
    

# setup cache dir
__scriptname__  = 'ITV'
__scriptid__ = "plugin.video.itv"
__addoninfo__ = utils.get_addoninfo(__scriptid__)
__addon__ = __addoninfo__["addon"]
__settings__   = xbmcaddon.Addon(id=__scriptid__)



DIR_USERDATA   = xbmc.translatePath(__addoninfo__["profile"])
SUBTITLES_DIR  = os.path.join(DIR_USERDATA, 'Subtitles')
IMAGE_DIR      = os.path.join(DIR_USERDATA, 'Images')

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


############## SUBS #################

def chomps(s):
    return s.rstrip('\n')

def httpget(url):
    resp = ''
    data = ''
    http = get_httplib()
    resp, data = http.request(url, "GET")
    return data
    
    
def download_subtitles_HLS(url, offset):

    logging.info('subtitles at =%s' % url)
    outfile = os.path.join(SUBTITLES_DIR, 'itv.srt')
    fw = open(outfile, 'w')
    
    if not url:
        fw.write("1\n0:00:00,001 --> 0:01:00,001\nNo subtitles available\n\n")
        fw.close() 
        return outfile
    txt = OPEN_URL(url)


    fw.write(txt)
    fw.close()    
    return outfile


def download_subtitles(url, offset):

    logging.info('subtitles at =%s' % url)
    outfile = os.path.join(SUBTITLES_DIR, 'itv.srt')
    fw = open(outfile, 'w')
    
    if not url:
        fw.write("1\n0:00:00,001 --> 0:01:00,001\nNo subtitles available\n\n")
        fw.close() 
        return outfile
    txt = httpget(url)
    try:
        txt = txt.decode("utf-16")
    except UnicodeDecodeError:
        txt = txt[:-1].decode("utf-16")
    txt = txt.encode('latin-1')
    txt = re.sub("<br/>"," ",txt)
    #print "SUBS %s" % txt
    p= re.compile('^\s*<p.*?begin=\"(.*?)\.([0-9]+)\"\s+.*?end=\"(.*?)\.([0-9]+)\"\s*>(.*?)</p>')
    i=0
    prev = None

    entry = None
    for line in txt.splitlines():
        subtitles1 = re.findall('<p.*?begin="(...........)" end="(...........)".*?">(.*?)</p>',line)
        if subtitles1:
            for start_time, end_time, text in subtitles1:
                r = re.compile('<[^>]*>')
                text = r.sub('',text)
                start_hours = re.findall('(..):..:..:..',start_time)
                start_mins = re.findall('..:(..):..:..', start_time)
                start_secs = re.findall('..:..:(..):..', start_time)
                start_msecs = re.findall('..:..:..:(..)',start_time)
#               start_mil = start_msecs +'0'
                end_hours = re.findall('(..):..:..:..',end_time)
                end_mins = re.findall('..:(..):..:..', end_time)
                end_secs = re.findall('..:..:(..):..', end_time)
                end_msecs = re.findall('..:..:..:(..)',end_time)
#               end_mil = end_msecs +'0'
                entry = "%d\n%s:%s:%s,%s --> %s:%s:%s,%s\n%s\n\n" % (i, start_hours[0], start_mins[0], start_secs[0], start_msecs[0], end_hours[0], end_mins[0], end_secs[0], end_msecs[0], text)
                i=i+1
                #print "ENTRY" + entry
        if entry: 
            fw.write(entry)
    
    fw.close()    
    return outfile



def CATS():
        if os.path.exists(favorites)==True:
            addDir('[COLOR yellow]Favorites[/COLOR]','url',12,'')
            
        addDir('Shows','http://www.itv.com/hub/shows',1,icon,isFolder=True)
        # addDir('Categories','cats',205,icon,isFolder=True)
        addDir('Live','Live',206,icon,isFolder=True)
        setView('tvshows', 'default')

        
                        
def getsim(channel):
    if 'ITV' == channel.upper():return ('ITV','1')

    if 'ITV2' in channel.upper():return ('ITV2','2')

    if 'ITV3' in channel.upper():return ('ITV3','3')

    if 'ITV4' in channel.upper():return ('ITV4','4')

    if 'CITV' in channel.upper():return ('CITV','7')

    if 'ITVBE' in channel.upper():return ('ITVBe','8')
                        
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

        
        
def PLAY_STREAM(name,url,iconimage):
    ENDING=''
    if len(url)>4:
            
        STREAM=url

    else:    
        #SoapMessage=TEMPLATE(url,'itv'+url.replace('sim',''))
        #headers={'Content-Length':'%d'%len(SoapMessage),'Content-Type':'text/xml; charset=utf-8','Host':'secure-mercury.itv.com','Origin':'http://www.itv.com',
                 #'Referer':'http://www.itv.com/Mercury/Mercury_VideoPlayer.swf?v=null',
                 #'SOAPAction':"http://tempuri.org/PlaylistService/GetPlaylist",
                 #'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}

        res, response = http.request("https://mediaplayer.itv.com/flash/playlists/ukonly/%s.xml" %url.lower())
        #res, response = http.request("https://secure-mercury.itv.com/PlaylistService.svc", 'POST', headers=headers, body=SoapMessage)
 
        response = response.decode('utf-8')
        rtmp=re.compile('<MediaFiles base="(.+?)"').findall(response)[0]
        if 'CITV' in name:
            r='CDATA\[(citv.+?)\]'
        else:
            r='CDATA\[(itv.+?)\]'
        playpath=re.compile(r,re.DOTALL).findall(response) [0]
        STREAM=rtmp+' playpath='+playpath+' swfUrl=http://www.itv.com/mediaplayer/ITVMediaPlayer.swf live=true timeout=10 swfvfy=true'
       
        
    liz = xbmcgui.ListItem(name)
    liz.setArt({'icon' : 'DefaultVideo.png', 'thumb' : iconimage})
    liz.setInfo(type='Video', infoLabels={'Title':name})
    liz.setProperty("IsPlayable","true")
    liz.setPath(STREAM+ENDING)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

    

def STREAMS():
        streams=[]
        key = get_url('http://www.itv.com/_app/dynamic/AsxHandler.ashx?getkey=please')
        for channel in range(1,5):
                streaminfo = get_url('http://www.itv.com/_app/dynamic/AsxHandler.ashx?key='+key+'&simid=sim'+str(channel)+'&itvsite=ITV&itvarea=SIMULCAST.SIM'+str(channel)+'&pageid=4567756521')
                stream=re.compile('<TITLE>(.+?)</TITLE><REF href="(.+?)" />').findall(streaminfo)
                streams.append(stream[1])
        for name,url in streams:
                addLink(name,url)

def BESTOF(url):
        response = get_url(url).replace('&amp;','&')
        match=re.compile('<li><a href="(.+?)"><img src=".+?" alt=".+?"></a><h4><a href=".+?">(.+?)</a></h4>').findall(response)
        for url,name in match:
                addDir(name,url,5,'')
                
def BESTOFEPS(name,url):
    
        response = get_url(url).replace('&amp;','&')
        eps=re.compile('<a [^>]*?title="Play" href=".+?vodcrid=crid://itv.com/(.+?)&DF=0"><img\s* src="(.*?)" alt="(.*?)"').findall(response)
        if eps:
            for url,thumb,name in eps:
                addDir(name,url,3,'http://itv.com/'+thumb,isFolder=False)
            return
        eps=re.compile('<a [^>]*?title="Play" href=".+?vodcrid=crid://itv.com/(.+?)&DF=0">(.+?)</a>').findall(response)
        if not eps: eps=re.compile('href=".+?vodcrid=crid://itv.com/(.+?)&G=.+?&DF=0">(.+?)</a>').findall(response)
        if not eps:
                eps=re.compile('<meta name="videoVodCrid" content="crid://itv.com/(.+?)">').findall(response)
                name=re.compile('<meta name="videoMetadata" content="(.+?)">').findall(response)
                eps=[(eps[0],name[0])]
        for url,name in eps:
                addDir(name,url,3,'',isFolder=False)
        
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
                TIME= parse_Date(str(date), '%Y-%m-%dT%H:%MZ','%H:%M%p')
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
    
def VIDEO(url,iconimage):
    return HLS(url,iconimage)
                
def setView(content, viewType):
        # set content type so library shows more views and info
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
                
def decode_redirect(url):
    
    # some of the the urls passed in are redirects that are not handled by XBMC.
    # These are text files with multiple stream urls

    #if environment in ['xbox', 'linux']:
    #    # xbox xbmc works just fine with redirects
    #    return url

    response = get_url(url).replace('&amp;','&')
    match=re.compile('Ref1\=(http.*)\s').findall(response)

    stream_url = None
    if match:
        stream_url = match[0].rstrip()
    else:
        # no match so pass url to xbmc and see if the url is directly supported 
        stream_url = url

    return stream_url

def decode_date(date):
    # format eg Sat 10 Jan 2009
    (dayname,day,monthname,year) = date.split(' ')
    if not year:
        return date
    month=1
    monthname = monthname.lower()
    lookup = {'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5, 'jun':6, 'jul':7, 'aug':8, 'sep':9, 'oct':10, 'nov':11, 'dec':12}
    if monthname[:3] in lookup:
        month=lookup[monthname[:3]]
    
    try:
        # yes I know the colons are weird but the 2009-01-25 xbox release
        # when in filemode (but not library mode) converts YYYY-MM-DD in (YYYY)
        sep='-'
        if environment == 'xbox': sep=':' 
        ndate = "%04d%s%02d%s%02d" % (int(year),sep,int(month),sep,int(day))
    except:
        # oops funny date, return orgional date
        return date
    #print "Date %s from %s" % (ndate, date)
    return ndate

def get_url(url):
    http = get_httplib()
    data = None    
    try:
        resp, data = http.request(url, 'GET')
    except: pass
    
    # second try
    if not data:
        try:
            resp, data = http.request(url, 'GET')
        except: 
            dialog = xbmcgui.Dialog()
            dialog.ok('Network Error', 'Failed to fetch URL', url)
            print ('Network Error. Failed to fetch URL %s' % url)
            raise
    
    return data

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

      
def addLink(name,url):
        ok=True
        thumbnail_url = url.split( "thumbnailUrl=" )[ -1 ]
        liz=xbmcgui.ListItem(name)
        liz.setArt({'icon' : 'DefaultVideo.png', 'thumb' : thumbnail_url})
        liz.setInfo( type="Video", infoLabels={ "Title": name,'Premiered' : '2012-01-01','Episode' : '1'} )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDir(name,url,mode,iconimage,plot='',isFolder=True):
    
        try:
            PID = iconimage.split('episode/')[1].split('?')[0]
        except:pass    
        u=sys.argv[0]+"?url="+urllib.parse.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.parse.quote_plus(name)+"&iconimage="+urllib.parse.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name)
        liz.setArt({'icon' : 'DefaultVideo.png', 'thumb' : iconimage})
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot,'Premiered' : '2012-01-01','Episode' : '7-1' } )
        liz.setProperty('Fanart_Image', iconimage.replace('w=512&h=288','w=1280&h=720'))
        menu=[]
        if mode == 2:
            menu.append(('[COLOR yellow]Add To Favourites[/COLOR]','XBMC.RunPlugin(%s?mode=13&url=%s&name=%s&iconimage=%s)'% (sys.argv[0],url,name,PID)))
        if mode == 204:
            menu.append(('[COLOR yellow]Remove Favourite[/COLOR]','XBMC.RunPlugin(%s?mode=14&url=%s&name=%s&iconimage=%s)'% (sys.argv[0],url,name,iconimage)))
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
print ("Mode: "+str(mode))
print ("URL: "+str(url))
print ("Name: "+str(name))
print ("iconimage: "+str(iconimage))

if mode==None or url==None or len(url)<1:
        print ("categories")
        CATS()
elif mode==1:
        print ("index of : "+url)
        SHOWS(url)
elif mode==2:
        print ("Getting Episodes: "+url)
        EPS(name,url)
elif mode==3:
        print ("Getting Videofiles: "+url)
        VIDEO(url,iconimage)
elif mode==4:
        print ("Getting Videofiles: "+url)
        BESTOF(url)
elif mode==5:
        print ("Getting Videofiles: "+url)
        BESTOFEPS(name,url)
elif mode==6:
        print ("Getting Videofiles: "+url)
        STREAMS()
elif mode==7:
        print ("Getting Videofiles: "+url)
        PLAY_STREAM(name,url,iconimage)
elif mode==8:
        print ("Getting Videofiles: "+url)
        PLAY_STREAM_HLS_LIVE(name,url,iconimage)        

elif mode==12:
    print ("")
    getFavorites()

elif mode==13:
    print ("")
    addFavorite(name,url,iconimage)

elif mode==14:
    print ("")
    rmFavorite(name)

elif mode==204:
    EPS(name,url)
        
elif mode==205:
    CATEGORIES()
    
elif mode==206:
    LIVE()   
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))

