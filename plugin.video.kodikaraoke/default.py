import urllib,urllib2,re,sys,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,xbmcvfs,string
import net
import settings
import json
import datetime
import time
import requests


PLUGIN='plugin.video.kodikaraoke'

net=net.Net()
begurl='http://www.sunflykaraoke.com/search/genre/'
          
endurl='?sort_Karaoke Tracks=popularity-desc'

THESITE ='kodikaraoke.com'

local = xbmcaddon.Addon(id=PLUGIN)

ADDON = settings.addon()
home = ADDON.getAddonInfo('path')
sfdownloads= xbmc.translatePath(os.path.join(ADDON.getSetting('sfdownloads'),''))

Kfolder= 'http://'+THESITE+'/payments/karaoke/'
K_db=Kfolder+'Karaoke.db'

db_dir = os.path.join(xbmc.translatePath("special://database"), 'Karaoke.db')


datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
newfont=ADDON.getSetting('newfont').lower()
cookie_path = os.path.join(datapath, 'cookies')
cookie_jar = os.path.join(cookie_path, "kodikaraoke")
FORCOOKIE  = os.path.join(cookie_path, "FORCOOKIE")

if os.path.exists(FORCOOKIE)==True:
    HAHA=open(FORCOOKIE).read()


if os.path.exists(datapath)==False:
    os.mkdir(datapath) 
if ADDON.getSetting('sfenable') == True:
    os.makedirs(sfdownloads)
if ADDON.getSetting('visitor_ga')=='':
    from random import randint
    ADDON.setSetting('visitor_ga',str(randint(0, 0x7fffffff)))
    




#addon = Addon('plugin.video.kodikaraoke',sys.argv)
art= "%s/KaraokeArt/"%local.getAddonInfo("path")
from sqlite3 import dbapi2 as database


def download_DB():
    import downloader
    dp = xbmcgui.DialogProgress()
    db_dir = xbmc.translatePath(os.path.join(home,'Karaoke.db'))
    dp.create("Kodi Karaoke","",'Building Database Please Wait', ' ')
    downloader.download(K_db, db_dir,dp)
    

def Update(s):
    import downloader
    dp = xbmcgui.DialogProgress()
    dp.create("Kodi Karaoke","",'Building Database Please Wait', ' ')
    downloader.download(K_db, db_dir,s,dp)


def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
  
       
      
db = database.connect(db_dir)
db.execute('CREATE TABLE IF NOT EXISTS tracklist (sunfly_name, number, artist, track, iconimage, url)')
db.execute('CREATE TABLE IF NOT EXISTS favourites (track_name, artist, track, iconimage, url)')
db.commit()
db.close()



def GRABBER(type,mode,item):
    db = database.connect( db_dir );cur = db.cursor()
    if type == 1:#EXACT MATCH ALL
        item = '%'+item+'%'
        cached = cur.fetchall()
        try: cur.execute('SELECT * FROM tracklist WHERE %s = "%s"' %(mode,item))
        except:pass
    elif type == 2: #EXACT MATCH ONE
        item = '%'+item+'%'
        try: cur.execute('SELECT * FROM tracklist WHERE %s = "%s"' %(mode,item))
        except:pass
        cached = cur.fetchone()
    elif type == 3:#NEAREST MATCH ONE
        item = '%'+item+'%'
        try: cur.execute('SELECT * FROM tracklist WHERE %s LIKE "%s"' %(mode,item))
        except:pass
        cached = cur.fetchone()
    elif type == 4:# NEAREST MATCH ALL
        item = '%'+item+'%'
        try: cur.execute('SELECT * FROM tracklist WHERE %s LIKE "%s"' %(mode,item))
        except:pass
        cached = cur.fetchall()
    elif type == 5:# NEAREST MATCH ALL BY FIRST LETTER
        item = item+'%'
        try: cur.execute('SELECT * FROM tracklist WHERE %s LIKE "%s"' %(mode,item))
        except:pass
        cached = cur.fetchall()
    if cached:
        db.close()
        return cached

def STRIP(name):
  return re.sub(r'\[.*?\]|\(.*?\)|\W -', ' ', name).strip()


def SYSEXIT():
    sys.exit()
    xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
    xbmc.executebuiltin("XBMC.ActivateWindow(Videos)")


def parse_date(dateString):
    import time
    return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))

def getday():
    today = datetime.datetime.today()
    return today.strftime("%A")  

def getYday():
    from datetime import timedelta
    today = datetime.datetime.today()-timedelta(hours=24)
    return today.strftime("%A") 

def sessionExpired():
   
    expiry=ADDON.getSetting('login_time')


    now        = datetime.datetime.today()
 
    
    prev = parse_date(expiry)


    return (now > prev)


