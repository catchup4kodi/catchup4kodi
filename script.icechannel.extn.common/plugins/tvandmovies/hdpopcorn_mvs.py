'''
    Duckpool
    http://hdpopcorns.com
    Copyright (C) 2017 DandyMedia

    version 0.1

'''

from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common
import xbmc


class hdpopcorn(MovieSource):
    implements = [MovieSource]
	
    name = "hdpopcorn"
    source_enabled_by_default = 'true'
    display_name = "HD Popcorn"
    base_url = 'http://hdpopcorns.com'
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    
    
    def GetFileHosts(self, url, list, lock, message_queue, RES):


        from md_request import open_url
        import re
        
        OPEN = open_url(url).content
        #print '>>>>>>>>>>>>>>>>>OPEN FUNC' + OPEN
        headers = {'Origin':'http://hdpopcorns.com', 'Referer':url,
        'X-Requested-With':'XMLHttpRequest', 'User-Agent':self.User_Agent}
        
        try:
            params = re.compile('FileName1080p.+?value="(.+?)".+?FileSize1080p.+?value="(.+?)".+?value="(.+?)"',re.DOTALL).findall(OPEN)
            for param1, param2,param3 in params:
                request_url = 'http://hdpopcorns.com/select-movie-quality/'
                form_data = {'FileName1080p':param1,'FileSize1080p':param2,'FSID1080p':param3}
            link = open_url(request_url, method='post', data=form_data, headers=headers,timeout=3).content
            final_url = re.compile('<strong>1080p</strong>.+?href="(.+?)"',re.DOTALL).findall(link)[0]
            res = '1080P'
        except:
            params = re.compile('FileName720p.+?value="(.+?)".+?FileSize720p".+?value="(.+?)".+?value="(.+?)"',re.DOTALL).findall(OPEN)
            for param1, param2,param3 in params:
                request_url = 'http://hdpopcorns.com/select-movie-quality/'
                form_data = {'FileName720p':param1,'FileSize720p':param2,'FSID720p':param3}
            link = open_url(request_url,method='post', data=form_data, headers=headers,timeout=3).content
            final_url = re.compile('<strong>720p</strong>.+?href="(.+?)"',re.DOTALL).findall(link)[0]
            res = '720P'
        
        final_url = final_url.replace('#038;','')
        HOST='DIRECTLINK'

        self.AddFileHost(list, res, final_url,host=HOST)




    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        from md_request import open_url
        import re
        
        headers={'User-Agent':self.User_Agent}

        name = self.CleanTextForSearch(name.lower())
        
        movie_url = '%s/search/%s' %(self.base_url,name.replace(' ','+'))
        link = open_url(movie_url,headers=headers,timeout=5).content

        try:
            links = re.compile('<header>.+?href="(.+?)" title="(.+?)"',re.DOTALL).findall(link)
            for m_url,m_title in links:
                #print 'MovieURL >>>   ' + m_url
                #print 'Title >>>   ' + m_title
                if name.lower() in self.CleanTextForSearch(m_title.lower()):
                    if year in m_title:
                        self.GetFileHosts(m_url, list, lock, message_queue, m_title)
        except:pass

