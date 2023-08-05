#!/usr/bin/env python3

__all__ = ['poco_download']

import sys
sys.path.append('../')

from ..utils import r0

def return_dic(p):
    title = r0(r'<title>(.*)<\/title>' ,p)
    title = ''.join(title)
    author = r0(r'<a href=\"\/\">(.*)<\/a>' ,p)
    author = ''.join(author)
    pics = r0(r'originPhoto:\'(http[^\']+)\'',p)
    _pics = []
    for i in pics:
        _pics.append((i.split("?")[0], i.split("?")[0]))
    if _pics != []:
        pics = _pics[:]
    return {'title': title, 'author': author, 'pics': pics}

if __name__ == '__main__':
    import requests
    ret = requests.get('http://my.poco.cn/lastphoto_v2.htx&id=5415252&user_id=57250626&p=0&temp=3853').text
    print(return_dic(ret))