def CheckUserData():    
    if ADDON.getSetting('user')=='':
        dialog = xbmcgui.Dialog()
        if dialog.yesno(THESITE.upper(), "If You Dont Have An Account", "Please Sign Up At",THESITE.upper(),"Exit","Carry On"):
            
            dialog.ok(THESITE.upper(), "You Now Need To Input", "Your [COLOR yellow]Username[/COLOR]")
            search_entered = ''
            keyboard = xbmc.Keyboard(search_entered, THESITE.upper())
            keyboard.doModal()
            if keyboard.isConfirmed():
                search_entered = keyboard.getText() 
            ADDON.setSetting('user',search_entered)
            
            dialog.ok(THESITE.upper(), "You Now Need To Input", "Your [COLOR yellow]Password[/COLOR]")
            search_entered = ''
            keyboard = xbmc.Keyboard(search_entered, THESITE.upper())
            keyboard.doModal()
            if keyboard.isConfirmed():
                search_entered = keyboard.getText() 
            ADDON.setSetting('pass',search_entered)
            ADDON.setSetting('login_time','2000-01-01 00:00:00')
        else:
            EXIT()

def Login():
    s = requests.session()
    loginurl = 'http://'+THESITE+'/payments/login'
    username = ADDON.getSetting('user')
    password = ADDON.getSetting('pass')

    TIME = time.time()- 3600
    
    data={'amember_login':username,'amember_pass':password,'login_attempt_id':str(TIME).split('.')[0],'remember_login':'1','':'Login'} 
  

    headers={'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'en-US,en;q=0.9',
    'Connection':'keep-alive',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Host':THESITE,
    'Origin':'http://'+THESITE,
    'Referer':'http://'+THESITE+'/payments/login',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest'}

    html = s.post(loginurl, data, headers=headers,allow_redirects=False)

    if 'true' in html.content:
       

     
       if os.path.exists(cookie_path) == False:
               os.makedirs(cookie_path)
       f = open(cookie_jar, 'w')
       f.write(html.headers['Set-Cookie'])
       f.close()

       IDNUMBER = s.get('http://'+THESITE+'/payments/karaoke/update.txt', headers=headers).content

       if int(IDNUMBER) > int(ADDON.getSetting('id')):
           dp = xbmcgui.Dialog()
           dp.ok("Kodi Karaoke","",'There is a New Database Update', 'Please Wait')
           Update(s)
           

       ADDON.setSetting('login_time',str(datetime.datetime.today()+ datetime.timedelta(hours=6)).split('.')[0])
       if int(IDNUMBER) > int(ADDON.getSetting('id')):
           ADDON.setSetting('id',IDNUMBER)
           

    if 'false' in html.content:
       import json
       link=json.loads(html)
       error=link['error']
       dialog = xbmcgui.Dialog()
       dialog.ok(THESITE.upper(), '',str(error).replace("[u'",'').replace("']",''), "")
       dialog.ok(THESITE.upper(), '','We Will Exit Kodi Karaoke Now', "")
       if not 'please' in str(error).lower() or not 'administator' in str(error).lower():
          username = ADDON.setSetting('user','')
          password = ADDON.setSetting('pass','')
          try:os.remove(cookie_jar)
          except:pass
       SYSEXIT()
       return False  

def KaraokeSource(url):
    tagNAME='Kodi Karoke Folder'; tagURL=url;
    path=os.path.join(xbmc.translatePath('special://home'),'userdata','sources.xml')
    if not os.path.exists(path): f=open(path,mode='w'); f.write('<sources><files><source><name>'+tagNAME+'</name><path pathversion="1">'+tagURL+'</path></source></files></sources>'); f.close();
    f=open(path,mode='r'); str=f.read(); f.close()
    if not tagURL in str:
        if '</files>' in str: str=str.replace('</files>','<source><name>'+tagNAME+'</name><path pathversion="1">'+tagURL+'</path></source></files>'); f=open(path,mode='w'); f.write(str); f.close()
        else: str=str.replace('</sources>','<files><source><name>'+tagNAME+'</name><path pathversion="1">'+tagURL+'</path></source></files></sources>'); f=open(path, mode='w'); f.write(str); f.close()

    
  
def CATEGORIES():  
        freeyoutube('url')


        
            
def freeyoutube(url):
        addDir('[COLOR '+newfont+']'+'Visit[/COLOR] [COLOR lime]>>> [/COLOR][COLOR orange]kodikaraoke.com[/COLOR] [COLOR lime]<<< [/COLOR][COLOR '+newfont+']'+'for pro features[/COLOR]','url',15,art+'Main/favorites.png','',1)
        addDir('[COLOR '+newfont+']'+'Search[/COLOR]-[COLOR '+newfont+']'+'L[/COLOR]ite Version','url',5003,art+'Main/Search.png','none',1)
        if ADDON.getSetting('downloads') == 'true':
            addDir('[COLOR '+newfont+']'+'D[/COLOR]ownloads','url',15,art+'Main/favorites.png','',1)
        addDir('[COLOR '+newfont+']'+'Most[/COLOR] Popular','http://www.sunflykaraoke.com/tracks?dir=asc&limit=200&order=popular',7,art+'AtoZ/P.png','none',1)
        addDir('[COLOR '+newfont+']'+'L[/COLOR]atest','http://www.sunflykaraoke.com/tracks?dir=asc&limit=200&order=latestalbums',7,art+'AtoZ/L.png','none',1)
        addDir('[COLOR '+newfont+']'+'Browse[/COLOR] Artist','http://www.lyricsmania.com/lyrics/%s.html',1,art+'Main/Artist.png','none',4)
        addDir('[COLOR '+newfont+']'+'Browse[/COLOR] Tracks','http://www.sunflykaraoke.com/tracks/search/byletter/letter/%s/',1,art+'Main/Title.png','none',7)
        addDir('[COLOR '+newfont+']'+'G[/COLOR]enre','http://www.sunflykaraoke.com/',8,art+'Main/Genre.png','none',1)
        setView('movies', 'MAIN')
        
def ProKaraoke(url):
        try:
            if ADDON.getSetting('user')=='':
                CheckUserData()
            if sessionExpired() or os.path.exists(cookie_jar) == False:
                Login()  
            addDir('[COLOR '+newfont+']'+'Search[/COLOR]-[COLOR '+newfont+']'+'K[/COLOR]odi Karaoke','url',5003,art+'Main/Search.png','none',1)
            if ADDON.getSetting('sfenable') == 'true':
                KaraokeSource(sfdownloads)
                addDir('[COLOR '+newfont+']'+'D[/COLOR]ownloads','url',31,art+'Main/favorites.png','',1)
            addDir('[COLOR '+newfont+']'+'Search[/COLOR] By Number','url',25,art+'Main/Search.png','none',1)
            addDir('[COLOR '+newfont+']'+'Browse[/COLOR] Artist','http://www.sunflykaraoke.com/',1,art+'Main/Artist.png','none',23)
            addDir('[COLOR '+newfont+']'+'Browse[/COLOR] Tracks','http://www.sunflykaraoke.com/',1,art+'Main/Title.png','none',24)
            addDir('[COLOR '+newfont+']'+'G[/COLOR]enre','http://www.sunflykaraoke.com/',32,art+'Main/Genre.png','none',1)
            addDir('[COLOR '+newfont+']'+'D[/COLOR]ownload Database / Fix Database','url',103,'','none',1)
        except:
            addDir('[COLOR '+newfont+']'+'F[/COLOR]ix Database','url',103,'','none',1)
        setView('movies', 'MAIN')

def AtoZ(url,number,fanart):

    if '%s' in url:
        addDir('0-9',url%'0-9',number,"%s/KaraokeArt/AtoZ/%s.png"%(local.getAddonInfo("path"),'0-9'),fanart,1)
        for i in string.ascii_uppercase:
            addDir(i,url%i,number,"%s/KaraokeArt/AtoZ/%s.png"%(local.getAddonInfo("path"),i),fanart,1)
    else:
        for i in string.ascii_uppercase:
            addDir(i,url,number,"%s/KaraokeArt/AtoZ/%s.png"%(local.getAddonInfo("path"),i),fanart,1)
    setView('movies', 'A-Z')

def FAVOURITES(switch,name,iconimage,url):
   
    if 'http' in Kfolder:
        url=url.replace(' ','%20')
        iconimage=iconimage.replace(' ','%20')
        
       
    IMAGE = os.path.join(ADDON.getAddonInfo('path'), 'icon.png')
   
    db = database.connect( db_dir );cur = db.cursor()
    if switch == 'add':
        sql = "INSERT OR REPLACE INTO favourites (track_name,iconimage,url) VALUES(?,?,?)"
        cur.execute(sql, (name,iconimage.replace(Kfolder,''),url.replace(Kfolder,'')))
        db.commit(); db.close()
        xbmc.executebuiltin('XBMC.Notification('+name+',Added to Favorites,2000,'+IMAGE+')')
    if switch == 'delete':
        cur.execute("DELETE FROM favourites WHERE track_name='%s'"%name)
        db.commit(); db.close()
        xbmc.executebuiltin('XBMC.Notification('+name.replace('  ',' ')+',Deleted from Favorites,2000,'+IMAGE+')')
        xbmc.executebuiltin("XBMC.Container.Refresh")
    if switch == 'display':
        cur.execute("SELECT * FROM favourites")
        cached = cur.fetchall()
        if cached:
            for name,artist,track,iconimage,url in cached:
                if url[-4]=='.':
                    addLinkSF(name,url,url.replace('.avi','.jpg'))
                else:
                    addLink(name,url,iconimage, '',showcontext=True)
        
def GENRE(url):
        link=net.http_GET('http://www.sunflykaraoke.com/genre').content.encode('ascii','ignore')
        match=re.compile('class="thumb_img">.+?<img src="(.+?)".+?href="(.+?)">(.+?)</a>',re.DOTALL).findall(link)
        for iconimage,url , name in match:
            addDir(name,url+'?dir=asc&limit=200&order=latestalbums',10,iconimage,art+'Main/Fanart_G.jpg',1) 
        
        setView('movies', 'GENRE')
        
def GENRESF(url):
        link=net.http_GET('http://www.sunflykaraoke.com/genre').content.encode('ascii','ignore')
        match=re.compile('class="thumb_img">.+?<img src="(.+?)".+?href="(.+?)">(.+?)</a>',re.DOTALL).findall(link)
        for iconimage,url , name in match:
            addDir(name,url+'?dir=asc&limit=200&order=latestalbums',33,iconimage,art+'Main/Fanart_G.jpg',1) 
        
        setView('movies', 'GENRE')
            
def Next_Page(link):
    link = link.split('class="paging-bar-pages">')[1]
    link=link.split('<a href=')
    for l in link:
        match=re.compile('"(.+?)#.+?" class="arrow">&gt;</a>').findall(l)        
        if match:
            return match
    return None 


def FirstSearchDir(name):
    if 'odi' in name:
        mode=16
        addDir('[COLOR '+newfont+']'+'Search[/COLOR]-[COLOR '+newfont+']'+'K[/COLOR]odi Karaoke','url',16,art+'Main/Search.png','none',1)

    else:
        mode=3
        addDir('[COLOR '+newfont+']'+'Search[/COLOR]-[COLOR '+newfont+']'+'L[/COLOR]ite Version','url',3,art+'Main/Search.png','none',1)
        
    favs = ADDON.getSetting('favs').split(',')
    for title in favs:
        if len(title)>1:
            addDir(title.title(),title.lower(),mode,art+'Main/Search.png','none',1)
    
def SEARCH(search_entered):
        PAGE=1
        favs = ADDON.getSetting('favs').split(',')
        if 'url' in search_entered:
            keyboard = xbmc.Keyboard('', 'KODIKARAOKE.COM')
            keyboard.doModal()
            if keyboard.isConfirmed() and len(keyboard.getText())>0:
               search_entered = keyboard.getText()
            else: return
        
        search_entered = search_entered.replace(',', '')

        if len(search_entered) == 0:
            return

        TXT='https://www.youtube.com/results?search_query=%s+karaoke&hl=en-GB&page='  % (search_entered.replace(' ','+'))
        html=OPEN_URL(TXT+str(PAGE))
        if not search_entered in favs:
            favs.append(search_entered)
            ADDON.setSetting('favs', ','.join(favs))
        
        link=html.split('yt-lockup-title')
        
        for p in link:
            #print p
            try:
                url=p.split('watch?v=')[1]
                url=url.split('"')[0]
                if '&amp' in url:
                    url=url.split('&amp')[0]
                name= p.split('title="')[1]
                name=name.split('"')[0]  
                name = str(name).replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","").replace("[","").replace("]","").replace("-"," ")
                iconimage = 'http://i.ytimg.com/vi/%s/0.jpg' % url
                if not 'video_id' in name:
                    if not '_title_' in name:
                        if not 'video search' in name.lower():
                            addLink(name,url ,iconimage,'')
            except:pass
   
        addDir('[COLOR royalblue][B]Next Page >>[/B][/COLOR]',TXT,11,art+'nextpage.png','',PAGE)
        setView('movies', 'VIDEO')
        
                                                                                
def ARTIST_INDEX(url, iconimage):
        link=net.http_GET(url).content.encode('ascii','ignore')
        match = re.compile('<a href="(.+?)" title="(.+?)"').findall(link)
        for url, name in match:
            url = 'http://www.lyricsmania.com'+url   
            name = str(name).replace("lyrics","")
            addDir(name,url,5,iconimage,art+'Main/Fanart_A.jpg',1)
        setView('movies', 'DEFAULT')


def ARTIST_SONG_INDEX(url,name):
        link=net.http_GET(url).content
        match = re.compile('http://www.musictory.com/(.+?)"').findall(link)
        url1 = 'http://www.musictory.com/'+match[0]+'/Songs'
        link1=net.http_GET(url1).content
        url = re.compile('<h1 itemprop="name">(.+?) Songs<').findall(link1)[0]
        match1 = re.compile('<span itemprop="name">(.+?)</span>').findall(link1)
        fanart = art+'Main/Fanart_A.jpg'
        for name in match1:
            name=name.encode('ascii','ignore')
            name = str(name).replace("&Agrave;","A").replace('&eacute;','e').replace('&ecirc;','e').replace('&egrave;','e').replace("&agrave;","A")
            addDir(name,'url',6,iconimage,fanart,1)
        setView('tvshow', 'DEFAULT')
            

    
def TRACK_INDEX(url, iconimage):
        link=OPEN_URL(url.replace(' ','%20'))
        #link=str(link1).replace('&___c=___c#listingTrack0_link','')
        match = re.compile('<li><span>.+?href=.+?title="(.+?)">.+?> - <.+?>(.+?)</a>').findall(link)
        #nextpageurl=Next_Page(link)[0]       
        uniques = []        
        for name, url, in match:

                name = str(name).replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","")  
                url = str(url).replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","") 
                name = name+ '   ('+ url+')'
                if not '</a>' in name:
                    if name not in uniques:
                        uniques.append(name)      
                        addDir(name,url,9,iconimage,art+'Main/Fanart_T.jpg',1)
        setView('movies', 'DEFAULT')
        #try:
                #url='http://www.sunflykaraoke.com'+str(nextpageurl)
                #name= '[COLOR '+newfont+']'+'[B]Next Page >>[/B][/COLOR]'
                #addDir(name,url,7,art+'next.png','none',1)    
                #setView('movies', 'DEFAULT') 
        #except:
                #pass
                
def GENRE_INDEX(name,url, iconimage):
        link=OPEN_URL(url.replace(' ','%20'))
        match = re.compile('<div class="track_det" style="width:80%">.+?<p><a href=".+?s">(.+?)<.+?<p class="trkname">.+?href=".+?">(.+?)<',re.DOTALL).findall(link)
        #nextpageurl=Next_Page(link)[0]
        uniques=[]
        for name, url, in match:
            name = str(name).replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","")  
            url = str(url).replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","") 
            name = name+ '   ('+ url+')'
            if not '</a>' in name:
                if name not in uniques:
                    uniques.append(name)      
    
                    addDir(name,url,9,iconimage,art+'Main/Fanart_G.jpg',1)
        setView('movies', 'DEFAULT')
        #try:
                #url='http://www.sunflykaraoke.com'+str(nextpageurl)
                #name= '[COLOR '+newfont+']'+'[B]Next Page >>[/B][/COLOR]'
                #addDir(name,url,7,art+'next.png','none',1)    
                #setView('movies', 'DEFAULT') 
        #except:
                #pass
            
            
def GENRE_INDEXSF(name,url, iconimage):
        link=OPEN_URL(url.replace(' ','%20'))
        match = re.compile('<div class="track_det" style="width:80%">.+?<p><a href=".+?">(.+?)<.+?<p class="trkname">.+?href=".+?">(.+?)<',re.DOTALL).findall(link)
        #nextpageurl=Next_Page(link)[0]
        uniques=[]
        for name, url, in match:
            passto = re.sub('[\(\)\{\}<>]', '', name.replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","").replace("&quot;",""))
            name = re.sub('[\(\)\{\}<>]', '', name.replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","").replace("&quot;","").replace("'",""))
            url = str(url).replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","") 
            name = name#+ '   ('+ url+')'
            if not '</a>' in name:
                if name not in uniques:
                    uniques.append(name)      

                    addDir('[COLOR '+newfont+']'+'%s[/COLOR] - %s'%(passto,url),name,34,iconimage,art+'Main/Fanart_G.jpg',1)
        setView('movies', 'DEFAULT')
        #try:
                #url='http://www.sunflykaraoke.com'+str(nextpageurl)
                #name= '[COLOR '+newfont+']'+'[B]Next Page >>[/B][/COLOR]'
                #addDir(name,url,33,art+'next.png','none',1)    
                #setView('movies', 'DEFAULT') 
        #except:
                #pass
          
        
def SEARCH_GENRE(url,name):

    #url=url.split('(')[0].strip()
    #url=url.slpit('[')[0]
    passit = False 
    db=GRABBER(4,'track',re.sub('\A(a|A|the|THE|The|)\s','',url))
    if not db: addLinkSF('[COLOR red]TRACK NOT AVAILABLE.[/COLOR]',url,'');return
    for sf,number,artist,track,icon,burl in db:
        if 'ft' in artist.lower() or 'feat' in artist.lower():
            passit = True
        if passit == False:   
            if artist.lower() in name.split('-')[1].lower().strip():
                addLinkSF('[COLOR '+newfont+']'+'%s ~ [/COLOR]%s'%(artist,track),burl,icon,split=1)
        else:
            if name.split('-')[1].lower().strip():
                addLinkSF('[COLOR '+newfont+']'+'%s ~ [/COLOR]%s'%(artist,track),burl,icon,split=1)            
        
def YOUTUBE_SONG_INDEX(name, url, iconimage, fanart):
        PAGE=1
        url = str(url).replace(' ','+').replace('_','+')  
        name = str(name).replace(' ','+') 
        url = 'https://www.youtube.com/results?search_query=%s+%s+karaoke&hl=en-GB&page=' % (name, url) 
        html=OPEN_URL(url)
        link=html.split('yt-lockup-title')
        for p in link:
            try:
                url=p.split('watch?v=')[1]
                url=url.split('"')[0]
                if '&amp' in url:
                    url=url.split('&amp')[0]
                name= p.split('title="')[1]
                name=name.split('"')[0]  
                name = str(name).replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","").replace("[","").replace("]","").replace("-"," ")
                iconimage = 'http://i.ytimg.com/vi/%s/0.jpg' % url
                if not 'video_id' in name:
                    if not '_title_' in name:
                        if not 'video search' in name.lower():
                            addLink(name,url ,iconimage,'')
            except:pass
   
        addDir('[COLOR royalblue][B]Next Page >>[/B][/COLOR]',url,11,art+'nextpage.png','',PAGE)
        setView('movies', 'VIDEO')
            
def TITLE_ORDERS_YOUTUBE(name, url,fanart):
        PAGE=1
        name = str(name).replace('   (','+') .replace(' ','+') .replace(')','')
        url = 'https://www.youtube.com/results?search_query=%s+karaoke&hl=en-GB&page=' % (name) 
        #print url
        html=OPEN_URL(url)
        link=html.split('yt-lockup-title')
        for p in link:
            try:
                url=p.split('watch?v=')[1]
                url=url.split('"')[0]
                if '&amp' in url:
                    url=url.split('&amp')[0]
                name= p.split('title="')[1]
                name=name.split('"')[0]  
                name = str(name).replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","").replace("[","").replace("]","").replace("-"," ")
                iconimage = 'http://i.ytimg.com/vi/%s/0.jpg' % url
                if not 'video_id' in name:
                    if not '_title_' in name:
                        if not 'video search' in name.lower():
                            addLink(name,url ,iconimage,'')
            except:pass
   
        addDir('[COLOR royalblue][B]Next Page >>[/B][/COLOR]',url,11,art+'nextpage.png','',PAGE)
        setView('movies', 'VIDEO')
        
        
def SF_Download(name,url,iconimage,split):
    import downloader
    name=name.replace(' [/COLOR]','').split('~')[split]
    dp = xbmcgui.DialogProgress()
    dp.create("Kodi Karaoke","",'Downloading', name)
    path = xbmc.translatePath(os.path.join(sfdownloads))
    name=name.upper()

    s = requests.session()
    loginurl = 'http://'+THESITE+'/payments/login'
    username = ADDON.getSetting('user')
    password = ADDON.getSetting('pass')

    TIME = time.time()- 3600
    
    data={'amember_login':username,'amember_pass':password,'login_attempt_id':str(TIME).split('.')[0],'remember_login':'1','':'Login'} 
  

    headers={'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'en-US,en;q=0.9',
    'Connection':'keep-alive',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Host':THESITE,
    'Origin':'http://'+THESITE,
    'Referer':'http://'+THESITE+'/payments/login',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest'}

    html = s.post(loginurl, data, headers=headers,allow_redirects=False)
    lib=os.path.join(path, name+'.avi')
    downloader.download(iconimage.replace('.jpg','.avi'),lib,s,dp)
    lib=os.path.join(path, name+'.jpg')
    downloader.download(iconimage,lib,s,dp)
    
def DOWNLOADS(downloads):
     import glob
     path = downloads
     for infile in glob.glob(os.path.join(path, '*.*')):
         addFile(infile)
    
    
def SFDOWNLOADS(sfdownloads):
     import glob
     path = sfdownloads
     for infile in glob.glob(os.path.join(path, '*.avi')):
         addFileSF(infile)
        
            
def nextpage(url,number):
        URL=url
        PAGE=int(number)+1
        html=OPEN_URL(url+str(PAGE))
        link=html.split('yt-lockup-title')
        for p in link:
            try:
                url=p.split('watch?v=')[1]
                url=url.split('"')[0]
                if '&amp' in url:
                    url=url.split('&amp')[0]
                name= p.split('title="')[1]
                name=name.split('"')[0]  
                name = str(name).replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","").replace("[","").replace("]","").replace("-"," ")
                iconimage = 'http://i.ytimg.com/vi/%s/0.jpg' % url
                if not 'video_id' in name:
                    if not '_title_' in name:
                        if not 'video search' in name.lower():
                            addLink(name,url ,iconimage,'')
            except:pass
   
        addDir('[COLOR royalblue][B]Next Page >>[/B][/COLOR]',URL,11,art+'nextpage.png','',PAGE)
        setView('movies', 'VIDEO')
            
def addFile(file):
        name = file.replace(downloads,'').replace('.mp4','')
        name = name.split('-[')[-2]
        thumb = icon(file)[0]
        iconimage = 'http://i.ytimg.com/vi/%s/0.jpg' % thumb
        url=file
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name})
        liz.setProperty("IsPlayable","true")
        liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        contextMenu = []
        contextMenu.append(('Delete', 'XBMC.RunPlugin(%s?mode=102&url=%s&iconimage=%s)'% (sys.argv[0], file,iconimage)))
        liz.addContextMenuItems(contextMenu,replaceItems=True)
        xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url=url,listitem = liz, isFolder = False)
        setView('movies', 'VIDEO')
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)    

