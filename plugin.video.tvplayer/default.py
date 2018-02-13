import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os
from datetime import datetime,tzinfo,timedelta
import json
import base64

import net

net=net.Net()

ADDON = xbmcaddon.Addon(id='plugin.video.tvplayer')

datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
cookie_path = os.path.join(datapath, 'cookies')
cookie_jar = os.path.join(cookie_path, 'tvplayer.lwp')
if os.path.exists(cookie_path) == False:
        os.makedirs(cookie_path)

    
class Zone(tzinfo):
    
    def __init__(self,offset,isdst,name):
        self.offset = offset
        self.isdst = isdst
        self.name = name
    def utcoffset(self, dt):
        return timedelta(hours=self.offset) + self.dst(dt)
    def dst(self, dt):
            return timedelta(hours=1) if self.isdst else timedelta(0)
    def tzname(self,dt):
         return self.name


def login():
    loginurl = 'https://tvplayer.com/account/login/'
    email = ADDON.getSetting('email')
    password = ADDON.getSetting('password')


    UA='Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'





    headers={'Host':'tvplayer.com',
            'Connection':'keep-alive',
            'Cache-Control':'max-age=0',
            'Origin':'https://tvplayer.com',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Content-Type':'application/x-www-form-urlencoded',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer':'https://tvplayer.com/account/login',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'en-GB,en-US;q=0.9,en;q=0.8'}


    

    link=net.http_GET(loginurl, headers).content
    net.save_cookies(cookie_jar)
    token=re.compile('name="token" value="(.+?)"').findall(link)[0]
    data={'email':email,'password':str(password),'token':str(token)}


    net.set_cookies(cookie_jar)

    yo=net.http_POST(loginurl, data, headers).content

    net.save_cookies(cookie_jar)

    

    
def CATEGORIES():
   
    EST =Zone(0,False,'GMT')
    EST= datetime.now(EST).strftime('%Y-%m-%dT%H:%M:%S')
    URL='http://api.tvplayer.com/api/v2/epg/?service=1&platform=ios-staging&from=%s&hours=1' %str(EST)
    response=OPEN_URL(URL)
    
    link=json.loads(response)
    

    data=link['tvplayer']['response']['channels']
    


    uniques=[]
    for field in data:
        id= str(field['id'])
        name= field['name']
        icon= field['logo']['colour']
        try:title=field['programmes'][0]['title']
        except:title=''
        GENRE=field["genre"]
        if str(GENRE)=='None':
                GENRE=field["group"]
        if str(GENRE)=='None':
                GENRE=field['programmes'][0]['category']          
        try:desc=field['programmes'][0]['synopsis'].encode("utf-8")
        except:desc=''
        if field['type']=='free':
                add=''
        else:
                add=' [COLOR magenta]  -  (Premium)[/COLOR]'     
        name   = '[COLOR royalblue]'+name.encode("utf-8")+'[/COLOR] - [COLOR white]'+title.encode("utf-8")+'[/COLOR]'+add
        status = field['status']
        try:fanart=field['programmes'][0]['thumbnail']
        except:fanart=''
        if status=='online':
            if ADDON.getSetting('genre')== 'false':
                if ADDON.getSetting('premium')== 'true':
                    addDir(name,id,200,icon,desc,fanart,GENRE)
                else:
                    if field['type']=='free':
                        addDir(name,id,200,icon,desc,fanart,GENRE)
            else:
                if GENRE not in uniques:
                    uniques.append(GENRE)
                    addDir(GENRE,'url',2,'',GENRE,'')
    if ADDON.getSetting('sort')== 'true':    
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)             
    setView('movies', 'default') 


       
def GENRE(name,url):
    
    EST =Zone(0,False,'GMT')
    EST= datetime.now(EST).strftime('%Y-%m-%dT%H:%M:%S')
    URL='http://api.tvplayer.com/api/v2/epg/?service=1&platform=ios&from=%s&hours=1' %str(EST)
    response=OPEN_URL(URL)
    
    link=json.loads(response)
    

    data=link['tvplayer']['response']['channels']
    


    genre=name
    for field in data:
        id= str(field['id'])
        name= field['name']
        icon= field['logo']['colour']
        title=field['programmes'][0]['title']
        GENRE=field["genre"]
        if str(GENRE)=='None':
                GENRE=field["group"]
        if str(GENRE)=='None':
                GENRE=field['programmes'][0]['category']
        try:desc=field['programmes'][0]['synopsis'].encode("utf-8")
        except:desc=''
        if field['type']=='free':
                add=''
        else:
                add=' [COLOR magenta]  -  (Premium)[/COLOR]'     
        name   = '[COLOR royalblue]'+name.encode("utf-8")+'[/COLOR] - [COLOR white]'+title.encode("utf-8")+'[/COLOR]'+add

        status = field['status']
        fanart=field['programmes'][0]['thumbnail']
        if status=='online':
            if GENRE in genre:
                if ADDON.getSetting('premium')== 'true':
                    addDir(name,id,200,icon,desc,fanart,GENRE)
                else:
                    if field['type']=='free':
                        addDir(name,id,200,icon,desc,fanart,GENRE)


    if ADDON.getSetting('sort')== 'true':    
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)             
    setView('movies', 'default')
    
 
