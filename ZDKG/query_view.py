# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

from ZDJ.QA.MainProgram import run
import json

#问题查询
def query(request):
    ctx = {}
    #根据传入的实体名称搜索出关系
    if(request.GET):
        query = request.GET['query']
        answer = run(query)
        if len(answer) == 0:
            #若数据库中无法找到该实体，则返回数据库中无该实体
            ctx= {'title' : '<h2>暂未查到答案</h1>'}
            return render(request,'query.html'.encode("utf-8"),{'ctx':json.dumps(ctx,ensure_ascii=False)})
        else:
           

            return render(request,'query.html'.encode("utf-8"),{'answer':answer,'query':query})
    #需要进行类型转换
    return render(request,"query.html".encode("utf-8"),{'ctx':ctx})


 