def addFileSF(file):
        file = xbmc.translatePath(file) 
        iconimage = file.replace('.avi','.jpg').replace('.mp4','.jpg')
        name = file.replace(xbmc.translatePath(sfdownloads),'').replace('.avi','').replace('.mp4','')
        url=file

        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name})
        liz.setProperty("IsPlayable","true")
        contextMenu = []
        contextMenu.append(('Delete', 'XBMC.RunPlugin(%s?mode=102&url=%s&iconimage=%s)'% (sys.argv[0], file,iconimage)))
        liz.addContextMenuItems(contextMenu,replaceItems=True)
        xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url=url,listitem = liz, isFolder = False)
        setView('movies', 'VIDEO')
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)   
        
                
def deleteFileSF(file,iconimage):
    tries    = 0
    maxTries = 10
    while os.path.exists(file) and tries < maxTries:
        try:
            os.remove(file)
            break
        except:
            xbmc.sleep(500)
            tries = tries + 1
    while os.path.exists(iconimage) and tries < maxTries:
        try:
            os.remove(iconimage)
            break
        except:
            xbmc.sleep(500)
            tries = tries + 1
            
            
    if os.path.exists(file):
        d = xbmcgui.Dialog()
        d.ok('Kodi Karaoke', 'Failed to delete file')         
                           
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
        

