'''
    DuckPool
    http://fullmovies24.net
    Copyright (C) 2017 DandyMedia

    version 0.1

'''

from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common
import xbmc





class fullmovies24(MovieSource):
    implements = [MovieSource]
	
    name = "fullmovies24"
    source_enabled_by_default = 'true'
    display_name = "fullmovies24"
    base_url = 'http://fullmovies24.net'
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    
    
    def GetFileHosts(self, url, list, lock, message_queue, RES):


        from md_request import open_url
        import re
        

        
        headers={'User-Agent':self.User_Agent}
        
        content = open_url(url,headers=headers).content

        final_url = re.compile('<iframe src="(.+?)"',re.DOTALL).findall(content)[0]
                
        HOST='DIRECTLINK'

        self.AddFileHost(list, '720P', final_url)




    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        from md_request import open_url
        import re
        
        headers={'User-Agent':self.User_Agent}

        name = self.CleanTextForSearch(name.lower())

        movie_url = '%s/?s=%s' %(self.base_url,name.replace(' ','+'))
        link = open_url(movie_url,headers=headers,timeout=5).content

        links = link.split('class="title"')[1]

        try:
            m_url = re.compile('href="(.+?)"',re.DOTALL).findall(links)[0]
            m_title = re.compile('title="(.+?)"',re.DOTALL).findall(links)[0]
            if name.lower() in self.CleanTextForSearch(m_title.lower()):
                if year in m_title:
                    self.GetFileHosts(m_url, list, lock, message_queue, m_title)

        except:pass

    # def Resolve(self, url):

   
        # #print url
        # from entertainment import duckpool
        # import requests

        # redirect= requests.head(url, allow_redirects=True).url
        
        # return duckpool.ResolveUrl(redirect)
        
    # def Resolve(self, url):                 
        # url=url.replace('amp;','')
        # if 'requiressl=yes' in url:
            # url = url.replace('http://', 'https://')
        # from entertainment import duckpool
        # resolved =duckpool.ResolveUrl(url)
        # return resolved 