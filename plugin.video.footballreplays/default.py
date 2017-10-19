# -*- coding: utf-8 -*-
import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os
import datetime,time,net,copy
from urlparse import urlparse, parse_qs, urlunparse
from bs4 import BeautifulSoup as BeautifulSoup


net=net.Net()
Ok = lambda x:xbmcgui.Dialog().ok('TEST',x)
PLUGIN='plugin.video.footballreplays'
ADDON = xbmcaddon.Addon(id='plugin.video.footballreplays')
maxVideoQuality = ADDON.getSetting("maxVideoQuality")

qual = ["480p", "720p", "1080p"]
maxVideoQuality = qual[int(maxVideoQuality)]


datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
cookie_path = os.path.join(datapath, 'cookies')
cookie_jar = os.path.join(cookie_path, "football.lwp")

VERSION = "1.0.2"
PATH = "Football Replays"
UATRACK="UA-35537758-1"
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

addonPath = xbmc.translatePath(ADDON.getAddonInfo('path'))


if os.path.exists(cookie_path) == False:
		os.makedirs(cookie_path)
		net.save_cookies(cookie_jar)

def CATEGORIES():
	addDir('Full Matches','url',3,'','1')
	addDir('Highlights','url',5 ,'','1')
	addDir('Find a Team','url',4,'','1')
	addDir('Pick a League','url',11,'','1')
	addDir('Upcoming Matches','http://livefootballvideo.com/streaming',12,'','1')
	setView('movies', 'movie-view')
	   #setView is setting the automatic view.....first is what section "movies"......second is what you called it in the settings xml

def CATEGORIES2():
	link=iiNT3LiiCheckURL('http://livefootballvideo.com/fullmatch')

	if link != False:
		r='<div class="cover"><a href="(.+?)" rel="bookmark" title="(.+?) vs (.+?)".+?<img src="(.+?)".+? longdate" rel=".+?">(.+?)/(.+?)/(.+?)</p>'
		match=re.compile(r,re.DOTALL).findall(link)

		for url,team_a,team_b,iconimage,month,day,year in match:
			_date='%s-%s-%s'%(month,day,year)
			_name = '[COLOR ghostwhite]'+team_a+'[/COLOR]  [COLOR deepskyblue]vs[/COLOR]  [COLOR ghostwhite]'+team_b+'[/COLOR] '+' : '+' '+_date
			addDir(_name,url,1,iconimage,'')
		addDir('[COLOR deepskyblue]Next Page[/COLOR] [COLOR ghostwhite]>>[/COLOR]','url',2,'','1')
		setView('movies', 'movie-view')
		#setView is setting the automatic view.....first is what section "movies"......second is what you called it in the settings xml

	else:
		iiNT3LiiFLAG()

def NEXTPAGE(page):
	pagenum=int(page) +1
	link=iiNT3LiiCheckURL('http://livefootballvideo.com/fullmatch/page/'+str(pagenum))

	if link != False:
		r='<div class="cover"><a href="(.+?)" rel="bookmark" title="(.+?) vs (.+?)">.+?<img src="(.+?)".+?<p class="postmetadata longdate" rel=".+?">(.+?)/(.+?)/(.+?)</p>'
		match=re.compile(r,re.DOTALL).findall(link)
		print match
		for url,team_a,team_b,iconimage,month,day,year in match:
			_date='%s-%s-%s'%(month,day,year)
			_name = '[COLOR ghostwhite]'+team_a+'[/COLOR]  [COLOR deepskyblue]vs[/COLOR]  [COLOR ghostwhite]'+team_b+'[/COLOR] '+' : '+' '+_date
			addDir(_name,url,1,iconimage,'')
		addDir('[COLOR deepskyblue]Next Page[/COLOR] [COLOR ghostwhite]>>[/COLOR]','url',2,'','1')
		setView('movies', 'movie-view')

	else:
		iiNT3LiiFLAG()

