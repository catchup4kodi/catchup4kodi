'''
    ICE CHANNEL
    buzzfilms.co
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common
import os



class gomoviesalt(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
    
    name = "GoMovies 2"
    display_name = "GoMovies 2"
    #base_url = 'https://123movies.is'

    UA ='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    
    profile_path = common.profile_path
    cookie_file = os.path.join(profile_path, 'cookies', 'gomoviesNEW.cookies')

    source_enabled_by_default = 'true'



    

    def GetFileHosts(self, url, list, lock, message_queue, season, episode,type,year,query,base_url,s):

        THEHOST=url.split('//')[1]
        THEHOST=THEHOST.split('/')[0]

        REF=url

        from entertainment import requests
        requests.packages.urllib3.disable_warnings()
        
        import re,json
       
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36','Referer':base_url + ''}
        
      
        LINK = s.get(url,headers=headers,verify=False).content
        STREAM =re.compile('<iframe src="(.+?)"',re.DOTALL).findall(LINK)[0]
        STREAMLINK = s.get(STREAM,headers=headers,verify=False).content
        OPEN =re.compile("locationPath = '(.+?)'",re.DOTALL).findall(STREAMLINK)[0]
       
        GETOPEN = s.get(OPEN,headers=headers,verify=False).content
        OPENLOAD=re.compile(';" src="(.+?)"',re.DOTALL).findall(GETOPEN)[0]
        self.AddFileHost(list, '720P', OPENLOAD)

        
        headers={'referer':url,'origin':'https://putstream.com'}
        POST_URL= 'https://putstream.com/external-google-grab'
        TYPE =re.compile("'type': '(.+?)'",re.DOTALL).findall(STREAMLINK)[0]
        imd_id =re.compile("'imd_id': '(.+?)'",re.DOTALL).findall(STREAMLINK)[0]
        GTOKEN = re.compile('_token": "(.+?)"',re.DOTALL).findall(STREAMLINK)[0]
        data={'type': TYPE,
              "imd_id": imd_id,
              "_token":GTOKEN}
        HTML = s.post(POST_URL,data,headers=headers,verify=False).content
        LINK = json.loads(HTML)
        if 'success' in HTML:
            DATA=LINK['links'][0]

            for field in DATA:
                FINAL_URL= field['file']
                RES= field['label']
                if ' ' in RES:
                    RES = RES.split(' ')[0]
                self.ADDIT(list,FINAL_URL,RES)



    def GetTVFileHosts(self, url, list, lock, message_queue, season, episode,type,year,query,base_url,s):

        THEHOST=url.split('//')[1]
        THEHOST=THEHOST.split('/')[0]

        REF=url

        from entertainment import requests
        requests.packages.urllib3.disable_warnings()
        
        import re,json
        season_pull = "0%s"%season if len(season)<2 else season
        episode_pull = "0%s"%episode if len(episode)<2 else episode
       
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36','Referer':base_url + ''}
        
        PASS='%sx%s' % (season,episode)
        
        LINK = s.get(url,headers=headers,verify=False).content
        getfinal=re.compile('<a href="(.+?)"').findall(LINK)
        for ep in getfinal:
            if PASS in ep and '?watching=' in ep:
                STREAM =re.compile('<iframe src="(.+?)"',re.DOTALL).findall(LINK)[0]
                STREAMLINK = s.get(STREAM,headers=headers,verify=False).content
                OPEN =re.compile("locationPath = '(.+?)'",re.DOTALL).findall(STREAMLINK)[0]
               
                GETOPEN = s.get(OPEN,headers=headers,verify=False).content
                OPENLOAD=re.compile(';" src="(.+?)"',re.DOTALL).findall(GETOPEN)[0]
                self.AddFileHost(list, '720P', OPENLOAD)

                
                headers={'referer':url,'origin':'https://putstream.com'}
                POST_URL= 'https://putstream.com/external-google-grab'
                TYPE =re.compile("'type': '(.+?)'",re.DOTALL).findall(STREAMLINK)[0]
                imd_id =re.compile("'imd_id': '(.+?)'",re.DOTALL).findall(STREAMLINK)[0]
                GTOKEN = re.compile('_token": "(.+?)"',re.DOTALL).findall(STREAMLINK)[0]
                data={'type': TYPE,
                      "imd_id": imd_id,
                      "_token":GTOKEN,
                      'seasonsNo': season_pull,
                      'episodesNo': episode_pull}
                HTML = s.post(POST_URL,data,headers=headers,verify=False).content
                LINK = json.loads(HTML)
                if 'success' in HTML:
                    DATA=LINK['links'][0]

                    for field in DATA:
                        FINAL_URL= field['file']
                        RES= field['label']
                        if ' ' in RES:
                            RES = RES.split(' ')[0]
                        self.ADDIT(list,FINAL_URL,RES)
                        

                            
    def ADDIT(self,list,FINAL_URL,res): 
        if not FINAL_URL.endswith('.srt'):
            res=res.replace('p','').replace('P','').replace('CAM','360')
            if not res.isdigit():
                res='720'
            #print res
            #res=int(res)
            #print res
            if res =='360':
                res='SD'
            if res =='480':
                res='DVD'
            if res =='720':
                res='720P'
            if res =='1080':
                res='1080P'
              

            HOST=FINAL_URL.split('//')[1]
            HOST=HOST.split('/')[0]  
            

            

            self.AddFileHost(list, res, FINAL_URL,host=HOST.upper())



            
    def GetDomain(self):                 
        
        return 'https://gomovies.co/' 

            
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):  
    
        from entertainment import requests
        requests.packages.urllib3.disable_warnings()

        import re

        base_url = self.GetDomain()
        s = requests.session()
        title = self.CleanTextForSearch(title) 
        query = self.CleanTextForSearch(name)
        #print ':::::::::::::::::::::::::::::::::'
        
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36','Referer':base_url}
                
        search=base_url + 'search?s=' + str(query.lower()).replace(' ','+')


        #net.set_cookies(self.cookie_file)
        html=s.get(search,headers=headers,verify=False).content

        match=re.compile('<div class="tiptitle"><h4>(.+?)</h4>.+?"jt-info">(.+?)</div>.+?<div class="jtip-bottom".+?href="(.+?)" class="btn btn-block btn-successful"',re.DOTALL).findall(html)

        for title , YEAR , url in match:
            if query.lower() in self.CleanTextForSearch(title.lower()):
                link = s.get(url,headers=headers,verify=False).content
                TOKEN =re.compile('href="(.+?)"',re.DOTALL).findall(link)
                for movie_url in TOKEN:
                    if '?watching=' in movie_url:
          
                       if type == 'tv_episodes':
                           self.GetTVFileHosts(movie_url, list, lock, message_queue,season, episode,type,year,query,base_url,s)
                                
                       else:
                           if year in YEAR:
                               self.GetFileHosts(movie_url, list, lock, message_queue,season, episode,type,year,query,base_url,s)

            

                    
            



                
                
