import urllib,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,urllib2
import settings
import json
import net
from threading import Timer
import datetime
import time
net = net.Net()


PLUGIN='plugin.video.notfilmon'
ADDON = xbmcaddon.Addon(id=PLUGIN)

#Global Constants
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
channel= 'http://www.filmon.com/channel/'
base='http://dl.dropbox.com/u/129714017/hubmaintenance/'
logo = 'http://static.filmon.com/couch/channels/'
res= settings.res()
addon = xbmcaddon.Addon(id='plugin.video.notfilmon')

datapath = xbmc.translatePath(addon.getAddonInfo('profile'))
cookie_path = os.path.join(datapath, 'cookies')

loginurl = 'http://www.filmon.com/ajax/login'
email    =ADDON.getSetting('user')
password =ADDON.getSetting('pass')

if os.path.exists(cookie_path) == False:
        os.makedirs(cookie_path)


cookie_jar = os.path.join(cookie_path, "FilmOn.lwp")
def login():
    header_dict = {}
    header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    header_dict['Host'] = 'www.filmon.com'
    header_dict['Referer'] = 'http://www.filmon.com/'
    header_dict['User-Agent'] = 'Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev>(KHTML, like Gecko) Chrome/<Chrome Rev> Safari/<WebKit Rev>'
    header_dict['Content-Type'] = 'application/x-www-form-urlencoded'
    header_dict['Connection'] = 'keep-alive'
    form_data = ({'login': email, 'password': password,'remember': '1'})	
    net.set_cookies(cookie_jar)
    login = net.http_POST('http://www.filmon.com/user/login', form_data=form_data, headers=header_dict)
    net.save_cookies(cookie_jar)
    keep_alive()

if ADDON.getSetting('visitor_ga')=='':
    from random import randint
    ADDON.setSetting('visitor_ga',str(randint(0, 0x7fffffff)))

VERSION = "4.6.1"
PATH = "FilmOn"            
UATRACK="UA-3174686-20"

def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev>(KHTML, like Gecko) Chrome/<Chrome Rev> Safari/<WebKit Rev>')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
    
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Magic Browser')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
def CATEGORIES():
                url='http://www.filmon.com/group'
                net.set_cookies(cookie_jar)
                html = net.http_GET(url).content
                link = html.encode('ascii', 'ignore')
                match=re.compile('<li class="group-item">.+?<a href="(.+?)">.+?"logo" src="(.+?)" title="(.+?)"',re.DOTALL).findall(link)
                for url, iconimage , name in match:
                         
                        addDir(name,url,3,iconimage,'',name)
                #addDir('Need Help??','url',2000,base+'images/help.jpg',base+'images/fanart/expert.jpg','')
                setView('movies', 'default') 
                
def Channels(url,name,group):
        r='<li class="channel i-box-sizing".+?channel_id="(.+?)">.+?"channel_logo" src="(.+?)" title="(.+?)"'
        net.set_cookies(cookie_jar)
        html = OPEN_URL('http://www.filmon.com'+url)
        match=re.compile(r,re.DOTALL).findall(html)
        for id , iconimage , name in match:
            addDir(name,'http://www.filmon.com'+url.replace('channel','tv'),2,iconimage,id,group)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
        setView('movies', 'default') 
        #GA('None',group) 
                
def regex_from_to(text, from_string, to_string, excluding=True):
    if excluding:
        r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
    else:
        r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
    return r
        
