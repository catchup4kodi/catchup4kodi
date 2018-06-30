import os,xbmc,xbmcaddon

PLUGIN='plugin.video.itv'
ADDON = xbmcaddon.Addon(id=PLUGIN)


if ADDON.getSetting('delcache')=='true':
    cache = xbmc.translatePath(os.path.join('special://temp'))

    for root, dirs, files in os.walk(cache):


                    
        for f in files:
            if not '.log' in f:
                try:os.unlink(os.path.join(root, f))
                except:pass
