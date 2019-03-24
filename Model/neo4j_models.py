# -*- coding: utf-8 -*-
from py2neo import Graph,Node,Relationship,NodeMatcher
import re
import json
#版本说明：Py2neo v4
class Neo4j_Handle():
	graph = None
	matcher = None
	def __init__(self):
		print("Neo4j Init ...")

	def connectDB(self):
		self.graph = Graph("http://59.110.243.182:7474", username="neo4j", password="qzwkx333530")
		self.matcher = NodeMatcher(self.graph)


	def getRelType(self,answers):
		item = []
		for answer in answers:
			#print(answer)
			relname = re.findall(r".*?:(.*?) {}]->.*?",str(answer['rel']))
			if relname:
				answer['rel']['type'] = relname[0]
				item.append(answer)
			else:
				item = []
		return item

	def matchEntityItem(self,value):
		answer = self.graph.run("MATCH (entity1) WHERE entity1.name = \"" + value + "\" RETURN entity1").data()
		return answer


	def matchRelatedEntity(self,value):
		answer  = self.graph.run("match(n) where n.name =~'%s.*' return n.name,n.uuid limit 5"%(value)).data()
		if answer:
			return list(answer)
		else:
			return []


	#实体查询
	def getEntityRelationbyEntity(self,value):
		#查询实体：不考虑实体类型，只考虑关系方向
		#print("MATCH (entity1) - [rel] -> (entity2)  WHERE entity1.name = \"" + value + "\" RETURN entity1")
		answer = self.graph.run("MATCH (entity1) - [rel] -> (entity2)  WHERE entity1.name = \"" + value + "\" RETURN entity1,rel,entity2").data()
		answer = self.getRelType(answer)
		return answer


	#关系查询:实体1
	def findRelationByEntity1(self,entity1):

		answer = self.graph.run("MATCH (n1{name:\""+entity1+"\"})- [rel] -> (n2) RETURN n1,rel,n2" ).data()
		answer = self.getRelType(answer)
		return answer


	#关系查询：实体2
	def findRelationByEntity2(self,entity1):
		answer = self.graph.run("MATCH (n1)- [rel] -> (n2{name:\""+entity1+"\"}) RETURN n1,rel,n2" ).data()
		answer = self.getRelType(answer)
		return answer

	#关系查询：实体1+关系
	def findOtherEntities(self,entity,relation):
		answer = self.graph.run("MATCH (n1{name:\"" + entity + "\"})- [rel:`"+relation+"`] -> (n2) RETURN n1,rel,n2" ).data()
		answer = self.getRelType(answer)
		return answer

	#关系查询：关系+实体2
	def findOtherEntities2(self,entity,relation):
		answer = self.graph.run("MATCH (n1)- [rel:`"+relation+"`] -> (n2{name:\"" + entity + "\"}) RETURN n1,rel,n2" ).data()
		answer = self.getRelType(answer)
		return answer

	def matchShortestPath(self,entity1,entity2):
		#item = []
		#print('MATCH (p1{name:"%s"}),(p2{name:"%s"}),p=shortestpath((p1)-[r*..10]-(p2)) return r,p1,p2'%(entity1,entity2))
		answers = self.graph.run('MATCH (p1{name:"%s"}),(p2{name:"%s"}),p=shortestpath((p1)-[r*..10]-(p2)) return r'%(entity1,entity2)).data()
		
		if answers:
			items = []
			answer_lst = [str(answer) for answer in answers[0]['r']]
			for answer in answer_lst:
				print(answer)
				entity1toentity2 = re.findall(r"\((.*?)\)-\[:(.*?) {}]->\((.*?)\)",answer)[0]
				#print(entity1toentity2)
				item = {}
				item['n1'] = {}
				item['rel'] = {}
				item['n2'] = {}
				item['n1']['name'] = entity1toentity2[0]
				item['rel']['type'] = entity1toentity2[1]
				item['n2']['name'] = entity1toentity2[2]
				items.append(item)

			return items
		else:
			return answers


	#查询数据库中是否有对应的实体-关系匹配
	def findEntityRelation(self,entity1,relation,entity2):
		answer = self.graph.run("MATCH (n1{name:\"" + entity1 + "\"})- [rel:`"+relation+"`] -> (n2{name:\""+entity2+"\"}) RETURN n1,rel,n2" ).data()
		answer = self.getRelType(answer)
		return answer

	def findRelation(self,relation):
		answer = self.graph.run("MATCH (n1)-[rel:`"+relation+"`] ->(n2) return n1,rel,n2 ").data()
		answer = self.getRelType(answer)
		return answer


if __name__ == "__main__":
	import json
	db = Neo4j_Handle()
	db.connectDB()
	#print(db.getEntityRelationbyEntity("罗马帝国"))
	print(db.matchShortestPath("法国","恺撒"))
	#print(db.findEntityRelation("马略","国籍","罗马帝国"))
	#print(db.findRelation("国籍"))
	#print(db.findOtherEntities("罗马帝国","击败"))
	#print(json.dumps(db.findRelationByEntity1("罗马帝国"),ensure_ascii=False))




