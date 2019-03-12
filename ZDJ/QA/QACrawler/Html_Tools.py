# -*- coding: utf-8 -*-

import urllib
import re
import time
from bs4 import BeautifulSoup
import requests

headers = {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}



def get_info(basicInfo_block):
    info = {}
    
    for bI_LR in basicInfo_block.contents[1:3]:
        for bI in bI_LR:
            if bI.name == None:
                continue
            ##print(bI.name)
            ##print(bI.string)
            if bI.name == 'dt':
                #获取属性名
                for bi in bI.contents: 
                    attrName = bi.string.strip().replace(u" ",u"")             
            elif bI.name == 'dd':
                info[attrName] = bI.contents
    return info



def load_synonyms_word_inattr(word,synsdic,attr):
    fr = open(synsdic,'r')
    tar_word = ''
    line = fr.readline().strip()
    while line:
        words = line.split(" ")
        if word in words:
            for w in words:
                if w in attr:
                  tar_word = w
                  break
        if tar_word != '':
            break
        line = fr.readline()
    fr.close()
    if tar_word == '':
        tar_word = 'Empty'
    return  tar_word

def load_baikeattr_name(attrdic):
    fr = open(attrdic,'r')
    attr = []
    line = fr.readline()
    while line:
        attr.append(line.strip())
        line = fr.readline()
    fr.close()
    return  attr

def query(entity,attr):
    """
    发起查询
    :param entity: 询问实体
    :param attr: 询问属性
    """
    soup = get_html_baike("http://baike.baidu.com/item/"+entity)
    basicInfo_block = soup.find(class_= 'basic-info cmn-clearfix')
    if not basicInfo_block:
        return '抱歉，找不到相关信息'
    else:
        info  = get_info(basicInfo_block)
        if info.get(attr):
            return info[attr]
        else:
            attr_list = T.load_baikeattr_name(os.path.dirname(os.path.split(os.path.realpath(__file__))[0])+'/resources/Attribute_name.txt')

    ##print(basicInfo_block)

if __name__ == "__main__":
    #print(query('耶稣','出生日期'))