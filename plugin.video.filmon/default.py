if 64 - 64: i11iIiiIii
if 65 - 65: O0 / iIii1I11I1II1 % OoooooooOO - i1IIi
if 73 - 73: II111iiii
import urllib , urllib2 , re , xbmcplugin , xbmcgui , xbmcaddon , xbmc , os
if 22 - 22: I1IiiI * Oo0Ooo / OoO0O00 . OoOoOO00 . o0oOOo0O0Ooo / I1ii11iIi11i
if 48 - 48: oO0o / OOooOOo / I11i / Ii1I
if 48 - 48: iII111i % IiII + I1Ii111 / ooOoO0o * Ii1I
if 46 - 46: ooOoO0o * I11i - OoooooooOO
if 30 - 30: o0oOOo0O0Ooo - O0 % o0oOOo0O0Ooo - OoooooooOO * O0 * OoooooooOO
if 60 - 60: iIii1I11I1II1 / i1IIi * oO0o - I1ii11iIi11i + o0oOOo0O0Ooo
if 94 - 94: i1IIi % Oo0Ooo
if 68 - 68: Ii1I / O0
if 46 - 46: O0 * II111iiii / IiII * Oo0Ooo * iII111i . I11i
if 62 - 62: i11iIiiIii - II111iiii % I1Ii111 - iIii1I11I1II1 . I1ii11iIi11i . II111iiii
if 61 - 61: oO0o / OoOoOO00 / iII111i * OoO0O00 . II111iiii
if 1 - 1: II111iiii - I1ii11iIi11i % i11iIiiIii + IiII . I1Ii111
if 55 - 55: iIii1I11I1II1 - I1IiiI . Ii1I * IiII * i1IIi / iIii1I11I1II1
if 79 - 79: oO0o + I1Ii111 . ooOoO0o * IiII % I11i . I1IiiI
if 94 - 94: iII111i * Ii1I / IiII . i1IIi * iII111i
if 47 - 47: i1IIi % i11iIiiIii
if 20 - 20: ooOoO0o * II111iiii
import settings
from hashlib import md5
import json
from threading import Timer
import net
import datetime
import time
oO0o0o0ooO0oO = net.Net ( )
if 52 - 52: II111iiii - i11iIiiIii % I1Ii111
O0OoOoo00o = 'plugin.video.filmon'
iiiI11 = xbmcaddon . Addon ( id = O0OoOoo00o )
OOooO = iiiI11 . getSetting ( 'res' )
OOoO00o = iiiI11 . getLocalizedString
if 9 - 9: I1IiiI - Ii1I % i1IIi % OoooooooOO
#Global Constants
i1iIIi1 = 'http://dl.dropbox.com/u/129714017/hubmaintenance/'
if 50 - 50: i11iIiiIii - Ii1I
oo0Ooo0 = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
I1I11I1I1I = 'http://www.filmon.com/channel/'
OooO0OO = 'http://static.filmon.com/couch/channels/'
iiiIi = 'http://www.filmon.com/api/'
IiIIIiI1I1 = 'http://www.filmon.com/tv/api/'
OoO000 = iiiI11 . getSetting ( 'user' )
IIiiIiI1 = iiiI11 . getSetting ( 'pass' )
iiIiIIi = md5 ( IIiiIiI1 ) . hexdigest ( )
ooOoo0O = 'http://www.filmon.com/api/keep-alive?session_key='
OooO0 = 'http://www.filmon.com/tv/themes/filmontv/img/mobile/filmon-logo-stb.png'
if iiiI11 . getSetting ( 'visitor_ga' ) == '' :
 from random import randint
 iiiI11 . setSetting ( 'visitor_ga' , str ( randint ( 0 , 0x7fffffff ) ) )
II11iiii1Ii = "4.6.1"
OO0o = "FilmOn"
Ooo = "UA-3174686-20"
if 68 - 68: I11i + OOooOOo . iIii1I11I1II1 - IiII % iIii1I11I1II1 - ooOoO0o
def oOOO00o ( ) :
 O0O00o0OOO0 = xbmcgui . getCurrentWindowId ( ) in [ 10025 , 12005 ]
 if not O0O00o0OOO0 :
  print '=======================Ending Session======================='
  Ii1iIIIi1ii = xbmcgui . Window ( 10000 ) . getProperty ( "SessionID" )
  o0oo0o0O00OO = iiiIi + 'logout?session_key=%s' % ( Ii1iIIIi1ii )
  o0oO = urllib2 . Request ( o0oo0o0O00OO )
  I1i1iii = urllib2 . urlopen ( o0oO )
  i1iiI11I = I1i1iii . read ( )
  I1i1iii . close ( )
  print '===============LOGGED OUT !!==============='
  xbmcgui . Window ( 10000 ) . clearProperty ( "SessionID" )
  return
  if 29 - 29: OoooooooOO
 iI = xbmcgui . Window ( 10000 ) . getProperty ( "SessionID" )
 print '=======================KEEPING THE SESSION ALIVE =%s !!===========================' % ( iI )
 oO0o0o0ooO0oO . http_GET ( ooOoo0O + iI ) . content
 I1i1I1II = Timer ( 60.0 , oOOO00o )
 I1i1I1II . start ( )
i1 = ''
def IiIiiI ( i , t1 , t2 = [ ] ) :
 I1i1I1II = i1
 for I1I in t1 :
  I1i1I1II += chr ( I1I )
  i += 1
  if i > 1 :
   I1i1I1II = I1i1I1II [ : - 1 ]
   i = 0
 for I1I in t2 :
  I1i1I1II += chr ( I1I )
  i += 1
  if i > 1 :
   I1i1I1II = I1i1I1II [ : - 1 ]
   i = 0
 return I1i1I1II
 if 80 - 80: OoOoOO00 - OoO0O00
 if 87 - 87: oO0o / I11i - i1IIi * OOooOOo / OoooooooOO . O0
 if 1 - 1: II111iiii - I11i / I11i
if not xbmcgui . Window ( 10000 ) . getProperty ( "SessionID" ) :
 if 46 - 46: Ii1I * OOooOOo - OoO0O00 * oO0o - I1Ii111
 oo0 = IiIiiI ( 997 , [ 54 , 104 , 197 , 116 ] , [ 108 , 116 , 253 , 112 , 176 , 58 , 76 , 47 , 156 , 47 , 94 , 119 , 212 , 119 , 97 , 119 , 208 , 46 , 5 , 102 , 134 , 105 , 171 , 108 , 89 , 109 , 149 , 111 , 104 , 110 , 176 , 46 , 20 , 99 , 194 , 111 , 227 , 109 , 83 , 47 , 237 , 116 , 109 , 118 , 2 , 47 , 118 , 97 , 94 , 112 , 218 , 105 , 136 , 47 , 244 , 105 , 133 , 110 , 184 , 105 , 53 , 116 , 235 , 63 , 188 , 97 , 18 , 112 , 218 , 112 , 167 , 95 , 133 , 105 , 206 , 100 , 141 , 61 , 244 , 120 , 54 , 109 , 166 , 98 , 185 , 99 , 34 , 95 , 55 , 97 , 47 , 112 , 66 , 112 , 3 , 38 , 13 , 97 , 223 , 112 , 36 , 112 , 177 , 95 , 130 , 115 , 206 , 101 , 162 , 99 , 63 , 114 , 197 , 101 , 239 , 116 , 244 , 61 , 28 , 49 , 140 , 98 , 32 , 56 , 86 , 69 , 223 , 101 , 90 , 110 , 129 , 51 , 196 , 101 ] )
 o0oO = urllib2 . Request ( oo0 )
 o0oO . add_header ( 'User-Agent' , oo0Ooo0 )
 I1i1iii = urllib2 . urlopen ( o0oO )
 i1iiI11I = I1i1iii . read ( )
 o00 = re . compile ( '"session_key":"(.+?)"' ) . findall ( i1iiI11I )
 Ii1iIIIi1ii = o00 [ 0 ]
 if iiiI11 . getSetting ( 'filmon' ) == 'true' :
  OooOooo = iiiIi + 'login?session_key=%s&login=%s&password=%s' % ( Ii1iIIIi1ii , OoO000 , iiIiIIi )
  o0oO = urllib2 . Request ( OooOooo )
  o0oO . add_header ( 'User-Agent' , oo0Ooo0 )
  I1i1iii = urllib2 . urlopen ( o0oO )
  i1iiI11I = I1i1iii . read ( )
  I1i1iii . close ( )
  xbmcgui . Window ( 10000 ) . setProperty ( "SessionID" , Ii1iIIIi1ii )
  oOOO00o ( )
  print '=======================LOGGED IN !! ==========================='
 if iiiI11 . getSetting ( 'filmon' ) == 'false' :
  xbmcgui . Window ( 10000 ) . setProperty ( "SessionID" , Ii1iIIIi1ii )
  oOOO00o ( )
  print '=======================NOT LOGGED IN !! ==========================='
  if 97 - 97: ooOoO0o - OOooOOo * i11iIiiIii / OoOoOO00 % I1Ii111 - OoooooooOO
