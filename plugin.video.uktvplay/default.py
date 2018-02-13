import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os

import json


ADDON = xbmcaddon.Addon(id='plugin.video.uktvplay')

img=os.path.join(ADDON.getAddonInfo('path'),'resources','img')

#http://c.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId=2134509084001

def CATEGORIES():
    addDir('Categories','drama',3,'','')
    addDir('A To Z','url',5,'','')
    addDir('Search','url',11,'','')
    addDir('Dave','dave',1,img+'/dave.jpg','')
    addDir('Really','really',1,img+'/really.jpg','')
    addDir('Yesterday','yesterday',1,img+'/yesterday.png','')
    addDir('Drama','drama',1,img+'/drama.jpg','')


def GetContent(url):
    CHANNEL = url       
    xunity='http://vschedules.uktv.co.uk/mobile/v2/most_popular?channel=%s&carousel_limit=100&platform=ios&app_ver=4.1.0' % CHANNEL
    
    response=OPEN_URL(xunity)
    
    link=json.loads(response)

    for field in link:
        name= field['brand_name'].encode("utf-8")
        iconimage= field['brand_image'].encode("utf-8")
        channel=field['channel'].encode("utf-8")
        try:desc=field['teaser_text'].encode("utf-8")
        except:desc=''
        brand_id=field['brand_id']
        if CHANNEL in channel:
            
            addDir(name.strip(),str(brand_id),2,iconimage,desc)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)            
    setView('movies', 'default')


def GetCat(url):
       
    xunity='http://vschedules.uktv.co.uk/mobile/v2/genres?platform=ios&app_ver=4.1.0'
    
    response=OPEN_URL(xunity)
    
    link=json.loads(response)

    #data=link['data']

    for field in link:
        name= field['title'].encode("utf-8")
        iconimage= field['image'].encode("utf-8")
        brand_id=field['name']
        addDir(name.strip(),str(brand_id),4,iconimage,'')
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)            
    setView('movies', 'default')

def GetCatList(url):
       
    xunity='http://vschedules.uktv.co.uk/mobile/v2/genre_items?genre_name=%s&platform=ios&app_ver=4.1.0' % url.upper()
    
    response=OPEN_URL(xunity)
    
    link=json.loads(response)

    #data=link['data']

    for field in link:
        count=field['video_count']
        channel=field['channel'].encode("utf-8")
        color='grey'
        if 'Dave' in channel:
            color='green'
        if 'Drama' in channel:
            color='red' 
        if 'Yesterday' in channel:
            color='yellow'
        if 'Really' in channel:
            color='orange'   
        name= field['brand_name'].encode("utf-8") + ' (%s Episodes) - [COLOR %s]%s[/COLOR]' % (str(count),color,channel)
        iconimage= field['brand_image'].encode("utf-8")
        brand_id=field['brand_id']
        addDir(name.strip(),str(brand_id),2,iconimage,'')
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)            
    setView('movies', 'default')     

def GetEpisodes(url):
    xunity='http://vschedules.uktv.co.uk/mapi/branddata/?format=json&brand_id='+url
    
    response=OPEN_URL(xunity)
    
    link=json.loads(response)

    data=link['videos']

    for field in data:
        name= 'S'+field['series_txt']+'E'+field['episode_txt']+' - '+field['brand_name'].encode("utf-8")
        iconimage= field['episode_img_cached'].encode("utf-8")
        channel=field['channel'].encode("utf-8")
        desc=field['teaser_text'].encode("utf-8")
        brightcove_id_from_json=field['brightcove_video_id']
        watch_online_link=field['watch_online_link']
        matches = re.search('video=([0-9]+)$', watch_online_link)
        video_id_from_online_link=matches.group(1)
        addDir(name,str(video_id_from_online_link),200,iconimage,desc)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
    setView('movies', 'default') 


def char_range(c1, c2):
    
    for c in xrange(ord(c1), ord(c2)+1):
        yield chr(c)


def AtoZ():
    nameurl=[]
    urlurl=[]
    for name in char_range('A', 'Z'):
        nameurl.append(name)
        urlurl.append(name.upper())
        
    URL = 'http://vschedules.uktv.co.uk/mobile/v2/brand_list?channel=&letter=%s&&platform=ios&app_ver=4.1.0' %  urlurl[xbmcgui.Dialog().select('Please Select', nameurl)]
    response=OPEN_URL(URL)
    
    link=json.loads(response)


    for field in link:
        count=field['video_count']
        channel=field['channel'].encode("utf-8")
        color='grey'
        if 'Dave' in channel:
            color='green'
        if 'Drama' in channel:
            color='red' 
        if 'Yesterday' in channel:
            color='yellow'
        if 'Really' in channel:
            color='orange'   
        name= field['brand_name'].encode("utf-8") + ' (%s Episodes) - [COLOR %s]%s[/COLOR]' % (str(count),color,channel)
        iconimage= field['brand_image'].encode("utf-8")
        brand_id=field['brand_id']
        addDir(name.strip(),str(brand_id),2,iconimage,'')
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)            
    setView('movies', 'default')   


