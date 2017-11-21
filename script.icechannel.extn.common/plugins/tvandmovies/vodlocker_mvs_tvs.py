'''
    DUCKPOOL Extension

    vodlockerAPI
    Copyright (C) 2017 DandyMedia

    version 0.1

'''

from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common




class vutlockerapi(MovieSource, TVShowSource):

    implements = [MovieSource, TVShowSource]
	
    name = 'vodlocker'
    display_name = 'Vodlocker'
    base_url = 'http://vodlocker.to'

    source_enabled_by_default = 'true'



    def GetFileHosts(self, url, list, lock, message_queue):

        from md_request import open_url
        from entertainment import googledocs
        import re,urlresolver
        #print 'XXXXXXXXXXXXXXXXXXXXXXXXXX'+url
        html = open_url(url).content
        sources = re.compile('onclick=\'show_player\(".+?", "(.+?)"',re.DOTALL).findall(html)
        for link in sources:
            if 'google'in link: 
                for res, final_url in googledocs.GLinks(link):
                    self.AddFileHost(list, res, final_url)
            else:
                if urlresolver.HostedMediaFile(link):
                    res = 'DVD'
                    self.AddFileHost(list, res, link)




    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        from md_request import open_url
        import re
        
        name = self.CleanTextForSearch(name.lower()).strip()
        if type == 'tv_episodes':
            search = '%s/embed?t=%s&season=%s&episode=%s' %(self.base_url,name.replace(' ','%20'),season,episode)
        else:
            search = '%s/embed?t=%s&y=%s' %(self.base_url,name.replace(' ','%20'),year)
        #print 'SEARCH:::::::::::'+search
        link = open_url(search, timeout=3).content
        

        try:
            movID =  re.compile('var id = "(.+?)"',re.DOTALL).findall(link)[0]
            if type == 'tv_episodes':
                item_url = '%s/embed/movieStreams/?id=%s&e=%s&cat=episode' %(self.base_url,movID,episode)
            else:
                item_url = '%s/embed/movieStreams/?id=%s' %(self.base_url,movID)
            self.GetFileHosts(item_url, list, lock, message_queue)

        except:pass
