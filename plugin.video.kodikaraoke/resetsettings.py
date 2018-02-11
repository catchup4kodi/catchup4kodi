import sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin,urllib2,re
import shutil
import time

addon         = 'plugin.video.kodikaraoke'
ADDONID       = addon
addon_name    = addon
icon = xbmc.translatePath(os.path.join('special://home/addons', addon, 'icon.png'))
addonPath = xbmc.translatePath(os.path.join('special://home', 'addons', addon))
basePath = xbmc.translatePath(os.path.join('special://profile', 'addon_data', addon))
dbPath = xbmc.translatePath(xbmcaddon.Addon(addon).getAddonInfo('profile'))
dialog = xbmcgui.Dialog();dp = xbmcgui.DialogProgress()



def reset():
    db_dir = os.path.join(xbmc.translatePath("special://database"), 'Karaoke.db')
    AddonData = xbmc.translatePath('special://userdata/addon_data/plugin.video.kodikaraoke')

    for root, dirs, files in os.walk(AddonData):
        file_count = 0
        file_count += len(files)
        if file_count > 0:            
            for f in files:
                try:
                    os.unlink(os.path.join(root, f))
                except: pass
    try:os.unlink(os.path.join(db_dir))
    except:pass
    notify('Addon Reset','Reset Successfully Performed.',os.path.join('special://home/addons', addon, 'icon.png'))##NOTIFY##  

#

def SetSetting(param, value):
    value = str(value)
    if GetSetting(param) == value:
        return
    xbmcaddon.Addon(ADDONID).setSetting(param, value)

def GetSetting(param):
    return xbmcaddon.Addon(ADDONID).getSetting(param)

#
def notify(header,msg,icon_path):
    duration=1500
    #xbmc.executebuiltin("XBMC.Notification(%s,%s, %s, %s)" % (header, msg, duration, icon_path))
    xbmcgui.Dialog().notification(header, msg, icon=icon_path, time=duration, sound=False)
#

reset()