def Sunflysearch(search_entered):
    search_entered = search_entered.replace(',', '')
    favs = ADDON.getSetting('favs').split(',')
    if 'url' in search_entered:
        keyboard = xbmc.Keyboard('', '[COLOR grey3]Search by[/COLOR] [COLOR '+newfont+']'+'Artist[/COLOR] [COLOR grey3]or[/COLOR] [COLOR '+newfont+']'+'Track[/COLOR]')
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered=keyboard.getText()
            db=GRABBER(4,'artist',search_entered)
            if not db: db=GRABBER(4,'artist',re.sub('\A(a|A|the|THE|The)\s','',search_entered))
            if not db: db=GRABBER(4,'track',search_entered)
            if not db: db=GRABBER(4,'track',re.sub('\A(a|A|the|THE|The)\s','',search_entered))
            if not db: addLinkSF('[COLOR red]TRACK NOT AVAILABLE.[/COLOR]',url,'');return
            for sf,number,artist,track,icon,burl in db:
                addLinkSF('[COLOR '+newfont+']'+'%s ~ [/COLOR]%s'%(artist,track),burl,icon)
                
         
            if not search_entered in favs:
                favs.append(search_entered)
                ADDON.setSetting('favs', ','.join(favs))
    
    else:

            
        db=GRABBER(4,'artist',search_entered)
        if not db: db=GRABBER(4,'artist',re.sub('\A(a|A|the|THE|The)\s','',search_entered))
        if not db: db=GRABBER(4,'track',search_entered)
        if not db: db=GRABBER(4,'track',re.sub('\A(a|A|the|THE|The)\s','',search_entered))
        if not db: addLinkSF('[COLOR red]TRACK NOT AVAILABLE.[/COLOR]',url,'');return
        for sf,number,artist,track,icon,burl in db:
            addLinkSF('[COLOR '+newfont+']'+'%s ~ [/COLOR]%s'%(artist,track),burl,icon)

        
             