def OPEN_URL(url):                                   
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link


def OPEN_URL_STREAM_URL(url):
    import time
    timestamp =int(time.time()) + 4 * 60 * 60
    header={'Token':ADDON.getSetting('token'),'Token-Expiry': ADDON.getSetting('expiry'),'Referer':ADDON.getSetting('referer'),'User-Agent': 'iPhone/iOS 8.4 (iPhone; U; CPU iPhone OS 8_4 like Mac OS X;)'}
    req = urllib2.Request(url,headers=header)
    
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    cookie=response.info()['Set-Cookie']               
    return link ,cookie



def tvplayer(url):
    if ADDON.getSetting('premium')== 'true':
        login()
    net.set_cookies(cookie_jar)
    headers={'Host': 'tvplayer.com',
            'Connection': 'keep-alive',
            'Origin': 'http://tvplayer.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.8'}

    html=net.http_GET('http://tvplayer.com/watch/', headers).content
    
    DATA_TOKEN=re.compile('data-token="(.+?)"').findall(html)[0]
 
    URL='https://tvplayer.com/watch/context?resource=%s&gen=%s' % (url,DATA_TOKEN)
  
    html=net.http_GET(URL, headers).content

    VALIDATE=re.compile('"validate":"(.+?)"').findall(html)[0]
    
    
    if ADDON.getSetting('premium')== 'true':
         TOKEN=re.compile('"token":"(.+?)"').findall(html)[0]
    else:TOKEN='null'
    
    data={'service':'1',
          'platform':'chrome',
          'id':url,
          'token':TOKEN,
          'validate':VALIDATE}

         
    POSTURL='http://api.tvplayer.com/api/v2/stream/live'
    headers={'Host': 'api.tvplayer.com',
            'Connection': 'keep-alive',
            'Origin': 'http://api.tvplayer.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.8'}
    try:
            LINK=net.http_POST(POSTURL, data,headers=headers).content
            net.save_cookies(cookie_jar)
         
            return re.compile('stream":"(.+?)"').findall(LINK)[0].replace(' ','')
    except Exception as e:
                if '401' in str(e):
                    add='Please Sign up for free account and enter details in addon settings'
                else:
                    add=''
                dialog = xbmcgui.Dialog()
                dialog.ok("TV Player", '',str(e), add)
                return None
            
    #GET WORKS TOO
    #POSTURL='http://api.tvplayer.com/api/v2/stream/live?service=1&platform=website&id=%stoken=null&validate=%s'% (url,VALIDATE)
    #LINK=net.http_GET(POSTURL,headers=headers).content
    #return re.compile('stream": "(.+?)"').findall(LINK)[0]

def PLAY_STREAM(name,url,iconimage):

    STREAM =tvplayer(url)
    if not STREAM:
            return ''
    HOST=STREAM.split('//')[1]
    HOST=HOST.split('/')[0]
    headers={'Host': HOST,
            'Connection': 'keep-alive',
            'Origin': 'http://'+HOST,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

    TOKEN= open(cookie_jar).read()
    TOKEN ='AWSELB='+re.compile('AWSELB=(.+?);').findall (TOKEN)[0]

    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title':name})
    liz.setProperty("IsPlayable","true")
    liz.setPath(STREAM+'|Cookies='+TOKEN)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    
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

def addDir(name,url,mode,iconimage,description,fanart,genre=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)+"&genre="+urllib.quote_plus(genre)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description,"Genre": genre} )
        liz.setProperty('fanart_image',str(fanart))
        if mode ==200:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
        
 
        
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
fanart=None
genre=None

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
    
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        genre=urllib.unquote_plus(params["genre"])
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
       
elif mode==2:

        GENRE(name,url)
        
elif mode==200:

        PLAY_STREAM(name,url,iconimage)
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
