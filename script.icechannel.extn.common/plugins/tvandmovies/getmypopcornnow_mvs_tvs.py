'''
    DUCKPOOL Extension

    GetMyPopcornNow
    Copyright (C) 2017 DandyMedia

    version 0.1

'''

from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common




class getmypopcornnow(MovieSource, TVShowSource):

    implements = [MovieSource, TVShowSource]
	
    name = 'GetMyPopcornNow'
    display_name = 'GetMyPopcornNow'
    base_url = 'http://getmypopcornnow.xyz'

    source_enabled_by_default = 'true'

    # def GetFileHosts(self, url, list, lock, message_queue):

        # from md_request import open_url
        # import re
        # print 'fh URL' + url
        # link = open_url(url, timeout=3).content.replace(' ', '')
        # data = re.compile('"file":"([^"]+)","label":"([^"]+)"').findall(link)
        
        # for final_url,res in data:

            # if '1080' in res:
                # res='1080P'                   
            # elif '720' in res:
                # res='720P'
            # elif  '480' in res:
                # res='DVD'
            # elif '360' in res:
                # res='SD'
            # else:
                # res='DVD'
            # final_url = final_url.replace('\/','/')
            # self.AddFileHost(list, res, final_url)


    def GetFileHosts(self, url, list, lock, message_queue):

        from md_request import open_url
        import re
        link = open_url(url, timeout=3).content.replace(' ', '')
        data = re.compile('file.+?"([^"]+)"').findall(link)
        
        for final_url in data:
            if 'requiressl' in final_url:
                if 'itag=37' in final_url:
                    res='1080P'                   
                elif 'itag=22' in final_url:
                    res='720P'
                elif  'itag=59' in final_url:
                    res='DVD'
                elif 'itag=18' in final_url:
                    res='SD'
                else:
                    res='DVD'
                final_url = final_url.replace('\/','/')
                self.AddFileHost(list, res, final_url)




    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        from md_request import open_url
        import re
        
        name = self.CleanTextForSearch(name.lower()).strip()

        search = '%s/?s=%s' %(self.base_url,name.replace(' ','+'))

        link = open_url(search, timeout=3).content
        links = link.split('result-item')

        for p in links:

            try:

                item_url = re.compile('href="([^"]+)"').findall(p)[0]
                item_title = re.compile('alt="([^"]+)"').findall(p)[0]
                item_year = re.compile('"year">([^<>]*)<').findall(p)[0].strip()

                if name in self.CleanTextForSearch(item_title.lower()):
                    if int(year) == int(item_year):

                        if type == 'tv_episodes':
                            item_url = item_url[:-1].replace('/tvseries/', '/episodes/') + '-%sx%s/' %(season,episode)
                        
                        self.GetFileHosts(item_url, list, lock, message_queue)

            except:pass