if iiiI11 . getSetting ( 'filmon' ) == 'true' :
 iiiI11 . setSetting ( id = 'firstrun' , value = 'true' )
iI = xbmcgui . Window ( 10000 ) . getProperty ( "SessionID" )
if 59 - 59: O0 + I1IiiI + IiII % I1IiiI
if 70 - 70: iII111i * I1ii11iIi11i
if 46 - 46: ooOoO0o / OoO0O00
def OOOoO0O0o ( ) :
 if iiiI11 . getSetting ( 'filmon' ) == 'true' :
  O0o0Ooo ( OOoO00o ( 30059 ) , 'url' , 5 , 'http://www.filmon.com/tv/themes/filmontv/img/mobile/filmon-logo-stb.png' , '' , '' , '' , '' , '' , '' , '' , '' , 'My Recordings' )
 if iiiI11 . getSetting ( 'filmon' ) == 'true' :
  O0o0Ooo ( OOoO00o ( 30060 ) , 'url' , 9 , 'http://www.filmon.com/tv/themes/filmontv/images/category/favorites_stb.png' , '' , '' , '' , '' , '' , '' , '' , '' , 'Favorites' )
 O00 = 'http://www.filmon.com/api/groups?session_key=%s' % ( iI )
 i1iiI11I = oO0o0o0ooO0oO . http_GET ( O00 ) . content
 iI1Ii11iII1 = json . loads ( i1iiI11I )
 for Oo0O0O0ooO0O in iI1Ii11iII1 :
  oo0 = Oo0O0O0ooO0O [ 'group_id' ]
  IIIIii = Oo0O0O0ooO0O [ 'group' ]
  O0o0 = Oo0O0O0ooO0O [ 'logo_148x148_uri' ]
  IIIIii = IIIIii . encode ( "utf-8" )
  O0o0Ooo ( IIIIii , oo0 , 3 , O0o0 , '' , '' , '' , '' , '' , '' , '' , '' , IIIIii )
 O0o0Ooo ( 'Need Help??' , 'url' , 2000 , i1iIIi1 + 'images/help.jpg' , i1iIIi1 + 'images/fanart/expert.jpg' , 'Fusion Installer' , '' , '' , '' , '' , '' , '' , '' )
 OO00Oo ( 'tvshows' , 'default' )
 if 51 - 51: IiII * o0oOOo0O0Ooo + I11i + OoO0O00
def o0O0O00 ( name , url , group ) :
 o000o ( 'None' , name )
 if iiiI11 . getSetting ( 'firstrun' ) == 'false' :
  I11IiI1I11i1i = xbmcgui . Dialog ( )
  if I11IiI1I11i1i . yesno ( OOoO00o ( 30021 ) , OOoO00o ( 30022 ) , '' , OOoO00o ( 30023 ) , OOoO00o ( 30024 ) , OOoO00o ( 30025 ) ) :
   if I11IiI1I11i1i . yesno ( OOoO00o ( 30021 ) , '' , '   ' , OOoO00o ( 30026 ) , OOoO00o ( 30027 ) , OOoO00o ( 30028 ) ) :
    iI1ii1Ii = None
    oooo000 = xbmc . Keyboard ( '' , OOoO00o ( 30307 ) )
    oooo000 . doModal ( )
    if oooo000 . isConfirmed ( ) :
     iI1ii1Ii = oooo000 . getText ( )
    if iI1ii1Ii == None :
     return False
     if 16 - 16: I1ii11iIi11i + OoO0O00 - II111iiii
    oOoOO0 = None
    oooo000 = xbmc . Keyboard ( '' , OOoO00o ( 30308 ) )
    oooo000 . doModal ( )
    if oooo000 . isConfirmed ( ) :
     oOoOO0 = oooo000 . getText ( )
    if oOoOO0 == None :
     return False
    try :
     IiI11iII1 = 'http://www.filmon.com/api/register?session_key=%s&email=%s&password=%s' % ( iI , iI1ii1Ii , oOoOO0 )
     o0oO = urllib2 . Request ( IiI11iII1 )
     o0oO . add_header ( 'User-Agent' , oo0Ooo0 )
     I1i1iii = urllib2 . urlopen ( o0oO )
     i1iiI11I = I1i1iii . read ( )
     if re . search ( ( iI1ii1Ii ) , i1iiI11I ) :
      iiiI11 . setSetting ( 'user' , value = iI1ii1Ii )
      iiiI11 . setSetting ( 'pass' , value = oOoOO0 )
      iiiI11 . setSetting ( id = 'firstrun' , value = 'true' )
      iiiI11 . setSetting ( id = 'filmon' , value = 'true' )
    except :
     I11IiI1I11i1i . ok ( OOoO00o ( 30021 ) , OOoO00o ( 30029 ) , OOoO00o ( 30030 ) , OOoO00o ( 30031 ) )
    try :
     IIII11I1I = settings . RETURN_COUNTRIES ( url )
     OOO0o = ''
     oooo000 = xbmc . Keyboard ( '' , OOoO00o ( 30309 ) )
     oooo000 . doModal ( )
     if oooo000 . isConfirmed ( ) :
      OOO0o = oooo000 . getText ( )
      if OOO0o == None :
       return False
     IiI1 = { "country" : IIII11I1I , "city" : OOO0o }
     IiI11iII1 = 'http://www.filmon.com/api/accountLocation?session_key=%s' % ( iI )
     iI1Ii11iII1 = urllib . urlencode ( IiI1 )
     o0oO = urllib2 . Request ( IiI11iII1 , iI1Ii11iII1 )
     o0oO . add_header ( 'User-Agent' , oo0Ooo0 )
     I1i1iii = urllib2 . urlopen ( o0oO )
     i1iiI11I = I1i1iii . read ( )
     if re . search ( 'Accepted' , i1iiI11I ) :
      I11IiI1I11i1i . ok ( OOoO00o ( 30021 ) , OOoO00o ( 30032 ) , "" , OOoO00o ( 30033 ) )
    except :
     I11IiI1I11i1i . ok ( OOoO00o ( 30021 ) , OOoO00o ( 30034 ) , OOoO00o ( 30035 ) , OOoO00o ( 30036 ) )
   else :
    iI1ii1Ii = None
    oooo000 = xbmc . Keyboard ( '' , OOoO00o ( 30307 ) )
    oooo000 . doModal ( )
    if oooo000 . isConfirmed ( ) :
     iI1ii1Ii = oooo000 . getText ( )
    if iI1ii1Ii == None :
     return False
     if 54 - 54: II111iiii % OoOoOO00 % I11i % iIii1I11I1II1 + iIii1I11I1II1 * ooOoO0o
    oOoOO0 = None
    oooo000 = xbmc . Keyboard ( '' , OOoO00o ( 30308 ) )
    oooo000 . doModal ( )
    if oooo000 . isConfirmed ( ) :
     oOoOO0 = oooo000 . getText ( )
    if oOoOO0 == None :
     return False
    iiiI11 . setSetting ( 'user' , value = iI1ii1Ii )
    iiiI11 . setSetting ( 'pass' , value = oOoOO0 )
    iiiI11 . setSetting ( id = 'firstrun' , value = 'true' )
    iiiI11 . setSetting ( id = 'filmon' , value = 'true' )
    I11IiI1I11i1i . ok ( OOoO00o ( 30021 ) , OOoO00o ( 30037 ) , "" , OOoO00o ( 30038 ) )
  else :
   iiiI11 . setSetting ( id = 'firstrun' , value = 'true' )
 O00O0oOO00O00 = 'http://www.filmon.com/api/group/%s?session_key=%s' % ( url , iI )
 i1Oo00 = oO0o0o0ooO0oO . http_GET ( O00O0oOO00O00 ) . content
 i1iiI11I = i1Oo00 . encode ( 'ascii' , 'ignore' )
 iI1Ii11iII1 = json . loads ( i1iiI11I , encoding = 'utf8' )
 i1i = iI1Ii11iII1 [ 'channels' ]
 for Oo0O0O0ooO0O in iI1Ii11iII1 [ 'channels' ] :
  iiI111I1iIiI = Oo0O0O0ooO0O [ "id" ]
  name = Oo0O0O0ooO0O [ "title" ]
  II = Oo0O0O0ooO0O [ "big_logo" ]
  O0o0 = str ( II ) . replace ( '/logo' , '/extra_big_logo' )
  Ii1I1IIii1II = ''
  name = name . encode ( "utf-8" )
  O0o0Ooo ( name , 'url' , 12 , O0o0 , Ii1I1IIii1II , iiI111I1iIiI , '' , '' , '' , 'tvguide' , str ( iiI111I1iIiI ) , '' , group )
  OO00Oo ( 'episodes' , 'default' )
  if 65 - 65: Ii1I . iIii1I11I1II1 / O0 - Ii1I
  if 21 - 21: I1IiiI * iIii1I11I1II1
