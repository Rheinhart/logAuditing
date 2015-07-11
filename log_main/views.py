# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from logRefresh import *
from ticketCheck import PinnacleCheck,ZhiboCheck,SboCheck
from bs4 import BeautifulSoup
#from antiCapcha import *
import json

try:
    from django.http import JsonResponse
except ImportError:
    from .tool import JsonResponse

logList=[]
webInfo={'Pinnacle_username':'CK8T720','Pinnacle_passowrd':'','Zhibo_username':'j102020i01t7sub00','Zhibo_password':'','Sbo_username':'eehet711','Sbo_passowrd':''}

def index(request):

    return render(request, 'index.html')

def ajax_refreshLog(request):

    global logList

    lRefresh = logRefresh()
    logList=lRefresh.logCheck()
    return HttpResponse(json.dumps(logList), content_type='application/json')

def ajax_check(request,num):

    global logList

    i= int(num)

    #to judge the account in the logList

    if logList[i]['Account']=='Pinnacle':
        tcheck = PinnacleCheck(webInfo['Pinnacle_username'],webInfo['Pinnacle_passowrd'])
        logList[i]['Status'] = tcheck.ticketCheck(logList[i]['Ticket'])

    elif logList[i]['Account']=='Zhibo':
        tcheck =  ZhiboCheck(webInfo['Zhibo_username'],webInfo['Zhibo_password'])
        logList[i]['Status'] = tcheck.ticketCheck(logList[i]['Username'],logList[i]['Ticket'])

    elif logList[i]['Account']=='Sbo':
        tcheck =  Sbo(webInfo['Sbo_username'],webInfo['Sbo_password'])
        #logList[i]['Status'] = tcheck.ticketCheck(logList[i]['Username'],logList[i]['Ticket'])

    return HttpResponse(json.dumps(logList), content_type='application/json')


def ajax_checkAll(request):

    global logList

    for log in logList:
        if log['Status']=='Waiting':
            if log['Account']=='Pinnacle':
                print 'Checking '+log['Account']+' '+log['Ticket']
                tcheck= PinnacleCheck(webInfo['Pinnacle_username'],webInfo['Pinnacle_passowrd'])
                log['Status'] = tcheck.ticketCheck(log['Ticket'])
            elif log['Account']=='Zhibo':
                print 'Checking '+log['Account']+' '+log['Ticket']
                tcheck =  ZhiboCheck(webInfo['Zhibo_username'],webInfo['Zhibo_password'])
                log['Status'] = tcheck.ticketCheck(log['Username'],log['Ticket'])
            elif logList[i]['Account']=='Zhibo':
                print 'Checking '+log['Account']+' '+log['Ticket']
                tcheck =  Sbo(webInfo['Sbo_username'],webInfo['Sbo_password'])
                #logList[i]['Status'] = tcheck.ticketCheck('J102020I01T7103',logList[i]['Ticket'])

    cache=open('cache.txt','w+')
    cPickle.dump(logList, cache)
    cache.close()

    return HttpResponse(json.dumps(logList), content_type='application/json')