def AZ_ARTIST_SEARCH(name):
    db=GRABBER(5,'artist',name)
    if not db: addLinkSF('[COLOR red]ARTIST NOT AVAILABLE.[/COLOR]',url,'');return
    for sf,number,artist,track,icon,burl in db:
            addLinkSF('[COLOR '+newfont+']'+'%s ~ [/COLOR]%s'%(artist,track),burl,icon,split=1)
    
def SF_SEARCH(url):
    sunfly = 'SF'
    keyboard = xbmc.Keyboard(sunfly, 'Enter Sunfly Disc Number:-')
    keyboard.doModal()
    if keyboard.isConfirmed():
        db=GRABBER(4,'sunfly_name',keyboard.getText())
        if not db: addLinkSF('[COLOR red]DISC NOT AVAILABLE.[/COLOR]',url,'');return
        for sf,number,artist,track,icon,burl in db:
            addLinkSF('[COLOR '+newfont+']'+'%s:-%s ~ [/COLOR]%s'%(sf,number,track),burl,icon,split=1)
        
        
def AZ_TRACK_SEARCH(name):
    db=GRABBER(5,'track',re.sub('\A(a|A|the|THE|The)\s','',name))
    if not db: addLinkSF('[COLOR red]TRACK NOT AVAILABLE.[/COLOR]',url,'');return
    for sf,number,artist,track,icon,burl in db:
            addLinkSF('[COLOR '+newfont+']'+'%s ~ [/COLOR]%s'%(track,artist),burl,icon,split=0)    


