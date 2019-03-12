# -*- coding: utf-8 -*-

import sys
import os
cur_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(cur_path)
from QA.Tools import Html_Tools as To
from QA.Tools import TextProcess as T



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
                info[attrName] = bI.get_text()
    return info



def query(entity,attr):
    soup = To.get_html_baike("http://baike.baidu.com/item/"+entity)
    basicInfo_block = soup.find(class_= 'basic-info cmn-clearfix')
    if not basicInfo_block:
        return '找不到'
    else:
        info  = get_info(basicInfo_block)
        ##print(info)
        if info.get(attr):
            return info[attr].strip()
        else:
            attr_list = T.load_baikeattr_name(os.path.dirname(os.path.split(os.path.realpath(__file__))[0])+'/resources/Attribute_name.txt')
            attr = T.load_synonyms_word_inattr(attr,os.path.dirname(os.path.split(os.path.realpath(__file__))[0])+'/resources/SynonDic.txt',attr_list)
            if info.get(attr):
                return info[attr].strip()
            else:
                return '找不到'





if __name__ == "__main__":
    pass
    #print(query('印度','人口数量'))
