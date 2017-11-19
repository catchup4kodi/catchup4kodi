# load lib directory
# begin
import xbmc,os,shutil
import re
xbmc_version =  re.search('^(\d+)', xbmc.getInfoLabel( "System.BuildVersion" ))
if xbmc_version:
    xbmc_version = int(xbmc_version.group(1))
else:
    xbmc_version = 1


main_path = xbmc.translatePath(os.path.join('special://home/addons', 'repository.mdrepo'))
repo_path = xbmc.translatePath(os.path.join('special://home/addons', 'repository.duckpool'))
repoxml = xbmc.translatePath(os.path.join('special://home/addons', 'repository.duckpool','addon.xml'))
addonxml=xbmc.translatePath(os.path.join('special://home/addons', 'repository.mdrepo','addon.xml'))




old = ['repository.istream', 'script.icechannel.iStream.about.settings', 'script.istream.dialogs',
       'script.icechannel.iStream.internetconnection.settings', 'script.icechannel.iStream.lists.settings',
       'script.icechannel.iStream.live_tv.settings', 'script.icechannel.iStream.movies.settings',
       'script.icechannel.iStream.tv_shows.settings', 'script.icechannel.iStream.xbmcintegration.settings',
       'script.icechannel.extn.xunity.tv.common', 'script.icechannel.extn.xunitytalk'
       'script.icechannel.theme.xunity', 'script.icechannel.theme.xunityhd']

delete_old = any(xbmc.getCondVisibility('System.HasAddon(%s)' % (addon)) for addon in old)

if delete_old:

        for root, dirs, files in os.walk(xbmc.translatePath('special://home/addons')):

            dirs[:] = [d for d in dirs if d in old]
            for d in dirs:
                    try:
                            shutil.rmtree(os.path.join(root, d), ignore_errors=True)

                    except OSError:
                            pass

                    xbmc.executebuiltin('UpdateLocalAddons')
                    xbmc.executebuiltin("UpdateAddonRepos")




if xbmc_version >= 16.9:
        dependencies = ['repository.catchup4kodi','script.module.elementtree', 'script.module.muckys.common',
                        'script.common.plugin.cache','script.icechannel.dialogs', 'script.module.addon.common',
                        'script.module.beautifulsoup', 'script.module.dnspython', 'script.video.F4mProxy',
                        'script.module.feedparser', 'script.module.metahandler', 'script.module.myconnpy',
                        'script.module.parsedom', 'script.module.pyamf', 'script.module.simple.downloader',
                        'script.module.socksipy', 'script.module.t0mm0.common', 'script.module.unidecode',
                        'script.module.universal', 'script.module.urlresolver','script.icechannel.theme.default',]
        
        import glob


        folder = xbmc.translatePath('special://home/addons/')

        for DEPEND in glob.glob(folder+'script.icechannel*'):
            try:dependencies.append(DEPEND.rsplit('\\', 1)[1])
            except:dependencies.append(DEPEND.rsplit('/', 1)[1])


        for THEPLUGIN in dependencies:
            xbmc.log(str(THEPLUGIN))
            query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":"%s","enabled":true}, "id":1}' % (THEPLUGIN)
         
            xbmc.executeJSONRPC(query)
    
        xbmc.executebuiltin('UpdateLocalAddons') 
        xbmc.executebuiltin("UpdateAddonRepos")

                
if xbmc_version >= 14:
    addon_id = 'script.icechannel'
    lib_addon_dir_name = "lib"
    import xbmcaddon
    import os
    from os.path import join, basename
    import sys
    addon = xbmcaddon.Addon(id=addon_id)
    addon_path = addon.getAddonInfo('path')
    sys.path.append(addon_path)
    lib_addon_dir_path = os.path.join( addon_path, lib_addon_dir_name)
    sys.path.append(lib_addon_dir_path)
    for dirpath, dirnames, files in os.walk(lib_addon_dir_path):
        sys.path.append(dirpath)
# end

from entertainment import common
import os

common._update_settings_xml()

services_path = os.path.join(common.addon_path, 'services')

sti=1

for dirpath, dirnames, files in os.walk(services_path):
    for f in files:
        if f.endswith('.py'):
            service_py = os.path.join(dirpath, f)
            #cmd = 'RunScript(%s,%s)' % (service_py, '1')
            #xbmc.executebuiltin(cmd)
            common.SetScriptOnAlarm(f[:-3], service_py, duration=sti)
            sti = sti + 1

import xbmcaddon


PLUGIN='script.icechannel'
ADDON = xbmcaddon.Addon(id=PLUGIN)
