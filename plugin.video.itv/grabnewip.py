import urllib2,re,xbmcaddon,xbmcgui
PLUGIN='plugin.video.itv'
ADDON = xbmcaddon.Addon(id=PLUGIN)


def OPEN_URL(url):
    req = urllib2.Request(url, headers={'User-Agent' : "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G34 Safari/601.1"}) 
    con = urllib2.urlopen( req )
    link= con.read()
    return link


import random  
link=OPEN_URL('http://free-proxy-list.net/uk-proxy.html')
match=re.compile('<tr><td>(.+?)</td><td>').findall(link)
ip=random.choice(match)
ADDON.setSetting('custom_ip',ip)


dialog = xbmcgui.Dialog()
dialog.ok('ITV Player', '','New Ip Address Is [COLOR green]%s[/COLOR]' %ip, 'Try Again Now')
    