def oooooOoo0ooo ( channels , resolution , watch_timeout ) :
 print channels
 print '============ RESOLUTION IS SET TO %s =============' % ( str ( resolution ) . replace ( '0' , 'LOW' ) . replace ( '1' , 'HIGH' ) . replace ( '2' , 'AUTO SELECTED' ) )
 watch_timeout = str ( watch_timeout )
 if resolution == '0' :
  I1I1IiI1 = 'LOW'
  if not re . search ( 'low' , str ( channels ) , re . IGNORECASE ) :
   I1I1IiI1 = 'HIGH'
 if resolution == '1' :
  I1I1IiI1 = 'HIGH'
 if resolution == '2' :
  I1I1IiI1 = 'LOW'
  if len ( watch_timeout ) > 5 :
   I1I1IiI1 = 'HIGH'
  if not re . search ( 'low' , str ( channels ) , re . IGNORECASE ) :
   I1I1IiI1 = 'HIGH'
 print '=========== STREAMING %s QUALITY ================' % ( I1I1IiI1 )
 for III1iII1I1ii in channels :
  if III1iII1I1ii [ 'quality' ] . upper ( ) == I1I1IiI1 :
   return III1iII1I1ii
 return None
 if 61 - 61: II111iiii
 if 64 - 64: ooOoO0o / OoOoOO00 - O0 - I11i
def O0oOoOOOoOO ( programme_id , name ) :
 iI = ii1ii11IIIiiI ( )
 oo0 = 'http://www.filmon.com/api/channel/%s?session_key=%s' % ( programme_id , iI )
 print '============ GETTING NEW SESSION_ID = %s  ==================' % ( iI )
 i1iiI11I = oO0o0o0ooO0oO . http_GET ( oo0 ) . content
 iI1Ii11iII1 = json . loads ( i1iiI11I )
 i1i = iI1Ii11iII1 [ 'streams' ]
 O00OOOoOoo0O = iI1Ii11iII1 [ 'watch-timeout' ]
 O000OOo00oo = oooooOoo0ooo ( i1i , OOooO , O00OOOoOoo0O )
 if O000OOo00oo is not None :
  oo0OOo = O000OOo00oo [ 'url' ] + '<'
  ooOOO00Ooo = O000OOo00oo [ 'name' ]
  name = O000OOo00oo [ 'quality' ]
 # if re . search ( 'mp4' , ooOOO00Ooo , re . IGNORECASE ) :
   #IiIIIi1iIi = re . compile ( 'rtmp://(.+?)/(.+?)/(.+?)/<' )
   #ooOOoooooo = IiIIIi1iIi . search ( oo0OOo )
   #II1I = '%s/%s/' % ( ooOOoooooo . group ( 2 ) , ooOOoooooo . group ( 3 ) )
   #O0i1II1Iiii1I11 = 'http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf'
   #oo0 = O000OOo00oo [ 'url' ] + ooOOO00Ooo
  if re . search ( 'm4v' , ooOOO00Ooo , re . IGNORECASE ) :
   II1I = 'vodlast'
   O0i1II1Iiii1I11 = 'http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf'
   oo0 = O000OOo00oo [ 'url' ] + '/' + ooOOO00Ooo
  else :
   try :
    IiIIIi1iIi = re . compile ( 'rtmp://(.+?)/live/(.+?)id=(.+?)<' )
    o00 = IiIIIi1iIi . search ( oo0OOo )
    II1I = 'live/%sid=%s' % ( o00 . group ( 2 ) , o00 . group ( 3 ) )
    oo0 = O000OOo00oo [ 'url' ]
    O0i1II1Iiii1I11 = 'http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf'
   except :
    pass
   try :
    IiIIIi1iIi = re . compile ( 'rtmp://(.+?)/(.+?)id=(.+?)"' )
    ooOOoooooo = IiIIIi1iIi . search ( oo0OOo )
    II1I = '%sid=%s' % ( ooOOoooooo . group ( 2 ) , ooOOoooooo . group ( 3 ) )
    O0i1II1Iiii1I11 = 'http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf?v=28'
   except :
    pass
   try :
    IiIIIi1iIi = re . compile ( 'rtmp://(.+?)/(.+?)/<' )
    o00 = IiIIIi1iIi . search ( oo0OOo )
    II1I = '%s/' % ( o00 . group ( 2 ) )
    oo0 = O000OOo00oo [ 'url' ] + '/' + ooOOO00Ooo
    O0i1II1Iiii1I11 = 'http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf'
   except :
    pass
  IIII = O000OOo00oo [ 'url' ]
  iiIiI = 'http://www.filmon.com/'
  if iiiI11 . getSetting ( 'protocol' ) == '1' :
      oo0 = str ( oo0 ).replace('rtmp://','http://').replace('/live/','/live/'+str ( ooOOO00Ooo ) +'/playlist.m3u8')
  else:
      oo0 = str ( oo0 ) + ' playpath=' + str ( ooOOO00Ooo ) + ' app=' + str ( II1I ) + ' swfUrl=' + str ( O0i1II1Iiii1I11 ) + ' tcUrl=' + str ( IIII ) + ' pageurl=' + str ( iiIiI ) + ' live=true'
 o00oooO0Oo ( str ( programme_id ) , name )
 return oo0
 if 78 - 78: Ii1I % I1Ii111 + I1ii11iIi11i
 if 64 - 64: oO0o * O0 . I1IiiI + II111iiii
def IIi1i ( url ) :
 from datetime import date
 from datetime import datetime
 url = 'http://www.filmon.com/api/dvr-list?session_key=%s&format=json' % ( iI )
 print url
 i1iiI11I = oO0o0o0ooO0oO . http_GET ( url ) . content
 iI1Ii11iII1 = json . loads ( i1iiI11I )
 OOOO00O0O = iI1Ii11iII1 [ 'recordings' ]
 for Oo0O0O0ooO0O in OOOO00O0O :
  iii = Oo0O0O0ooO0O [ 'id' ]
  IIIIii = Oo0O0O0ooO0O [ 'title' ]
  oOooOOOoOo = Oo0O0O0ooO0O [ 'description' ]
  I1I11I1I1I = Oo0O0O0ooO0O [ 'channel_id' ]
  time = Oo0O0O0ooO0O [ 'time_start' ]
  i1Iii1i1I = Oo0O0O0ooO0O [ 'status' ]
  url = Oo0O0O0ooO0O [ 'stream_url' ]
  time = float ( time )
  oOooOOOoOo = oOooOOOoOo . encode ( 'utf-8' )
  OOoO00 = date . fromtimestamp ( time ) . strftime ( "%d/%m/%Y" )
  Ii1I1IIii1II = '[B][%s][/B]\n%s' % ( OOoO00 , oOooOOOoOo )
  O0o0 = 'https://static.filmon.com/couch/channels/%s/extra_big_logo.png' % str ( I1I11I1I1I )
  if i1Iii1i1I == 'Recorded' :
   i1Iii1i1I = OOoO00o ( 30050 )
   IIIIii = '%s %s' % ( i1Iii1i1I , IIIIii )
   IIIIii = IIIIii . encode ( 'utf-8' )
   IiI111111IIII ( IIIIii , url , O0o0 , Ii1I1IIii1II , '' , '' , '' , 'delete' , '' , '' , iii )
  if i1Iii1i1I == 'Accepted' :
   i1Iii1i1I = OOoO00o ( 30051 )
   IIIIii = '%s %s' % ( i1Iii1i1I , IIIIii )
   IIIIii = IIIIii . encode ( 'utf-8' )
   IiI111111IIII ( IIIIii , url , O0o0 , Ii1I1IIii1II , '' , '' , '' , 'delete' , '' , '' , iii )
  if i1Iii1i1I == 'Recording' :
   i1Iii1i1I = OOoO00o ( 30052 )
   IIIIii = '%s %s' % ( i1Iii1i1I , IIIIii )
   IIIIii = IIIIii . encode ( 'utf-8' )
   IiI111111IIII ( IIIIii , url , O0o0 , Ii1I1IIii1II , '' , '' , '' , 'delete' , '' , '' , iii )
  if i1Iii1i1I == 'Failed' :
   i1Iii1i1I = OOoO00o ( 30053 )
   IIIIii = '%s %s' % ( i1Iii1i1I , IIIIii )
   IIIIii = IIIIii . encode ( 'utf-8' )
   IiI111111IIII ( IIIIii , url , O0o0 , Ii1I1IIii1II , '' , '' , '' , 'delete' , '' , '' , iii )
  OO00Oo ( 'movies' , 'epg' )
  o000o ( 'My Recordings' , 'None' )
  if 37 - 37: I1Ii111 / OoOoOO00
