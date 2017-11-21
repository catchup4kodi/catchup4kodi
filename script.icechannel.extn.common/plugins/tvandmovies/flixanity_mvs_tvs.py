'''
    Flixanity   
    Copyright (C) 2017 Dandymedia
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common


class flixanity(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
    
    name = "Flixanity"
    display_name = "Flixanity"
    base_url = 'https://flixanity.cc'
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
   
    source_enabled_by_default = 'true'




    def GetFileHosts(self, url, list, lock, message_queue, type, content):

        from md_request import open_url
        import re,time,base64
        
        headers = {'Accept':'application/json, text/javascript, */*; q=0.01',
                   'Accept-Encoding':'gzip, deflate',
                   'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                   'Origin':self.base_url, 'Referer':self.base_url,
                   'User-Agent':self.User_Agent, 'X-Requested-With':'XMLHttpRequest'}
        content = open_url(url,headers=headers,verify=False,timeout=3).content
        TIME = time.time()- 3600
        TIME = str(TIME).split('.')[0]
        TIME = base64.b64encode(TIME,'strict')
        TIME = TIME.replace('==','%3D%3D')
        
        token = re.compile("var tok.+?'([^']*)'").findall(content)[0]        
        match = re.compile('elid.+?"([^"]*)"').findall(content)
        id = match[0]

        headers =  {'accept':'application/json, text/javascript, */*; q=0.01',
                    'accept-encoding':'gzip, deflate, br', 'accept-language':'en-US,en;q=0.8',
                    'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
                    'origin':self.base_url, 'referer':url, 'user-agent':self.User_Agent,
                    'x-requested-with':'XMLHttpRequest'}


        if type == 'tv_episodes':
            get='getEpisodeEmb'

        else:
            get='getMovieEmb'
            
        post_url = '%s/ajax/gonlflhyad.php' %self.base_url
        data={'action':get,'idEl':id,'token':token,'elid':TIME}
        content = open_url(post_url, method='post', data=data, headers=headers,verify=False,timeout=3).content

        r = '"type":"([^"]*)".*?iframe.*?src="([^"]*)"' #% option
        final_link = re.findall(r, content.replace('\\',''), re.I|re.DOTALL)

        for res, final_url in final_link:

            if '1080' in res:
                res='1080P'                   
            elif '720' in res:
                res='720P'
            elif  '480' in res:
                res='DVD'
            elif '360' in res:
                res='SD'
            else:
                res='720P'

            self.AddFileHost(list, res, final_url)
    
        
        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        from md_request import open_url
        import re

        name = self.CleanTextForSearch(name.lower()).strip()
        print 'xxxxxxxxxxx'+name
        headers = {'Origin':self.base_url, 'Referer':self.base_url,
                   'User-Agent':self.User_Agent, 'X-Requested-With':'XMLHttpRequest'}
        
        start_url = 'https://api.flixanity.cc/api/v1/0A6ru35yevokjaqbb3'
        form_data = {'q':name,'sl':'xxx'}
        
        content = open_url(start_url, method='post', data=form_data, headers=headers,verify=False,timeout=3).content
   
        try:
            Regex = re.compile('"title":"(.+?)","year":(.+?),"permalink":"(.+?)"',re.DOTALL).findall(content)
            for item_title,item_year,item_url in Regex:
                item_url = self.base_url + item_url
                                
                if name == self.CleanTextForSearch(item_title.lower()).strip():
                    if int(year) == int(item_year):
                        
                        if type == 'tv_episodes':
                            item_url = '%s/season/%s/episode/%s' %(item_url,season,episode)

                        self.GetFileHosts(item_url, list, lock, message_queue, type, content)
        except:pass
