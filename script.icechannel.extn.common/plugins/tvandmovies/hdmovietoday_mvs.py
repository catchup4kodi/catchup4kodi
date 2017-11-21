'''
    DuckPool
    http://hdmovie7.today
    Copyright (C) 2017 DandyMedia

    version 0.1

'''

from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common
import xbmc





class hdmovietoday(MovieSource):
    implements = [MovieSource]
	
    name = "hdmovietoday"
    source_enabled_by_default = 'true'
    display_name = "HDMovieToday"
    base_url = 'http://duckfilm.net'
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    
    
    def GetFileHosts(self, url, list, lock, message_queue, RES):


        from md_request import open_url
        import re

        
        content = open_url(url, timeout=3).content
        refx='|User-Agent=Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36&Referer='+url
        holderpage = re.compile('<div class="fiml-img".+?href="(.+?)"').findall(content)[0]
        links = open_url(holderpage, timeout=3).content
        data = re.compile('"file":"(.+?)".+?"label":"(.+?)"').findall(links)

        for final_url,res in data:

            if '1080' in res:
                res='1080P'                   
            elif '720' in res:
                res='720P'
            elif  '480' in res:
                res='DVD'
            elif '360' in res:
                res='SD'
            else:
                res='DVD'
            final_url= url+refx
            HOST='DIRECTLINK'
            self.AddFileHost(list, res, final_url,host=HOST)




    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        from md_request import open_url
        import re
        
        headers={'User-Agent':self.User_Agent}

        name = self.CleanTextForSearch(name.lower())

        movie_url = '%s/search/%s' %(self.base_url,name.replace(' ','+'))
        #print 'searchurl' + movie_url
        link = open_url(movie_url,headers=headers,timeout=3).content
        
        links = re.compile('<p class="title"><a href="(.+?)" title=(.+?)</p>',re.DOTALL).findall(link)
        try:
            for m_url,m_title in links:
                if name.lower() in self.CleanTextForSearch(m_title.lower()):
                    if year in m_title:
                        self.GetFileHosts(m_url, list, lock, message_queue, m_title)

        except:pass