def GETLINKS(name,url):#  cause mode is empty in this one it will go back to first directory

	links=OPEN_URL(url)
	links= links.split("class='heading-more open'><span>")

	for link in links:
		# try:
			language=link.split('<')[0]
			if len(language)>1:
				addDir ('[COLOR green]%s[/COLOR]'%language, url , 200 , '', '' )

			if "proxy.link=lfv*" in link :
				import base64
				import decrypter
				match = re.compile('proxy\.link=lfv\*(.+?)&').findall(link)
				match = uniqueList(match)
				match = [decrypter.decrypter(198,128).decrypt(i,base64.urlsafe_b64decode('Y0ZNSENPOUhQeHdXbkR4cWJQVlU='),'ECB').split('\0')[0] for i in match]
				print match
				for url in match:

					url = replaceHTMLCodes(url)
					if url.startswith('//') : url = 'http:' + url
					url = url.encode('utf-8')
					_name=url.split('://')[1]
					_name=_name.split('/')[0].upper()
					addDir( name+' - [COLOR red]%s[/COLOR]'%_name , url , 200 , '' , '' )
			if "www.youtube.com/embed/" in link :
				r = 'youtube.com/embed/(.+?)"'
				match = re.compile(r,re.DOTALL).findall(link)
				yt= match[0]
				iconimage = 'http://i.ytimg.com/vi/%s/0.jpg' % yt.replace('?rel=0','')
				url = 'plugin://plugin.video.youtube/play/?video_id=%s' % yt.replace('?rel=0','')
				addDir( name+' - [COLOR red]YOUTUBE[/COLOR]' , url , 200 , iconimage , '' )
			if "dailymotion.com" in link :
				r = 'src="//www.dailymotion.com/embed/video/(.+?)"'
				match = re.compile(r,re.DOTALL).findall(link)

				for url in match :
					addDir ( name+' - [COLOR red]DAILYMOTION[/COLOR]' , url , 200 , GETTHUMB(url), '' )
			if "streamable.com" in link :
				# r = 'src="https://streamable.com/s/.+?/(.+?)\?.+?"></iframe>'
				r = '<iframe src="(.+?)"'
				match = re.compile(r,re.DOTALL).findall(link)
				for url in match:
					if 'streamable' in url:
						addDir ( name+' - [COLOR red]STREAMABLE[/COLOR]' , url , 200 , GETTHUMB(url), '' )
			if "http://videa" in link :
				r = 'http://videa.+?v=(.+?)"'
				match = re.compile(r,re.DOTALL).findall(link)
				for url in match :
					addDir (name+' - [COLOR red]VIDEA[/COLOR]',url,200,'', '' )

			if "rutube.ru" in link :
				r = 'ttp://rutube.ru/video/embed/(.+?)\?'
				match = re.compile(r,re.DOTALL).findall(link)
				print match
				for url in match :
					addDir (name+' - [COLOR red]RUTUBE[/COLOR]',url,200,'', '' )
			if 'cdn.playwire.com' in link :
				r = 'data-config="(.+?)"'
				match = re.compile(r,re.DOTALL).findall(link)
				for vid in match :
					if not 'http' in vid:
							vid='http:'+vid
					url=vid.replace('zeus.json','manifest.f4m')
					addDir (name+' - [COLOR red]PLAYWIRE[/COLOR]',url,200,'', '' )
			if "vk.com" in link :
				r = 'vk.com/(.+?)"'
				match = re.compile(r,re.DOTALL).findall(link)
				for url in match :
					addDir (name+' - [COLOR red]VK.COM[/COLOR]','http://vk.com/'+url,200,'', '' )
			if "mail.ru" in link :
				r = 'http://videoapi.my.mail.ru/videos/embed/(.+?)\.html'
				match = re.compile(r,re.DOTALL).findall(link)
				for url in match :
					addDir (name+' - [COLOR red]MAIL.RU[/COLOR]','http://videoapi.my.mail.ru/videos/%s.json'%url,200,'', '' )
			if "openload.co" in link :
				r = 'data-lazy-src="(.+?)"'
				match = re.compile(r,re.DOTALL).findall(link)
				for url in match :
					addDir (name+' - [COLOR red]OPENLOAD.CO[/COLOR]',url,200,'', '' )
				r = 'iframe src="(.+?)"'
				match = re.compile(r,re.DOTALL).findall(link)
				for url in match :
					if 'openload' in url:
						addDir (name+' - [COLOR red]OPENLOAD.CO[/COLOR]',url,200,'', '' )
			if "//player.footballfullmatch" in link :
				r = 'src="(.+?player.footballfullmatch.com.+?)"'
				match = re.compile(r,re.DOTALL).findall(link)
				for url in match :
					addDir (name+' - [COLOR red]FOOTBALLFULLMATCH.COM[/COLOR]',url,200,'', '' )
		# except:pass



def uniqueList(name):
	uniques = []
	for n in name:
		if n not in uniques:
			uniques.append(n)
	return uniques

def replaceHTMLCodes(txt):
	import HTMLParser

	# Fix missing ; in &#<number>;
	txt = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", makeUTF8(txt))

	txt = HTMLParser.HTMLParser().unescape(txt)
	txt = txt.replace("&amp;", "&")
	return txt

def makeUTF8(data):
	return data
	try:
		return data.decode('utf8', 'xmlcharrefreplace') # was 'ignore'
	except:
		s = u""
		for i in data:
			try:
				i.decode("utf8", "xmlcharrefreplace")
			except:
				log("Can't convert character", 4)
				continue
			else:
				s += i
		return s

