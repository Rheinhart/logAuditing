# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from logRefresh import *
from ticketCheck import PinnacleCheck,ZhiboCheck,SboCheck,loadAccount
from bs4 import BeautifulSoup
#from antiCapcha import *
import json
import ConfigParser

try:
    from django.http import JsonResponse
except ImportError:
    from .tool import JsonResponse


webInfo=loadAccount('config.ini') #load username and password
logList=[] #全局变量, 所有log中是waiting状态的数据解析后都储存在这里


def index(request):

    return render(request, 'index.html')

def ajax_refreshLog(request):

    global logList

    lRefresh = logRefresh()
    logList=lRefresh.logCheck()
    return HttpResponse(json.dumps(logList), content_type='application/json')

def ajax_check(request,num):

    """检查所有账户账单"""
    global logList

    i= int(num)

    #to find the account in the logList

    if logList[i]['Account']=='Pinnacle':
        tcheck = PinnacleCheck(webInfo['Pinnacle_username'],webInfo['Pinnacle_password'])

    elif logList[i]['Account']=='Zhibo':
        tcheck = ZhiboCheck(webInfo['Zhibo_username'],webInfo['Zhibo_password'])

    elif logList[i]['Account']=='Sbo':
        tcheck = SboCheck(webInfo['Sbo_username'],webInfo['Sbo_password'])

    logList[i]['Status'] = tcheck.ticketCheck(logList[i]['Username'],logList[i]['Ticket'])

    return HttpResponse(json.dumps(logList), content_type='application/json')


def ajax_checkAll(request, account):

    global logList

    if account == 'All':
        for log in logList:
            if log['Status'] =='Waiting':
                if log['Account'] == 'Pinnacle':
                    tcheck= PinnacleCheck(webInfo['Pinnacle_username'],webInfo['Pinnacle_password'])
                elif log['Account'] == 'Zhibo':
                    tcheck = ZhiboCheck(webInfo['Zhibo_username'],webInfo['Zhibo_password'])
                elif log['Account'] == 'Sbo':
                    tcheck = SboCheck(webInfo['Sbo_username'],webInfo['Sbo_password'])

                print 'Checking '+log['Account']+' '+log['Ticket']
                logList['Status'] = tcheck.ticketCheck(log['Username'],logList['Ticket'])

    elif account == 'Pinnacle':
        for log in logList:
            if log['Status'] == 'Waiting' and log['Account'] == 'Pinnacle':
                    print 'Checking '+log['Account']+' '+log['Ticket']
                    tcheck= PinnacleCheck(webInfo['Pinnacle_username'],webInfo['Pinnacle_password'])
                    log['Status'] = tcheck.ticketCheck(log['Username'],log['Ticket'])

    elif account == 'Zhibo':
        for log in logList:
            if log['Status'] == 'Waiting' and log['Account'] == 'Zhibo':
                    print 'Checking '+log['Account']+' '+log['Ticket']
                    tcheck = ZhiboCheck(webInfo['Zhibo_username'],webInfo['Zhibo_password'])
                    log['Status'] = tcheck.ticketCheck(log['Username'],log['Ticket'])

    elif account == 'Sbo':
        for log in logList:
            if log['Status'] == 'Waiting' and log['Account'] == 'Zhibo':
                    print 'Checking '+log['Account']+' '+log['Ticket']
                    tcheck = SboCheck(webInfo['Sbo_username'],webInfo['Sbo_password'])
                    logList['Status'] = tcheck.ticketCheck(log['Username'],logList['Ticket'])

    #缓存当前数据
    cache=open('cache.txt','w+')
    cPickle.dump(logList, cache)
    cache.close()

    return HttpResponse(json.dumps(logList), content_type='application/json')

def ajax_saveLog(request):
    """保存检查过的log文件"""

    global logList

    WAITING_STATUS = '\xd7\xb4\xcc\xac:Waiting' #Tag
    logname=datetime.date.today().strftime("%Y-%m-%d")
    newlogfile ='new_logs\\'+logname+'.log'#新log地址
    logfile = log_path + logname + '.log'
    try:
        if os.path.isfile(newlogfile):
            os.remove(newlogfile)
        log=open(logfile,'r')
        lines = log.readlines()
        for line in lines:
            line = line.split()
            if WAITING_STATUS in line:
                ticket = re.findall("\xb5\xa5\xba\xc5:(.*)",line[5])[0] #paser ticket
                for logline in logList:
                    if ticket == logline['Ticket']:
                        NEWSTATUS = (u'状态:').encode('gb2312')+logline['Status'].encode('gb2312')
                        line[6]=line[6].replace(WAITING_STATUS,NEWSTATUS)
                    else:
                        pass
            line.append('\n')
            line='\t'.join(line)
            open(newlogfile,'a+').writelines(line)
    except IOError:
        print('Log file Error!')
    finally:
        log.close()

    return HttpResponse(json.dumps(logList), content_type='application/json')

