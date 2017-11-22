'''
    Cartoon HD    
    Copyright (C) 2013 Mikey1234
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common


class cartoonhd(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
    
    name = "Cartoon HD"
    display_name = "Cartoon HD"
    base_url = 'https://cartoonhd.life' #'https://cartoonhd.be' #'http://cartoonhd.website/'
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
   
    source_enabled_by_default = 'true'




    def GetFileHosts(self, url, list, lock, message_queue, type, content):

        from entertainment.net import Net
        net = Net(cached=False)
        
        import re,time,base64

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
                    'origin':self.base_url, 'referer':url, 'user-agent':self.User_Agent,'cookie':TIME,
                    'x-requested-with':'XMLHttpRequest'}


        if type == 'tv_episodes':
            get='getEpisodeEmb'

        else:
            get='getMovieEmb'
            
        THE_JS=self.base_url+'/templates/cartoonhd/assets/scripts/videojs-flixanity.js'
        GET_JS = net.http_GET(THE_JS,headers=headers).content

        EMBED=GET_JS.split(get)[1]
        EMBED=EMBED.split('ajax/')[1]
        EMBED=EMBED.split('.php')[0]
        
        post_url = '%s/ajax/%s.php' %(self.base_url,EMBED)
        data={'action':get,'idEl':id,'token':token,'elid':TIME}
        content = net.http_POST(post_url,form_data=data, headers=headers).content

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
            if not 'http' in final_url:
                final_url='http:'+final_url
            self.AddFileHost(list, res, final_url)
    
        
        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        from md_request import open_url
        import re

        name = self.CleanTextForSearch(name.lower()).strip()

        headers = {'Accept':'application/json, text/javascript, */*; q=0.01',
                   'Accept-Encoding':'gzip, deflate',
                   'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                   'Origin':self.base_url, 'Referer':self.base_url,
                   'User-Agent':self.User_Agent, 'X-Requested-With':'XMLHttpRequest'}

        if type == 'tv_episodes':

            item_url = '%s/show/%s' %(self.base_url,name.replace(' ','-'))
            content = open_url(item_url,headers=headers,verify=False,timeout=3).content
        
            if 'OOPS, ' in content:

                item_url = '%s/show/%s-%s' %(self.base_url,name.replace(' ','-'),year)
                content = open_url(item_url,headers=headers,verify=False,timeout=3).content

        else:

            item_url = '%s/full-movie/%s' %(self.base_url,name.replace(' ','-'))

            content = open_url(item_url,headers=headers,verify=False,timeout=3).content
        
            if 'OOPS, ' in content:
                item_url = '%s/full-movie/%s-%s' %(self.base_url,name.replace(' ','-'),year)
                content = open_url(item_url,headers=headers,verify=False,timeout=3).content

        try:
            item_title = re.compile('<h2><b><a href=.+?>([^<>]*)</').findall(content)[0]
        except:
            item_title = re.compile('<h2><a href=.*?title="([^"]*)"').findall(content)[0]

        item_year = re.compile('class="dat">([^<>]*)</').findall(content)[0]

        if name == self.CleanTextForSearch(item_title.lower()).strip():
            if int(year) == int(item_year):
                if type == 'tv_episodes':
                    item_url = '%s/season/%s/episode/%s' %(item_url,season,episode)
                    content = open_url(item_url,headers=headers,verify=False,timeout=3).content

                referer = re.compile('"canonical" content="([^"]*)"').findall(content)[0]
                self.GetFileHosts(referer, list, lock, message_queue, type, content)


