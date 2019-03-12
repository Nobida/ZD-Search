# -*- coding: utf-8 -*-

import requests
from py2neo import Graph
import re
import json


#def py2neodb():
#    test_graph = Graph(
#    'http://59.110.243.182:7474',
#    username='xxxxx',
#    password='xxxxxxx'
#    )
#    return test_graph#
#

#def keywords(keywords):
#    test_graph = py2neodb()
#    find_node  = test_graph.run(
#        "match(n) where n.name =~'%s.*' return \
#        n.name,n.uuid limit 5"%(keywords))
#    if find_node:
#        return list(find_node) #
#

#def path(entity1,entity2):
#    test_graph = py2neodb()
#    find_path = test_graph.run(
#        'MATCH (p1{name:"%s"}),(p2{name:"%s"}),\
#        p=shortestpath((p1)-[r*..10]-(p2)) \
#        return r,p1.uuid,p2.uuid'%(entity1,entity2))
#    if find_path:
#        return list(find_path)#

#def net(entity,limit_num):
#    limit_num = str(limit_num)
#    test_graph = py2neodb()
#    find_path = test_graph.run(
#        'MATCH (p1{ name:"%s"})<-[r]->(p2) \
#        RETURN r,p1.uuid,p2.uuid limit %s'%(entity,limit_num))
#    if find_path:
#        return list(find_path)