def karaokanta_LOGIN():
    
    loginurl = 'http://www.karaokantalive.com/login.php?action=process'
    username = ADDON.getSetting('karaokantaliveuser')
    password = ADDON.getSetting('karaokantalivepass')

    html = net.http_GET('http://www.karaokantalive.com').content
    formid=re.compile('name="formid" value="(.+?)"').findall (html)[0]
    data     = {'formid':formid,'password': password,
                                            'email_address': username,
                                            'submit.x':'0','submit.y':'0'}
    headers  = {'Host':'www.karaokantalive.com',
                                            'Origin':'http://www.karaokantalive.com',
                                            'Referer':'http://www.karaokantalive.com'}
    
    html = net.http_POST(loginurl, data, headers).content
  
    if os.path.exists(cookie_path) == False:
            os.makedirs(cookie_path)
    net.save_cookies(cookie_jar)


        
def addDir(name,url,mode,iconimage,fanart,number):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&number="+str(number)
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty( "Fanart_Image", fanart )
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        menu=[]
        if mode == 3 or mode==16 :
            menu.append(('[COLOR orange]Remove Search[/COLOR]','XBMC.Container.Update(%s?mode=5002&name=%s&url=url)'% (sys.argv[0],name)))
            liz.addContextMenuItems(items=menu, replaceItems=False)
        if (mode == 2000)or mode==103 or mode==203:
            if mode ==203:
                liz.setProperty("IsPlayable","true")
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz, isFolder=False)
        else:
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz, isFolder=True)
        if not mode==1 and mode==20 and mode==19:
            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
            
        