def play_filmon(name,url,iconimage,description):
    streamerlink = net.http_GET(url).content.encode("utf-8").rstrip()
    net.save_cookies(cookie_jar)
    swfplay = 'http://www.filmon.com' + regex_from_to(streamerlink, '"streamer":"', '",').replace("\/", "/")

    name = name.replace('[COLOR cyan]','').replace('[/COLOR]','')
    dp = xbmcgui.DialogProgress()
    dp.create('Opening ' + name.upper())
    utc_now = datetime.datetime.now()
    channel_name=name
    net.set_cookies(cookie_jar)
    url='http://www.filmon.com/channel/%s' % (description)
    link = net.http_GET(url,headers={'Accept':'application/json, text/javascript, */*; q=0.01'}).content
    link = json.loads(link)
    link = str(link)
	
    next_p = regex_from_to(link, "next_playing'", "u'title")
    try:
        n_start_time = datetime.datetime.fromtimestamp(int(regex_from_to(next_p, "startdatetime': u'", "',")))
        n_end_time = datetime.datetime.fromtimestamp(int(regex_from_to(next_p, "enddatetime': u'", "',")))
        n_programme_name = regex_from_to(next_p, "programme_name': u'", "',")
        n_start_t = n_start_time.strftime('%H:%M')
        n_end_t = n_end_time.strftime('%H:%M')
        n_p_name = "[COLOR cyan]Next: %s (%s-%s)[/COLOR]" % (n_programme_name, n_start_t, n_end_t)
    except:
        n_p_name = ""
		
    now_p = regex_from_to(link, "now_playing':", "u'tvguide")
    try:
        start_time = datetime.datetime.fromtimestamp(int(regex_from_to(now_p, "startdatetime': u'", "',")))
        end_time = datetime.datetime.fromtimestamp(int(regex_from_to(now_p, "enddatetime': u'", "',")))
        programme_name = regex_from_to(now_p, "programme_name': u'", "',")
        description = ""
        start_t = start_time.strftime('%H:%M')
        end_t = end_time.strftime('%H:%M')
        p_name = "%s (%s-%s)" % (programme_name, start_t, end_t)
        dp.update(50, p_name)
    except:
        try:
            p_name = programme_name
        except:
            p_name = name
    streams = regex_from_to(link, "streams'", "u'tvguide")
    hl_streams = regex_get_all(streams, '{', '}')
    if ADDON.getSetting('res') == '1':
        url = regex_from_to(hl_streams[0], "url': u'", "',")
        name = regex_from_to(hl_streams[0], "name': u'", "',")
    else:
        url = regex_from_to(hl_streams[1], "url': u'", "',")
        name = regex_from_to(hl_streams[1], "name': u'", "',")      
    try:
        timeout = regex_from_to(hl_streams[1], "watch-timeout': u'", "',")
    except:
        timeout = '86500'



    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    handle = str(sys.argv[1])
    try:
        listitem = xbmcgui.ListItem(p_name + ' ' + n_p_name, iconImage=iconimage, thumbnailImage=iconimage, path=url)
        if handle != "-1":	
            listitem.setProperty("IsPlayable", "true")
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
        else:
            xbmcPlayer = xbmc.Player()
            xbmcPlayer.play(url,listitem)
    except:
        listitem = xbmcgui.ListItem(channel_name, iconImage=iconimage, thumbnailImage=iconimage, path=url)
        if handle != "-1":
            listitem.setProperty("IsPlayable", "true")
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
        else:
            xbmcPlayer = xbmc.Player()
            xbmcPlayer.play(url,listitem)
    dp.close()

def regex_get_all(text, start_with, end_with):
    r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
    return r
            
def filmon_epg(url,group):
        url1='http://www.filmon.com/tvguide/'
        html = net.http_GET(url1).content
        link1 = html.encode('ascii', 'ignore')
        link=str(link1).replace('\n','')
        match=re.compile('bottom">(.+?)</h3>.+?href="(.+?)" >                <img src="(.+?)".+?.+?div class="title">.+?</div>.+?h4>(.+?)/h4>.+?"description">(.+?)/div>').findall(link)
        for name,  url1, iconimage, showname, description in match:
                cleandesc=str(description).replace('",','').replace('                ','').replace('<a class="read-more" href="/tvguide/','').replace('">Read more... &rarr;</a>','').replace('\xc3','').replace('\xa2','').replace('\xe2','').replace('\x82','').replace('\xac','').replace('\x84','').replace('\xa2s','').replace('\xc2','').replace('\x9d','').replace('<','')
                showname = str(showname).replace('<','')
                description = '[B]%s [/B]\n\n%s' % (showname,cleandesc)
                url = 'http://www.filmon.com'+str(url1)
                addDir(name,url,2,iconimage,description,'TV Guide')
                xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
                setView('movies', 'epg')
         
                
                
