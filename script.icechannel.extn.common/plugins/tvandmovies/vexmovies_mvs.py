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




class vexmovies(MovieSource):

    implements = [MovieSource]
	
    name = 'vexmovies'
    display_name = 'VexMovies'
    base_url = 'http://vexmovies.org'
    source_enabled_by_default = 'true'
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'


    def GetFileHosts(self, url, list, lock, message_queue):

        from md_request import open_url
        import re
        import HTMLParser
        clean_up = HTMLParser.HTMLParser()
        
        #print 'FILEPAGE>> '+url
        headers = {'User_Agent':self.User_Agent}
        html = open_url(url,headers=headers,verify=False,timeout=3).content
        #print html
        source = re.compile('<iframe src="(.+?)"',re.DOTALL).findall(html)[0]
        if 'consistent.stream' in source:
            #print 'grab stream '+ source
            headers = {'User_Agent':self.User_Agent}
            holder = open_url(source,headers=headers,verify=False,timeout=3).content
            page = re.compile(""":title=["'](.+?)["']\>""").findall(holder)[0]
            decode = clean_up.unescape(page)
            sources= re.compile('"sources.+?"(http.+?)"',re.DOTALL).findall(decode)
            for link in sources:
                link=link.replace('\\','')
                #print 'link chk '+ link
                if '1080' in link:
                    res='1080P'
                elif '720' in link:
                    res = '720P'
                else:
                    res = 'DVD'
                self.AddFileHost(list, res, link)
        else:
            if '1080' in link:
                res='1080p'
            elif '720' in link:
                res = '720p'
            else:
                res = 'DVD'
            self.AddFileHost(list, res, link)

    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        from md_request import open_url
        import re
        
        name = self.CleanTextForSearch(name.lower()).strip()

        search = '%s/?s=%s' %(self.base_url,name.replace(' ','+'))
        #print 'SEARCH:::::::::::'+search
        link = open_url(search, timeout=3).content

        try:
            match = re.compile('class="item".+?href="(.+?)".+?alt="(.+?)".+?class="year">(.+?)</span>',re.DOTALL).findall(link)
            for item_url,item_title,r_date in match:
                if name in self.CleanTextForSearch(item_title.lower()):
                    if year in r_date:
                        self.GetFileHosts(item_url, list, lock, message_queue)

        except:pass
