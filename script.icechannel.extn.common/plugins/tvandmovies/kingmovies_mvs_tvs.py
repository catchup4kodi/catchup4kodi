

#DUCKPOOL Extension
#KingMovies
#Copyright (C) 2017 mucky duck


from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin




class kingmovies(MovieSource,TVShowSource):

    implements = [MovieSource,TVShowSource]

    name = 'KingMovies'
    display_name = 'KingMovies'
    base_url = 'https://kingmovies.is'
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'

    source_enabled_by_default = 'true'




    def GetLinks(self, list, episode_id, referer, res, type):

        from md_request import open_url
        import re

        embed = 'https://embed.streamdor.co'
        embed_url = '%s/video/%s' %(embed,episode_id)
        embed_link = open_url(embed_url, verify=False, timeout=3).headers

        if 'location' in embed_link:

            if type == 'tv_episodes':
                res = '720P'
            else:
                res = res.upper()

            final_url = embed_link['location']
            self.AddFileHost(list, res, final_url)

        else:

            post_url = '%s/api/video/%s' %(embed,episode_id)
            token_url = '%s/token.php?episode=%s' %(embed,episode_id)
            token_link = open_url(token_url, verify=False, timeout=3).content
            token = re.compile("token([^']*),").findall(token_link)[0]
            token = token.replace('"','').replace("'",'').replace(":",'').strip()

            data = {'type':'sources', 'token':token, 'ref':referer}

            headers = {'Accept':'application/json, text/javascript, */*; q=0.01',
                       'Accept-Encoding':'gzip, deflate, br',
                       'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                       'Origin':embed, 'Referer':embed_url,
                       'User-Agent':self.User_Agent, 'requested-With':'XMLHttpRequest'}

            final_link = open_url(post_url, method='post', data=data, headers=headers, verify='False', timeout=3).json()

            js_data = final_link['playlist'][0]['sources']

            uniques = []

            for field in js_data:
                final_url = field['file']
                res = field['label']

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
        
        

    def GetFileHosts(self, url, list, lock, message_queue, season, episode, type, year, query):

        from md_request import open_url
        import re

        referer = url

        link = open_url(url, verify=False, timeout=3).content
        media_year = re.compile('>Released:([^<:]*)<').findall(link)[0].strip()
        links = link.split('ep-item">')[1:]
        
        for p in links:

            server = re.compile('href="([^"]*)"').findall(p)[0]
            epi = re.compile('href=.*?>([^<>]*)</a>').findall(p)[0]
            
            if type == 'tv_episodes':

                try:

                    episode_pull = '0%s' %episode if len(episode) <2 else episode

                    if 'episode %s' %episode_pull in epi.lower():
                        link2 = open_url(server, verify=False, timeout=3).content
                        episode_id = re.compile('episode: "([^"]*)"').findall(link2)[0].strip()
                        self.GetLinks(list, episode_id, referer, epi, type)
                    

                except:pass
                
            else:

            
                link2 = open_url(server, verify=False, timeout=3).content
                episode_id = re.compile('episode: "([^"]*)"').findall(link2)[0].strip()
                self.GetLinks(list, episode_id, referer, epi, type)





    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        from md_request import open_url
        import re
                
        name = self.CleanTextForSearch(name.lower()).strip()
        search =  '%s/search?q=%s' %(self.base_url,str(name).replace(' ','+'))
        link = open_url(search, verify=False, timeout=3).content
        links = link.split('movie-item')[1:]

        for p in links:

        
            media_url = re.compile("href='([^']*)'",re.DOTALL).findall(p)[0]
            media_title = re.compile('title="([^"]*)"',re.DOTALL).findall(p)[0]
            if type == 'tv_episodes':
                if name in self.CleanTextForSearch(media_title.lower()):
                    eps = re.compile("eps'>([^<>]*)<",re.DOTALL).findall(p)[0]
                    if 'eps' in eps.lower():
                        season_pull = '0%s' %season if len(season) <2 else season
                        if 'season %s' %season in media_title.lower() or 'season %s' %season_pull in media_title.lower() or 'iron fist' in media_title.lower():
                            self.GetFileHosts(media_url+'/watching.html', list, lock, message_queue, season, episode, type, year, name)
            else:
                if name in self.CleanTextForSearch(media_title.lower()):
                    self.GetFileHosts(media_url+'/watching.html', list, lock, message_queue, season, episode, type, year, name)

         
            
                
                