def HIGHLIGHTS():
	showScore = xbmcaddon.Addon(id='plugin.video.footballreplays').getSetting('highScore')
	link=iiNT3LiiCheckURL('http://livefootballvideo.com/highlights')

	if link != False:
		r= '<div class="team home column">(.+?)&nbsp;.+?<a href="(.+?)" class="score">(.+?)</a>.+?">&nbsp;(.+?)</div>'
		match = re.compile ( r , re.DOTALL).findall (link)
		for team_a ,url,score,  team_b  in match :

			if score.startswith('<span'):
				score = score.split('/span>')[1]
			if score.endswith('</span>'):
				score = score.split('<span')[0]

			if showScore == "true":
				theScore = score.replace(' ','').split('-')
				score = '[ '+' [COLOR deepskyblue]'+str(theScore[0])+'[/COLOR]  -  [COLOR deepskyblue]'+str(theScore[1])+'[/COLOR] '+' ]'
				name = '[COLOR ghostwhite]%s[/COLOR] %s [COLOR ghostwhite]%s[/COLOR]' % ( team_a ,score, team_b )

			else:
				name = '[COLOR ghostwhite]%s[/COLOR] [COLOR deepskyblue]vs[/COLOR] [COLOR ghostwhite]%s[/COLOR]' % ( team_a ,team_b )


			iconimage = 'http://livefootballvideo.com'
			addDir(name,url,7,iconimage,'')
		addDir('[COLOR deepskyblue]Next Page[/COLOR] [COLOR ghostwhite]>>[/COLOR]' , 'url' , 6 , '' , '1' )
		setView('movies', 'movie-view')

	else:
		iiNT3LiiFLAG()

def HIGHLIGHTS_NEXTPAGE( page ):
	showScore = xbmcaddon.Addon(id='plugin.video.footballreplays').getSetting('highScore')
	page_num =int ( page ) + 1
	link=iiNT3LiiCheckURL( 'http://livefootballvideo.com/highlights/page/' + str ( page_num ) )

	if link != False:
		r= '<div class="team home column">(.+?)&nbsp;.+?<a href="(.+?)" class="score">(.+?)</a>.+?">&nbsp;(.+?)</div>'
		match = re.compile ( r , re.DOTALL).findall (link)

		for team_a ,url,score,  team_b  in match:

			if showScore == "true":
				theScore = score.replace(' ','').split('-')
				score = '[ '+' [COLOR deepskyblue]'+str(theScore[0])+'[/COLOR]  -  [COLOR deepskyblue]'+str(theScore[1])+'[/COLOR] '+' ]'
				name = '[COLOR ghostwhite]%s[/COLOR] %s [COLOR ghostwhite]%s[/COLOR]' % ( team_a ,score, team_b )

			else:
				name = '[COLOR ghostwhite]%s[/COLOR] [COLOR deepskyblue]vs[/COLOR] [COLOR ghostwhite]%s[/COLOR]' % ( team_a , team_b )

			iconimage = 'http://livefootballvideo.com'
			addDir(name,url,7,iconimage,'')
		addDir('[COLOR deepskyblue]Next Page[/COLOR] [COLOR ghostwhite]>>[/COLOR]' , 'url' , 6 , '' , '1' )
		setView('movies', 'movie-view')

	else:
		iiNT3LiiFLAG()

def HIGHLIGHTS_LINKS(name,url):
	GETLINKS(name,url)

###############################################################################################################################
##### Some Qoodoo

def to_utf8(obj):
	if isinstance(obj, unicode):
		obj = obj.encode('utf-8', 'ignore')
	elif isinstance(obj, dict):
		obj = copy.deepcopy(obj)
		for key, val in obj.items():
			obj[key] = to_utf8(val)
	elif obj is not None and hasattr(obj, "__iter__"):
		obj = obj.__class__([to_utf8(x) for x in obj])
	else:
		pass
	return obj

def to_unicode(obj):
	if isinstance(obj, basestring):
		try:
			obj = unicode(obj, 'utf-8')
		except TypeError:
			pass
	elif isinstance(obj, dict):
		obj = copy.deepcopy(obj)
		for key, val in obj.items():
			obj[key] = to_unicode(val)
	elif obj is not None and hasattr(obj, "__iter__"):
		obj = obj.__class__([to_unicode(x) for x in obj])
	else:
		pass
	return obj

###############################################################################################################################
##### ][NT3L][G3NC][


def iiNT3LiiCheckURL(url):
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		return link
	except:
		return False


def iiNT3LiiFLAG():

	class flagDialog(xbmcgui.WindowXMLDialog):

		def onInit(self):
			pass

		def onAction(self, action):
			KEY_BUTTON_BACK = 275
			KEY_KEYBOARD_ESC = 61467
			ACTION_PREVIOUS_MENU = 10
			ACTION_SELECT_ITEM = 7
			ACTION_BACKSPACE = 92
			buttonCode          =  action.getButtonCode()
			actionID            =  action.getId()
			if action           == ACTION_PREVIOUS_MENU:    self.close()
			elif action         == ACTION_BACKSPACE:        self.close()

	redFlag = flagDialog('down.xml', addonPath,'default')
	redFlag.doModal()
	del redFlag


