import urllib,urllib2,re,sys,socket,os,datetime,xbmcplugin,xbmcgui, xbmcaddon,json
from hashlib import md5


# external libs
sys.path.insert(0, xbmc.translatePath(os.path.join('special://home/addons/plugin.video.itv', 'lib')))
import utils, httplib2, socks, httplib, logging, time
import urllib2
import datetime
import time



PLUGIN='plugin.video.itv'
ADDON = xbmcaddon.Addon(id=PLUGIN)
icon = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.itv', 'icon.png'))
foricon = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.itv', ''))
from BeautifulSoup import BeautifulSoup
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

livepro = ADDON.getSetting('livepro')
SHOWLIVE=ADDON.getSetting('SHOWLIVE')

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
        addDir('Categories','cats',205,icon,isFolder=True)
        addDir('Live','Live',206,icon,isFolder=True)
        if SHOWLIVE == 'true':
            try:LIVE('dont')
            except:pass
        setView('tvshows', 'default')

        
                        
def getsim(channel):
    if 'ITV' == channel.upper():return ('ITV','1')

    if 'ITV2' in channel.upper():return ('ITV2','2')

    if 'ITV3' in channel.upper():return ('ITV3','3')

    if 'ITV4' in channel.upper():return ('ITV4','4')

    if 'CITV' in channel.upper():return ('CITV','7')

    if 'ITVBE' in channel.upper():return ('ITVBe','8')

    
                        