def i1I1iI1iIi111i ( url , programme_id , startdate_time ) :
 url = 'http://filmon.com/api/dvr-add?session_key=%s&channel_id=%s&programme_id=%s&start_time=%s' % ( iI , url , programme_id , startdate_time )
 try :
  i1iiI11I = oO0o0o0ooO0oO . http_GET ( url ) . content
  try :
   if 44 - 44: i1IIi % II111iiii + I11i
   if re . search ( 'true' , i1iiI11I , re . IGNORECASE ) :
    I11IiI1I11i1i = xbmcgui . Dialog ( )
    I11IiI1I11i1i . ok ( OOoO00o ( 30021 ) , OOoO00o ( 30039 ) , ' ' , OOoO00o ( 30040 ) )
   if re . search ( 'false' , i1iiI11I , re . IGNORECASE ) :
    I11IiI1I11i1i = xbmcgui . Dialog ( )
    I11IiI1I11i1i . ok ( OOoO00o ( 30021 ) , OOoO00o ( 30041 ) , ' ' , OOoO00o ( 30042 ) )
  except :
   I11IiI1I11i1i = xbmcgui . Dialog ( )
   I11IiI1I11i1i . ok ( OOoO00o ( 30021 ) , OOoO00o ( 30040 ) , OOoO00o ( 30043 ) , OOoO00o ( 30044 ) )
 except :
  I11IiI1I11i1i = xbmcgui . Dialog ( )
  I11IiI1I11i1i . ok ( OOoO00o ( 30021 ) , OOoO00o ( 30311 ) , OOoO00o ( 30312 ) , OOoO00o ( 30313 ) )
  if 45 - 45: iII111i / iII111i + I1Ii111 + ooOoO0o
def iI111i ( startdate_time ) :
 oo0 = 'http://www.filmon.com/api/dvr-remove?session_key=%s&recording_id=%s' % ( iI , startdate_time )
 try :
  i1iiI11I = oO0o0o0ooO0oO . http_GET ( oo0 ) . content
  if re . search ( 'Task is removed' , i1iiI11I , re . IGNORECASE ) :
   I11IiI1I11i1i = xbmcgui . Dialog ( )
   I11IiI1I11i1i . ok ( OOoO00o ( 30021 ) , OOoO00o ( 30045 ) , '' , OOoO00o ( 30046 ) )
  else :
   I11IiI1I11i1i = xbmcgui . Dialog ( )
   I11IiI1I11i1i . ok ( OOoO00o ( 30021 ) , '' , OOoO00o ( 30047 ) , '' )
 except :
  I11IiI1I11i1i = xbmcgui . Dialog ( )
  I11IiI1I11i1i . ok ( OOoO00o ( 30021 ) , '' , OOoO00o ( 30047 ) , '' )
  if 26 - 26: I1ii11iIi11i * iII111i . II111iiii * Ii1I
def II1 ( url , iconimage ) :
 from datetime import date
 from datetime import datetime
 url = 'http://www.filmon.com/api/channel/%s?session_key=%s' % ( url , iI )
 print url
 i1iiI11I = oO0o0o0ooO0oO . http_GET ( url ) . content
 iI1Ii11iII1 = json . loads ( i1iiI11I )
 iiiIi1 = iI1Ii11iII1 [ 'tvguide' ]
 for Oo0O0O0ooO0O in iiiIi1 :
  iiI111I1iIiI = Oo0O0O0ooO0O [ "programme" ]
  i1I1ii11i1Iii = Oo0O0O0ooO0O [ "startdatetime" ]
  I1IiiiiI = Oo0O0O0ooO0O [ "enddatetime" ]
  o0O = Oo0O0O0ooO0O [ "channel_id" ]
  oOooOOOoOo = Oo0O0O0ooO0O [ "programme_description" ]
  IIIIii = Oo0O0O0ooO0O [ "programme_name" ]
  IiIIii1iII1II = float ( i1I1ii11i1Iii )
  Iii1I1I11iiI1 = float ( I1IiiiiI )
  I1I1i1I = datetime . fromtimestamp ( IiIIii1iII1II )
  ii1I = datetime . fromtimestamp ( Iii1I1I11iiI1 )
  O0oO0 = I1I1i1I . strftime ( '%a %H:%M' )
  oO0 = ii1I . strftime ( '%H:%M' )
  IIIIii = '[COLOR white][%s][/COLOR] [COLOR yellow][B]%s[/B][/COLOR]' % ( O0oO0 , IIIIii )
  iconimage = 'http://static.filmon.com/couch/channels/%s/extra_big_logo.png' % ( o0O )
  IIIIii = IIIIii . encode ( 'utf-8' )
  Ii1I1IIii1II = oOooOOOoOo . encode ( 'utf-8' )
  url = str ( o0O )
  O0o0Ooo ( IIIIii , url , 2 , iconimage , Ii1I1IIii1II , '' , '' , 'record' , '' , '' , str ( iiI111I1iIiI ) , i1I1ii11i1Iii , '' )
  OO00Oo ( 'movies' , 'epg' )
  if 75 - 75: ooOoO0o + OoOoOO00 + o0oOOo0O0Ooo * I11i % oO0o . iII111i
def oO ( url ) :
 O00O0oOO00O00 = 'http://www.filmon.com/api/channel/%s?session_key=%s' % ( url , iI )
 i1iiI11I = oO0o0o0ooO0oO . http_GET ( O00O0oOO00O00 ) . content
 iI1Ii11iII1 = json . loads ( i1iiI11I )
 IIIIii = iI1Ii11iII1 [ 'title' ]
 IIIIii = IIIIii . encode ( 'utf-8' )
 return IIIIii
 if 31 - 31: OOooOOo + i11iIiiIii + Oo0Ooo * ooOoO0o
 if 28 - 28: O0 * Oo0Ooo - OOooOOo % iIii1I11I1II1 * Ii1I - i11iIiiIii
 if 7 - 7: Oo0Ooo + oO0o - I1Ii111 % Ii1I + I1ii11iIi11i
def ooo0OOOoo ( url ) :
 O00 = 'http://www.filmon.com/api/favorites?session_key=%s&run=get' % ( iI )
 i1iiI11I = oO0o0o0ooO0oO . http_GET ( O00 ) . content
 iI1Ii11iII1 = json . loads ( i1iiI11I )
 I1Ii1 = iI1Ii11iII1 [ 'result' ]
 for Oo0O0O0ooO0O in I1Ii1 :
  iiI111I1iIiI = Oo0O0O0ooO0O [ 'channel_id' ]
  O0o0 = 'http://static.filmon.com/couch/channels/%s/extra_big_logo.png' % ( str ( iiI111I1iIiI ) )
  IIIIii = oO ( str ( iiI111I1iIiI ) )
  O0o0Ooo ( IIIIii , url , 12 , O0o0 , '' , '' , str ( iiI111I1iIiI ) , '' , '' , 'tvguide' , str ( iiI111I1iIiI ) , '' , 'Favourites' )
  OO00Oo ( 'movies' , 'default' )
  if 46 - 46: O0 + iII111i % I1IiiI / o0oOOo0O0Ooo . IiII * I11i
def OOooo0oOO0O ( url ) :
 I11IiI1I11i1i = xbmcgui . Dialog ( )
 O00 = 'http://www.filmon.com/api/favorites?session_key=%s&channel_id=%s&run=add' % ( iI , url )
 i1iiI11I = oO0o0o0ooO0oO . http_GET ( O00 ) . content
 I11IiI1I11i1i . ok ( OOoO00o ( 30021 ) , OOoO00o ( 30048 ) , ' ' , '' )
 if 62 - 62: I1IiiI
def O00o0OO0 ( url ) :
 I11IiI1I11i1i = xbmcgui . Dialog ( )
 O00 = 'http://www.filmon.com/api/favorites?session_key=%s&channel_id=%s&run=remove' % ( iI , url )
 i1iiI11I = oO0o0o0ooO0oO . http_GET ( O00 ) . content
 I11IiI1I11i1i . ok ( OOoO00o ( 30021 ) , OOoO00o ( 30049 ) , ' ' , '' )
 if 35 - 35: oO0o % ooOoO0o / I1Ii111 + iIii1I11I1II1 . OoooooooOO . I1IiiI
 if 71 - 71: IiII * II111iiii * oO0o