def FilmOn(name,url,iconimage,description,group):
                GA(group,name)
                pageurl=str(url)
                net.set_cookies(cookie_jar)
                html = net.http_GET(url).content
                link1 = html.encode('ascii', 'ignore')
                link=str(link1).replace('\n','')
                link=str(link1).replace('\n','')
                if ADDON.getSetting('res') == '0':
                        match=re.compile('"name":"(.+?)".+?"quality":"(.+?)".+?"url":"(.+?)}').findall(link)
                        for playPath,quality, a in match:
                                try:
                                    a=match[1][2]
                                except:
                                    pass
                                if 'mp4' in playPath:
                                    if not 'promo' in playPath:
                                            url1=str(a).replace('\\','')
                                            url2=str(a).replace('\\','').replace('"','')
                                            regex = re.compile('rtmp://(.+?)/(.+?)/(.+?)/"')
                                            match1 = regex.search(url1)
                                            app = '%s/%s/' %(match1.group(2), match1.group(3))
                                            swfUrl='http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf?v=28'
                                            url2=str(url2)+str(playPath)
                                elif 'm4v' in playPath:
                                        url1=str(a).replace('\\','')
                                        url2=str(a).replace('\\','').replace('"','')
                                        app = 'vodlast'
                                        swfUrl= 'http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf'
                                        url2=str(url2)+'/'+str(playPath)
                                else:
                                    try:
                                            url1=str(a).replace('\\','')
                                            url2=str(a).replace('\\','').replace('"','')
                                            regex = re.compile('rtmp://(.+?)/(.+?)id=(.+?)"')
                                            match1 = regex.search(url1)
                                            app = '%sid=%s' %(match1.group(2), match1.group(3))
                                            swfUrl='http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf?v=28'
                                            url2=str(url2)+'/'+str(playPath)
                                    except:
                                            pass
                                    try:
                                            url1=str(a).replace('\\','')
                                            url2=str(a).replace('\\','').replace('"','')
                                            regex = re.compile('rtmp://(.+?)/(.+?)/(.+?)id=(.+?)"')
                                            match1 = regex.search(url1)
                                            app = '%s/%sid=%s' %(match1.group(2), match1.group(3),match1.group(4))
                                            swfUrl= 'http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf'
                                    except:
                                            pass
                                if 'mp4' in url2:
                                    url= str(url2)+'/'+str(playPath)+' playpath='+str(playPath)+' app='+str(app)+' swfUrl='+str(swfUrl)+' pageurl='+str(url)+' live=true'
                                else:
                                    iconimage=str(iconimage)
                                    tcUrl=str(url2)
                                    pageUrl = pageurl
                                    url= str(url2)+'/'+str(playPath)+' playpath='+str(playPath)+' app='+str(app)+' swfUrl='+str(swfUrl)+' tcUrl='+str(tcUrl)+' pageurl='+str(pageUrl)+' live=true'
                                quality=quality.replace('480p','HIGH').replace('360p','LOW')
                                addLink(quality,url,iconimage,name,'','','','','')
                else:
                        match=re.compile('"name":"(.+?)".+?"quality":".+?".+?"url":"(.+?)}').findall(link)
                        if 'promo' in match[0][0]:
                            playPath=match[1][0]
                        else:
                            playPath=match[0][0]
                        if ADDON.getSetting('res') == '1':
                            playPath=str(playPath).replace('high','low')
                        elif ADDON.getSetting('res') == '2':
                            playPath=str(playPath).replace('low','high')
                        a=match[1][1]
                        if 'mp4:' in playPath:
                                url1=str(a).replace('\\','')
                                url2=str(a).replace('\\','').replace('"','')
                                regex = re.compile('rtmp://(.+?)/(.+?)/(.+?)/"')
                                match1 = regex.search(url1)
                                app = '%s/%s/' %(match1.group(2), match1.group(3))
                                swfUrl='http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf?v=28'
                                url2=str(url2)+str(playPath)
                        elif 'm4v' in playPath:
                                url1=str(a).replace('\\','')
                                url2=str(a).replace('\\','').replace('"','')
                                app = 'vodlast'
                                swfUrl= 'http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf'
                                url2=str(url2)+'/'+str(playPath)
                        else:
                                try:
                                    url1=str(a).replace('\\','')
                                    url2=str(a).replace('\\','').replace('"','')
                                    regex = re.compile('rtmp://(.+?)/(.+?)id=(.+?)"')
                                    match1 = regex.search(url1)
                                    app = '%sid=%s' %(match1.group(2), match1.group(3))
                                    swfUrl='http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf?v=28'
                                    url2=str(url2)+'/'+str(playPath)
                                except:
                                    pass
                                try:
                                    url1=str(a).replace('\\','')
                                    url2=str(a).replace('\\','').replace('"','')
                                    regex = re.compile('rtmp://(.+?)/(.+?)/(.+?)id=(.+?)"')
                                    match1 = regex.search(url1)
                                    app = '%s/%sid=%s' %(match1.group(2), match1.group(3),match1.group(4))
                                    swfUrl= 'http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf'
                                except:
                                    pass
                        if 'mp4' in url2:
                            stream= str(url2)+'/'+str(playPath)+' playpath='+str(playPath)+' app='+str(app)+' swfUrl='+str(swfUrl)+' pageurl='+str(url)+' live=true'
                            PLAY_STREAM(name,stream,iconimage)
                        else:
                            iconimage=str(iconimage)
                            tcUrl=str(url2)
                            pageUrl = pageurl
                            url= str(url2)+'/'+str(playPath)+' playpath='+str(playPath)+' app='+str(app)+' swfUrl='+str(swfUrl)+' tcUrl='+str(tcUrl)+' pageurl='+str(pageUrl)+' live=true'
                            PLAY_STREAM(name,url,iconimage)
                                        
