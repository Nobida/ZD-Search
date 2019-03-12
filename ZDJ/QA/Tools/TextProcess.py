# -*- coding: utf-8 -*-

import jieba
import jieba.posseg as pseg
import os
import sys



'''
initialize jieba Segment
'''
def jieba_initialize():
    jieba.load_userdict(os.path.dirname(os.path.split(os.path.realpath(__file__))[0])+'/resources/QAattrdic.txt')
    jieba.initialize()
'''
POS Tagging
'''
def postag(text):
    
    words = pseg.cut(text)
    # for w in words:
    #     #print w.word, w.flag
    #返回的是生成器
    return words

'''
Load baike attribut name
'''
def load_baikeattr_name(attrdic):
    fr = open(attrdic,'r',encoding='utf-8')
    attr = []
    line = fr.readline()
    while line:
        attr.append(line.strip())
        line = fr.readline()
    fr.close()
    return  attr

'''
Segment words by jieba
'''
def wordSegment(text):
    text = text.strip()
    seg_list = jieba.cut(text)
    result = " ".join(seg_list)
    return result

'''
Synonyms Analysis,return word in baike attr
word 原始词
synsdic 同义词典
attr 属性
'''
def load_synonyms_word_inattr(word,synsdic,attr):
    fr = open(synsdic,'r',encoding='utf-8')
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

