#!/usr/bin/env python3

__all__ = ['163_download']

import sys
sys.path.append('../')

from utils import r0, LibError

def return_dic(p):
    title = r0(r',picSetTitle:\'(.*)\'' ,p)
    title = ''.join(title)
    author = r0(r'profile:{nickName : \'(.*)\'' ,p)
    author = ''.join(author)
    pics = r0(r'pictureId:\d+,url:\'([^\']*)\'' ,p)
    return {'title': title, 'author': author, 'pics': pics}