def LIVE(url):
    try:
        link = OPEN_URL('https://www.itv.com/hub/tv-guide')

        link = link.split('class="guide__item')
        for p in link:
            if 'watch live' in p.lower():

                title = '[COLOR orange]'+re.compile('title="(.+?)"').findall(p)[0].replace('amp;','')+'[/COLOR]'
                channel = re.compile('live on (.+?)"').findall(p)[0]
                sim, icon_num=getsim(channel)
                if livepro=='true':
                    mode = 8
                else:
                    mode = 7
                    sim = 'itv'+icon_num
                    
                if url=='dont':
                    name = '[COLOR plum]On Now[/COLOR] - [COLOR green]%s[/COLOR] - %s' % (channel,title)
                    addDir(name,sim,mode,foricon+'art/%s.png' % icon_num,isFolder=False)
                else:
                    addDir(channel + ' - '+title,sim,mode,foricon+'art/%s.png' % icon_num,isFolder=False)
                
        if url !='dont':
            addDir('Events/Sport','https://itvliveevents-i.akamaihd.net/hls/live/203496/itvliveevents/ITVEVTMN/master.m3u8',7,foricon+'art/9.jpg',isFolder=False)#sim9
        
    except: 
        addDir('ITV1','sim1',7,foricon+'art/1.png',isFolder=False)#sim1   https://itv1liveios-i.akamaihd.net/hls/live/203437/itvlive/ITV1MN/master.m3u8
        addDir('ITV2','sim2',7,foricon+'art/2.png',isFolder=False)#sim2   https://itv2liveios-i.akamaihd.net/hls/live/203495/itvlive/ITV2MN/master.m3u8
        addDir('ITV3','sim3',7,foricon+'art/3.png',isFolder=False)#sim3   https://itv3liveios-i.akamaihd.net/hls/live/207262/itvlive/ITV3MN/master.m3u8
        addDir('ITV4','sim4',7,foricon+'art/4.png',isFolder=False)#sim4   https://itv4liveios-i.akamaihd.net/hls/live/207266/itvlive/ITV4MN/master.m3u8
        addDir('ITVBe','sim8',7,foricon+'art/8.jpg',isFolder=False)#    https://itvbeliveios-i.akamaihd.net/hls/live/219078/itvlive/ITVBE/master.m3u8
        addDir('CITV','sim7',7,foricon+'art/7.png',isFolder=False)#sim7  https://citvliveios-i.akamaihd.net/hls/live/207267/itvlive/CITVMN/master.m3u8
        addDir('Events/Sport','https://itvliveevents-i.akamaihd.net/hls/live/203496/itvliveevents/ITVEVTMN/master.m3u8',7,foricon+'art/9.jpg',isFolder=False)#sim9

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
    quality = int(__settings__.getSetting('live_stream'))
    
    if len(url)>4:
            
        STREAM=url

    else:    
        #SoapMessage=TEMPLATE(url,'itv'+url.replace('sim',''))
        #headers={'Content-Length':'%d'%len(SoapMessage),'Content-Type':'text/xml; charset=utf-8','Host':'secure-mercury.itv.com','Origin':'http://www.itv.com',
                 #'Referer':'http://www.itv.com/Mercury/Mercury_VideoPlayer.swf?v=null',
                 #'SOAPAction':"http://tempuri.org/PlaylistService/GetPlaylist",
                 #'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}

        if ADDON.getSetting('proxy')=='true':
            if ADDON.getSetting('custom_ip')=='':
                IP=getip()
            else:
                IP=ADDON.getSetting('custom_ip')
            #headers={"X-Forwarded-For":IP,'Content-Length':'%d'%len(SoapMessage),'Content-Type':'text/xml; charset=utf-8','Host':'secure-mercury.itv.com','Origin':'http://www.itv.com','Referer':'http://www.itv.com/Mercury/Mercury_VideoPlayer.swf?v=null','SOAPAction':"http://tempuri.org/PlaylistService/GetPlaylist",'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36'}

            ENDING='|X-Forwarded-For='+IP

        res, response = http.request("https://mediaplayer.itv.com/flash/playlists/ukonly/%s.xml" %url.lower())
        #res, response = http.request("https://secure-mercury.itv.com/PlaylistService.svc", 'POST', headers=headers, body=SoapMessage)
 
        rtmp=re.compile('<MediaFiles base="(.+?)"').findall(response)[0]
        if 'CITV' in name:
            r='CDATA\[(citv.+?)\]'
        else:
            r='CDATA\[(itv.+?)\]'
        playpath=re.compile(r,re.DOTALL).findall(response) [0]



        STREAM=rtmp+' playpath='+playpath+' swfUrl=http://www.itv.com/mediaplayer/ITVMediaPlayer.swf live=true timeout=10 swfvfy=true'
       
        
    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
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
        
    if __settings__.getSetting('proxy_use') == 'true':
        proxy_server = None
        proxy_type_id = 0
        proxy_port = 8080
        proxy_user = None
        proxy_pass = None
        try:
            proxy_server = __settings__.getSetting('proxy_server')
            proxy_type_id = __settings__.getSetting('proxy_type')
            proxy_port = __settings__.getSetting('proxy_port')
            proxy_user = __settings__.getSetting('proxy_user')
            proxy_pass = __settings__.getSetting('proxy_pass')
        except:
            pass
        passmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        proxy_details = 'http://' + proxy_server + ':' + proxy_port
        passmgr.add_password(None, proxy_details, proxy_user, proxy_pass) 
        authinfo = urllib2.ProxyBasicAuthHandler(passmgr)
        proxy_support = urllib2.ProxyHandler({"http" : proxy_details})

        opener = urllib2.build_opener(proxy_support, authinfo)
        urllib2.install_opener(opener)
    f = urllib2.urlopen(url)
    buf = f.read()
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
            print 'Making Favorites File'
            favList.append((name.split(' -')[0],url,iconimage))
            a = open(favorites, "w")
            a.write(json.dumps(favList))
            a.close()
        else:
            print 'Appending Favorites'
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
        print 'Remove Favorite'
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

    if __settings__.getSetting('proxy_use') == 'true':
        proxy_server = None
        proxy_type_id = 0
        proxy_port = 8080
        proxy_user = None
        proxy_pass = None
        try:
            proxy_server = __settings__.getSetting('proxy_server')
            proxy_type_id = __settings__.getSetting('proxy_type')
            proxy_port = __settings__.getSetting('proxy_port')
            proxy_user = __settings__.getSetting('proxy_user')
            proxy_pass = __settings__.getSetting('proxy_pass')
        except:
            pass
        passmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        proxy_details = 'http://' + proxy_server + ':' + proxy_port
        passmgr.add_password(None, proxy_details, proxy_user, proxy_pass) 
        authinfo = urllib2.ProxyBasicAuthHandler(passmgr)
        proxy_support = urllib2.ProxyHandler({"http" : proxy_details})

        opener = urllib2.build_opener(proxy_support, authinfo)
        urllib2.install_opener(opener)

    f = urllib2.urlopen(url)
    buf = f.read()
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
    req = urllib2.Request(url, headers={'User-Agent' : "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G34 Safari/601.1"}) 
    con = urllib2.urlopen( req )
    link= con.read()
    return link





        
