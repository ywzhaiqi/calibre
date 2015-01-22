#!/usr/bin/env python
# vim:fileencoding=utf-8
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__license__ = 'GPL v3'
__copyright__ = '2015, Kovid Goyal <kovid at kovidgoyal.net>'

import posixpath, os, time, types
from collections import namedtuple, defaultdict, Counter

from calibre.ebooks.oeb.polish.container import OEB_DOCS, OEB_STYLES, OEB_FONTS
from calibre.ebooks.oeb.polish.spell import get_all_words
from calibre.utils.icu import numeric_sort_key, ord_string, safe_chr
from calibre.utils.magick.draw import identify

File = namedtuple('File', 'name dir basename size category')

def get_category(name, mt):
    category = 'misc'
    if mt.startswith('image/'):
        category = 'image'
    elif mt in OEB_FONTS:
        category = 'font'
    elif mt in OEB_STYLES:
        category = 'style'
    elif mt in OEB_DOCS:
        category = 'text'
    ext = name.rpartition('.')[-1].lower()
    if ext in {'ttf', 'otf', 'woff'}:
        # Probably wrong mimetype in the OPF
        category = 'font'
    elif ext == 'opf':
        category = 'opf'
    elif ext == 'ncx':
        category = 'toc'
    return category

def safe_size(container, name):
    try:
        return os.path.getsize(container.name_to_abspath(name))
    except Exception:
        return 0

def safe_img_data(container, name, mt):
    if 'svg' in mt:
        return 0, 0
    try:
        width, height, fmt = identify(container.name_to_abspath(name))
    except Exception:
        width = height = 0
    return width, height

def files_data(container, book_locale):
    for name, path in container.name_path_map.iteritems():
        yield File(name, posixpath.dirname(name), posixpath.basename(name), safe_size(container, name),
                   get_category(name, container.mime_map.get(name, '')))

Image = namedtuple('Image', 'name mime_type usage size basename id width height')

LinkLocation = namedtuple('LinkLocation', 'name line_number text_on_line')

def sort_locations(container, locations):
    nmap = {n:i for i, (n, l) in enumerate(container.spine_names)}
    def sort_key(l):
        return (nmap.get(l.name, len(nmap)), numeric_sort_key(l.name), l.line_number)
    return sorted(locations, key=sort_key)

def images_data(container, book_locale):
    image_usage = defaultdict(set)
    link_sources = OEB_STYLES | OEB_DOCS
    for name, mt in container.mime_map.iteritems():
        if mt in link_sources:
            for href, line_number, offset in container.iterlinks(name):
                target = container.href_to_name(href, name)
                if target and container.exists(target):
                    mt = container.mime_map.get(target)
                    if mt and mt.startswith('image/'):
                        image_usage[target].add(LinkLocation(name, line_number, href))

    image_data = []
    for name, mt in container.mime_map.iteritems():
        if mt.startswith('image/') and container.exists(name):
            image_data.append(Image(name, mt, sort_locations(container, image_usage.get(name, set())), safe_size(container, name),
                                    posixpath.basename(name), len(image_data), *safe_img_data(container, name, mt)))
    return tuple(image_data)

Word = namedtuple('Word', 'id word locale usage')

def words_data(container, book_locale):
    count, words = get_all_words(container, book_locale, get_word_count=True)
    return (count, tuple(Word(i, word, locale, v) for i, ((word, locale), v) in enumerate(words.iteritems())))

Char = namedtuple('Char', 'id char codepoint usage count')

def chars_data(container, book_locale):
    chars = defaultdict(set)
    counter = Counter()
    def count(codepoint):
        counter[codepoint] += 1

    for name, is_linear in container.spine_names:
        if container.mime_map.get(name) not in OEB_DOCS:
            continue
        raw = container.raw_data(name)
        counts = Counter(ord_string(raw))
        counter.update(counts)
        for codepoint in counts:
            chars[codepoint].add(name)

    nmap = {n:i for i, (n, l) in enumerate(container.spine_names)}
    def sort_key(name):
        return nmap.get(name, len(nmap)), numeric_sort_key(name)

    for i, (codepoint, usage) in enumerate(chars.iteritems()):
        yield Char(i, safe_chr(codepoint), codepoint, sorted(usage, key=sort_key), counter[codepoint])

def gather_data(container, book_locale):
    timing = {}
    data = {}
    for x in 'files images words chars'.split():
        st = time.time()
        data[x] = globals()[x + '_data'](container, book_locale)
        if isinstance(data[x], types.GeneratorType):
            data[x] = tuple(data[x])
        timing[x] = time.time() - st
    return data, timing
