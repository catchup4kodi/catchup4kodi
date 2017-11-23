

'''

    Duckpool Extension
    hollymoviehd.com
    Copyright (C) 2017 DandyMedia

    version 0.2

'''




from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common




class hollymoviehd(MovieSource):

    implements = [MovieSource]

    name = "hollymoviehd"
    display_name = "HollymovieHD"
    base_url = 'https://www.hollymoviehd.com'
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'

    source_enabled_by_default = 'true'




    def GetFileHosts(self, url, list, lock, message_queue):

        from entertainment import googledocs
        from md_request import open_url
        import re

        link = open_url(url,timeout=5).content
        iframe = re.findall(r'iframe.*?-src="([^"]*)"', link, re.I|re.DOTALL)

        for iframe_url in iframe:
            
            if not 'https:' in iframe_url:
                iframe_url = 'https:' + iframe_url

            else:
                iframe_url = iframe_url

            if 'wp-embed.php' in iframe_url:
                
                link2 = open_url(iframe_url, timeout=5).content

                if 'drive.google.com' in str(link2):

                    link2 = link2.replace(' ', '')
                    match = re.findall(r'iframe.*?src="([^"]*)"', str(link2), re.I|re.DOTALL)[0]

                    for res, final_url in googledocs.GLinks(match):
                        self.AddFileHost(list, res, final_url)

                else:
                    
                    iframe_url2 = re.findall(r'iframe.*?src="([^"]*)"', link2, re.I|re.DOTALL)[0]
                    iframe_url2 = '%s/embed/%s' %(self.base_url,iframe_url2)

                    getdata = open_url(iframe_url2, timeout=3).content

                    headers = {'Origin':self.base_url, 'Referer':iframe_url2,
                               'Accept': 'application/json, text/javascript, */*; q=0.01',
                               'User_Agent':self.User_Agent, 'X-Requested-With':'XMLHttpRequest'}

                    post_url = '%s/embed/Htplugins/Loader.php' %self.base_url
                    form_data = {'data':re.compile('Htplugins_Load\("(.+?)"',re.DOTALL).findall(getdata)[0]}
                    final_link = open_url(post_url, method='post', data=form_data, headers=headers, verify=False, timeout=3).json()

                    if '/securesc/' in final_link['l'][0]:
                        for res, final_url in googledocs.GLinks(final_link['l'][0]):
                            self.AddFileHost(list, res, final_url)

                    else:

                        match = zip(final_link['q'],final_link['l'])

                        for res, final_url in match:

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

                            self.AddFileHost(list, res, final_url)
                        
                    




    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        from md_request import open_url
        import re

        name = self.CleanTextForSearch(name.lower()).strip()
        
        movie_url = '%s/?s=%s' %(self.base_url,name.replace(' ','+'))
        link = open_url(movie_url, timeout=3).content

        try:

            links = re.compile('class="ml-item".+?href="(.+?)".+?alt="(.+?)"',re.DOTALL).findall(link)
            for m_url,m_title in links:
                if name in self.CleanTextForSearch(m_title.lower()):
                    if year in m_title:
                        self.GetFileHosts(m_url, list, lock, message_queue)

        except:pass
