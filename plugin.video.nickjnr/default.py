import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os
import json
import net
import htmlcleaner

net=net.Net()

#ee3fa
ADDON = xbmcaddon.Addon(id='plugin.video.nickjnr')
ICON = ADDON.getAddonInfo('icon')
FANART = ADDON.getAddonInfo('fanart')

ART = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.nickjnr/img/'))





def CATEGORIES():
    DOTCOM , THEPAGE ,API = GetLang()
    link = net.http_GET('http://www.nickjr.%s'%DOTCOM).content
    match= re.compile('"seriesKey":"(.+?)"').findall(link)
    for key in match:
        name = key.replace('-',' ').title()
        addDir(name,key,1,ART+ADDON.getSetting('lang')+'/'+key+'.jpg','0')
        
    setView('movies', 'default')


 

def Episodes(url,page):
    page = int(page)+1
    DOTCOM , THEPAGE ,API = GetLang()
    headers={'Referer':'http://www.nickjr.%s'%DOTCOM, 'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13 (.NET CLR 3.5.30729)'}
    link = net.http_GET('http://www.nickjr.%s/data/property%s.json?&urlKey=%s&apiKey=%s&page=%s' % (DOTCOM,THEPAGE,url,API,page),headers=headers).content

    link=json.loads(link)
    data=link['stream']
    for k in data:
        for w in k['items']:
            try:
                try:URL=w['data']['id']
                except:URL=None
                try:duration =' - [' +w['data']['duration']+']'
                except:duration = ''
                try:name=w['data']['title'] + duration
                except:
                    try:name=htmlcleaner.cleanUnicode(w['data']['title']) + duration
                    except:
                        try:name=htmlcleaner.clean(w['data']['title']) + duration
                        except:
                            name=''
                try:iconimage=w['data']['images']['thumbnail']['r1-1']
                except:
                    try:iconimage = w['data']['images']['thumbnail']['r25-12']
                    except:iconimage=''
       
                try:plot=htmlcleaner.cleanUnicode(w['data']['description'])
                except:
                    plot=''

                    

                if URL:    
                    addDir(name,URL,200,iconimage ,plot)
            except:
                pass
    if data:        
        addDir('Next Page >>',url,1,'' ,str(page))
    setView('movies', 'episode-view')



def GetError():
    lang = ADDON.getSetting('lang')
    if lang=='English':return 'Error Getting Stream'        
    if lang=='Spanish':return 'Error al obtener la transmision'
    if lang=='German':return 'Fehler beim Streamen'
    if lang=='Dutch':return 'Fout bij ophalen van stream'

def GetLang():
    lang = ADDON.getSetting('lang')
    if lang=='English':return 'tv','StreamPage','global_Nickjr_web'        
    if lang=='Spanish':return 'es','StreamPage','es_global_Nickjr_web'
    if lang=='German':return 'de','StreamPage','global_Nickjr_web'
    if lang=='Dutch':return 'nl','StreamPage','global_Nickjr_web'



def GrabStream(url):
    DOTCOM , THEPAGE ,API = GetLang()
    headers={'Host':'media.mtvnservices.com',
            'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13 (.NET CLR 3.5.30729)',
            'Referer':'http://www.nickjr.%s' % DOTCOM,
            'Connection':'close',
            'Accept-Encoding':'gzip, deflate'}
             
    new_url='http://media.mtvnservices.com/pmt/e1/access/index.html?uri=mgid:arc:video:nickjr.tv:%s&configtype=edge' % url
    link = net.http_GET(new_url,headers=headers).content

    link=json.loads(link)

    try:
        data=link['feed']['items'][0]['group']['content']+'&format=json'
        
        headers={'Host':'media-utils.mtvnservices.com',
                'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13 (.NET CLR 3.5.30729)',
                'Referer':'http://www.nickjr.%s' % DOTCOM,
                'Connection':'close',
                'Accept-Encoding':'gzip, deflate'}
        
        link = net.http_GET(data.replace('{device}','iPhone10,3'),headers=headers).content
        link=json.loads(link)

        return link['package']['video']['item'][0]['rendition'][0]['src']
    except:
        return False
    
def PLAY_STREAM(name,url,iconimage):
    STREAM =GrabStream(url)
    if STREAM:
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={'Title':name})
        liz.setProperty("IsPlayable","true")
        liz.setPath(STREAM)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    else:
        dialog = xbmcgui.Dialog()
        dialog.ok("Nick Jnr", GetError(),'', '')
    


def addDir(name,url,mode,iconimage,description):
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
            ok=True

            liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
            liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
            if mode ==200 or mode ==6 or mode ==14:
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
description = None


try:    url=params["url"]
except: pass

try:    name = params["name"]
except: pass

try:    iconimage = params["iconimage"]
except: pass

try:    mode = int(params["mode"])
except: pass

try:    description = params["description"]
except: pass

  

#these are the modes which tells the plugin where to go
       

if mode==1:
        Episodes(url,description)         


    
elif mode==200:

        PLAY_STREAM(name,url,iconimage)

else:
    CATEGORIES()
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