def ii1ii11IIIiiI ( ) :
 oo0 = iiiIi + 'init/'
 o0oO = urllib2 . Request ( oo0 )
 o0oO . add_header ( 'User-Agent' , oo0Ooo0 )
 I1i1iii = urllib2 . urlopen ( o0oO )
 i1iiI11I = I1i1iii . read ( )
 o00 = re . compile ( '"session_key":"(.+?)"' ) . findall ( i1iiI11I )
 Ii1iIIIi1ii = o00 [ 0 ]
 if iiiI11 . getSetting ( 'filmon' ) == 'true' :
  OooOooo = iiiIi + 'login?session_key=%s&login=%s&password=%s' % ( Ii1iIIIi1ii , OoO000 , iiIiIIi )
  o0oO = urllib2 . Request ( OooOooo )
  o0oO . add_header ( 'User-Agent' , oo0Ooo0 )
  I1i1iii = urllib2 . urlopen ( o0oO )
  i1iiI11I = I1i1iii . read ( )
  I1i1iii . close ( )
  xbmcgui . Window ( 10000 ) . setProperty ( "SessionID" , Ii1iIIIi1ii )
 if iiiI11 . getSetting ( 'filmon' ) == 'false' :
  xbmcgui . Window ( 10000 ) . setProperty ( "SessionID" , Ii1iIIIi1ii )
 return Ii1iIIIi1ii
 if 56 - 56: I1IiiI
def O0oO ( dateString ) :
 try :
  return datetime . datetime . fromtimestamp ( time . mktime ( time . strptime ( dateString . encode ( 'utf-8' , 'replace' ) , "%Y-%m-%d %H:%M:%S" ) ) )
 except :
  return datetime . datetime . today ( ) - datetime . timedelta ( days = 1 )
  if 73 - 73: I1ii11iIi11i * i11iIiiIii % oO0o . I1ii11iIi11i
  if 66 - 66: oO0o + oO0o + ooOoO0o / iII111i + OOooOOo
  if 30 - 30: O0
  if 44 - 44: oO0o / I11i / I11i
  if 87 - 87: Oo0Ooo . I1IiiI - II111iiii + O0 / Oo0Ooo / oO0o
  if 25 - 25: I1IiiI . I1IiiI - OoOoOO00 % OoOoOO00 - i11iIiiIii / I1Ii111
  if 51 - 51: Oo0Ooo / OoOoOO00 . OOooOOo * o0oOOo0O0Ooo + OoO0O00 * IiII
def OOOoOo ( ) :
 if 51 - 51: ooOoO0o / iIii1I11I1II1 % Oo0Ooo * I1IiiI % I1Ii111
 oOoooOOO = 60 * 60
 oo00oO0O0 = 2 * oOoooOOO
 if 30 - 30: OOooOOo + I1ii11iIi11i * I11i % i11iIiiIii % OoOoOO00
 OO0OoOO0o0o = datetime . datetime . today ( )
 oo = O0oO ( iiiI11 . getSetting ( 'ga_time' ) )
 I1111i = OO0OoOO0o0o - oo
 iIIii = I1111i . days
 o00O0O = I1111i . seconds
 if 20 - 20: i1IIi - ooOoO0o
 i1iI = ( iIIii > 0 ) or ( o00O0O > oo00oO0O0 )
 if not i1iI :
  return
  if 94 - 94: iIii1I11I1II1 / Oo0Ooo % iII111i * iII111i * II111iiii
 iiiI11 . setSetting ( 'ga_time' , str ( OO0OoOO0o0o ) . split ( '.' ) [ 0 ] )
 IIiIiI ( )
 if 94 - 94: oO0o . i1IIi - o0oOOo0O0Ooo % O0 - OoO0O00
 if 72 - 72: Ii1I
 if 1 - 1: OoO0O00 * IiII * OoooooooOO + ooOoO0o
 if 33 - 33: O0 * o0oOOo0O0Ooo - I1Ii111 % I1Ii111
def I11I ( utm_url ) :
 I11iIi1i1II11 = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
 import urllib2
 try :
  o0oO = urllib2 . Request ( utm_url , None ,
 { 'User-Agent' : I11iIi1i1II11 }
 )
  I1i1iii = urllib2 . urlopen ( o0oO ) . read ( )
 except :
  print ( "GA fail: %s" % utm_url )
 return I1i1iii
 if 47 - 47: OoooooooOO . OoOoOO00
def o00oooO0Oo ( group , name ) :
 try :
  try :
   from hashlib import md5
  except :
   from md5 import md5
  from random import randint
  import time
  from urllib import unquote , quote
  from os import environ
  from hashlib import sha1
  i1I1i111Ii = iiiI11 . getSetting ( 'visitor_ga' )
  ooo = "http://www.google-analytics.com/__utm.gif"
  if not group == 'None' :
   i1i1iI1iiiI = ooo + "?" + "utmwv=" + II11iiii1Ii + "&utmn=" + str ( randint ( 0 , 0x7fffffff ) ) + "&utmt=" + "event" + "&utme=" + quote ( "5(channel*click*" + group + ':' + name + ")" ) + "&utmac=" + Ooo + "&utmcc=__utma=%s" % "." . join ( [ "1" , i1I1i111Ii , i1I1i111Ii , i1I1i111Ii , i1I1i111Ii , "2" ] )
   if 51 - 51: I1IiiI % I1Ii111 . oO0o / iIii1I11I1II1 / I11i . oO0o
   if 42 - 42: o0oOOo0O0Ooo + i1IIi - Ii1I / IiII
   if 9 - 9: O0 % O0 - o0oOOo0O0Ooo
   if 51 - 51: I1IiiI . iIii1I11I1II1 - I1ii11iIi11i / O0
   if 52 - 52: o0oOOo0O0Ooo + O0 + iII111i + Oo0Ooo % iII111i
   if 75 - 75: I1IiiI . ooOoO0o . O0 * I1Ii111
   try :
    print "============================ POSTING TRACK EVENT ============================"
    I11I ( i1i1iI1iiiI )
   except :
    print "============================  CANNOT POST TRACK EVENT ============================"
 except :
  print "================  CANNOT POST TRACK EVENT ANALYTICS  ================"
  if 4 - 4: Ii1I % oO0o * OoO0O00
def o000o ( group , name ) :
 try :
  try :
   from hashlib import md5
  except :
   from md5 import md5
  from random import randint
  import time
  from urllib import unquote , quote
  from os import environ
  from hashlib import sha1
  i1I1i111Ii = iiiI11 . getSetting ( 'visitor_ga' )
  ooo = "http://www.google-analytics.com/__utm.gif"
  if name == "None" :
   o0O0OOOOoOO0 = ooo + "?" + "utmwv=" + II11iiii1Ii + "&utmn=" + str ( randint ( 0 , 0x7fffffff ) ) + "&utmp=" + quote ( OO0o ) + "&utmac=" + Ooo + "&utmcc=__utma=%s" % "." . join ( [ "1" , i1I1i111Ii , i1I1i111Ii , i1I1i111Ii , i1I1i111Ii , "2" ] )
   if 23 - 23: i11iIiiIii
   if 30 - 30: o0oOOo0O0Ooo - i1IIi % II111iiii + I11i * iIii1I11I1II1
   if 81 - 81: IiII % i1IIi . iIii1I11I1II1
   if 4 - 4: i11iIiiIii % OoO0O00 % i1IIi / IiII
   if 6 - 6: iII111i / I1IiiI % OOooOOo - I1IiiI
  else :
   if group == "None" :
    o0O0OOOOoOO0 = ooo + "?" + "utmwv=" + II11iiii1Ii + "&utmn=" + str ( randint ( 0 , 0x7fffffff ) ) + "&utmp=" + quote ( OO0o + "/" + name ) + "&utmac=" + Ooo + "&utmcc=__utma=%s" % "." . join ( [ "1" , i1I1i111Ii , i1I1i111Ii , i1I1i111Ii , i1I1i111Ii , "2" ] )
    if 31 - 31: OOooOOo
    if 23 - 23: I1Ii111 . IiII
    if 92 - 92: OoOoOO00 + I1Ii111 * Ii1I % I1IiiI
    if 42 - 42: Oo0Ooo
    if 76 - 76: I1IiiI * iII111i % I1Ii111
   else :
    o0O0OOOOoOO0 = ooo + "?" + "utmwv=" + II11iiii1Ii + "&utmn=" + str ( randint ( 0 , 0x7fffffff ) ) + "&utmp=" + quote ( OO0o + "/" + group + "/" + name ) + "&utmac=" + Ooo + "&utmcc=__utma=%s" % "." . join ( [ "1" , i1I1i111Ii , i1I1i111Ii , i1I1i111Ii , i1I1i111Ii , "2" ] )
    if 57 - 57: iIii1I11I1II1 - i1IIi / I1Ii111 - O0 * OoooooooOO % II111iiii
    if 68 - 68: OoooooooOO * I11i % OoOoOO00 - IiII
    if 34 - 34: I1Ii111 . iIii1I11I1II1 * OoOoOO00 * oO0o / I1Ii111 / I1ii11iIi11i
    if 78 - 78: Oo0Ooo - o0oOOo0O0Ooo / OoOoOO00
    if 10 - 10: iII111i + Oo0Ooo * I1ii11iIi11i + iIii1I11I1II1 / I1Ii111 / I1ii11iIi11i
    if 42 - 42: I1IiiI
  print "============================ POSTING ANALYTICS ============================"
  I11I ( o0O0OOOOoOO0 )
  if 38 - 38: OOooOOo + II111iiii % ooOoO0o % OoOoOO00 - Ii1I / OoooooooOO
 except :
  print "================  CANNOT POST TO ANALYTICS  ================"
  if 73 - 73: o0oOOo0O0Ooo * O0 - i11iIiiIii
  if 85 - 85: Ii1I % iII111i + I11i / o0oOOo0O0Ooo . oO0o + OOooOOo
  if 62 - 62: i11iIiiIii + i11iIiiIii - o0oOOo0O0Ooo
  if 28 - 28: iII111i . iII111i % iIii1I11I1II1 * iIii1I11I1II1 . o0oOOo0O0Ooo / iII111i
