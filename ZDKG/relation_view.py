# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from toolkit.pre_load import neo4jconn
from django.http import JsonResponse
import os
from Model.neo4j_models import Neo4j_Handle

import json
relationCountDict = {}
filePath = os.path.abspath(os.path.join(os.getcwd(),"."))

with open(filePath+"/toolkit/relationStaticResult.txt","r") as fr:
	for line in fr:
		relationNameCount = line.split(",")
		relationName = relationNameCount[0][2:-1]
		relationCount = relationNameCount[1][1:-2]
		relationCountDict[relationName] = int(relationCount)
def sortDict(relationDict):
	for i in range(len(relationDict) ):
		#relationName = relationDict[i]['rel']['type']
		relationCount = relationCountDict.get(relationName)
		if(relationCount is None ):
			relationCount = 0
		relationDict[i]['relationCount'] = relationCount

	relationDict = sorted(relationDict,key = lambda item:item['relationCount'],reverse = True)

	return relationDict

#实体查询
def search_entity(request):
	ctx = {}
	#根据传入的实体名称搜索出关系
	if(request.GET):
		db = neo4jconn
		entity = request.GET['user_text']
		#print(entity)
		#连接数据库
		#db = Neo4j_Handle()
		entityRelation = db.getEntityRelationbyEntity(entity)
		if len(entityRelation) == 0:
			#若数据库中无法找到该实体，则返回数据库中无该实体
			ctx= {'title' : '<h2>数据库中暂未添加该实体</h1>'}
			return render(request,'entity.html'.encode("utf-8"),{'ctx':json.dumps(ctx,ensure_ascii=False)})
		else:


			return render(request,'entity.html'.encode("utf-8"),{'entityRelation':json.dumps(entityRelation,ensure_ascii=False)})
	#需要进行类型转换
	return render(request,"entity.html".encode("utf-8"),{'ctx':ctx})



def search_relation(request):
	ctx = {}
	if(request.GET):
		db =neo4jconn
		entity1 = request.GET['entity1_text']
		#print(entity1)
		relation = request.GET['relation_name_text']
		entity2 = request.GET['entity2_text']
		relation = relation.lower()
		searchResult = {}
		#若只输入entity1,则输出与entity1有直接关系的实体和关系
		if(len(entity1) != 0 and len(relation) == 0 and len(entity2) == 0):
			searchResult = db.findRelationByEntity1(entity1)
			#searchResult = sortDict(searchResult)
			#print(json.dumps(searchResult,ensure_ascii=False))
			if(len(searchResult)>0):
				return render(request,'relation.html'.encode("utf-8"),{'searchResult':json.dumps(searchResult,ensure_ascii=False)})

		#若只输入entity2则,则输出与entity2有直接关系的实体和关系
		if(len(entity1) == 0 and len(relation) == 0 and len(entity2) != 0):
			searchResult = db.findRelationByEntity2(entity2)
			#searchResult = sortDict(searchResult)
			if(len(searchResult)>0):
				return render(request,'relation.html'.encode("utf-8"),{'searchResult':json.dumps(searchResult,ensure_ascii=False)})

		#若输入entity1和relation，则输出与entity1具有relation关系的其他实体
		if(len(entity1)!=0 and len(relation)!=0 and len(entity2) == 0):
			searchResult = db.findOtherEntities(entity1,relation)
			if(len(searchResult)>0):
				return render(request,'relation.html'.encode("utf-8"),{'searchResult':json.dumps(searchResult,ensure_ascii=False)})
		#若输入entity2和relation，则输出与entity2具有relation关系的其他实体
		if(len(entity1)==0 and len(relation)!=0 and len(entity2) != 0):
			searchResult = db.findOtherEntities2(entity2,relation)
			#searchResult = sortDict(searchResult)
			if(len(searchResult)>0):
				return render(request,'relation.html'.encode("utf-8"),{'searchResult':json.dumps(searchResult,ensure_ascii=False)})


		#若输入entity1,entity2和relation,则输出entity1、entity2是否具有相应的关系
		if(len(entity1)!=0 and len(entity2)!=0 and len(relation)==0):
		#if(len(entity1)!=0 and len(entity2)!=0 and len(relation)!=0):
			searchResult = db.matchShortestPath(entity1,entity2)
			#print(searchResult)
			if(len(searchResult)>0):
				return render(request,'relation.html'.encode("utf-8"),{'searchResult':json.dumps(searchResult,ensure_ascii=False)})

		if(len(entity1)!=0 and len(entity2)!=0 and len(relation)!=0):
			searchResult = db.findEntityRelation(entity1,relation,entity2)
			if(len(searchResult)>0):
				return render(request,'relation.html'.encode("utf-8"),{'searchResult':json.dumps(searchResult,ensure_ascii=False)})

		if(len(entity1)==0 and len(entity2)==0 and len(relation)!=0):
			searchResult = db.findRelation(relation)
			if(len(searchResult)>0):
				return render(request,'relation.html'.encode("utf-8"),{'searchResult':json.dumps(searchResult,ensure_ascii=False)})

		#全为空
		if(len(entity1)==0 and len(relation)==0 and len(entity2)==0 ):
			pass
		ctx= {'title' : '<h1>暂未找到相应的匹配</h1>'}
		return render(request,'relation.html'.encode("utf-8"),{'ctx':ctx})

	return render(request,'relation.html'.encode("utf-8"),{'ctx':ctx})