class upcomingDialog(xbmcgui.WindowXMLDialog):

	def __init__( self, *args, **kwargs ):
		self.url = kwargs["url"]

	def onInit(self):
		self.CurrentWindow = xbmcgui.getCurrentWindowId()
		self.nextButton = self.getControl(33000)
		self.prevButton = self.getControl(33001)
		self.nextButton.setVisible(False)
		self.prevButton.setVisible(False)
		self.setDetails(self.url)


	def iiNT3LiiCheckedURL(self,url):
		try:
			req = urllib2.Request(url)
			req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
			response = urllib2.urlopen(req)
			link=response.read()
			response.close()
			return link
		except:
			return False


	def setDetails(self,url):
		theSource = self.iiNT3LiiCheckedURL(url)

		if theSource != False:
			pageRegex = r'<div class=.navigation.>.<div class=.wp-pagenavi.>.<span class=.pages.>Page ([^ ]*) of (.?)</span>'
			regexLive = r'<div class="league column">.<a href="([^"]*)" title="[^"]*">([^<>]*)</a>.</div>.<div class="date_time column"><span class="starttime time" rel="[^"]*">([^<>]*)</span> - <span class="endtime time" rel="[^"]*">([^<>]*)</span><span class="startdate date" rel="[^"]*">([^<>]*)</span></div>.<div class="team column"><img [^=]*="[^"]*".+?src="[^"]*"><span>([^<>]*)</span></div>.<div class="versus column">vs.</div>.<div class="team away column"><span>([^<>]*)</span><img [^=]*="[^"]*".+?src="[^"]*"></div>.<div class="live_btn column">.<a href="([^"]*)">'
			matchLive = re.compile(regexLive,re.DOTALL).findall(theSource)
			gotPage = re.compile(pageRegex,re.DOTALL).findall(theSource)
			items = []
			theCount = len(matchLive) / 2
			theCounted = 0

			if len(gotPage) != 0:

				if int(gotPage[0][0]) == 1:
					self.next = url+'/page/'+str(int(gotPage[0][0]) + 1)
					self.nextButton.setVisible(True)
					self.prevButton.setVisible(False)

				elif int(gotPage[0][0]) == 2:
					self.next = url.replace('/page/'+str(gotPage[0][0]),'/page/'+str(int(gotPage[0][0]) + 1))
					self.prev = url.replace('/page/'+str(gotPage[0][0]),"")
					self.nextButton.setVisible(True)
					self.prevButton.setVisible(True)


				elif int(gotPage[0][0]) != int(gotPage[0][1]):
					self.next = url.replace('/page/'+str(gotPage[0][0]),'/page/'+str(int(gotPage[0][0]) + 1))
					self.prev = url.replace('/page/'+str(gotPage[0][0]),'/page/'+str(int(gotPage[0][0]) - 1))
					self.nextButton.setVisible(True)
					self.prevButton.setVisible(True)

				else:
					self.prev = url.replace('/page/'+str(gotPage[0][0]),'/page/'+str(int(gotPage[0][0]) - 1))
					self.nextButton.setVisible(False)
					self.prevButton.setVisible(True)

			else:
				self.nextButton.setVisible(False)
				self.prevButton.setVisible(False)

			for leagueURL,leagueName,startTime,endTime,theDate,team_a,team_b,url in matchLive:
				item = xbmcgui.ListItem(team_a + "|" + team_b)
				item.setProperty('team_a',team_a)
				item.setProperty('team_b',team_b)
				item.setProperty('leagueName',leagueName)
				item.setProperty('date',theDate+" @ "+startTime)
				item.setProperty('url',url)
				items.append(item)
				#theCounted += 1

				#if theCounted == theCount:
			self.getControl(32502).addItems(items)
					#items = []

				#if theCounted == len(matchLive):
					#self.getControl(32502).addItems(items)

			#xbmc.executebuiltin("ClearProperty(loading,Home)")
			xbmc.executebuiltin("SetProperty(has_history,1,home)")


		else:
			iiNT3LiiFLAG()



	def onAction(self, action):
		KEY_BUTTON_BACK = 275
		KEY_KEYBOARD_ESC = 61467
		ACTION_PREVIOUS_MENU = 10
		ACTION_SELECT_ITEM = 7
		ACTION_BACKSPACE = 92
		buttonCode          =  action.getButtonCode()
		actionID            =  action.getId()
		if action           == ACTION_PREVIOUS_MENU:    self.close()
		elif action         == ACTION_BACKSPACE:        self.close()

	def onClick(self,controlId):
		if controlId == 32502:
			url = self.getControl(controlId).getSelectedItem().getProperty("url")
		elif controlId == 32505:
			self.getControl(32502).reset()
			self.setDetails(self.next)
		elif controlId == 32506:
			self.getControl(32502).reset()
			self.setDetails(self.prev)


def iiNT3LiiLiiV3(url):
	main = upcomingDialog('upcomingMatches.xml', addonPath,'default',url=url)
	main.doModal()
	del main


