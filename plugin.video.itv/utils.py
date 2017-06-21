#!/usr/bin/python

import os, sys, re
import xbmc, xbmcaddon

__plugin_handle__ = int(sys.argv[1])

def get_addoninfo(id):
    dict = {}
    dict["id"]       = id
    dict["addon"]    = xbmcaddon.Addon(id)
    dict["language"] = dict["addon"].getLocalizedString
    dict["version"]  = dict["addon"].getAddonInfo("version")
    dict["path"]     = dict["addon"].getAddonInfo("path")
    dict["profile"]  = xbmc.translatePath(dict["addon"].getAddonInfo('profile'))
    return dict

def get_os():
    try: xbmc_os = os.environ.get("OS")
    except: xbmc_os = "unknown"
    return xbmc_os
