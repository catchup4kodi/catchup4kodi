'''
    directdownload    
    Copyright (C) 2013 Coolwave
'''

from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common
import re
#import xbmc,os
# datapath = xbmc.translatePath(os.path.join('special://home/userdata/addon_data','script.icechannel'))
# cookie_path = os.path.join(datapath, 'cookies')

# do_no_cache_keywords_list = ["alert('Please Login!');"]

class directdownload(TVShowSource,CustomSettings):
    implements = [TVShowSource,CustomSettings]
    
    name = "directdownload"
    display_name = "Direct Download"
    base_url = 'https://directdownload.tv/'
    source_enabled_by_default = 'false'
    # cookie_file = os.path.join(common.cookies_path, 'DDlogin.cookie')
    
    # def __init__(self):
        # xml = '<settings>\n'
        # xml += '<category label="Account">\n'
        # xml += '<setting id="tv_user" type="text" label="Username" default="xunity" />\n'
        # xml += '<setting id="tv_pwd" type="text" option="hidden" label="Password" default="xunity" />'
        # xml += '</category>\n' 
        # xml += '</settings>\n'
        # self.CreateSettings(self.name, self.display_name, xml)

    
    def GetFileHosts(self, url, list, lock, message_queue): 
        
        import re,urlresolver
        from md_request import open_url

        content = open_url(url, timeout=5).content
        links=re.compile('"http(.+?)"',re.DOTALL).findall(content)
        for url in links:
            url = 'http' + url.replace('\/', '/')
            if '720p' in url:
                res = '720P'
            elif '1080p' in url:
                res = '1080P'  
            else:
                res='480P'
            if urlresolver.HostedMediaFile(url).valid_url():
                if 'k2s.cc' not in url:
                    if 'oboom.com' not in url:                
                        self.AddFileHost(list, res, url)
            
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        name = self.CleanTextForSearch(name) 
        season = self.CleanTextForSearch(season) 
        episode = self.CleanTextForSearch(episode)
        
        season_pull = "0%s"%season if len(season)<2 else season
        episode_pull = "0%s"%episode if len(episode)<2 else episode

        search_term = name
        #match=re.compile('{"release":"([^"]+?)","when":.+?,"size":".+?","links":(.+?),"idtvs".+?"quality":"([^"]+?)".+?}').findall(html)
        
        searchUrl='https://directdownload.tv/api?key=4B0BB862F24C8A29&qualities/disk-480p,disk-1080p-x265,tv-480p,tv-720p,web-480p,web-720p,web-1080p,web-1080p-x265,movie-480p-x265,movie-1080p-x265&limit=50&keyword=%s+s%se%s' %(name.lower(),season_pull,episode_pull)        
        searchUrl = searchUrl.replace(' ','%20')

        self.GetFileHosts(searchUrl, list, lock, message_queue)

        
