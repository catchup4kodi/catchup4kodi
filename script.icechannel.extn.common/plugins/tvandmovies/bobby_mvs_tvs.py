'''
    Bobby  
    Copyright (C) 2013 Mikey1234
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
import xbmc



class bobby(MovieSource,TVShowSource):

    implements = [MovieSource,TVShowSource]
    
    name = "BobbyMovies"
    display_name = "Bobby Movies"

    source_enabled_by_default = 'true'
    base_url = 'http://bobby.kohimovie.com' #'https://bobby.kohimovie.com/jp/2.1.0/'



        
    def GetFileHosts(self, url, list, lock, message_queue,type,episode):

    
        import re,json
        from md_request import open_url



        headers={'Host':'bobby.kohimovie.com',
                'Accept':'*/*',
                'User-Agent':'BobbyMovie/3.1.4 (iPhone; iOS 10.1.1; Scale/2.00)',
                'Accept-Language':'en-GB;q=1',
                'Accept-Encoding':'gzip, deflate',
                'Connection':'keep-alive'}
        

        URL = 'https://bobby.kohimovie.com/jp/3.1.4/getDetail?alias=%s' %(url)
        
        link = open_url(URL,headers=headers,timeout=3).content
        data=json.loads(link)
        if type=='tv_episodes':
            data=data['data']['episodes']
            for field in data:
                id=field['alias']
                EPISODE=int(field['episode'])

                if int(episode)==EPISODE:  
                    THE_URL= 'https://bobby.kohimovie.com/jp/3.1.4/getMovieStream?serverId=&serialAlias=%s&episodeAlias=%s&episode=%s' %(url,id,episode)
                                        
                    THELINK = open_url(THE_URL,headers=headers,timeout=3).content
                    DATA=json.loads(THELINK)
                    DATA=DATA['data']
                    for field in DATA:
                        URL=field['streamUrl']
                        RES=str(field['quality'])
                
                        if '1080' in RES:
                            res='1080P'
                        elif '720' in RES:
                            res='720P'
                        elif '480' in RES:
                            res='DVD'                    
                        elif '360' in RES:
                            res='SD'
                        else:
                            res='DVD'
                        
                        FINAL_URL=URL.split('//')[1]
                        FINAL_URL=FINAL_URL.split('/')[0]
                        self.AddFileHost(list, res, URL,host=FINAL_URL.upper())   
                
        else:
            data=data['data']['servers']

            for field in data:
                id=field['serverId']
                TITLE=field['serverName']
                
                THE_URL= 'https://bobby.kohimovie.com/jp/3.1.4/getMovieBySource2?serialAlias=%s&serverId=%s' %(url,id)
                
                THELINK = open_url(THE_URL,headers=headers,timeout=3).content
                DATA=json.loads(THELINK)
                URL=DATA['data'][0]['streaming']
                RES=str(DATA['data'][0]['quality'])
            
            
                if '1080' in RES:
                    res='1080P'
                elif '720' in RES:
                    res='720P'
                elif '480' in RES:
                    res='DVD'                    
                elif '360' in RES:
                    res='SD'
                else:
                    res='DVD'
                
                FINAL_URL=URL.split('//')[1]
                FINAL_URL=FINAL_URL.split('/')[0]
                self.AddFileHost(list, res, URL,host=FINAL_URL.upper())                    

   
                    
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
    
        import re,json
        from md_request import open_url

        name = self.CleanTextForSearch(name.lower()).strip()
        
        headers={'Host':'bobby.kohimovie.com',
                'Accept':'*/*',
                'User-Agent':'BobbyMovie/3.1.4 (iPhone; iOS 10.1.1; Scale/2.00)',
                'Accept-Language':'en-GB;q=1',
                'Accept-Encoding':'gzip, deflate',
                'Connection':'keep-alive'}
        

        search = 'https://bobby.kohimovie.com/jp/3.1.4/search?q=%s&page=1' %(name.replace(' ','%20'))
        
        link = open_url(search,headers=headers,timeout=3).content
        data=json.loads(link)
        data=data['data']

        
        for field in data:
            id=field['alias']
            TITLE=field['name']
            YEAR=str(field['year'])
         
            if type=='tv_episodes':
                if name.lower() in self.CleanTextForSearch(TITLE.lower()):
                      if season in TITLE:
                          self.GetFileHosts(id, list, lock, message_queue,type,episode)
            else:
                if name == self.CleanTextForSearch(TITLE.lower()):
                    if YEAR == year:
                        self.GetFileHosts(id, list, lock, message_queue,type,episode)