def MySearch():
    addDir('Search','',9,'','')
    favs = ADDON.getSetting('favs').split(',')
    for title in favs:
        if not len(title)<2:
            NEW_URL='http://vschedules.uktv.co.uk/mobile/v2/search?q=%s&platform=ios&app_ver=4.1.0' % title.replace(' ','%20')        
            addDir(title,NEW_URL,8,'','')


def Search(search_entered):
    favs = ADDON.getSetting('favs').split(',')
    if not search_entered:
        keyboard = xbmc.Keyboard('', 'Search iPlayer')
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText()

    search_entered = search_entered.replace(',', '')

    if len(search_entered) == 0:
        return

    if not search_entered in favs:
        favs.append(search_entered)
        ADDON.setSetting('favs', ','.join(favs))

    NEW_URL ='http://vschedules.uktv.co.uk/mobile/v2/search?q=%s&platform=ios&app_ver=4.1.0' % (search_entered.replace(' ','%20'))

    
    FindSearch(NEW_URL)

def FindSearch(url):
    response=OPEN_URL(url)
    
    link=json.loads(response)

    link=link['brands']
    
    for field in link:
        count=field['video_count']
        channel=field['channel'].encode("utf-8").title()
        color='grey'
        if 'Dave' in channel:
            color='green'
        if 'Drama' in channel:
            color='red' 
        if 'Yesterday' in channel:
            color='yellow'
        if 'Really' in channel:
            color='orange'   
        name= field['brand_name'].encode("utf-8") + ' (%s Episodes) - [COLOR %s]%s[/COLOR]' % (str(count),color,channel)
        iconimage= field['brand_image'].encode("utf-8")
        brand_id=field['brand_id']
        addDir(name.strip(),str(brand_id),2,iconimage,'')
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)            
    setView('movies', 'default')   


def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link


def PLAY_STREAM(name,url,iconimage):
    url='http://c.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId='+url
    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title':name})
    liz.setProperty("IsPlayable","true")
    liz.setPath(url)
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


def addDir(name,url,mode,iconimage,description):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
    menu=[]
    
    
    if mode == 8:
        menu.append(('[COLOR orange]Remove Search[/COLOR]','XBMC.Container.Update(%s?mode=12&name=%s)'% (sys.argv[0],name)))
        liz.addContextMenuItems(items=menu, replaceItems=False)
        is_Folder=False

    elif mode == 12:
        is_Folder=False
        
    elif mode ==200:
        liz.setProperty("IsPlayable","true")
        is_Folder=False

    else:
        is_Folder=True
        
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=is_Folder)

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





if mode==1:
    xbmc.log("UKTVPlay 1: "+str(url),xbmc.LOGNOTICE)
    GetContent(url)

elif mode==2:
    xbmc.log("UKTVPlay 2: "+str(url),xbmc.LOGNOTICE)
    GetEpisodes(url)

elif mode==3:
    xbmc.log("UKTVPlay 3: "+str(url),xbmc.LOGNOTICE)
    GetCat(url)

elif mode==4:
    xbmc.log("UKTVPlay 4: "+str(url),xbmc.LOGNOTICE)
    GetCatList(url)

elif mode==5:
    AtoZ()

elif mode==8:
    xbmc.log("UKTVPlay 8: "+str(url),xbmc.LOGNOTICE)
    FindSearch(url)

elif mode==9:
    xbmc.log("UKTVPlay 9: "+str(url),xbmc.LOGNOTICE)
    Search(url)

elif mode==11:
    MySearch()

elif mode == 12:
    favs = ADDON.getSetting('favs').split(",")
    try:
        favs.remove(name)
        ADDON.setSetting('favs', ",".join(favs))
    except:pass

elif mode==200:
    xbmc.log("UKTVPlay 200: "+str(url),xbmc.LOGNOTICE)
    PLAY_STREAM(name,url,iconimage)

else:
    CATEGORIES()


xbmcplugin.endOfDirectory(int(sys.argv[1]))
