# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from logRefresh import LogRefresh
from ticketCheck import PinnacleCheck,ZhiboCheck,SboCheck,load_account
import json
import cPickle
import re
import os
import datetime



webInfo = load_account('config.ini')     #load username and password
p_check = z_check = s_check = ''           #pinnacle, Zhibo, Sbo object, global
LOGLIST = []                            #global, 所有log中是waiting状态的数据解析后都储存在这里


def index(request):

    return render(request, 'index.html')

def login(request,account):
    """login"""

    global p_check, z_check, s_check

    if account == 'All':
        p_check = PinnacleCheck(webInfo['Pinnacle_username'],webInfo['Pinnacle_password'])
        z_check = ZhiboCheck(webInfo['Zhibo_username'],webInfo['Zhibo_password'])
        s_check = SboCheck(webInfo['Sbo_username'],webInfo['Sbo_password'])

    elif account == 'Pinnacle':
        p_check=PinnacleCheck(webInfo['Pinnacle_username'],webInfo['Pinnacle_password'])
    elif account == 'Zhibo':
        z_check = ZhiboCheck(webInfo['Zhibo_username'],webInfo['Zhibo_password'])
    elif account == 'Sbo':
        s_check = SboCheck(webInfo['Sbo_username'],webInfo['Sbo_password'])

    return HttpResponse(json.dumps(LOGLIST), content_type='application/json')

def ajax_refresh_log(request):

    global LOGLIST

    lRefresh = LogRefresh()
    LOGLIST=lRefresh.log_check()
    return HttpResponse(json.dumps(LOGLIST), content_type='application/json')

def ajax_check(request,num):
    """依照单号检查账户账单"""

    global LOGLIST

    i= int(num)

    #to find the account in the logList

    if LOGLIST[i]['Account'] == 'Pinnacle':
        LOGLIST[i]['Status'] = p_check.ticket_check(LOGLIST[i]['Username'],LOGLIST[i]['Ticket'])

    elif LOGLIST[i]['Account'] == 'Zhibo':
        LOGLIST[i]['Status'] = z_check.ticket_check(LOGLIST[i]['Username'],LOGLIST[i]['Ticket'])

    elif LOGLIST[i]['Account'] == 'Sbo':
        LOGLIST[i]['Status'] = s_check.ticket_check(LOGLIST[i]['Username'],LOGLIST[i]['Ticket'])

    return HttpResponse(json.dumps(LOGLIST), content_type='application/json')


def ajax_check_all(request, account):
    """检查所有账户账单"""

    global LOGLIST

    if account == 'All':
        for log in LOGLIST:
            if log['Status'] == 'Waiting':
                if log['Account'] == 'Pinnacle':
                    LOGLIST['Status'] = p_check.ticket_check(log['Username'], log['Ticket'])
                elif log['Account'] == 'Zhibo':
                    LOGLIST['Status'] = z_check.ticket_check(log['Username'], log['Ticket'])
                elif log['Account'] == 'Sbo':
                    LOGLIST['Status'] = s_check.ticket_check(log['Username'], log['Ticket'])

                print 'Checking '+log['Account']+' '+log['Ticket']

    elif account == 'Pinnacle':
        for log in LOGLIST:
            if log['Status'] == 'Waiting' and log['Account'] == 'Pinnacle':
                    print 'Checking '+log['Account']+' '+log['Ticket']
                    log['Status'] = p_check.ticket_check(log['Username'], log['Ticket'])

    elif account == 'Zhibo':
        for log in LOGLIST:
            if log['Status'] == 'Waiting' and log['Account'] == 'Zhibo':
                    print 'Checking '+log['Account']+' '+log['Ticket']
                    log['Status'] = z_check.ticket_check(log['Username'], log['Ticket'])

    elif account == 'Sbo':
        for log in LOGLIST:
            if log['Status'] == 'Waiting' and log['Account'] == 'Zhibo':
                    print 'Checking '+log['Account']+' '+log['Ticket']
                    LOGLIST['Status'] = s_check.ticket_check(log['Username'], log['Ticket'])

    #缓存当前数据
    cache=open('cache.txt','w+')
    cPickle.dump(LOGLIST, cache)
    cache.close()

    return HttpResponse(json.dumps(LOGLIST), content_type='application/json')

def ajax_save_log(request):
    """保存检查过的log文件"""

    WAITING_STATUS = '\xd7\xb4\xcc\xac:Waiting'            #Tag
    logname=datetime.date.today().strftime("%Y-%m-%d")
    newlogfile ='new_logs\\'+logname+'.log'                #新log地址
    logfile = logRefresh.log_path + logname + '.log'
    try:
        if os.path.isfile(newlogfile):
            os.remove(newlogfile)
        log=open(logfile,'r')
        lines = log.readlines()
        for line in lines:
            line = line.split()
            if WAITING_STATUS in line:
                ticket = re.findall("\xb5\xa5\xba\xc5:(.*)", line[5])[0] #paser ticket
                for logline in LOGLIST:
                    if ticket == logline['Ticket']:
                        NEWSTATUS = (u'状态:').encode('gb2312')+logline['Status'].encode('gb2312')
                        line[6]=line[6].replace(WAITING_STATUS, NEWSTATUS)
                    else:
                        pass
            line.append('\n')
            line = '\t'.join(line)
            open(newlogfile, 'a+').writelines(line)
    except IOError:
        print('Log file Error!')
    finally:
        log.close()

    return HttpResponse(json.dumps(LOGLIST), content_type='application/json')

