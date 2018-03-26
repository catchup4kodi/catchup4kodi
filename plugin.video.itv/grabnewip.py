import random,xbmcaddon,xbmcgui


PLUGIN='plugin.video.itv'
ADDON = xbmcaddon.Addon(id=PLUGIN)

#82.0.0.0	82.23.146.47

ip = '82.%s.%s.%s' % (random.randint(0,23),random.randint(0,146),random.randint(0,47))

ADDON.setSetting('custom_ip',ip)


dialog = xbmcgui.Dialog()
dialog.ok('ITV Player', '','New Ip Address Is [COLOR green]%s[/COLOR]' %ip, 'Try Again Now')
    