def IIiIiI ( ) :
 iII1i1 = int ( xbmc . getInfoLabel ( "System.BuildVersion" ) [ 0 : 2 ] )
 if iII1i1 < 12 :
  if xbmc . getCondVisibility ( 'system.platform.osx' ) :
   if xbmc . getCondVisibility ( 'system.platform.atv2' ) :
    O0oOOoooOO0O = '/var/mobile/Library/Preferences'
   else :
    O0oOOoooOO0O = os . path . join ( os . path . expanduser ( '~' ) , 'Library/Logs' )
  elif xbmc . getCondVisibility ( 'system.platform.ios' ) :
   O0oOOoooOO0O = '/var/mobile/Library/Preferences'
  elif xbmc . getCondVisibility ( 'system.platform.windows' ) :
   O0oOOoooOO0O = xbmc . translatePath ( 'special://home' )
   OooOooo = os . path . join ( O0oOOoooOO0O , 'kodi.log' )
   try:ooo00Ooo = open ( OooOooo , 'r' ) . read ( )
   except:ooo00Ooo = open ( OooOooo.replace('kodi.log','xbmc.log') , 'r' ) . read ( )
  elif xbmc . getCondVisibility ( 'system.platform.linux' ) :
   O0oOOoooOO0O = xbmc . translatePath ( 'special://home/temp' )
  else :
   O0oOOoooOO0O = xbmc . translatePath ( 'special://logpath' )
  OooOooo = os . path . join ( O0oOOoooOO0O.replace('kodi.log','xbmc.log') , 'kodi.log' )
  try:ooo00Ooo = open ( OooOooo , 'r' ) . read ( )
  except:ooo00Ooo = open ( OooOooo , 'r' ) . read ( )  
  o00 = re . compile ( 'Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?' ) . findall ( ooo00Ooo )
 elif iII1i1 > 11 :
  print '======================= more than ===================='
  O0oOOoooOO0O = xbmc . translatePath ( 'special://logpath' )
  OooOooo = os . path . join ( O0oOOoooOO0O , 'kodi.log' )
  ooo00Ooo = open ( OooOooo , 'r' ) . read ( )
  o00 = re . compile ( 'Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?' ) . findall ( ooo00Ooo )
 else :
  ooo00Ooo = 'Starting XBMC (Unknown Git:.+?Platform: Unknown. Built.+?'
  o00 = re . compile ( 'Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?' ) . findall ( ooo00Ooo )
 print '==========================   ' + OO0o + ' ' + II11iiii1Ii + '   =========================='
 try :
  from hashlib import md5
 except :
  from md5 import md5
 from random import randint
 import time
 from urllib import unquote , quote
 from os import environ
 from hashlib import sha1
 import platform
 i1I1i111Ii = iiiI11 . getSetting ( 'visitor_ga' )
 for Oo0o0O00 , ii1 in o00 :
  if re . search ( '12.' , Oo0o0O00 , re . IGNORECASE ) :
   Oo0o0O00 = "Frodo"
  if re . search ( '11.' , Oo0o0O00 , re . IGNORECASE ) :
   Oo0o0O00 = "Eden"
  if re . search ( '13.' , Oo0o0O00 , re . IGNORECASE ) :
   Oo0o0O00 = "Gotham"
  if re . search ( '14.' , Oo0o0O00 , re . IGNORECASE ) :
   Oo0o0O00 = "Helix"
  if re . search ( '15.' , Oo0o0O00 , re . IGNORECASE ) :
   Oo0o0O00 = "Isengard"
  if re . search ( '16.' , Oo0o0O00 , re . IGNORECASE ) :
   Oo0o0O00 = "Jarvis"   
  print Oo0o0O00
  print ii1
  ooo = "http://www.google-analytics.com/__utm.gif"
  i1i1iI1iiiI = ooo + "?" + "utmwv=" + II11iiii1Ii + "&utmn=" + str ( randint ( 0 , 0x7fffffff ) ) + "&utmt=" + "event" + "&utme=" + quote ( "5(APP LAUNCH*" + Oo0o0O00 + "*" + ii1 + ")" ) + "&utmp=" + quote ( OO0o ) + "&utmac=" + Ooo + "&utmcc=__utma=%s" % "." . join ( [ "1" , i1I1i111Ii , i1I1i111Ii , i1I1i111Ii , i1I1i111Ii , "2" ] )
  if 39 - 39: Ii1I / ooOoO0o . o0oOOo0O0Ooo % O0 * iII111i + I1IiiI
  if 77 - 77: Ii1I + II111iiii . OoOoOO00 * I1Ii111 + OOooOOo + OOooOOo
  if 9 - 9: I11i % OoooooooOO . oO0o % I11i
  if 32 - 32: i11iIiiIii
  if 31 - 31: iIii1I11I1II1 / OoO0O00 / I1ii11iIi11i
  if 41 - 41: Oo0Ooo
  if 10 - 10: Oo0Ooo / Oo0Ooo / I1Ii111 . I1Ii111
  try :
   print "============================ POSTING APP LAUNCH TRACK EVENT ============================"
   I11I ( i1i1iI1iiiI )
  except :
   print "============================  CANNOT POST APP LAUNCH TRACK EVENT ============================"
   if 98 - 98: Oo0Ooo / I1IiiI . O0 + OoO0O00
class ii ( xbmcgui . WindowXMLDialog ) :
 def __init__ ( self , * args , ** kwargs ) :
  self . shut = kwargs [ 'close_time' ]
  xbmc . executebuiltin ( "Skin.Reset(AnimeWindowXMLDialogClose)" )
  xbmc . executebuiltin ( "Skin.SetBool(AnimeWindowXMLDialogClose)" )
  if 25 - 25: OoooooooOO - I1IiiI . I1IiiI * oO0o
 def onInit ( self ) :
  xbmc . Player ( ) . play ( '%s/resources/skins/DefaultSkin/media/xbmchub.mp3' % iiiI11 . getAddonInfo ( 'path' ) )
  while self . shut > 0 :
   xbmc . sleep ( 1000 )
   self . shut -= 1
  xbmc . Player ( ) . stop ( )
  self . _close_dialog ( )
  if 81 - 81: iII111i + IiII
 def onFocus ( self , controlID ) : pass
 if 98 - 98: I1IiiI
 def onClick ( self , controlID ) :
  if controlID == 12 :
   xbmc . Player ( ) . stop ( )
   self . _close_dialog ( )
   if 95 - 95: ooOoO0o / ooOoO0o
 def onAction ( self , action ) :
  if action in [ 5 , 6 , 7 , 9 , 10 , 92 , 117 ] or action . getButtonCode ( ) in [ 275 , 257 , 261 ] :
   xbmc . Player ( ) . stop ( )
   self . _close_dialog ( )
   if 30 - 30: I1ii11iIi11i + Oo0Ooo / Oo0Ooo % I1ii11iIi11i . I1ii11iIi11i
 def _close_dialog ( self ) :
  xbmc . executebuiltin ( "Skin.Reset(AnimeWindowXMLDialogClose)" )
  time . sleep ( .4 )
  self . close ( )
  if 55 - 55: ooOoO0o - I11i + II111iiii + iII111i % Ii1I
  if 41 - 41: i1IIi - I11i - Ii1I
