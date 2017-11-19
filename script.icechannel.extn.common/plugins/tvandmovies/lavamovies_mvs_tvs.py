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
    HEADERS={'Host':'lavamovies.com',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}



    source_enabled_by_default = 'true'
    BASE ='http://lavamovies.com'


    

        
    def GetFileHosts(self, url, list, lock, message_queue,type,season,episode):

        REF=url
        GetEmbeds = 'http://lavamovies.com/UI/GetEmbeds'
        
        if not type == 'tv_episodes':
            episode_is='false'
        else:
            episode_is='true'
            
  
        import json,re
        from entertainment.net import Net
        net = Net(cached=False)

        link = net.http_GET(url,headers=self.HEADERS).content
        
        UNIQUE_ID=re.compile('<a href="/download/(.+?)"').findall(link)[0]
        match=re.compile('getEmbeds\((.+?)\)').findall(link)[0]
        if ',' in match:
            match=match.split(',')[0]
        data={'id':match,
             'episode':episode_is}

       
        link = json.loads(net.http_POST(GetEmbeds,data,headers=self.HEADERS).content)

         
        data=link['content']

        for field in data:
            hashed=field['hash']
            server=field['server']
            LINKURL = 'http://lavacdn.xyz/stream/' +hashed
            
            S_HEADERS ={'Host':'lavacdn.xyz',
                        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                        'Referer':'%s'%LINKURL,
                        'Accept-Encoding':'gzip, deflate',
                        'Accept-Language':'en-US,en;q=0.8'}

            
            LINKURL_GET = net.http_GET(LINKURL,headers=S_HEADERS).content
            if 'script src=' in LINKURL_GET:
                if '"playlist": [' in LINKURL_GET:
                    self.GRABIT_2(list, LINKURL_GET, UNIQUE_ID,LINKURL)
                else:    
                    self.GRABIT(list, LINKURL_GET, UNIQUE_ID,LINKURL)
                
            else:
                try:
                    FINAL=re.compile("<iframe src='(.+?)'").findall(LINKURL_GET)[0]
                    self.AddFileHost(list, 'DVD', FINAL)
                except:pass



    def GRABIT(self,list, LINKURL_GET, UNIQUE_ID,REF):
        import re,json
        from entertainment.net import Net
        net = Net(cached=False)
        LINK=LINKURL_GET.split('script src')[1]
        XY   =   re.compile("<script>_x='(.+?)', _y='(.+?)';</script>").findall(LINKURL_GET)
        _y   =   XY[0][1]
        _x   =   XY[0][0]

        eid  =   re.compile("eid: (.+?),").findall(LINKURL_GET)[0]
        hashed  =   re.compile("hash: '(.+?)'").findall(LINKURL_GET)[0]   
        unique_id  =   re.compile("unique_id: '(.+?)'").findall(LINKURL_GET)[0]

        
        data={'y': _y,
              'x': _x,
              'eid': eid,
              'hash': hashed,
              'unique_id': unique_id}
            
        S_HEADERS ={'Host':'lavacdn.xyz',
                    'Origin':'http://lavacdn.xyz',
                    'X-Requested-With':'XMLHttpRequest',
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                    'Accept':'application/json, text/javascript, */*; q=0.01',
                    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                    'Referer':'%s'%REF,
                    'Accept-Encoding':'gzip, deflate',
                    'Accept-Language':'en-US,en;q=0.8'}
        
        GETLINK='http://lavacdn.xyz/movie_sources.php'
        
        link = json.loads(net.http_POST(GETLINK,data,headers=S_HEADERS).content)
        data= link['playlist']
        for field in data:
            try:
                FINAL = field['sources']['file']
                
                self.AddFileHost(list, '720P', FINAL)
            except:
            
                GET_ANOTHER = 'http://lavacdn.xyz/get_another.php'
                
                data={'unique_id': unique_id,
                    'current_hash': hashed}
                
                link = json.loads(net.http_POST(GET_ANOTHER,data,headers=S_HEADERS).content)
                data= link['hash']
                FINAL = 'http://lavacdn.xyz/stream/%s/backup' % data
                self.AddFileHost(list, '720P', FINAL)

    def GRABIT_2(self,list, LINKURL_GET, UNIQUE_ID,REF):
        import re,json
        from entertainment.net import Net
        net = Net(cached=False)

        hashed  =   re.compile("current_hash: '(.+?)'").findall(LINKURL_GET)[0]   
        unique_id  =   re.compile("unique_id: '(.+?)'").findall(LINKURL_GET)[0]


            
        S_HEADERS ={'Host':'lavacdn.xyz',
                    'Origin':'http://lavacdn.xyz',
                    'X-Requested-With':'XMLHttpRequest',
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                    'Accept':'application/json, text/javascript, */*; q=0.01',
                    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                    'Referer':'%s'%REF,
                    'Accept-Encoding':'gzip, deflate',
                    'Accept-Language':'en-US,en;q=0.8'}
        

        link=json.loads('{"sources"'+re.compile('"sources"(.+?)}').findall(LINKURL_GET)[0]+'}]}')
       
        
        data= link['sources']
        for field in data:

                FINAL = field['file']
                
                self.AddFileHost(list, '720P', FINAL)

    
        GET_ANOTHER = 'http://lavacdn.xyz/get_another.php'
        
        data={'unique_id': unique_id,
            'current_hash': hashed}
        
        link = json.loads(net.http_POST(GET_ANOTHER,data,headers=S_HEADERS).content)
        if link['status']==1:
            data= link['hash']
            FINAL = 'http://lavacdn.xyz/stream/%s/backup' % data
            self.AddFileHost(list, '720P', FINAL)
                    
        
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









            
