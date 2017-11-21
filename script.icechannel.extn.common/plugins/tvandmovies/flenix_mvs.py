'''
    Duckpool
    flenix.net
    Copyright (C) 2017 DandyMedia

    version 0.1

'''

from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common
from entertainment import requests
import xbmc
requests.packages.urllib3.disable_warnings()
s = requests.session()




class flenix(MovieSource):
    implements = [MovieSource]
	
    name = "flenix"
    source_enabled_by_default = 'true'
    display_name = "Flenix - GW"
    base_url = 'https://flenix.net'
    search_url = 'https://www.google.co.uk'
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    
    
    def GetFileHosts(self, url, list, lock, message_queue, RES):


        from entertainment import requests
        import re
        
        ID = url.split('movies/')[1].split('-')[0]
        headers = {'User-Agent': self.User_Agent}
        page_url= 'https://flenix.net/movies/%s/watch/'%ID
        page = s.get(page_url,headers=headers) 
        req_url = 'https://flenix.net/?do=player_ajax&id=%s&xfn=player2' %ID


        end_url = s.get(req_url, headers=headers).content
        #print 'end > '+ end_url
        final_url = end_url
        HOST='DIRECTLINK'

        self.AddFileHost(list, '720P', final_url,host=HOST)




    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        from entertainment import requests
        import re
        
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'}
        
        scrape = self.CleanTextForSearch(name.lower()).replace(' ','+')
        start_url = '%s/search?q=flenix.net+%s+%s' %(self.search_url,scrape,year)
        #print 'GWWW'+start_url
        html = requests.get(start_url,headers=headers).content
        #print html
        results = re.compile('href="(.+?)"',re.DOTALL).findall(html)
        for m_url in results:
            #print m_url    
            try:
                if self.base_url in m_url:
                    if scrape.replace('+','-') in m_url:
                        self.GetFileHosts(m_url, list, lock, message_queue, name)
            except:
                pass

    def open_url(self, url, params=None, headers=''):
        
        if not headers:
            headers={'User-Agent':self.User_Agent,'Referer':self.base_url}

        link = s.get(url, params=params, headers=headers, verify=False, timeout=3)
        return link
