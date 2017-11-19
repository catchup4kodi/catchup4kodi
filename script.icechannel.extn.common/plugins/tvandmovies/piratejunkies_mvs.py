'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common


class piratejunkies(MovieSource):
    implements = [MovieSource]
    
    name = "PirateJunkies"
    display_name = "Pirate Junkies"

    base_url = 'http://www.iframetv.com/javascript/movies.js' #'http://piratejunkies.com/javascript/movies.js'
    
    source_enabled_by_default = 'true'




    def GetFileHosts(self, url, list, lock, message_queue):

        from entertainment import googledocs
        import urlresolver,xbmc

        url = url.replace('drive.google.com', 'docs.google.com')

        if 'docs.google.com' in url:

            for res, final_url in googledocs.GLinks(url):
                self.AddFileHost(list, res, final_url)

        else:
            
            if urlresolver.HostedMediaFile(url):
                self.AddFileHost(list, '1080P',url)




    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        from md_request import open_url
        import re
        
        name = self.CleanTextForSearch(name.lower()).replace(' ','')

        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.3'}
        link = open_url(self.base_url, timeout=3).content
        match=re.compile('getElementById\("(.+?)"\).+?"play\(\'(.+?)\'').findall(link)

        for item_name, item_url in match:
            if name in self.CleanTextForSearch(item_name.lower()):
                self.GetFileHosts(item_url, list, lock, message_queue)                  