def iiNT3LiiHLIGHTS(baseURL):
	theSource = iiNT3LiiCheckURL(baseURL)

	if theSource != False:
		showScore = xbmcaddon.Addon(id='plugin.video.footballreplays').getSetting('highScore')
		regexLight = r'<div class=.listhighlights.>.+?<div class=.navigation.>.<div class=.wp-pagenavi.>.<span class=.pages.>Page .? of .?</span>'
		#regex = r'<div class="leaguelogo column"><a href="([^"]*)" title="([^"]*)"><img src="[^"]*" alt="[^"]*" data-pagespeed-url-hash="[^"]*" onload="[^"]*".+?</div>.<div class="date_time column"><span class="starttime shortdate" rel="[^"]*">([^<>]*)</span></div>.<div class="team home column">[^<>]*<img alt="([^"]*)" src="[^"]*" data-pagespeed-url-hash="[^"]*" onload="[^"]*"></div>.<div class="result column"><a href="[^"]*" class="score">([^<>]*)</a></div>.<div class="team column"><img alt="([^"]*)" src="[^"]*" data-pagespeed-url-hash="[^"]*" onload="[^"]*">[^<>]*</div>.<div class="play_btn column"><a href="([^"]*)"'
		regex = r'<div class="leaguelogo column"><a href="([^"]*)" title="([^"]*)"><img src="[^"]*" alt="[^"]*".+?</div>.<div class="date_time column"><span class="starttime shortdate" rel="[^"]*">([^<>]*)</span></div>.<div class="team home column">[^<>]*<img alt="([^"]*)" src="[^"]*".+?</div>.<div class="result column"><a href="[^"]*" class="score">([^<>]*)</a></div>.<div class="team column"><img alt="([^"]*)".+?</div>.<div class="play_btn column"><a href="([^"]*)"'
		pageRegex = r'<div class=\Wnavigation\W>.<div class=\Wwp-pagenavi\W>.<span class=\Wpages\W>Page ([^ ]*) of (.?)</span>'
		matchLight = re.compile(regexLight, re.DOTALL).findall(theSource)

		if int(len(matchLight)) == 0:
			match = re.compile(regex, re.DOTALL).findall(theSource)

			for leagueURL,leagueName,theDate,team_a,score,team_b,url in match:
				date =  theDate.split('/')
				theDate = date[1]+'-'+date[0]

				if showScore == "true":
					theScore = score.replace(' ','').split('-')
					score = '[ '+' [COLOR deepskyblue]'+str(theScore[0])+'[/COLOR]  -  [COLOR deepskyblue]'+str(theScore[1])+'[/COLOR] '+' ]'
					name = '[COLOR ghostwhite]'+team_a+'[/COLOR]  '+score+'  [COLOR ghostwhite]'+team_b+'[/COLOR] '+' : '+' '+theDate

				else:
					name = '[COLOR ghostwhite]'+team_a+'[/COLOR]  [COLOR deepskyblue]vs[/COLOR]  [COLOR ghostwhite]'+team_b+'[/COLOR] '+' : '+' '+theDate

				iconimage = 'http://livefootballvideo.com'
				addDir2(leagueURL,leagueName,theDate,name,url,7,iconimage,'')

		else:
			match = re.compile(regex, re.DOTALL).findall(matchLight[0])
			gotPage = re.compile(pageRegex, re.DOTALL).findall(matchLight[0])

			if int(len(match)) != 0:

				for leagueURL,leagueName,theDate,team_a,score,team_b,url in match:
					date =  theDate.split('/')
					theDate = date[1]+'-'+date[0]

					if showScore == "true":
						theScore = score.replace(' ','').split('-')
						score = '[ '+' [COLOR deepskyblue]'+str(theScore[0])+'[/COLOR]  -  [COLOR deepskyblue]'+str(theScore[1])+'[/COLOR] '+' ]'
						name = '[COLOR ghostwhite]'+team_a+'[/COLOR]  '+score+'  [COLOR ghostwhite]'+team_b+'[/COLOR] '+' : '+' '+theDate

					else:
						name = '[COLOR ghostwhite]'+team_a+'[/COLOR]  [COLOR deepskyblue]vs[/COLOR]  [COLOR ghostwhite]'+team_b+'[/COLOR] '+' : '+' '+theDate

					iconimage = 'http://livefootballvideo.com'
					addDir2(leagueURL,leagueName,theDate,name,url,7,iconimage,'')

				if int(gotPage[0][0]) == 1:
					addDir('[COLOR deepskyblue]Next Page[/COLOR] [COLOR ghostwhite]>>[/COLOR]',baseURL+'/page/'+str(int(gotPage[0][0]) + 1),8,'','1')
				else:
					if int(gotPage[0][0]) != int(gotPage[0][1]):
						addDir('[COLOR deepskyblue]Next Page[/COLOR] [COLOR ghostwhite]>>[/COLOR]',baseURL.replace('/page/'+str(gotPage[0][0]),'/page/'+str(int(gotPage[0][0]) + 1)),8,'','1')

		setView('movies', 'movie-view')

	else:
		iiNT3LiiFLAG()