def III11I1 ( ) :
 if xbmc . getCondVisibility ( 'system.platform.ios' ) :
  if not xbmc . getCondVisibility ( 'system.platform.atv' ) :
   IIi1IIIi = ii ( 'hub1.xml' , iiiI11 . getAddonInfo ( 'path' ) , 'DefaultSkin' , close_time = 11 , logo_path = '%s/resources/skins/DefaultSkin/media/Logo/' % iiiI11 . getAddonInfo ( 'path' ) )
 elif xbmc . getCondVisibility ( 'system.platform.android' ) :
  IIi1IIIi = ii ( 'hub1.xml' , iiiI11 . getAddonInfo ( 'path' ) , 'DefaultSkin' , close_time = 11 , logo_path = '%s/resources/skins/DefaultSkin/media/Logo/' % iiiI11 . getAddonInfo ( 'path' ) )
 else :
  IIi1IIIi = ii ( 'hub.xml' , iiiI11 . getAddonInfo ( 'path' ) , 'DefaultSkin' , close_time = 11 , logo_path = '%s/resources/skins/DefaultSkin/media/Logo/' % iiiI11 . getAddonInfo ( 'path' ) )
  if 99 - 99: Ii1I + OoO0O00 * II111iiii . o0oOOo0O0Ooo - I1ii11iIi11i
 IIi1IIIi . doModal ( )
 del IIi1IIIi
 if 58 - 58: Ii1I + o0oOOo0O0Ooo - I1IiiI
def i1i1ii ( dateString ) :
 try :
  return datetime . datetime . fromtimestamp ( time . mktime ( time . strptime ( dateString . encode ( 'utf-8' , 'replace' ) , "%Y-%m-%d %H:%M:%S" ) ) )
 except :
  return datetime . datetime . today ( ) - datetime . timedelta ( days = 1000 )
  if 46 - 46: OoOoOO00 + OoO0O00
  if 70 - 70: iII111i / iIii1I11I1II1
def Oo0oooO0oO ( ) :
 if 19 - 19: i11iIiiIii + OoooooooOO - Oo0Ooo - I11i
 oo00oO0O0 = 120
 if 21 - 21: O0 % IiII . I1IiiI / II111iiii + IiII
 OO0OoOO0o0o = datetime . datetime . today ( )
 oo = i1i1ii ( iiiI11 . getSetting ( 'pop_time' ) )
 I1111i = OO0OoOO0o0o - oo
 iIIii = I1111i . days
 if 53 - 53: oO0o - I1IiiI - oO0o * iII111i
 i1iI = ( iIIii > oo00oO0O0 )
 if not i1iI :
  return
  if 71 - 71: O0 - iIii1I11I1II1
 iiiI11 . setSetting ( 'pop_time' , str ( OO0OoOO0o0o ) . split ( '.' ) [ 0 ] )
 III11I1 ( )
 if 12 - 12: OOooOOo / o0oOOo0O0Ooo
OOOoOo ( )
if 42 - 42: Oo0Ooo
if 19 - 19: oO0o % I1ii11iIi11i * iIii1I11I1II1 + I1IiiI
def iii11I ( ) :
 I1Iii1 = [ ]
 iiI11Iii = sys . argv [ 2 ]
 if len ( iiI11Iii ) >= 2 :
  O0o0O0 = sys . argv [ 2 ]
  Ii1II1I11i1 = O0o0O0 . replace ( '?' , '' )
  if ( O0o0O0 [ len ( O0o0O0 ) - 1 ] == '/' ) :
   O0o0O0 = O0o0O0 [ 0 : len ( O0o0O0 ) - 2 ]
  oOoooooOoO = Ii1II1I11i1 . split ( '&' )
  I1Iii1 = { }
  for Ii111 in range ( len ( oOoooooOoO ) ) :
   I111i1i1111 = { }
   I111i1i1111 = oOoooooOoO [ Ii111 ] . split ( '=' )
   if ( len ( I111i1i1111 ) ) == 2 :
    I1Iii1 [ I111i1i1111 [ 0 ] ] = I111i1i1111 [ 1 ]
    if 49 - 49: OoO0O00 / oO0o + O0 * o0oOOo0O0Ooo
 return I1Iii1
 if 28 - 28: ooOoO0o + i11iIiiIii / I11i % OoOoOO00 % Oo0Ooo - O0
 if 54 - 54: i1IIi + II111iiii
def O0o0Ooo ( name , url , mode , iconimage , description , favorites , deletefav , record , deleterecord , tvguide , programme_id , startdate_time , group ) :
 oOOO0oo0 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&iconimage=" + urllib . quote_plus ( iconimage ) + "&description=" + urllib . quote_plus ( description ) + "&programme_id=" + urllib . quote_plus ( programme_id ) + "&startdate_time=" + urllib . quote_plus ( startdate_time ) + "&group=" + urllib . quote_plus ( group )
 iIi1i1iIi1iI = True
 iiIi1iI1iIii = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 iiIi1iI1iIii . setInfo ( type = "Video" , infoLabels = { "Title" : name , "Plot" : description } )
 o00OooO0oo = [ ]
 if favorites :
  o00OooO0oo . append ( ( OOoO00o ( 30054 ) , 'XBMC.RunPlugin(%s?name=None&url=%s&mode=10&iconimage=None&description=None)' % ( sys . argv [ 0 ] , favorites ) ) )
  iiIi1iI1iIii . addContextMenuItems ( items = o00OooO0oo , replaceItems = True )
 if deletefav :
  o00OooO0oo . append ( ( OOoO00o ( 30055 ) , 'XBMC.RunPlugin(%s?name=None&url=%s&mode=11&iconimage=None&description=None)' % ( sys . argv [ 0 ] , deletefav ) ) )
  iiIi1iI1iIii . addContextMenuItems ( items = o00OooO0oo , replaceItems = True )
 if record :
  o00OooO0oo . append ( ( OOoO00o ( 30056 ) , 'XBMC.RunPlugin(%s?name=None&url=%s&mode=6&iconimage=None&description=None&programme_id=%s&startdate_time=%s)' % ( sys . argv [ 0 ] , url , programme_id , startdate_time ) ) )
  iiIi1iI1iIii . addContextMenuItems ( items = o00OooO0oo , replaceItems = True )
 if deleterecord :
  o00OooO0oo . append ( ( OOoO00o ( 30057 ) , 'XBMC.RunPlugin(%s?name=None&url=None&mode=7&iconimage=None&description=None&startdate_time=%s)' % ( sys . argv [ 0 ] , startdate_time ) ) )
  iiIi1iI1iIii . addContextMenuItems ( items = o00OooO0oo , replaceItems = True )
 if tvguide :
  o00OooO0oo . append ( ( OOoO00o ( 30058 ) , 'XBMC.Container.Update(%s?name=None&url=%s&mode=8&iconimage=%s&description=None)' % ( sys . argv [ 0 ] , programme_id , iconimage ) ) )
  iiIi1iI1iIii . addContextMenuItems ( items = o00OooO0oo , replaceItems = True )
  if 89 - 89: Ii1I
 if not mode == 12 and not mode == 2000 :
  iIi1i1iIi1iI = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = oOOO0oo0 , listitem = iiIi1iI1iIii , isFolder = True )
 else :
  iIi1i1iIi1iI = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = oOOO0oo0 , listitem = iiIi1iI1iIii , isFolder = False )
 return iIi1i1iIi1iI
 if 76 - 76: ooOoO0o
def IIIiI11ii1I ( name , url , iconimage , description , favorites , deletefav , record , deleterecord , tvguide , programme_id , startdate_time , group ) :
 o000o ( group , name )
 IiiiI = xbmcgui . DialogProgress ( )
 O00O0oOO00O00 = '    Please Wait While We Load [COLOR yellow][B]%s[/B][/COLOR]' % ( name )
 IiiiI . create ( "FilmOn" , '' , O00O0oOO00O00 , '' )
 iiIi1iI1iIii = xbmcgui . ListItem ( name , iconImage = "DefaultVideo.png" , thumbnailImage = iconimage )
 iiIi1iI1iIii . setInfo ( type = "Video" , infoLabels = { "Title" : name , "Plot" : description } )
 iiIi1iI1iIii . setProperty ( "IsPlayable" , "true" )
 url = O0oOoOOOoOO ( programme_id , name )
 O00OoOO0oo0 = xbmc . PlayList ( xbmc . PLAYLIST_VIDEO )
 O00OoOO0oo0 . clear ( )
 O00OoOO0oo0 . add ( url , iiIi1iI1iIii )
 xbmc . Player ( xbmc . PLAYER_CORE_MPLAYER ) . play ( O00OoOO0oo0 )
 IiiiI . close ( )
 if 96 - 96: OoOoOO00 . o0oOOo0O0Ooo - ooOoO0o
