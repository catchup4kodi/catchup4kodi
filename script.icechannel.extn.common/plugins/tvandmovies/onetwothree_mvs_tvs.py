'''
    Ice Channel
    onetwothree
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common
import os,xbmc



class onetwothree(MovieSource,TVShowSource):

    implements = [MovieSource,TVShowSource]
    
    name = "123Movies"
    display_name = "123Movies"
    base_url = 'http://123moviesfree.ac'
    User_Agent ='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    
    source_enabled_by_default = 'true'




    def googletag(self,url):
        import re
        quality = re.compile('itag=(\d*)').findall(url)
        quality += re.compile('=m(\d*)$').findall(url)
        try: quality = quality[0]
        except: return []

        if quality in ['37', '137', '299', '96', '248', '303', '46']:
            return [{'quality': '1080P', 'url': url}]
        elif quality in ['22', '84', '136', '298', '120', '95', '247', '302', '45', '102']:
            return [{'quality': '720P', 'url': url}]
        elif quality in ['35', '44', '135', '244', '94']:
            return [{'quality': 'SD', 'url': url}]
        elif quality in ['18', '34', '43', '82', '100', '101', '134', '243', '93']:
            return [{'quality': 'SD', 'url': url}]
        elif quality in ['5', '6', '36', '83', '133', '242', '92', '132']:
            return [{'quality': 'SD', 'url': url}]
        else:
            return []


                    
    def GetFileHosts(self, url, list,episode,type):


        REF=url
        from md_request import open_url

        import urllib,urlresolver,re

        headers={'User-Agent':self.User_Agent,'Referer':REF}

        link = open_url(url,headers=headers,timeout=3).content

        headers={'Accept':'*/*',
                'Origin':self.base_url,
                'X-Requested-With':'XMLHttpRequest',
                'User-Agent':self.User_Agent,
                'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                'Referer':REF,
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'en-US,en;q=0.8'}

        uniques=[]
        if type == 'tv_episodes':
            match=re.compile('<a class="episode_(.+?) .+?" href="(.+?)".+?data-film="(.+?)".+?data-name="(.+?)"',re.DOTALL).findall(link)
            
            for EP,ip_server , ip_film ,ip_name in match:

                if episode == EP:
                    if ip_server not in uniques:
                        uniques.append(ip_server) 
                        REF=ip_server

                        link = open_url(ip_server,headers=headers,timeout=3).content
                  
                        headers={'Accept':'*/*',
                                'Origin':self.base_url,
                                'X-Requested-With':'XMLHttpRequest',
                                'User-Agent':self.User_Agent,
                                'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                                'Referer':REF,
                                'Accept-Encoding':'gzip, deflate',
                                'Accept-Language':'en-US,en;q=0.8'}
                        
                        match = re.compile('ip_build_player\((.+?),(.+?),(.+?),(.+?)\)',re.DOTALL).findall(link)

                        for ip_film ,ip_server  ,ip_name , fix in match:
                            ip_name = ip_name.replace("'",'')
                            ip_server = ip_server.replace("'",'')

                            data = {'postid':'server', 'phimid':ip_film, 'keyurl':ip_name}
                            server_url = '%s/index.php' %self.base_url
                            server = open_url(server_url, method='post', data=data, headers=headers, timeout=3).content
                            match = re.findall(r'data-server="([^"]+)"', server, re.I|re.DOTALL)
                            for ip_server in match:

                                data={'ipplugins':'1',
                                    'ip_film':ip_film,
                                    'ip_server':ip_server,
                                    'ip_name':ip_name,
                                    'fix':fix}

                                post_url = '%s/ip.file/swf/plugins/ipplugins.php'%self.base_url

                                links = open_url(post_url,method='post',data=data,headers=headers,timeout=3).json()

                                params = {'u':links['s'], 'w':'100', 'h':'500', 's':ip_server, 'n':'0'}
                                request_url = '%s/ip.file/swf/ipplayer/ipplayer.php' %self.base_url

                                final_link = open_url(request_url,params=params,headers=headers,timeout=3).json()

                                data = final_link['data']

                                if 'youtube' in str(data):

                                    vid_id = data.split('=')[1].split('&type')[0]
                                    request_url2 = 'https://docs.google.com/get_video_info?docid=%s&eurl=%s' %(vid_id,REF)
                                    final_links = open_url(request_url2, verify=False, timeout=3)
                                    match = re.findall(r'itag\%3D.*?%26url\%3D(.*?)%253B', final_links.content, re.I|re.DOTALL)
                                    for url in match:
                                        url = urllib.unquote(url)
                                        url = urllib.unquote(url)
                                        if 'video/x-flv' in url:
                                                url = url.partition('url=')[2]

                                        for a in self.googletag(url):
                                            cookie = final_links.cookies.get_dict()
                                            cookie = urllib.quote('Cookie:DRIVE_STREAM=%s; NID=%s' %(cookie['DRIVE_STREAM'],cookie['NID']))
                                            g_url = a['url'] + '|' + cookie
                                            self.AddFileHost(list, a['quality'], g_url)

                                elif 'google' in str(data):

                                    uniques = []

                                    for field in data:
                                        final_url = field['files']
                                        res = field['quality']

                                        if '.srt' not in final_url:
                                            if '1080' in res:
                                                res='1080P'                   
                                            elif '720' in res:
                                                res='720P'
                                            elif  '480' in res:
                                                res='DVD'
                                            elif '360' in res:
                                                res='SD'
                                            else:
                                                res='DVD'

                                            if final_url not in uniques:
                                                uniques.append(final_url)
                                                self.AddFileHost(list, res, final_url)


                    
        else:

            match = re.compile('ip_build_player\((.+?),(.+?),(.+?),(.+?)\)',re.DOTALL).findall(link)

            for ip_film ,ip_server  ,ip_name , fix in match:
                ip_name = ip_name.replace("'",'')
                ip_server = ip_server.replace("'",'')

                data = {'postid':'server', 'phimid':ip_film, 'keyurl':ip_name}
                server_url = '%s/index.php' %self.base_url
                server = open_url(server_url, method='post', data=data, headers=headers, timeout=3).content
                match = re.findall(r'data-server="([^"]+)"', server, re.I|re.DOTALL)
                for ip_server in match:

                    data={'ipplugins':'1',
                        'ip_film':ip_film,
                        'ip_server':ip_server,
                        'ip_name':ip_name,
                        'fix':fix}

                    post_url = '%s/ip.file/swf/plugins/ipplugins.php'%self.base_url

                    links = open_url(post_url,method='post',data=data,headers=headers,timeout=3).json()

                    params = {'u':links['s'], 'w':'100', 'h':'500', 's':ip_server, 'n':'0'}
                    request_url = '%s/ip.file/swf/ipplayer/ipplayer.php' %self.base_url

                    final_link = open_url(request_url,params=params,headers=headers,timeout=3).json()

                    data = final_link['data']

                    
                    if 'youtube' in str(data):

                        
                        vid_id = data.split('=')[1].split('&type')[0]
                        
                        request_url2 = 'https://docs.google.com/get_video_info?docid=%s&eurl=%s' %(vid_id,REF)
                        final_links = open_url(request_url2, verify=False, timeout=3)
                        match = re.findall(r'itag\%3D.*?%26url\%3D(.*?)%253B', final_links.content, re.I|re.DOTALL)
                        for url in match:
                            url = urllib.unquote(url)
                            url = urllib.unquote(url)
                            if 'video/x-flv' in url:
                                    url = url.partition('url=')[2]

                            for a in self.googletag(url):
                                cookie = final_links.cookies.get_dict()
                                cookie = urllib.quote('Cookie:DRIVE_STREAM=%s; NID=%s' %(cookie['DRIVE_STREAM'],cookie['NID']))
                                g_url = a['url'] + '|' + cookie
                                self.AddFileHost(list, a['quality'], g_url)

                    elif 'google' in str(data):

                        uniques = []

                        for field in data:
                            final_url = field['files']
                            res = field['quality']

                            if '.srt' not in final_url:
                                if '1080' in res:
                                    res='1080P'                   
                                elif '720' in res:
                                    res='720P'
                                elif  '480' in res:
                                    res='DVD'
                                elif '360' in res:
                                    res='SD'
                                else:
                                    res='DVD'

                                if final_url not in uniques:
                                    uniques.append(final_url)
                                    self.AddFileHost(list, res, final_url)

                    else:

                        final_url = data
                        res = '720P'

                        if urlresolver.HostedMediaFile(final_url):
                            self.AddFileHost(list, res, final_url)
                    




    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):  
    
        from md_request import open_url
        import re
        
        season_pull = "0%s"%season if len(season)<2 else season
        
        query = self.CleanTextForSearch(name).lower().strip()
        #print ':::::::::::::::::::::::::::::::::'
        headers = {'User-Agent':self.User_Agent,'Referer':self.base_url+'/'}
                
        search = '%s/movie/search/%s.html' %(self.base_url,str(query).replace(' ','+'))

        link = open_url(search,headers=headers,timeout=3).content

        links = link.split('ml-item')
        for p in links:
            try:
               movie_url=re.compile('href="(.+?)"').findall(p)[0]
               name=re.compile('title="(.+?)"').findall(p)[0]

               if type == 'tv_episodes':
                   if query.lower() in self.CleanTextForSearch(name.lower()):                
                       if 's'+season_pull in name.lower():
                           self.GetFileHosts(movie_url, list,episode,type)
                        
               else:
                   if query.lower() == self.CleanTextForSearch(name.lower()):
                       self.GetFileHosts(movie_url, list,episode,type)

            except:pass


                        
            