def iiNT3LiiFULL(baseURL):
	theSource = iiNT3LiiCheckURL(baseURL)

	if theSource != False:
		regexFull = r'<h2>Full Matches</h2>.+?<div class="navigation">.<div class=\'wp-pagenavi\'>.<span class=\'pages\'>Page .? of .?</span>'
		regex ='<div class="cover"><a href="(.+?)" rel="bookmark" title="(.+?) vs (.+?)".+?<img src="(.+?)".+? longdate" rel=".+?">(.+?)/(.+?)/(.+?)</p>'
		pageRegex = r'<div class="navigation">.<div class=\'wp-pagenavi\'>.<span class=\'pages\'>Page ([^ ]*) of (.?)</span>'
		matchFull = re.compile(regexFull, re.DOTALL).findall(theSource)

		if int(len(matchFull)) == 0:
			match = re.compile(regex, re.DOTALL).findall(theSource)

			for url,team_a,team_b,iconimage,month,day,year in match:
				_date='%s-%s-%s'%(month,day,year)
				_name = '[COLOR ghostwhite]'+team_a+'[/COLOR]  [COLOR deepskyblue]vs[/COLOR]  [COLOR ghostwhite]'+team_b+'[/COLOR] '+' : '+' '+_date
				addDir(_name,url,1,iconimage,'')
			setView('movies', 'movie-view')

		else:
			match = re.compile(regex, re.DOTALL).findall(matchFull[0])
			gotPage = re.compile(pageRegex, re.DOTALL).findall(matchFull[0])

			for url,team_a,team_b,iconimage,month,day,year in match:
				_date='%s-%s-%s'%(month,day,year)
				_name = '[COLOR ghostwhite]'+team_a+'[/COLOR]  [COLOR deepskyblue]vs[/COLOR]  [COLOR ghostwhite]'+team_b+'[/COLOR] '+' : '+' '+_date
				addDir(_name,url,1,iconimage,'')

			if int(gotPage[0][0]) == 1:
				addDir('[COLOR deepskyblue]Next Page[/COLOR] [COLOR ghostwhite]>>[/COLOR]',baseURL+'/page/'+str(int(gotPage[0][0]) + 1),9,'','1')
			else:
				if int(gotPage[0][0]) != int(gotPage[0][1]):
					addDir('[COLOR deepskyblue]Next Page[/COLOR] [COLOR ghostwhite]>>[/COLOR]',baseURL.replace('/page/'+str(gotPage[0][0]),'/page/'+str(int(gotPage[0][0]) + 1)),9,'','1')
			setView('movies', 'movie-view')

	else:
		iiNT3LiiFLAG()



def iiNT3LiiT3AM():
	theURL = "http://livefootballvideo.com/teams"
	theSource = iiNT3LiiCheckURL(theURL)

	if theSource != False:
		theRegex = r'<a href="(/teams/[^"]*)" title="[^"]*">(.+?)</a>'
		theTeams = re.compile(theRegex).findall(theSource)
		for url,name in sorted(theTeams, key=lambda theTeams: theTeams[1]):
			addDir(to_utf8(name),"http://livefootballvideo.com"+url,10,'',1)
		setView('movies', 'movie-view')

	else:
		iiNT3LiiFLAG()



def iiNT3LiiL3AGU3():
	theURL = "http://livefootballvideo.com/competitions"
	theSource = iiNT3LiiCheckURL(theURL)

	if theSource != False:
		theRegex = r'<a href="(/competitions/[^"]*)" title="[^"]*">(.+?)</a>'
		theTeams = re.compile(theRegex).findall(theSource)
		for url,name in sorted(theTeams, key=lambda theTeams: theTeams[1]):
			addDir(to_utf8(name),"http://livefootballvideo.com"+url,10,'',1)
		setView('movies', 'movie-view')

	else:
		iiNT3LiiFLAG()



def iiNT3LiiM3NU(name,url):
	MenuItem = xbmcgui.Dialog().select('[COLOR deepskyblue]'+name+'[/COLOR]', ['[COLOR ghostwhite]Full Matches[/COLOR]','[COLOR ghostwhite]HighLights[/COLOR]'])
	if MenuItem==0:
		iiNT3LiiFULL(url)

	elif MenuItem==1:
		iiNT3LiiHLIGHTS(url)



##################################################################################################################################################

def GETTHUMB(url):
	try:
		import json
		content = OPEN_URL('https://api.dailymotion.com/video/%s?fields=thumbnail_large_url'%url)
		data = json.loads(content)
		icon=data['thumbnail_large_url']
		return icon
	except:
		return ''

def GrabRu(id):
	print id
	link = OPEN_URL('http://rutube.ru/api/play/trackinfo/%s/?format=xml'%str(id))
	r = '<m3u8>(.+?)</m3u8>'
	match = re.compile(r,re.DOTALL).findall(link)
	return match[0]

def getData(url,headers={}):
	net.save_cookies(cookie_jar)
	req = urllib2.Request(url)
	req.add_header('User-Agent', USER_AGENT)
	response = urllib2.urlopen(req)
	data=response.read()
	response.close()
	return data

