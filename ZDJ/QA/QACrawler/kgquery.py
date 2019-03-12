# -*- coding: utf-8 -*-

from py2neo import Graph,Node,Relationship,NodeMatcher,RelationshipMatcher
import re

def kgquery_entity(entity1, entity2):
    test_graph = Graph(
    'http://59.110.243.182:7474',
    username='xxxxx',
    password='xxxxxxx'
    )
    matcher = NodeMatcher(test_graph)
    find_rela  = test_graph.run(
        "MATCH ({name: '%s' })-[r:`%s`]->(n) RETURN n.name"%(entity1,entity2))
    if find_rela:
        for i in find_rela:
            yield pattern(str(i))

def pattern(string):
    pattern = re.compile(r"n.name='(.*?)'>")
    string = re.findall(pattern,string)[0]
    return string 
        

