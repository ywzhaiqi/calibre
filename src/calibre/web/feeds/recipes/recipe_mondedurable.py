#!/usr/bin/env  python

__license__   = 'GPL v3'
__copyright__ = '2009, Darko Miletic <darko.miletic at gmail.com>'
'''
mondedurable.science-et-vie.com
'''

from calibre.web.feeds.news import BasicNewsRecipe

class AdventureGamers(BasicNewsRecipe):
    title                 = 'Monde durable'
    language = 'fr'

    __author__            = 'Darko Miletic'
    description           = 'science news'    
    publisher             = 'Monde durable'
    category              = 'environnement, developpement durable, science & vie, science et vie'    
    oldest_article        = 30
    delay                 = 2
    max_articles_per_feed = 100
    no_stylesheets        = True
    encoding              = 'utf-8'
    remove_javascript     = True
    use_embedded_content  = False
    
    html2lrf_options = [
                          '--comment', description
                        , '--category', category
                        , '--publisher', publisher
                        ]
    
    html2epub_options = 'publisher="' + publisher + '"\ncomments="' + description + '"\ntags="' + category + '"' 

    keep_only_tags = [dict(name='div', attrs={'class':'post'})]

    remove_tags = [dict(name=['object','link','embed','form','img'])]
                  
    feeds = [(u'Articles', u'http://mondedurable.science-et-vie.com/feed/')]
    
    def preprocess_html(self, soup):
        mtag = '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>'
        soup.head.insert(0,mtag)    
        for item in soup.findAll(style=True):
            del item['style']
        return soup
