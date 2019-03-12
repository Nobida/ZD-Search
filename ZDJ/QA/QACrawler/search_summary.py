# -*- coding: utf-8 -*-

import sys
import os
cur_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(cur_path)
import operator
import time
from urllib.parse import quote

from QA.Tools import Html_Tools as To
from QA.Tools import TextProcess as T
from py2neo import Graph,Node,Relationship,NodeMatcher,RelationshipMatcher
import re

'''
对百度、Bing 的搜索摘要进行答案的检索
（需要加问句分类接口）
'''

def kgquery_entity(entity1, entity2):
    test_graph = Graph(
    'http://59.110.243.182:7474',
    username='neo4j',
    password='kcW584194150'
    )
    matcher = NodeMatcher(test_graph)
    find_rela  = test_graph.run(
        "MATCH ({name: '%s' })-[r:`%s`]->(n) RETURN n.name"%(entity1,entity2))
    ##print(list(find_rela))
    if find_rela:
        for i in find_rela:
            yield pattern(str(i))

def pattern(string):
    pattern = re.compile(r"n.name='(.*?)'>")
    string = re.findall(pattern,string)[0]
    return string 


def kwquery(query):
    #分词 去停用词 抽取关键词
    keywords = []
    words = T.postag(query)
    for k in words:
        #print(k)
        # 只保留名词
        if k.flag.__contains__("n"):
            # #print k.flag
            # #print k.word
            keywords.append(k.word)

    answer = []
    text = ''
    # 找到答案就置1
    flag = 0
    # 抓取百度前10条的摘要
    soup_baidu = To.get_html_baidu('https://www.baidu.com/s?wd='+quote(query))

    for i in range(1,10):
        if soup_baidu == None:
            break
        results = soup_baidu.find(id=i)
        if results == None:
            ##print("百度百科找不到答案")
            break    
        if results.attrs.get('mu') and i == 1:
            # #print results.attrs["mu"]
            r = results.find(class_='op_exactqa_s_answer')
            if r == None:
                pass
                ##print("百度知识图谱找不到答案")
            else:
                ##print("百度知识图谱找到答案")
                answer.append(r.get_text().strip())
                flag = 1
                break

        if flag == 0 and len(keywords)>1:
            ##print(keywords)

            ans_lst = list(kgquery_entity(keywords[0],keywords[1]))
    
            if len(ans_lst) != 0:
                answer = ans_lst
                flag = 1
                

        if results.find("h3") != None and flag == 0:
            if results.find("h3").find("a").get_text().__contains__(u"百度百科") and (i == 1 or i ==2):
                url = results.find("h3").find("a")['href']
                if url == None:
                    ##print("百度百科找不到答案")
                    continue
                else:
                    #print("百度百科找到答案")
                    baike_soup = To.get_html_baike(url)

                    r = baike_soup.find(class_='lemma-summary')
                    if r == None:
                        continue
                    else:
                        r = r.get_text().replace("\n","").strip()
                    answer.append(r)
                    flag = 1
                    break
        
        text += results.get_text().strip()


    if flag == 0:
        #分句
        cutlist = [u"。",u"?",u".", u"_", u"-",u":",u"！",u"？"]
        temp = ''
        sentences = []
        for i in range(0,len(text)):
            if text[i] in cutlist:
                if temp == '':
                    continue
                else:
                    # #print temp
                    sentences.append(temp)
                temp = ''
            else:
                temp += text[i]
        # 找到含有关键词的句子,去除无关的句子
        key_sentences = {}
        for s in sentences:
            for k in keywords:
                if k in s:
                    key_sentences[s]=1

        # 识别人名
        target_list = {}
        for ks in key_sentences:
            # #print ks
            words = T.postag(ks)
            for w in words:
                # #print "====="
                # #print w.word
                if w.flag == ("nr"):
                    if target_list.get(w.word):
                        target_list[w.word] += 1
                    else:
                        target_list[w.word] = 1

        sorted_lists = sorted(target_list.items(),key=operator.itemgetter(1),reverse=True)
        sorted_lists2 = []
        # 候选队列
        for i, st in enumerate(sorted_lists):
            # #print st[0]
            if st[0] in keywords:
                continue
            else:
                sorted_lists2.append(st)
        #print("返回前3个词频")
        answer = []
        for i,st in enumerate(sorted_lists2):
            # #print st[0]
            # #print st[1]
            if i< 3:
                # #print st[0]
                # #print st[1]
                answer.append(st[0])
    ##print(answer)
    return answer

    



if __name__ == '__main__':
    query = "伊利亚特的主角是"
    ans = kwquery(query)
    #print(ans)
    
    ##print "~~~~~~~"
    for a in ans:

        pass
        ##print(a.decode('utf-8'))
    ##print "~~~~~~~"