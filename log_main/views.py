# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from logRefresh import *
from logModify import *
from logCheck import *

try:
    from django.http import JsonResponse
except ImportError:
    from .tool import JsonResponse

import json

waiting_list=[]
lRefresh = logRefresh()

def index(request):

    return render(request, 'index.html')

def ajax_refreshLog(request):
    global waiting_list

    waiting_list=lRefresh.logCheck()
    print waiting_list
    return HttpResponse(json.dumps(waiting_list), content_type='application/json')

def ajax_check(request):
    global waiting_list

    lcheck= PinnacleCheck()
    username = ''
    password = ''
    lcheck.setInfo(username,password)
    print waiting_list
    waiting_list[0]=lcheck.logCheck(461665388)
    return HttpResponse(json.dumps(waiting_list), content_type='application/json')


def ajax_checkAll(request):
    global waiting_list
    waiting_list = []
    pinnacle = Pinnacle()
    username = ''
    password = ''

    pinnacle.setInfo(username,password)
    pinnacle.logModify()
    waiting_list = pinnacle.list
    return HttpResponse(json.dumps(waiting_list), content_type='application/json')

def ajax_dict(request):
    name_dict = {'twz': 'Love python and Django', 'zqxt': 'I am teaching Django'}
    return HttpResponse(json.dumps(name_dict), content_type='application/json')
