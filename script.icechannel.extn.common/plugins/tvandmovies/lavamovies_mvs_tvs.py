'''
    Cartoon HD Extra   
    Copyright (C) 2013 Mikey1234
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin



class lavamovies(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
    
    name = "LavaMovies"
    display_name = "LavaMovies"
    GETLINK='http://wowcartoon.com:8182/C4C/api/C4C/GetGenreDetail'
    HEADERS={'Host':'lavamovies.se',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}



    source_enabled_by_default = 'true'
    BASE ='http://lavamovies.se'


    

        
    def GetFileHosts(self, url, list, lock, message_queue,type,season,episode):

        REF=url
        GetEmbeds = 'http://lavamovies.se/UI/GetEmbeds'
        
        if not type == 'tv_episodes':
            episode_is='false'
        else:
            episode_is='true'
            
  
        import json,re
        from entertainment.net import Net
        net = Net(cached=False)

        link = net.http_GET(url,headers=self.HEADERS).content
        
        #UNIQUE_ID=re.compile('<a href="/download/(.+?)"').findall(link)[0]
        match=re.compile('var movie_id = (.+?);').findall(link)[0]
        if ',' in match:
            match=match.split(',')[0]
        data={'id':match,
             'episode':episode_is}

       
        link = net.http_POST(GetEmbeds,data,headers=self.HEADERS).content
        match=re.compile('"hash":"(.+?)"').findall(link)

        for hashed in  match:
            try:
                GETURL='http://lavamovies.se/ajax/get_sources.php?hash='+hashed
                LINKED = json.loads(net.http_GET(GETURL,headers=self.HEADERS).content)
                DATA = LINKED['response']
                if DATA['direct']<1:
                    FINAL = DATA['sources']
                    self.AddFileHost(list, 'HD', FINAL)
                else:
                    try:
                        final_url=DATA['sources']['playlist'][0]['sources']['file']
                        try:
                            res=DATA['sources']['playlist'][0]['sources']['label']
                        except: res='720'    
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
                    except:    
                        DATA=DATA['sources']['playlist'][0]['sources']
                        for field in DATA:
                            res=field['label']
                            final_url = field['file']
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
            except:pass


                    
        
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
    
        import json,re
        from entertainment.net import Net
        net = Net(cached=False)

        if len(episode)< 2:
            episode = '0'+episode
        if len(season)< 2:
            season = '0'+season


        name=self.CleanTextForSearch(name)
        data={'keyword':name}
        
        SEARCHLINK = self.BASE+'/UI/SuggestSearch'
        link = json.loads(net.http_POST(SEARCHLINK,data,headers=self.HEADERS).content)
     
        data=link['content'].replace('\r','').replace('\n','').replace('\t','')
        if type == 'tv_episodes':
            passtype='/tv-series'
        else:
            passtype='/movie'

        r = '<a href="(%s.+?)" class="ss-title">(.+?)</a><p>(.+?)</p>'   % passtype
        match= re.compile(r,re.DOTALL).findall(data)
        for URL , TITLE ,YEAR in match:
            THE_URL =self.BASE+URL
            if type == 'tv_episodes':
                if name.lower() in self.CleanTextForSearch(TITLE.lower()):
                    self.GetFileHosts(THE_URL+'/s%se%s' % (season,episode), list, lock, message_queue,type,season,episode)                
            else:    
                if name.lower() in self.CleanTextForSearch(TITLE.lower()):
                    if year in YEAR:
                        self.GetFileHosts(THE_URL, list, lock, message_queue,type,season,episode)

     



    def Resolve(self, url):

        if 'google' in url:
            return url
        elif 'blogspot' in url:
            return url
        elif 'lavacdn.xyz' in url:
            import re
            from entertainment.net import Net
            net = Net(cached=False)
            HEADERS ={'Host':'lavacdn.xyz',
                        'Origin':'http://lavacdn.xyz',
                        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                        'Accept-Encoding':'gzip, deflate',
                        'Accept-Language':'en-US,en;q=0.8'}
            
            LINK = net.http_GET(url,headers=HEADERS).content
            return re.compile('"file":"(.+?)"').findall(LINK)[0].replace('\\','')
        else:
            from entertainment import duckpool
            return duckpool.ResolveUrl(url)









            