def OPEN_URL_PROXY(url):
    PROXYBASE=ADDON.getSetting('new_custom_url')

    if 'just' in PROXYBASE:
        PROXYURL = 'http://www.justproxy.co.uk/index.php?q=%s'
        PROXYREF = 'http://www.justproxy.co.uk/'
        

    if 'england' in PROXYBASE:
        PROXYURL = 'https://www.englandproxy.co.uk/'
        PROXYREF = 'https://www.englandproxy.co.uk/'

        
    import base64
    if 'england' in PROXYREF:
        url=url.split('//')[1]
        req = urllib2.Request(PROXYURL + url)
    else:    
        req = urllib2.Request(PROXYURL % base64.b64encode(url))

        
    req.add_header('Referer', PROXYREF)                                                  
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link


def getip():
    import random  
    link=OPEN_URL('http://free-proxy-list.net/uk-proxy.html')
    match=re.compile('<tr><td>(.+?)</td><td>').findall(link)
    ip=random.choice(match)
    ADDON.setSetting('custom_ip',ip)
    return ip



def PLAY_STREAM_HLS_LIVE(name,url,iconimage):

    REF = 'https://www.itv.com/hub/'+url.lower()
    
    ENDING='|User-Agent=Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.0 Mobile/15E148 Safari/604.1'
    
    if ADDON.getSetting('proxy')=='false':
        buf = OPEN_URL('https://www.itv.com/hub/'+url.lower())
    else:
        buf = OPEN_URL_PROXY('https://www.itv.com/hub/'+url.lower())
        
        if ADDON.getSetting('custom_ip')=='':
            IP=getip()
        else:
            IP=ADDON.getSetting('custom_ip')

    TITLE= name
    POSTURL='https://magni.itv.com/playlist/itvonline/'+url
    hmac=re.compile('data-video-hmac="(.+?)"').findall(buf)[0]
    
    req = urllib2.Request(POSTURL)
    req.add_header('Host','magni.itv.com')
    req.add_header('hmac',hmac)
    req.add_header('Accept','application/vnd.itv.vod.playlist.v2+json')
    req.add_header('Proxy-Connection','keep-alive')
    req.add_header('Accept-Language','en-gb')
    req.add_header('Accept-Encoding','gzip, deflate')
    req.add_header('Content-Type','application/json')
    req.add_header('Origin','http://www.itv.com')
    req.add_header('Connection','keep-alive')
    if ADDON.getSetting('proxy')=='true':
        req.add_header('X-Forwarded-For',IP)
        ENDING='|User-Agent=Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.0 Mobile/15E148 Safari/604.1&X-Forwarded-For='+IP
    req.add_header('User-Agent','Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.0 Mobile/15E148 Safari/604.1')       
    req.add_header('Referer',REF)

    if ADDON.getSetting('UA')=='true':
        data  = {"user": {"itvUserId": "", "entitlements": [], "token": ""}, "device": {"manufacturer": "Safari", "model": "5", "os": {"name": "Windows NT", "version": "6.1", "type": "desktop"}}, "client": {"version": "4.1", "id": "browser"}, "variantAvailability": {"featureset": {"min": ["hls", "aes"], "max": ["hls", "aes"]}, "platformTag": "dotcom"}}
    else:
        data  = {"user":{"itvUserId":"","entitlements":[],"token":""},"device":{"manufacturer":"Apple","model":"iPad","os":{"name":"iPhone OS","version":"6.0","type":"ios"}},"client":{"version":"4.1","id":"browser"},"variantAvailability":{"featureset":{"min":["hls","aes"],"max":["hls","aes"]},"platformTag":"mobile"}}



    try:
        content = urllib2.urlopen(req, json.dumps(data)).read()
    except:
        
        dialog = xbmcgui.Dialog()
        if ADDON.getSetting('proxy')=='true':
            dialog.ok('ITV Player', 'Ooops Seems Your Uk IP Adress','[COLOR green]%s[/COLOR] Is Out Of Date' %IP, 'Gonna Grab New One Now')
            import grabnewip
        else:
            dialog.ok('ITV Player', '','Not Available', '')
        return ''


    link=json.loads(content)


    BEG = link['Playlist']['Video']['Base']
    bb= link['Playlist']['Video']['MediaFiles']

        
    for k in bb:
        END = bb[0]['Href']

        
    STREAM =  BEG+END

    HOST = BEG.split('//')[1].split('/')[0]

    
    
    liz = xbmcgui.ListItem(TITLE, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title':TITLE})
    liz.setProperty('mimetype', 'application/x-mpegURL')
    liz.setProperty("IsPlayable","true")
    
    liz.setPath(STREAM+ENDING)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)



    