def IiI111111IIII ( name , url , iconimage , description , favorites , deletefav , record , deleterecord , tvguide , programme_id , startdate_time ) :
 iiIi1iI1iIii = xbmcgui . ListItem ( name , iconImage = "DefaultVideo.png" , thumbnailImage = iconimage )
 iiIi1iI1iIii . setInfo ( type = "Video" , infoLabels = { "Title" : name , "Plot" : description } )
 iiIi1iI1iIii . setProperty ( "IsPlayable" , "true" )
 o00OooO0oo = [ ]
 if favorites :
  o00OooO0oo . append ( ( OOoO00o ( 30054 ) , 'XBMC.RunPlugin(%s?name=None&url=%s&mode=10&iconimage=None&description=None)' % ( sys . argv [ 0 ] , programme_id ) ) )
  iiIi1iI1iIii . addContextMenuItems ( items = o00OooO0oo , replaceItems = True )
 if deletefav :
  o00OooO0oo . append ( ( OOoO00o ( 30055 ) , 'XBMC.RunPlugin(%s?name=None&url=%s&mode=11&iconimage=None&description=None)' % ( sys . argv [ 0 ] , programme_id ) ) )
  iiIi1iI1iIii . addContextMenuItems ( items = o00OooO0oo , replaceItems = True )
 if record :
  o00OooO0oo . append ( ( OOoO00o ( 30056 ) , 'XBMC.RunPlugin(%s?name=None&url=%s&mode=6&iconimage=None&description=None&pid=%s&st=%s)' % ( sys . argv [ 0 ] , url , programme_id , startdate_time ) ) )
  iiIi1iI1iIii . addContextMenuItems ( items = o00OooO0oo , replaceItems = True )
 if deleterecord :
  o00OooO0oo . append ( ( OOoO00o ( 30057 ) , 'XBMC.RunPlugin(%s?name=None&url=None&mode=7&iconimage=None&description=None&startdate_time=%s)' % ( sys . argv [ 0 ] , startdate_time ) ) )
  iiIi1iI1iIii . addContextMenuItems ( items = o00OooO0oo , replaceItems = True )
  if 99 - 99: IiII . Oo0Ooo - Ii1I % Ii1I * O0 . II111iiii
 if tvguide :
  o00OooO0oo . append ( ( OOoO00o ( 30058 ) , 'XBMC.Container.Update(%s?name=None&url=%s&mode=8&iconimage=%s&description=None)' % ( sys . argv [ 0 ] , programme_id , iconimage ) ) )
  iiIi1iI1iIii . addContextMenuItems ( items = o00OooO0oo , replaceItems = True )
 xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = iiIi1iI1iIii , isFolder = False )
 if 4 - 4: Ii1I
 if 51 - 51: OoO0O00 - O0 % oO0o - II111iiii
 if 31 - 31: iII111i / Oo0Ooo - iII111i - OOooOOo
 if 7 - 7: iII111i % O0 . OoOoOO00 + I1IiiI - I11i
def OO00Oo ( content , viewType ) :
 if 75 - 75: I11i
 if content :
  xbmcplugin . setContent ( int ( sys . argv [ 1 ] ) , content )
 if iiiI11 . getSetting ( 'auto-view' ) == 'true' :
  xbmc . executebuiltin ( "Container.SetViewMode(%s)" % iiiI11 . getSetting ( viewType ) )
  if 71 - 71: ooOoO0o
  if 53 - 53: OoooooooOO % Ii1I . IiII / i11iIiiIii % iII111i
O0o0O0 = iii11I ( )
oo0 = None
IIIIii = None
iIiIIIIIii = None
O0o0 = None
Ii1I1IIii1II = None
OOo0 = None
ii11I1 = None
oO0oo = None
Ii111iIi1iIi = None
iiI111I1iIiI = None
i1I1ii11i1Iii = None
IIIII = None
if 78 - 78: Ii1I * i1IIi
try :
 oo0 = urllib . unquote_plus ( O0o0O0 [ "url" ] )
except :
 pass
try :
 IIIIii = urllib . unquote_plus ( O0o0O0 [ "name" ] )
except :
 pass
try :
 O0o0 = urllib . unquote_plus ( O0o0O0 [ "iconimage" ] )
except :
 pass
try :
 iIiIIIIIii = int ( O0o0O0 [ "mode" ] )
except :
 pass
try :
 Ii1I1IIii1II = urllib . unquote_plus ( O0o0O0 [ "description" ] )
except :
 pass
try :
 iiI111I1iIiI = urllib . unquote_plus ( O0o0O0 [ "programme_id" ] )
except :
 pass
try :
 i1I1ii11i1Iii = urllib . unquote_plus ( O0o0O0 [ "startdate_time" ] )
except :
 pass
try :
 IIIII = urllib . unquote_plus ( O0o0O0 [ "group" ] )
except :
 pass
 if 1 - 1: I1IiiI / IiII * ooOoO0o
print str ( OO0o ) + ': ' + str ( II11iiii1Ii )
print "Mode: " + str ( iIiIIIIIii )
print "URL: " + str ( oo0 )
print "Name: " + str ( IIIIii )
print "IconImage: " + str ( O0o0 )
if 1 - 1: I11i * o0oOOo0O0Ooo . OoOoOO00 / O0
if 100 - 100: I1Ii111 . o0oOOo0O0Ooo * Oo0Ooo % O0 * O0
if 14 - 14: I1ii11iIi11i . ooOoO0o + II111iiii / iII111i / I11i
if iIiIIIIIii == None or oo0 == None or len ( oo0 ) < 1 :
 print ""
 OOOoO0O0o ( )
 if 74 - 74: O0 / i1IIi
elif iIiIIIIIii == 2 :
 print "" + oo0
 O0oOoOOOoOO ( oo0 , O0o0 )
 if 78 - 78: OoooooooOO . OoO0O00 + ooOoO0o - i1IIi
elif iIiIIIIIii == 3 :
 print "" + oo0
 o0O0O00 ( IIIIii , oo0 , IIIII )
 if 31 - 31: OoooooooOO . OOooOOo
elif iIiIIIIIii == 4 :
 print "" + oo0
 Channel_Lists ( oo0 )
 if 83 - 83: iII111i . O0 / Oo0Ooo / OOooOOo - II111iiii
elif iIiIIIIIii == 5 :
 print "" + oo0
 IIi1i ( oo0 )
 if 100 - 100: OoO0O00
elif iIiIIIIIii == 6 :
 print "" + oo0
 i1I1iI1iIi111i ( oo0 , iiI111I1iIiI , i1I1ii11i1Iii )
 if 46 - 46: OoOoOO00 / iIii1I11I1II1 % iII111i . iIii1I11I1II1 * iII111i
elif iIiIIIIIii == 7 :
 print "" + oo0
 iI111i ( i1I1ii11i1Iii )
 if 38 - 38: I1ii11iIi11i - iII111i / O0 . I1Ii111
elif iIiIIIIIii == 8 :
 print "" + oo0
 II1 ( oo0 , O0o0 )
 if 45 - 45: I1Ii111
elif iIiIIIIIii == 9 :
 print "" + oo0
 ooo0OOOoo ( oo0 )
 if 83 - 83: OoOoOO00 . OoooooooOO
elif iIiIIIIIii == 10 :
 print "" + oo0
 OOooo0oOO0O ( oo0 )
 if 58 - 58: i11iIiiIii + OoooooooOO % OoooooooOO / IiII / i11iIiiIii
elif iIiIIIIIii == 11 :
 print "" + oo0
 O00o0OO0 ( oo0 )
 if 62 - 62: OoO0O00 / I1ii11iIi11i
elif iIiIIIIIii == 12 :
 print "" + oo0
 IIIiI11ii1I ( IIIIii , oo0 , O0o0 , Ii1I1IIii1II , OOo0 , ii11I1 , oO0oo , Ii111iIi1iIi , '' , iiI111I1iIiI , i1I1ii11i1Iii , IIIII )
elif iIiIIIIIii == 2000 :
 III11I1 ( )
xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
if 7 - 7: OoooooooOO . IiII
if 53 - 53: Ii1I % Ii1I * o0oOOo0O0Ooo + OoOoOO00
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
