'''
    DUCKPOOL Extension

    freedownlaod
    Copyright (C) 2017 DandyMedia

    version 0.1

'''

from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common




class freedownload(MovieSource):

    implements = [MovieSource]
	
    name = 'freedownload'
    display_name = 'freedownload'
    base_url = 'http://freemoviedownloads6.com'

    source_enabled_by_default = 'true'



    def GetFileHosts(self, url, list, lock, message_queue):

        from md_request import open_url
        import re
        #print 'XXXXXXXXXXXXXXXXXXXXXXXXXX'+url
        OPEN = open_url(url).content
        Regex = re.compile('href="(.+?)"',re.DOTALL).findall(OPEN)
        for link in Regex:
            if '.mkv' in link:
                if '1080' in link:
                    res = '1080P'
                elif '720' in link:
                    res = '720P'
                else:
                    res = 'SD' 
             
                self.AddFileHost(list, res, link)




    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        from md_request import open_url
        import re
        
        name = self.CleanTextForSearch(name.lower()).strip()

        search = '%s/?s=%s' %(self.base_url,name.replace(' ','+'))
        #print 'SEARCH:::::::::::'+search
        link = open_url(search, timeout=3).content
        #links = link.split('<h2 class="title"')

        try:
            match = re.compile('<h2 class="title".+?href="(.+?)".+?title="(.+?)"',re.DOTALL).findall(link)
            for item_url,item_title in match:
                if name in self.CleanTextForSearch(item_title.lower()):
                    if year in item_url:
                        self.GetFileHosts(item_url, list, lock, message_queue)

        except:pass