def GrabMailRu(url):
	print 'RESOLVING VIDEO.MAIL.RU VIDEO API LINK'

	import json
	items = []
	quality = "???"
	data = getData(url)
	cookie = net.get_cookies()
	for x in cookie:

		 for y in cookie[x]:

			  for z in cookie[x][y]:

				   l= (cookie[x][y][z])
	name=[]
	url=[]
	r = '"key":"(.+?)","url":"(.+?)"'
	match = re.compile(r,re.DOTALL).findall(data)
	for quality,stream in match:
		name.append(quality.title())
		test = str(l)
		test = test.replace('<Cookie ','')
		test = test.replace(' for .my.mail.ru/>','')
		url.append(stream +'|Cookie='+test)

	return url[xbmcgui.Dialog().select('Please Select Resolution', name)]

def GrabVidea(id):
	link = OPEN_URL('http://videa.hu/flvplayer_get_video_xml.php?v=%s&m=0'%str(id))
	name=[]
	url=[]
	r = 'version quality="(.+?)" video_url="(.+?)"'
	match = re.compile(r,re.DOTALL).findall(link)
	for quality,stream in match:
		name.append(quality.title())
		url.append(stream)
	return url[xbmcgui.Dialog().select('Please Select Resolution', name)]

def GrabVK(url):
	if not 'http:' in url:
			url='http:'+url
	print url.replace('amp;','')
	url=url.replace('amp;','')
	if 'ext.php' in url:
		html=OPEN_URL(url)
		r      ='"url(\d+)":"(.+?)"'
		name=[]
		url=[]
		match = re.compile(r,re.DOTALL).findall(html)
		for quality,stream in match:
			name.append(quality.replace('\\','')+'p')
			url.append(stream.replace('\/','/'))
		return url[xbmcgui.Dialog().select('Please Select Resolution', name)]

	else:
		try:
			dp = xbmcgui.DialogProgress()
			dp.create("Football Replays", '','Please Wait Trying to Resolve', '')
			if ADDON.getSetting('use_vk')== 'true':
					number=ADDON.getSetting('vk_user')
					password=ADDON.getSetting('vk_password')

			else:
					p=OPEN_URL('https://xunitytalk-repository.googlecode.com/svn/addons/plugin.video.footballreplays/accounts.txt')
					from random import randint
					match=re.compile('user=(.+?)pass=(.+?)"').findall (p)
					b = int(randint(0,len(match)-1))
					number= match[b][0]
					password= match[b][1]
			html=LOGIN_VK(number,password,url)
			r      ='"url(\d+)":"(.+?)"'
			name=[]
			url=[]
			match = re.compile(r,re.DOTALL).findall(html)
			for quality,stream in match:
				name.append(quality.replace('\\','')+'p')
				url.append(stream.replace('\/','/'))
			return url[xbmcgui.Dialog().select('Please Select Resolution', name)]
			dp.close()
		except:
			dialog = xbmcgui.Dialog()
			dialog.ok("Football Replays", '','Sorry Video Is Private', '')


def LOGIN_VK(number,password,GET_URL):
	headers = {}
	headers.update({'Content-Type': 'application/x-www-form-urlencoded', 'Connection': 'keep-alive',
					'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
					'Accept-Encoding': 'gzip,deflate,sdch', 'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
					'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36'})

	html = net.http_GET('http://vk.com')
	ip_h = re.search(r'ip_h\"\svalue=\"(.*?)\"', html.content, re.I)
	html = net.http_POST('https://login.vk.com/?act=login', {'act':'login','role':'al_frame','expire':'',
															 'captcha_sid':'','_origin':'http://vk.com','ip_h':ip_h.group(1),
															 'email':str(number),'pass':str(password)})
	if os.path.exists(cookie_path) == False:
		os.makedirs(cookie_path)
	net.save_cookies(cookie_jar)
	net.set_cookies(cookie_jar)
	html = net.http_GET(GET_URL).content.replace('\\','')
	return html

def PLAYSTREAM(name,url,iconimage):
		if 'YOUTUBE' in name:
			link = str(url)
		elif 'VIDEA' in name:
			try:
				url=url.split('-')[1]
			except:
				url=url
			link = GrabVidea(url)
		elif 'VK.COM' in name:
			link = GrabVK(url)

		elif 'MAIL.RU' in name:
			link = GrabMailRu(url)

		elif 'RUTUBE' in name:
			try:
				html = 'http://rutube.ru/api/play/trackinfo/%s/?format=xml'% url.replace('_ru','')
				print html
				link = OPEN_URL(html)
				r = '<m3u8>(.+?)</m3u8>'
				match = re.compile(r,re.DOTALL).findall(link)
				if match:
					link=match[0]
				else:
					dialog = xbmcgui.Dialog()
					dialog.ok("Football Replays", '','Sorry Video Is Private', '')
					return
			except:
				dialog = xbmcgui.Dialog()
				dialog.ok("Football Replays", '','Sorry Video Is Private', '')
				return
		elif 'PLAYWIRE' in name:
			link = OPEN_URL(url)
			r = '<baseURL>(.+?)</baseURL>'
			base=  re.compile(r,re.DOTALL).findall(link)[0]
			h='media url="(.+?)"'
			files = re.compile(h,re.DOTALL).findall(link)[0]

			if base:
				link=base+'/'+files

		elif 'DAILYMOTION' in name:
			import urlresolver
			link = 'http://www.dailymotion.com/embed/video/'+url
			link=urlresolver.resolve(str(link))

		elif 'FOOTBALLFULLMATCH.COM' in name:
			link = OPEN_URL(url).replace("'",'"')
			r = '"file": "(.+?)"'
			link=  re.compile(r,re.DOTALL).findall(link)[0]

		else:
			import urlresolver
			link=urlresolver.resolve(str(url))
		try:
			liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
			liz.setInfo( type="Video", infoLabels={ "Title": name} )
			liz.setProperty("IsPlayable","true")
			liz.setPath(link)
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
		except:pass

