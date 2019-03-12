# -*- coding: utf-8 -*-

import urllib
import re
import time
from bs4 import BeautifulSoup
import requests
import os

headers = {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}


'''
获取百度搜索的结果
'''
def get_html_baidu(url):

    soup_baidu = BeautifulSoup(requests.get(url=url, headers=headers).content.decode('utf-8'), "lxml")
    # 去除无关的标签  
    [s.extract() for s in soup_baidu(['script', 'style','img'])]
    # #print(soup.prettify())
    return soup_baidu

def get_html_baike(url):
    soup_baike = BeautifulSoup(requests.get(url=url, headers=headers).content, "lxml")
    # 去除无关的标签
    [s.extract() for s in soup_baike(['script', 'style', 'img', 'sup', 'b'])]
    return soup_baike

if __name__ == "__main__":
    pass