from py2neo import Graph,Node,Relationship,NodeMatcher
#版本说明：Py2neo v4
class Neo4j_Handle():
    graph = None
    matcher = None
    def __init__(self):
        self.graph = Graph("bolt: // localhost:7687", username="neo4j", password="qzwkx333530")
        self.matcher = NodeMatcher(self.graph)

    #实体查询，用于命名实体识别：品牌+车系+车型
    def matchEntityItem(self,value):
        answer = self.graph.run("MATCH (entity1) WHERE entity1.name = \"" + value + "\" RETURN entity1").data()
        return answer

    def matchRelatedEntity(self,value):
        answer  = self.graph.run(
            "match(n) where n.name =~'%s.*' return n.name,n.uuid limit 5"%(value)).data()
        if answer:
            return list(answer)

    def matchShortestPath(self,entity1,entity2):
        answer = self.graph.run('MATCH (p1{name:"%s"}),(p2{name:"%s"}),p=shortestpath((p1)-[r*..10]-(p2)) \
        return r,p1.uuid,p2.uuid'%(entity1,entity2))
        if answer:
            return list(answer.data())

    def matchEntityNets(self,entity,limit_num):
        limit_num = str(limit_num)
        answer = self.graph.run('MATCH (p1{ name:"%s"})<-[r]->(p2) RETURN r,p1.uuid,p2.uuid limit %s'%(entity,limit_num))
        if answer:
            return list(answer)

    #实体查询
    def getEntityRelationbyEntity(self,value):
        #查询实体：不考虑实体类型，只考虑关系方向
        answer = self.graph.run("MATCH (entity1) - [rel] -> (entity2)  WHERE entity1.name = \"" + value + "\" RETURN rel,entity2").data()
        if(len(answer) == 0):
            #查询实体：不考虑关系方向
            answer = self.graph.run("MATCH (entity1) - [rel] - (entity2)  WHERE entity1.name = \"" + value + " \" RETURN rel,entity2").data()
        #print(answer)
        return answer

    #关系查询:实体1
    def findRelationByEntity1(self,entity1):
        #基于品牌查询
        answer = self.graph.run("MATCH (n1{name:\""+entity1+"\"})- [rel] -> (n2) RETURN n1,rel,n2" ).data()
        if(len(answer) == 0):
            answer = self.graph.run("MATCH (n1:Serise {name:\""+entity1+" \"})- [rel] - (n2) RETURN n1,rel,n2" ).data()
        return answer
    #关系查询：实体2
    def findRelationByEntity2(self,entity1):
        #基于品牌
        answer = self.graph.run("MATCH (n1)<- [rel] - (n2{name:\""+entity1+"\"}) RETURN n1,rel,n2" ).data()
        return answer

    #关系查询：实体1+关系
    def findOtherEntities(self,entity,relation):
        print("MATCH (n1{name:\"" + entity + "\"})- [rel:`"+relation+"`}] -> (n2) RETURN n1,rel,n2")
        answer = self.graph.run("MATCH (n1{name:\"" + entity + "\"})- [rel:`"+relation+"`] -> (n2) RETURN n1,rel,n2" ).data()
        return answer

    #关系查询：关系+实体2
    def findOtherEntities2(self,entity,relation):
        print("findOtherEntities2==")
        print(entity,relation)
        answer = self.graph.run("MATCH (n1)- [rel:RELATION {type:\""+relation+"\"}] -> (n2:Bank {name:\"" + entity + "\"}) RETURN n1,rel,n2" ).data()
        if(len(answer) == 0):
            answer = self.graph.run("MATCH (n1)- [rel:RELATION {type:\""+relation+"\"}] -> (n2:Serise {name:\"" + entity + " \"}) RETURN n1,rel,n2" ).data()
        return answer

    #关系查询：实体1+实体2(注意Entity2的空格）
    def findRelationByEntities(self,entity1,entity2):
        #品牌 + 品牌
        answer = self.graph.run("MATCH (n1:Bank {name:\"" + entity1 + "\"})- [rel] -> (n2:Bank{name:\""+entity2+" \"}) RETURN n1,rel,n2" ).data()
        if(len(answer) == 0):
            #品牌 + 系列
            answer = self.graph.run("MATCH (n1:Bank {name:\"" + entity1 + "\"})- [rel] -> (n2:Serise{name:\""+entity2+" \"}) RETURN n1,rel,n2" ).data()
        if(len(answer) == 0):
            #系列 + 品牌
            answer = self.graph.run("MATCH (n1:Serise {name:\"" + entity1 + "\"})- [rel] -> (n2:Bank{name:\""+entity2+" \"}) RETURN n1,rel,n2" ).data()
        if(len(answer) == 0):
            #系列 + 系列
            answer = self.graph.run("MATCH (n1:Serise {name:\"" + entity1 + "\"})- [rel] -> (n2:Serise{name:\""+entity2+" \"}) RETURN n1,rel,n2" ).data()
        return answer

    #查询数据库中是否有对应的实体-关系匹配
    def findEntityRelation(self,entity1,relation,entity2):
        answer = self.graph.run("MATCH (n1:Bank {name:\"" + entity1 + "\"})- [rel:subbank {type:\""+relation+"\"}] -> (n2:Bank{name:\""+entity2+"\"}) RETURN n1,rel,n2" ).data()
        if(len(answer) == 0):
            answer = self.graph.run("MATCH (n1:Bank {name:\"" + entity1 + "\"})- [rel:subbank {type:\""+relation+"\"}] -> (n2:Serise{name:\""+entity2+"\"}) RETURN n1,rel,n2" ).data()
        if(len(answer) == 0):
            answer = self.graph.run("MATCH (n1:Serise {name:\"" + entity1 + "\"})- [rel:subbank {type:\""+relation+"\"}] -> (n2:Bank{name:\""+entity2+"\"}) RETURN n1,rel,n2" ).data()
        if(len(answer) == 0):
            answer = self.graph.run("MATCH (n1:Serise {name:\"" + entity1 + "\"})- [rel:subbank {type:\""+relation+"\"}] -> (n2:Serise{name:\""+entity2+"\"}) RETURN n1,rel,n2" ).data()

        return answer



if __name__ == '__main__':
    db = Neo4j_Handle()
    answer = db.findOtherEntities('米兰花园事件','主人公')
    answer2 = db.matchRelatedEntity('孔子')
    #answer = db.sortDict(answer)
    print(json.dumps(answer,ensure_ascii=False))
    print(json.dumps(answer2,ensure_ascii=False))