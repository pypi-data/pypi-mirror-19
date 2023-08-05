#!/usr/bin/env python3

__all__ = ['lofter_download']

import sys
sys.path.append('../')

from utils import r0

def return_dic(p):
    title = r0(r'<meta  property="og:title" content="([^"]*)', p)
    title = ''.join(title)
    author = r0(r'<a href=\"\/\">(.*)<\/a>', p)
    author = ''.join(author)
    pics = r0(r'<meta  property=\"og:image\" content=\"(https?:\/\/[^:]*)([^"]*)', p)
    _pics = []
    for i in pics:
        if 'large' not in i[1]:
            _pics.append(i[0] + ':large')
        else:
            _pics.append(i[0] + i[1])
    if _pics != []:
        pics = _pics[:]
    return {'title': title, 'author': author, 'pics': pics}