def MyRecordings(url,group):
                net.set_cookies(cookie_jar)
                url='http://www.filmon.com/my/recordings'
                html = net.http_GET(url).content
                link = html.encode('ascii', 'ignore')
                match=re.compile('"stream_url":"(.+?),"stream_name":"(.+?)","id":".+?","title":"(.+?)","description":"(.+?)","channel_id":"(.+?)"').findall(link)
                for a, playPath, name, description, channel in match:
                        url1=str(a).replace('\/','/')
                        url2=str(a).replace('\/','/').replace('"','')
                        regex = re.compile('rtmp://(.+?)/(.+?)/(.+?)/(.+?)/(.+?)/(.+?)/(.+?)"')
                        match1 = regex.search(url1)
                        try:
                                        app = '%s/%s/%s/%s/%s/%s' %(match1.group(2), match1.group(3),match1.group(4),match1.group(5),match1.group(6),match1.group(7))
                        except:
                                app=''
                        tcUrl=str(url2)
                        iconimage='https://static.filmon.com/couch/channels/%s/big_logo.png' % str(channel)
                        swfUrl= 'http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf'
                        pageUrl = 'http://www.filmon.com/my/recordings'
                        url= str(url2)+'/'+str(playPath)+' playpath='+str(playPath)+' app='+str(app)+' swfUrl='+str(swfUrl)+' tcUrl='+str(tcUrl)+' pageurl='+str(pageUrl)
                        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
                        addLink(name,url,iconimage,playPath,app,pageUrl,swfUrl,tcUrl,description)
                        setView('movies', 'epg') 

def parseDate(dateString):
    try:
        return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
    except:
        return datetime.datetime.today() - datetime.timedelta(days = 1) #force update


def checkGA():

    secsInHour = 60 * 60
    threshold  = 2 * secsInHour

    now   = datetime.datetime.today()
    prev  = parseDate(ADDON.getSetting('ga_time'))
    delta = now - prev
    nDays = delta.days
    nSecs = delta.seconds

    doUpdate = (nDays > 0) or (nSecs > threshold)
    if not doUpdate:
        return

    ADDON.setSetting('ga_time', str(now).split('.')[0])
    APP_LAUNCH()
    
    
    
                    
def send_request_to_google_analytics(utm_url):
    ua='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    import urllib2
    try:
        req = urllib2.Request(utm_url, None,
                                    {'User-Agent':ua}
                                     )
        response = urllib2.urlopen(req).read()
    except:
        print ("GA fail: %s" % utm_url)         
    return response
       
