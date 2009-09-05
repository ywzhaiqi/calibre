#!/usr/bin/env python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import with_statement

__license__   = 'GPL v3'
__copyright__ = '2009, Kovid Goyal <kovid@kovidgoyal.net>'
__docformat__ = 'restructuredtext en'

from calibre.web.feeds.news import BasicNewsRecipe

class H3(BasicNewsRecipe):
     title          = u'H\xedrszerz\u0151'
     oldest_article = 5
     max_articles_per_feed = 50
     language = 'hu'

     __author__ = 'Ezmegaz'


     feeds          = [(u'Belf\xf6ld',
 u'http://www.hirszerzo.hu/rss.belfold.xml'), (u'K\xfclf\xf6ld',
 u'http://www.hirszerzo.hu/rss.kulfold.xml'), (u'Profit',
 u'http://www.hirszerzo.hu/rss.profit.xml'), (u'Shake',
 u'http://www.hirszerzo.hu/rss.shake.xml'), (u'Publicisztika',
 u'http://www.hirszerzo.hu/rss.publicisztika.xml'), (u'Elemz\xe9s',
 u'http://www.hirszerzo.hu/rss.elemzes.xml'), (u'Sorok k\xf6z\xf6tt',
 u'http://www.hirszerzo.hu/rss.sorok_kozott.xml'), (u'Gal\xe9ria',
 u'http://www.hirszerzo.hu/rss.galeria.xml'), (u'Patro',
 u'http://www.hirszerzo.hu/rss.patro.xml')]

