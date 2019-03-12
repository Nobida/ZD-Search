# -*- coding: utf-8 -*-

import aiml
import os, sys
import os
cur_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(cur_path)

from QA.QACrawler import baike
from QA.Tools import Html_Tools as QAT
from QA.Tools import TextProcess as T
from QA.QACrawler import search_summary



#    print('''
#.----------------.  .-----------------. .----------------.  .----------------.  .----------------.
#| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
#| |    _______   | || | ____  _____  | || |      __      | || |  ___  ____   | || |  _________   | |
#| |   /  ___  |  | || ||_   \|_   _| | || |     /  \     | || | |_  ||_  _|  | || | |_   ___  |  | |
#| |  |  (__ \_|  | || |  |   \ | |   | || |    / /\ \    | || |   | |_/ /    | || |   | |_  \_|  | |
#| |   '.___`-.   | || |  | |\ \| |   | || |   / /__\ \   | || |   |  __'.    | || |   |  _|  _   | |
#| |  |`\____) |  | || | _| |_\   |_  | || | _/ /    \ \_ | || |  _| |  \ \_  | || |  _| |___/ |  | |
#| |  |_______.'  | || ||_____|\____| | || ||____|  |____|| || | |____||____| | || | |_________|  | |
#| |              | || |              | || |              | || |              | || |              | |
#| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
# '----------------'  '----------------'  '----------------'  '----------------'  '----------------'
#        ZDJ：你好，我是知道君。是阿笠博士把我创造出来的！╭(╯^╰)╮''')
def run(query):
    #if __name__ == '__main__':

    #初始化jb分词器
    T.jieba_initialize()

    #切换到语料库所在工作目录
    mybot_path = './'
    os.chdir(mybot_path)

    mybot = aiml.Kernel()
    mybot.learn(os.path.split(os.path.realpath(__file__))[0]+"/resources/std-startup.xml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/bye.aiml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/tools.aiml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/bad.aiml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/funny.aiml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/OrdinaryQuestion.aiml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/Common conversation.aiml")
    if len(query) > 60:
        answer = '句子长度过长'
    elif query.strip() == '':
        answer = mybot.respond('无')
    else:
        message = T.wordSegment(query)
        words = T.postag(query)
        response = mybot.respond(message)
        if response == '':
            answer = mybot.respond('找不到答案')
        elif response[0] == '#':
            if response.__contains__("searchbaike"):
                res = response.split(':')
                entity = str(res[1]).replace(" ","")
                attr = str(res[2]).replace(" ","")
                ans = baike.query(entity, attr)
                if '找不到' not in ans:
                    answer = ans

                elif ans.__contains__('找不到'):
                    answer = search_summary.kwquery(query)
                    if len(answer) == 0:
                        answer = mybot.respond('找不到答案')
                    elif len(answer) == 1:
                        print(answer)
                        answer = answer[0].strip().replace(' ','').replace("\n","")
                    else:
                        answer = '找不到答案'
            else:
                answer = '找不到答案'
        else:
            answer = search_summary.kwquery(query)
            if len(answer) == 0:
                answer = mybot.respond('找不到答案')
            elif len(answer) == 1:
                answer = answer[0].strip().replace(' ','').replace("\n","")
            else:
                answer = '找不到答案'                   
    return answer

if __name__ == "__main__":
    
    print(run('大时代是'))









#    while True:
#        input_message = input("Enter your message >> ")#

#        if len(input_message) > 60:
#            print(mybot.respond("句子长度过长"))
#            continue
#        elif input_message.strip() == '':
#            print(mybot.respond("无"))
#            continue#

#        print(input_message)
#        message = T.wordSegment(input_message)
#        #print(message)
#        # 去标点
#        #print 'word Seg:'+ message
#        #print '词性：'
#        words = T.postag(input_message)#
#

#        if message == 'q':
#            exit()
#        else:
#            response = mybot.respond(message)#

#            #print("=======")
#            #print(response)
#            #print("=======")#

#            if response == "":
#                ans = mybot.respond('找不到答案')
#                print('Eric：' + ans)
#            # 百科搜索
#            elif response[0] == '#':
#                # 匹配百科
#                if response.__contains__("searchbaike"):
#                    #print("searchbaike")
#                    print(response)
#                    res = response.split(':')
#                    #实体
#                    entity = str(res[1]).replace(" ","")
#                    #属性
#                    attr = str(res[2]).replace(" ","")
#                    print(entity+'<---->'+attr)#

#                    ans = baike.query(entity, attr)
#                    # 如果命中答案
#                    if '找不到' not in ans :
#                        print('Eric：' + ans)
#                        continue
#                    elif ans.__contains__('找不到'):
#                        #百度摘要
#                        ans = search_summary.kwquery(input_message)
#                        if len(ans) == 0:
#                            ans = mybot.respond('找不到答案')
#                            print('Eric：' + ans)
#                        elif len(ans) >1:#

#                            print("不确定候选答案")
#                            for a in ans:
#                                print(a.strip().replace(' ','').replace("\n",""))
#                        else:
#                            print('Eric：' + ans[0].strip().replace(' ','').replace("\n",""))
#                
#                else:                   
#                    ans = search_summary.kwquery(input_message)
#                    if len(ans) == 0:
#                        ans = mybot.respond('找不到答案')
#                        print('Eric：' + ans)
#                    elif len(ans) >1:
#                        
#                        print("不确定候选答案")
#                        for a in ans:
#                            print(a.strip().replace(' ','').replace("\n",""))
#                    else:
#                        print('Eric：' + ans[0].strip().replace(' ','').replace("\n",""))






