def GA_track(group,name):
        try:
            try:
                from hashlib import md5
            except:
                from md5 import md5
            from random import randint
            import time
            from urllib import unquote, quote
            from os import environ
            from hashlib import sha1
            VISITOR = ADDON.getSetting('visitor_ga')
            utm_gif_location = "http://www.google-analytics.com/__utm.gif"
            if not group=='None':
                    utm_track = utm_gif_location + "?" + \
                            "utmwv=" + VERSION + \
                            "&utmn=" + str(randint(0, 0x7fffffff)) + \
                            "&utmt=" + "event" + \
                            "&utme="+ quote("5(channel*click*"+group+':'+name+")")+\
                            "&utmac=" + UATRACK + \
                            "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR,VISITOR,"2"])
                    try:
                        print "============================ POSTING TRACK EVENT ============================"
                        send_request_to_google_analytics(utm_track)
                    except:
                        print "============================  CANNOT POST TRACK EVENT ============================" 
        except:
            print "================  CANNOT POST TRACK EVENT ANALYTICS  ================" 
    
def GA(group,name):
        try:
            try:
                from hashlib import md5
            except:
                from md5 import md5
            from random import randint
            import time
            from urllib import unquote, quote
            from os import environ
            from hashlib import sha1
            VISITOR = ADDON.getSetting('visitor_ga')
            utm_gif_location = "http://www.google-analytics.com/__utm.gif"
            if name=="None":
                    utm_url = utm_gif_location + "?" + \
                            "utmwv=" + VERSION + \
                            "&utmn=" + str(randint(0, 0x7fffffff)) + \
                            "&utmp=" + quote(PATH) + \
                            "&utmac=" + UATRACK + \
                            "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
            else:
                if group=="None":
                       utm_url = utm_gif_location + "?" + \
                                "utmwv=" + VERSION + \
                                "&utmn=" + str(randint(0, 0x7fffffff)) + \
                                "&utmp=" + quote(PATH+"/"+name) + \
                                "&utmac=" + UATRACK + \
                                "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
                else:
                       utm_url = utm_gif_location + "?" + \
                                "utmwv=" + VERSION + \
                                "&utmn=" + str(randint(0, 0x7fffffff)) + \
                                "&utmp=" + quote(PATH+"/"+group+"/"+name) + \
                                "&utmac=" + UATRACK + \
                                "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
                                
            print "============================ POSTING ANALYTICS ============================"
            send_request_to_google_analytics(utm_url)
            
        except:
            print "================  CANNOT POST TO ANALYTICS  ================" 
            
            
def APP_LAUNCH():
        try:
            log_path = xbmc.translatePath('special://logpath')
            log = os.path.join(log_path, 'xbmc.log')
            logfile = open(log, 'r').read()
            match=re.compile('Platform: (.+?)\. Built.+?').findall(logfile)
        except:
            logfile='Starting XBMC (Unknown Git:.+?Platform: Unknown. Built.+?'
            match=re.compile('Platform: (.+?)\. Built.+?').findall(logfile)
        print '==========================   '+PATH+' '+VERSION+'   =========================='
        try:
            from hashlib import md5
        except:
            from md5 import md5
        from random import randint
        import time
        from urllib import unquote, quote
        from os import environ
        from hashlib import sha1
        import platform
        VISITOR = ADDON.getSetting('visitor_ga')
        match=re.compile('Platform: (.+?)\. Built.+?').findall(logfile)
        for PLATFORM in match:
            print PLATFORM
            utm_gif_location = "http://www.google-analytics.com/__utm.gif"
            utm_track = utm_gif_location + "?" + \
                    "utmwv=" + VERSION + \
                    "&utmn=" + str(randint(0, 0x7fffffff)) + \
                    "&utmt=" + "event" + \
                    "&utme="+ quote("5(app*launch*"+PLATFORM+")")+\
                    "&utmac=" + UATRACK + \
                    "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR,VISITOR,"2"])
            try:
                print "============================ POSTING APP LAUNCH TRACK EVENT ============================"
                send_request_to_google_analytics(utm_track)
            except:
                print "============================  CANNOT POST APP LAUNCH TRACK EVENT ============================" 