def HLS(url,iconimage):
    #xbmc.log(str(url))  
    if url.endswith('##'):
        url=url.split('##')[0]
        if ADDON.getSetting('proxy')=='false':
            buf = OPEN_URL(url)
        else:
            buf = OPEN_URL_PROXY(url)
            
        link=buf.split('data-episode-current')[1]
        url=re.compile('href="(.+?)"').findall(link)[0]
    
    #xbmc.log(str(url))            
    ENDING=''
    
    if ADDON.getSetting('proxy')=='false':
        buf = OPEN_URL(url)
    else:
        buf = OPEN_URL_PROXY(url)
        
        if ADDON.getSetting('custom_ip')=='':
            IP=getip()
        else:
            IP=ADDON.getSetting('custom_ip')

    TITLE=re.compile('data-video-title="(.+?)"').findall(buf)[0]
    POSTURL=re.compile('data-video-id="(.+?)"').findall(buf)[0]
    hmac=re.compile('data-video-hmac="(.+?)"').findall(buf)[0]
    
    req = urllib2.Request(POSTURL)
    req.add_header('Host','magni.itv.com')
    req.add_header('hmac',hmac)
    req.add_header('Accept','application/vnd.itv.vod.playlist.v2+json')
    req.add_header('Proxy-Connection','keep-alive')
    req.add_header('Accept-Language','en-gb')
    req.add_header('Accept-Encoding','gzip, deflate')
    req.add_header('Content-Type','application/json')
    req.add_header('Origin','http://www.itv.com')
    req.add_header('Connection','keep-alive')
    if ADDON.getSetting('proxy')=='true':
        req.add_header('X-Forwarded-For',IP)
        ENDING='|X-Forwarded-For='+IP
    req.add_header('User-Agent','Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G34 Safari/601.1')       
    req.add_header('Referer',url)


   #data  = {"user":{"itvUserId":"","entitlements":[],"token":""},"device":{"manufacturer":"Apple","model":"iPhone","os":{"name":"iPad OS","version":"11.2.5","type":"ios"}},"client":{"version":"4.1","id":"browser"},"variantAvailability":{"featureset":{"min":["hls","aes"],"max":["hls","aes"]},"platformTag":"mobile"}}
    
    data  = {"user": {"itvUserId": "", "entitlements": [], "token": ""}, "device": {"manufacturer": "Safari", "model": "5", "os": {"name": "Windows NT", "version": "6.1", "type": "desktop"}}, "client": {"version": "4.1", "id": "browser"}, "variantAvailability": {"featureset": {"min": ["hls", "aes", "outband-webvtt"], "max": ["hls", "aes", "outband-webvtt"]}, "platformTag": "dotcom"}}
    #data  = {"user":{"itvUserId":"","entitlements":[],"token":""},"device":{"manufacturer":"Apple","model":"iPad","os":{"name":"iPhone OS","version":"6.0","type":"ios"}},"client":{"version":"4.1","id":"browser"},"variantAvailability":{"featureset":{"min":["aes","hls", "outband-webvtt"],"max":["hls","aes", "outband-webvtt"]},"platformTag":"mobile"}}


    try:
        content = urllib2.urlopen(req, json.dumps(data)).read()
    except:
        
        dialog = xbmcgui.Dialog()
        if ADDON.getSetting('proxy')=='true':
            dialog.ok('ITV Player', 'Ooops Seems Your Uk IP Adress','[COLOR green]%s[/COLOR] Is Out Of Date' %IP, 'Gonna Grab New One Now')
            import grabnewip
        else:
            dialog.ok('ITV Player', '','Not Available', '')
        return ''


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
            print "Subtitles at ", subtitles_file
            there_are_subtitles=1
        
    STREAM =  BEG+END
    
    liz = xbmcgui.ListItem(TITLE, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    try:
        if there_are_subtitles == 1:
            liz.setSubtitles([subtitles_file])
    except:pass     
    liz.setInfo(type='Video', infoLabels={'Title':TITLE})
    liz.setProperty("IsPlayable","true")
    liz.setPath(STREAM+ENDING)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

    
def VIDEO(url,iconimage):
    #xbmc.log(url)
    if ADDON.getSetting('proxy')=='false':
        if ADDON.getSetting('hls')=='true':
            return HLS(url,iconimage)

    if url.endswith('##'):
        url=url.split('##')[0]
        if ADDON.getSetting('proxy')=='false':
            buf = OPEN_URL(url)
        else:
            buf = OPEN_URL_PROXY(url)
            
        link=buf.split('data-episode-current')[1]
        url=re.compile('href="(.+?)"').findall(link)[0]

        
    if ADDON.getSetting('proxy')=='false':
        buf = OPEN_URL(url)
    else:
        buf = OPEN_URL_PROXY(url)
        
        if ADDON.getSetting('custom_ip')=='':
            IP=getip()
        else:
            IP=ADDON.getSetting('custom_ip')

    productionID=re.compile('data-video-production-id="(.+?)"').findall(buf)[0]
    
    SM_TEMPLATE = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/" xmlns:itv="http://schemas.datacontract.org/2004/07/Itv.BB.Mercury.Common.Types" xmlns:com="http://schemas.itv.com/2009/05/Common">
      <soapenv:Header/>
      <soapenv:Body>
        <tem:GetPlaylist>
          <tem:request>
        <itv:ProductionId>%s</itv:ProductionId>
        <itv:RequestGuid>FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF</itv:RequestGuid>
        <itv:Vodcrid>
          <com:Id/>
          <com:Partition>itv.com</com:Partition>
        </itv:Vodcrid>
          </tem:request>
          <tem:userInfo>
        <itv:Broadcaster>Itv</itv:Broadcaster>
        <itv:GeoLocationToken>
          <itv:Token/>
        </itv:GeoLocationToken>
        <itv:RevenueScienceValue>ITVPLAYER.12.18.4</itv:RevenueScienceValue>
        <itv:SessionId/>
        <itv:SsoToken/>
        <itv:UserToken/>
          </tem:userInfo>
          <tem:siteInfo>
        <itv:AdvertisingRestriction>None</itv:AdvertisingRestriction>
        <itv:AdvertisingSite>ITV</itv:AdvertisingSite>
        <itv:AdvertisingType>Any</itv:AdvertisingType>
        <itv:Area>ITVPLAYER.VIDEO</itv:Area>
        <itv:Category/>
        <itv:Platform>DotCom</itv:Platform>
        <itv:Site>ItvCom</itv:Site>
      </tem:siteInfo>
      <tem:deviceInfo>
        <itv:ScreenSize>Big</itv:ScreenSize>
      </tem:deviceInfo>
      <tem:playerInfo>
        <itv:Version>2</itv:Version>
      </tem:playerInfo>
        </tem:GetPlaylist>
      </soapenv:Body>
    </soapenv:Envelope>
    """
    

    SoapMessage = SM_TEMPLATE%(productionID)
    http = get_httplib()
    

    url = 'http://mercury.itv.com/PlaylistService.svc'

    if ADDON.getSetting('proxy')=='true':
        if ADDON.getSetting('custom_ip')=='':
            IP=getip()
        else:
            IP=ADDON.getSetting('custom_ip')
        headers = {"X-Forwarded-For":IP,"Host":"secure-mercury.itv.com","Referer":"http://www.itv.com/mercury/Mercury_VideoPlayer.swf?v=1.6.479/[[DYNAMIC]]/2","Content-type":"text/xml; charset=utf-8","Content-length":"%d" % len(SoapMessage),"SOAPAction":"http://tempuri.org/PlaylistService/GetPlaylist"}
        
    else:
        headers = {"Host":"secure-mercury.itv.com","Referer":"http://www.itv.com/mercury/Mercury_VideoPlayer.swf?v=1.6.479/[[DYNAMIC]]/2","Content-type":"text/xml; charset=utf-8","Content-length":"%d" % len(SoapMessage),"SOAPAction":"http://tempuri.org/PlaylistService/GetPlaylist"}
        
        
    response, res = http.request("https://secure-mercury.itv.com/PlaylistService.svc", 'POST', headers=headers, body=SoapMessage)
    title1= res.split("<ProgrammeTitle>")
    
    try:
        title2= title1[1].split("</ProgrammeTitle>")
        #print res
        match2 = re.findall(ur'<PosterFrame>.*?<URL><\!\[CDATA\[(.*?)\].*?</PosterFrame>', res, flags=re.DOTALL)
        #print "match %s" % match2[0]
        if match2:
            thumbfile = match2[0]
        else:
            thumbfile = icon
        res = re.search('<VideoEntries>.+?</VideoEntries>', res, re.DOTALL).group(0)
        rendition_offset= res.split("rendition-offset=")
        offset_seconds = rendition_offset[1].split(":")
        offset = int(offset_seconds[2])
    
       
        mediafile =  res.split("<MediaFile delivery=")
        try:
            subs=res.split('<ClosedCaptioningURIs>')[1]
            subs=subs.split('</ClosedCaptioningURIs>')[0]
            subtitles_file=re.compile('CDATA\[(.+?)\]').findall(subs)[0]
            there_are_subtitles=1
        except:     
            there_are_subtitles=0            
        match1 = re.findall(ur'<ClosedCaptioningURIs>.*?<URL><\!\[CDATA\[(.*?)\].*?</ClosedCaptioningURIs>', res, flags=re.DOTALL)
        if match1:
            if __settings__.getSetting('subtitles_control') == 'true':
                subtitles_file = download_subtitles(match1[0], offset)
                print "Subtitles at ", subtitles_file
                there_are_subtitles=1
    
        for index in range(len(mediafile)):
            print mediafile[index]
            print "MEDIA ENTRY"
    
        quality = int(__settings__.getSetting('video_stream'))
        selected_stream = 5
        
        if (quality == 0):
            selected_stream = index
            
        if (quality == 5):
            if(index==5):
                selected_stream = 5
            else:
                selected_stream = index    
        if (quality == 4):
            if(index==4):
                selected_stream = 4
            else:
                selected_stream = index
        
        if (quality == 3):
            if(index>=3):
                selected_stream = 3
            else:
                selected_stream = index
        
        if (quality == 2):
                if(index>=2):
                        selected_stream = 2
                else:
                        selected_stream = index

        if (quality == 1):
                if(index>=1):
                        selected_stream =1 
                else:
                        selected_stream = index

        rtmp = re.compile('(rtmp[^"]+)').findall(res)[0]
        playpath = re.compile('(mp4:[^\]]+)').findall(mediafile[selected_stream])[0]
        rtmp = rtmp.replace('&amp;','&')
    
        url = rtmp + " swfurl=http://www.itv.com/mediaplayer/ITVMediaPlayer.swf playpath=" + playpath + " swfvfy=true"
 
        liz = xbmcgui.ListItem(title2[0], iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        try:
            if there_are_subtitles == 1:
                liz.setSubtitles([subtitles_file])
        except:pass        
        liz.setInfo(type='Video', infoLabels={'Title':name})
        liz.setProperty("IsPlayable","true")
        liz.setPath(url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

    except:
        dialog = xbmcgui.Dialog()
        dialog.ok("ITV Player", "Sorry Cannot Resolve This Stream", "")

                
                
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
    if lookup.has_key(monthname[:3]):
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
            print 'Network Error. Failed to fetch URL %s' % url
            raise
    
    return data

    
    
def TEMPLATE(sim,channel):
        SM_TEMPLATE='''<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                  <SOAP-ENV:Body>
                    <tem:GetPlaylist xmlns:tem="http://tempuri.org/" xmlns:itv="http://schemas.datacontract.org/2004/07/Itv.BB.Mercury.Common.Types" xmlns:com="http://schemas.itv.com/2009/05/Common">
                      <tem:request>
                        <itv:RequestGuid>BF0B9A3C-4F65-C45D-4BC4-3F639208946F</itv:RequestGuid>
                        <itv:Vodcrid>
                          <com:Id>%s</com:Id>
                          <com:Partition>itv.com</com:Partition>
                        </itv:Vodcrid>
                      </tem:request>
                      <tem:userInfo>
                        <itv:Broadcaster>Itv</itv:Broadcaster>
                        <itv:GeoLocationToken>
                          <itv:Token/>
                        </itv:GeoLocationToken>
                        <itv:RevenueScienceValue/>
                      </tem:userInfo>
                      <tem:siteInfo>
                        <itv:AdvertisingRestriction>None</itv:AdvertisingRestriction>
                        <itv:AdvertisingSite>ITV</itv:AdvertisingSite>
                        <itv:Area>channels.%s</itv:Area>
                        <itv:Platform>DotCom</itv:Platform>
                        <itv:Site>ItvCom</itv:Site>
                      </tem:siteInfo>
                      <tem:deviceInfo>
                        <itv:ScreenSize>Big</itv:ScreenSize>
                      </tem:deviceInfo>
                    </tem:GetPlaylist>
                  </SOAP-ENV:Body>
                </SOAP-ENV:Envelope>
                '''
        return SM_TEMPLATE%(sim,channel)
        
    

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
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumbnail_url)
        liz.setInfo( type="Video", infoLabels={ "Title": name,'Premiered' : '2012-01-01','Episode' : '1'} )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDir(name,url,mode,iconimage,plot='',isFolder=True):
    
        try:
            PID = iconimage.split('episode/')[1].split('?')[0]
        except:pass    
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name,iconImage="DefaultVideo.png", thumbnailImage=iconimage)
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
            if ADDON.getSetting('hls')=='true':
                liz.setProperty('mimetype', 'application/x-mpegURL')
            if ADDON.getSetting('livepro')=='true':
                liz.setProperty('mimetype', 'application/x-mpegURL')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
        return ok

def addDir2(name,url,mode,date, episode,iconimage,plot='',isFolder=True):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name,iconImage="DefaultVideo.png", thumbnailImage=iconimage)
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
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "iconimage: "+str(iconimage)

if mode==None or url==None or len(url)<1:
        print "categories"
        CATS()
elif mode==1:
        print "index of : "+url
        SHOWS(url)
elif mode==2:
        print "Getting Episodes: "+url
        EPS(name,url)
elif mode==3:
        print "Getting Videofiles: "+url
        VIDEO(url,iconimage)
elif mode==4:
        print "Getting Videofiles: "+url
        BESTOF(url)
elif mode==5:
        print "Getting Videofiles: "+url
        BESTOFEPS(name,url)
elif mode==6:
        print "Getting Videofiles: "+url
        STREAMS()
elif mode==7:
        print "Getting Videofiles: "+url
        PLAY_STREAM(name,url,iconimage)

elif mode==8:
        print "Getting Videofiles: "+url
        PLAY_STREAM_HLS_LIVE(name,url,iconimage)        

elif mode==12:
    print ""
    getFavorites()

elif mode==13:
    print ""
    addFavorite(name,url,iconimage)

elif mode==14:
    print ""
    rmFavorite(name)

elif mode==204:
        
        EPS(name,url)
        
elif mode==205:
    CATEGORIES()
    
elif mode==206:
    LIVE(url)   
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))

