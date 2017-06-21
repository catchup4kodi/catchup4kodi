import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os
import re

ADDON = xbmcaddon.Addon(id='plugin.video.notfilmon')


def res():
    quality = ADDON.getSetting('res')
    if quality == '0':
        return ''
    elif quality == '1':
        return '360p'
    elif quality == '2':
        return '480p'
