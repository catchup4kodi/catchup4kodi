'''
    Duckool
    321movies.cc
    Copyright (C) 2017 DandyMedia

    version 0.1

'''


from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common
import xbmc





class movie321cc(MovieSource):
    implements = [MovieSource]
	
    name = "movie321cc"
    source_enabled_by_default = 'false'
    display_name = "Movie321cc"
    base_url = 'https://321movies.cc'
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    
    
    def GetFileHosts(self, url, list, lock, message_queue, RES):


        from md_request import open_url
        import urlresolver,re
        headers={'User-Agent':self.User_Agent}
        content = open_url(url,headers=headers).content
        links  = re.compile('</iframe>.+?class="metaframe rptss" src="(.+?)"',re.DOTALL).findall(content)
        for url in links:
            if urlresolver.HostedMediaFile(url):
                self.AddFileHost(list, '720P', url)
        




    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        from md_request import open_url
        import re
        
        headers={'User-Agent':self.User_Agent}

        name = self.CleanTextForSearch(name.lower())

        movie_url = '%s/?s=%s' %(self.base_url,name.replace(' ','+'))
        link = open_url(movie_url,headers=headers,timeout=10).content
        
        links = link.split('result-item')

        for p in links:
            try:
                m_url = re.compile('href="([^"]+)"').findall(p)[0]
                m_title = re.compile('alt="([^"]+)"').findall(p)[0]
                m_year = re.compile('class="year">(.+?)</span>').findall(p)[0]
                #print 'm_url >' + m_url
                #print 'm_title >' + m_title
                #print 'm_year >' + m_year
                if name.lower() in self.CleanTextForSearch(m_title.lower()):
                    if year in m_year:
                        self.GetFileHosts(m_url, list, lock, message_queue, m_title)
            except:pass

    def Resolve(self, url):

        import urlresolver
        play_url = urlresolver.resolve(url)
        return play_url