def OPEN_URL(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def OPEN_MAGIC(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent' , "Magic Browser")
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

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

# this is the listing of the items
def addDir(name,url,mode,iconimage,page):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&page="+str(page)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name} )
		if mode == 200:
			liz.setProperty("IsPlayable","true")
			ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
		elif mode == 12:
			ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
		else:
			ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
		return ok

def addDir2(leagueURL,leagueName,theDate,name,url,mode,iconimage,page):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&leagueURL="+urllib.quote_plus(leagueURL)+"&leagueName="+urllib.quote_plus(leagueName)+"&theDate="+urllib.quote_plus(theDate)+"&page="+str(page)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name} )
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
		return ok

def addDir3(name,mode,url):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name} )
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
		return ok


# same as above but this is addlink this is where you pass your playable content so you dont use addDir you use addLink "url" is always the playable content
def addLink(name,url,iconimage,description):
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
		liz.setProperty("IsPlayable","true")
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
		return ok

# below tells plugin about the views
def setView(content, viewType):
	''' Why recode whats allready written and works well,
	Thanks go to Eldrado for it '''
	if content:
		xbmcplugin.setContent(int(sys.argv[1]), content)
	if ADDON.getSetting('auto-view') == 'true':

		print ADDON.getSetting(viewType)
		if ADDON.getSetting(viewType) == 'Info':
			VT = '504'
		elif ADDON.getSetting(viewType) == 'Info2':
			VT = '503'
		elif ADDON.getSetting(viewType) == 'Info3':
			VT = '515'
		elif ADDON.getSetting(viewType) == 'Fanart':
			VT = '508'
		elif ADDON.getSetting(viewType) == 'Poster Wrap':
			VT = '501'
		elif ADDON.getSetting(viewType) == 'Big List':
			VT = '51'
		elif ADDON.getSetting(viewType) == 'Low List':
			VT = '724'
		elif ADDON.getSetting(viewType) == 'List':
			VT = '50'
		elif ADDON.getSetting(viewType) == 'Default Menu View':
			VT = ADDON.getSetting('default-view1')
		elif ADDON.getSetting(viewType) == 'Default TV Shows View':
			VT = ADDON.getSetting('default-view2')
		elif ADDON.getSetting(viewType) == 'Default Episodes View':
			VT = ADDON.getSetting('default-view3')
		elif ADDON.getSetting(viewType) == 'Default Movies View':
			VT = ADDON.getSetting('default-view4')
		elif ADDON.getSetting(viewType) == 'Default Docs View':
			VT = ADDON.getSetting('default-view5')
		elif ADDON.getSetting(viewType) == 'Default Cartoons View':
			VT = ADDON.getSetting('default-view6')
		elif ADDON.getSetting(viewType) == 'Default Anime View':
			VT = ADDON.getSetting('default-view7')

		xbmc.executebuiltin("Container.SetViewMode(%s)" % ( int(VT) ) )

	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_TITLE )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_TITLE )

params=get_params()
url=None
name=None
mode=None
iconimage=None
page=None


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
		page=int(params["page"])
except:
		pass




#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
		CATEGORIES()

elif mode==1:
		GETLINKS(name,url)

elif mode==2:
		NEXTPAGE(page)

elif mode==3:
		CATEGORIES2()

elif mode == 4:
		iiNT3LiiT3AM()

elif mode==5:
		HIGHLIGHTS()

elif mode == 6 :
	HIGHLIGHTS_NEXTPAGE(page)

elif mode == 7 :
	HIGHLIGHTS_LINKS(name,url)

elif mode == 8:
	iiNT3LiiHLIGHTS(url)

elif mode == 9:
	iiNT3LiiFULL(url)

elif mode == 10:
	iiNT3LiiM3NU(name,url)

elif mode == 11:
	iiNT3LiiL3AGU3()

elif mode == 12:
	iiNT3LiiLiiV3(url)

#elif mode == 13:
#	iiNT3LiiSTR3AMS(url)

elif mode==200:
		PLAYSTREAM(name,url,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