def addLink(name,url,iconimage, fanart,showcontext=True):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode=6003&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)
    #name=name.encode('ascii', 'ignore')
    #url=url.encode('ascii', 'ignore')
    cmd = 'plugin://plugin.video.youtube/?path=root/video&action=download&videoid=%s' % url
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty("IsPlayable","true")
    liz.setProperty("Fanart_Image", fanart )
    menu = []
    if showcontext:
          menu.append(('[COLOR green]Add[/COLOR] to Kodi Karaoke Favorites','XBMC.RunPlugin(%s?mode=2&iconimage=%s&url=%s&name=%s&switch=%s)' %(sys.argv[0],iconimage,url,name,'add')))         
          menu.append(('[COLOR red]Remove[/COLOR] Kodi Karaoke from Favourites','XBMC.RunPlugin(%s?mode=2&iconimage=%s&url=%s&name=%s&switch=%s)' %(sys.argv[0],iconimage,url,name,'delete')))


 
    liz.addContextMenuItems(items=menu, replaceItems=False)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)


def PlayYouTube(name,url,iconimage):
    youtube='plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=%s'% url
    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title':name})
    liz.setProperty("IsPlayable","true")
    liz.setPath(str(youtube))
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
                                
def addLinkSF(name,url,iconimage,showcontext=True,split=None):
        ADDCOOKIE='|Cookie='+open(cookie_jar).read()
        if 'http' in Kfolder:
            url=url.replace(' ','%20')
        iconimage = xbmc.translatePath(os.path.join(Kfolder,url)).replace('.mp4','.jpg').replace('.avi','.jpg')
        
        url = xbmc.translatePath(os.path.join(Kfolder,url))

        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage+ADDCOOKIE)
        liz.setInfo( type="Video", infoLabels={ "Title": name})
        liz.setProperty('mimetype', 'video/x-msvideo')
        liz.setProperty("IsPlayable","true")
        
            
        menu = []
        if showcontext:
            
            menu.append(('[COLOR green]Add[/COLOR] to Kodi Karaoke Favorites','XBMC.RunPlugin(%s?mode=2&iconimage=%s&url=%s&name=%s&switch=%s)' %(sys.argv[0],iconimage,url,name,'add')))
            menu.append(('[COLOR red]Remove[/COLOR] Kodi Karaoke from Favourites','XBMC.RunPlugin(%s?mode=2&iconimage=%s&url=%s&name=%s&switch=%s)' %(sys.argv[0],iconimage,url,name,'delete')))
        if ADDON.getSetting('sfenable') == 'true':
            menu.append(('[COLOR orange]Download[/COLOR]', 'XBMC.Container.Update(%s?&mode=30&url=%s&name=%s&iconimage=%s&split=%s)' %(sys.argv[0],url,name,iconimage,split)))  
        liz.addContextMenuItems(items=menu, replaceItems=False)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url+ADDCOOKIE,listitem=liz,isFolder=False)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)

      