class HUB( xbmcgui.WindowXMLDialog ): # The call MUST be below the xbmcplugin.endOfDirectory(int(sys.argv[1])) or the dialog box will be visible over the pop-up.
    def __init__( self, *args, **kwargs ):
        self.shut = kwargs['close_time'] 
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        xbmc.executebuiltin( "Skin.SetBool(AnimeWindowXMLDialogClose)" )
                                       
    def onInit( self ):
        xbmc.Player().play('%s/resources/skins/DefaultSkin/media/xbmchub.mp3'%ADDON.getAddonInfo('path'))# Music.
        while self.shut > 0:
            xbmc.sleep(1000)
            self.shut -= 1
        xbmc.Player().stop()
        self._close_dialog()
                
    def onFocus( self, controlID ): pass
    
    def onClick( self, controlID ): 
        if controlID == 12:
            xbmc.Player().stop()
            self._close_dialog()
        if controlID == 7:
            xbmc.Player().stop()
            self._close_dialog()

    def onAction( self, action ):
        if action in [ 5, 6, 7, 9, 10, 92, 117 ] or action.getButtonCode() in [ 275, 257, 261 ]:
            xbmc.Player().stop()
            self._close_dialog()

    def _close_dialog( self ):
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        time.sleep( .4 )
        self.close()



        
        
             
def pop():# Added Close_time for window auto-close length.....
    if xbmc.getCondVisibility('system.platform.ios'):
        if not xbmc.getCondVisibility('system.platform.atv'):
            popup = HUB('hub1.xml',ADDON.getAddonInfo('path'),'DefaultSkin',close_time=34,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%ADDON.getAddonInfo('path'))
    elif xbmc.getCondVisibility('system.platform.android'):
        popup = HUB('hub1.xml',ADDON.getAddonInfo('path'),'DefaultSkin',close_time=34,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%ADDON.getAddonInfo('path'))
    else:
        popup = HUB('hub.xml',ADDON.getAddonInfo('path'),'DefaultSkin',close_time=34,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%ADDON.getAddonInfo('path'))
    
    popup.doModal()
    del popup
                
def checkdate(dateString):
    try:
        return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
    except:
        return datetime.datetime.today() - datetime.timedelta(days = 1000) #force update


def check_popup():

    threshold  = 120

    now   = datetime.datetime.today()
    prev  = checkdate(ADDON.getSetting('pop_time'))
    delta = now - prev
    nDays = delta.days

    doUpdate = (nDays > threshold)
    if not doUpdate:
        return

    ADDON.setSetting('pop_time', str(now).split('.')[0])
    pop()
     
checkGA()
                
                            
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

                
def addDir(name,url,mode,iconimage,description,group):
                u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)+"&group="+urllib.quote_plus(group)
                ok=True
                liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
                liz.setInfo( type="Video", infoLabels={ "Title": name })
                if mode==2 and not mode==2000:
                    liz.setProperty("IsPlayable", "true")
                    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
                else:
                    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
                return ok
                                
def addLink(name,url,iconimage,playPath,app,pageUrl,swfUrl,tcUrl,description):
                ok=True
                liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
                liz.setInfo( type="Video", infoLabels={ "Title": playPath})
                liz.setProperty("IsPlayable","true")
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
                return ok 
                
def PLAY_STREAM(name,url,iconimage):
    dp = xbmcgui.DialogProgress()
    r='    Please Wait While We Load [COLOR yellow][B]%s[/B][/COLOR]'%(name)
    dp.create("NotFilmOn",'',r,'')
    programme_id=str(iconimage).replace('http://static.filmon.com/couch/channels/','').replace('/big_logo.png','')
    GA_track(programme_id,name)
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name} )
    liz.setProperty("IsPlayable","true")
    pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    pl.clear()
    pl.add(url, liz)
    xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(pl)
    dp.close()
                
                
def setView(content, viewType):
                # set content type so library shows more views and info
                if content:
                                xbmcplugin.setContent(int(sys.argv[1]), content)
                if ADDON.getSetting('auto-view') == 'true':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )
                                
                
                                   
#checkGA()
params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None
group=None

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
                group=urllib.unquote_plus(params["group"])
except:
                pass
                

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
print "Group: "+str(group)

if mode==None or url==None or len(url)<1:
                print ""
                CATEGORIES()
                         
elif mode==1:
                print ""+url
                filmon_epg(url,group)

elif mode==2:
                print ""+url
                play_filmon(name,url,iconimage,description)
                
elif mode==3:
                print ""+url
                Channels(url,name,group)
                
elif mode==4:
                print ""+url
                Channel_Lists(url)
                

                
elif mode==5:
                print ""+url
                MyRecordings(url,group)
                
elif mode==2000:
        pop()
xbmcplugin.endOfDirectory(int(sys.argv[1]))
#check_popup()
