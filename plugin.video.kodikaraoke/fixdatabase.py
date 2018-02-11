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

THESITE ='localhost'

local = xbmcaddon.Addon(id=PLUGIN)

ADDON = settings.addon()
home = ADDON.getAddonInfo('path')
sfdownloads= ADDON.getSetting('sfdownloads')

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

   import downloader
   dp = xbmcgui.DialogProgress()
   dp.create("Kodi Karaoke","",'Building Database Please Wait', ' ')
   downloader.download(K_db, db_dir,s,dp)

       

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