params=get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None

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
        switch=urllib.unquote_plus(params["switch"])
except:
        switch='display'
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        number=int(params["number"])
except:
        pass
try:        
        split=int(params["split"])
except:
        pass
                
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
print "FanartImage: "+str(fanart)
try:print "number: "+str(number)
except:pass

def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view') == 'true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )
        
        
if mode==None or url==None or len(url)<1:
        CATEGORIES()
       
elif mode==1:
    AtoZ(url,number,fanart)

elif mode==2:
    FAVOURITES(switch,name,iconimage,url)
        
elif mode==3:
        print ""+url
        SEARCH(url)
        
elif mode==4:
        ARTIST_INDEX(url, iconimage) 
        
elif mode==5:
        ARTIST_SONG_INDEX(url,name)
        
elif mode==6:
        YOUTUBE_SONG_INDEX(name, url, iconimage, fanart)
                                                             
elif mode==7:
        TRACK_INDEX(url, iconimage)
        
elif mode==8:
        GENRE(url)   
        
elif mode==9:
        TITLE_ORDERS_YOUTUBE(name, url, fanart)   
        
elif mode==10:
        GENRE_INDEX(name,url, iconimage)
                      
elif mode==11:
        nextpage(url,number)  
        
elif mode==12:
    pass
elif mode==13:
    addFavorite(name,url,iconimage,fanart)

elif mode==14:
    rmFavorite(name)
        
elif mode==15:
    DOWNLOADS(downloads)
    
elif mode==16:
    Sunflysearch(url)
    
elif mode==17:
    Sunflyurl(name)
    
elif mode==19:
    freeyoutube(url)

elif mode==20:
    ProKaraoke(url)

elif mode==23:
    AZ_ARTIST_SEARCH(name)
    
elif mode==24:
    AZ_TRACK_SEARCH(name)
    
elif mode==25:
    SF_SEARCH(name) 
    
elif mode==26:
    print ""
    LATEST_LIST(url)    
    
elif mode==27:
    addSF_Favorite(name,url,iconimage)

elif mode==28:
    rmSF_Favorite(name)
    
elif mode==29:
    getSF_Favorites()
    
elif mode==30:
    SF_Download(name,url,iconimage,split)
    
elif mode==31:
    SFDOWNLOADS(sfdownloads)
    
elif mode==32:
        GENRESF(url)   
elif mode==33:
        GENRE_INDEXSF(name,url, iconimage)
        
elif mode==34:
        SEARCH_GENRE(url,name)
       
elif mode==102:
    deleteFileSF(url,iconimage)
    xbmc.executebuiltin("Container.Refresh")
    
elif mode==103:
    import fixdatabase

    
elif mode==201:
    download_DB()

elif mode==202:
    karaokanta_GET(name,url)

elif mode==203:
    karaokanta_PLAY(name,url)    
    
elif mode==3000:
    test()

elif mode==3001:
    PlayYouTube (name,url,iconimage)

elif mode == 5002:
    favs = ADDON.getSetting('favs').split(",")
    try:
        favs.remove(name.lower())
        ADDON.setSetting('favs', ",".join(favs))
    except:pass

elif mode == 5003:
    FirstSearchDir(name)

elif mode ==6003:
    PlayYouTube(name,url,iconimage)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
