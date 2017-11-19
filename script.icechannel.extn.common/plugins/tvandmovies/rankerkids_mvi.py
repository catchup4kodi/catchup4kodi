'''
DUCKPOOL
Kids Zone

#Copyright (C) 2017 mucky duck
    
'''

from entertainment.plugnplay.interfaces import MovieIndexer
from entertainment import common
import xbmc



class rankerkids(MovieIndexer):

    implements = [MovieIndexer]
    
    name = "rankerkids"
    display_name = "Kids Zone"
    base_url = 'http://cache.api.ranker.com/lists/%s/items?limit=50&offset=0&include=votes,wikiText'
    img = common.get_themed_icon('kids.png')
    fanart = common.get_themed_fanart('kids.jpg')
    default_indexer_enabled = 'true'
    source_enabled_by_default = 'true'


    def ExtractContentAndAddtoList(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''): 

        if page == '':
            page = '1'
        from md_request import open_url
        import re,urllib

        new_url = urllib.unquote_plus(url)
            
        link = open_url(new_url).json()

        if len(link['listItems']) == 50:
            offset = re.compile('offset=(.*?)&').findall(url)[0]
            new_offset = 50 + int(offset)
            new_url = url.replace('offset=%s&' %offset, 'offset=%s&' %new_offset)
            
        self.AddInfo(list, indexer, section, new_url, type, page, '')

        mode = common.mode_File_Hosts

        if section == 'index' or 'new-release' or 'latest-added' or 'latest-hd' or 'latest-ts' or 'most-popular' or 'popular-today' or 'top-rated' or 'most-voted' or 'az' or 'genres' or 'year':
            for a in link['listItems']:
                year = ''
                name = a['name']
                title = self.CleanTextForSearch(name)
                match = re.compile('%s is a (.*?) ' %name,re.DOTALL).findall(str(a['node']['nodeWiki']))
                for year in match:
                    name = name + ' (' + year +')'
                
                self.AddContent(list,indexer,mode,name.replace('()','') ,'',type, url=new_url, name=title, year=year)




    def GetSection(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''):

        from md_request import open_url

        if section == 'main':

            if indexer == common.indxr_Movies:

                self.AddSection(list, indexer,'index','Best Superhero Movies Ever Made',self.base_url %'315081',indexer, img=common.get_themed_icon('kz_superhero.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Best Movies Based on Marvel Comics',self.base_url %'355348',indexer, img=common.get_themed_icon('kz_marvel.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Best PG-13 Teen Movies',self.base_url %'1064127',indexer, img=common.get_themed_icon('kz_teen.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Best PG-13 Family Movies',self.base_url %'1063791',indexer, img=common.get_themed_icon('kz_family.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Best PG-13 Horror Movies',self.base_url %'1064003',indexer, img=common.get_themed_icon('kz_horror.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Best PG-13 Action Movies',self.base_url %'1063981',indexer, img=common.get_themed_icon('kz_action.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Best \'00s Kids Movies',self.base_url %'2187563',indexer, img=common.get_themed_icon('kz_00kids.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Best \'80s Teen Movies',self.base_url %'1407499',indexer, img=common.get_themed_icon('kz_80teen.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Best \'80s Kids Movies',self.base_url %'2187569',indexer, img=common.get_themed_icon('kz_80kids.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Good Movies for 10 Year Olds',self.base_url %'1697939',indexer, img=common.get_themed_icon('kz_10year.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Best Family Movies Streaming on Hulu',self.base_url %'2180319',indexer, img=common.get_themed_icon('kz_hulu.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Best Movies for Kids',self.base_url %'693864',indexer, img=common.get_themed_icon('kz_kids.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Best Movies for Toddlers',self.base_url %'1443218',indexer, img=common.get_themed_icon('kz_todds.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Greatest Classic Films the Whole Family Will Love',self.base_url %'2547513',indexer, img=common.get_themed_icon('kz_classic.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Dinosaur Movies',self.base_url %'370068',indexer, img=common.get_themed_icon('kz_dino.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Best Live Action Animal Movies for Kids',self.base_url %'858027',indexer, img=common.get_themed_icon('kz_animal.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Best Adventure Movies for Kids',self.base_url %'1754597',indexer, img=common.get_themed_icon('kz_adventure.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Best Halloween Movies for Kids',self.base_url %'371510',indexer, img=common.get_themed_icon('kz_halloween.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Best Sports Movies for Kids',self.base_url %'2472516',indexer, img=common.get_themed_icon('kz_sports.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Best Live Action Kids Fantasy Movies',self.base_url %'2502919',indexer, img=common.get_themed_icon('kz_livefantasy.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Best Science Fiction Family Movies',self.base_url %'2513062',indexer, img=common.get_themed_icon('kz_science.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Great "Horror" Movies the Whole Family Can Enjoy',self.base_url %'2548835',indexer, img=common.get_themed_icon('kz_horror4all.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Best Movies for Tweens',self.base_url %'1443219',indexer, img=common.get_themed_icon('kz_tween.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','All Pixar Films, Ranked Best to Worst',self.base_url %'811686',indexer, img=common.get_themed_icon('kz_pixar.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Best Disney Live-Action Movies',self.base_url %'857009',indexer, img=common.get_themed_icon('kz_disneylive.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Best Disney Animated Movies of All Time',self.base_url %'2086672',indexer, img=common.get_themed_icon('kz_disneyani.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Best and Worst Disney Animated Movies',self.base_url %'366769',indexer, img=common.get_themed_icon('kz_worstdis.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Best Walt Disney Company Movies List',self.base_url %'165569',indexer, img=common.get_themed_icon('kz_waltdis.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Best Disney Princess Movies',self.base_url %'687771',indexer, img=common.get_themed_icon('kz_disneyprincess.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Best Fairy Tale Movies',self.base_url %'829312',indexer, img=common.get_themed_icon('kz_fairy.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Best Movies for Young Girls',self.base_url %'1697936',indexer, img=common.get_themed_icon('kz_younggirls.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Best Princess Movies',self.base_url %'360874',indexer, img=common.get_themed_icon('kz_princess.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Best Movies for Boys',self.base_url %'1697944',indexer, img=common.get_themed_icon('kz_boys.png'), fanart=common.get_themed_fanart('kids.jpg'))
                self.AddSection(list, indexer,'index','Best CGI Animated Films Ever Made',self.base_url %'338412',indexer, img=common.get_themed_icon('kz_cgi.png'), fanart=common.get_themed_fanart('kids.jpg'))
                
        else:
            self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)
