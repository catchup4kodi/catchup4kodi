import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os
import HTMLParser
import net
import htmlcleaner

net=net.Net()

#ee3fa
ADDON = xbmcaddon.Addon(id='plugin.video.tvcatchup.unrestricted')
ICON = ADDON.getAddonInfo('icon')
FANART = ADDON.getAddonInfo('fanart')
PROXYBASE=ADDON.getSetting('PROXYBASE')
ART = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvcatchup.unrestricted/img/'))
PROXY_ENABLED=ADDON.getSetting('new_proxy')


if PROXY_ENABLED=='true':
    if ADDON.getSetting('custom_ip')=='':
        import grabnewip

UA='Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25'
    


def CATEGORIES():
    headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'en-US,en;q=0.9',
            'Cache-Control':'no-cache',
            'Connection':'keep-alive',
            'Host':'tvcatchup.com',
            'Referer':'https://tvcatchup.com/',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25'}


    if PROXY_ENABLED=='true':
        link = OPEN_URL_PROXY('https://tvcatchup.com/channels')
        CHANGE=True
    else:
        link = net.http_GET('https://tvcatchup.com/channels',headers).content
        CHANGE=False

    match= re.compile('<p class="channelsicon".+?href="(.+?)".+?src="(.+?)".+?<br/>(.+?)<.+?alt="(.+?)"',re.DOTALL).findall(link)

    for url, iconimage, whatson, name in match:
        whatson=htmlcleaner.clean(whatson)
        if not 'http' in url:
            if CHANGE==True:
                _URL_ = 'https://' +url
            else:    
                _URL_ = 'https://tvcatchup.com' +url

        NAME = '%s - [COLOR orange]%s[/COLOR]' % (name.replace('Watch ',''),whatson.strip())    
        try:addDir(NAME,_URL_,200,iconimage+'|User-Agent='+UA)
        except:pass

    
    
def PLAY_STREAM(name,url,iconimage):
 
    headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'en-US,en;q=0.9',
            'Cache-Control':'no-cache',
            'Connection':'keep-alive',
            'Host':'tvcatchup.com',
            'Referer':'https://tvcatchup.com/channels',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25'}

    if PROXY_ENABLED=='true':
        link = OPEN_URL_PROXY(url)
        CHANGE=True
    else:
        link = net.http_GET(url,headers).content
        CHANGE=False
        
 
    stream= re.compile('<source src="(.+?)"').findall(link)[0].replace('amp;','')
    if CHANGE==True:
        stream = 'https://' +stream+'|X-Forwarded-For=%s' %ADDON.getSetting('custom_ip')
    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title':name})
    liz.setProperty("IsPlayable","true")
    liz.setPath(stream)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    



def OPEN_URL_PROXY(url):
    

    if 'just' in PROXYBASE:
        PROXYURL = 'http://www.justproxy.co.uk/index.php?q=%s'
        PROXYREF = 'http://www.justproxy.co.uk/'
        

    if 'england' in PROXYBASE:
        PROXYURL = 'http://www.englandproxy.co.uk/'
        PROXYREF = 'http://www.englandproxy.co.uk/'

        
    import base64
    if 'england' in PROXYREF:
        url=url.split('//')[1]
        req = PROXYURL + url
        REPLACE = 'http://www.englandproxy.co.uk:80/'
    else:    
        req = PROXYURL % base64.b64encode(url)
        REPLACE = PROXYURL % base64.b64encode(url)

    headers={'Referer':PROXYREF,
            'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25'}
    
    link = net.http_GET(req,headers).content
    return link.replace(REPLACE,'').replace('https://www.englandproxy.co.uk:443/','')



def addDir(name,url,mode,iconimage):
    
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name} )
        
        if mode ==200:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

                      
               
def get_params(path):
    params = {}
    path   = path.split('?', 1)[-1]
    pairs  = path.split('&')

    for pair in pairs:
        split = pair.split('=')
        if len(split) > 1:
            params[split[0]] = urllib.unquote_plus(split[1])

    return params
   
params      = get_params(sys.argv[2])            
url         = None
name        = None
mode        = None
iconimage   = None


try:    url=params["url"]
except: pass

try:    name = params["name"]
except: pass

try:    iconimage = params["iconimage"]
except: pass

try:    mode = int(params["mode"])
except: pass


#these are the modes which tells the plugin where to go
       

    
if mode==200:

        PLAY_STREAM(name,url,iconimage)

else:
    CATEGORIES()
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
