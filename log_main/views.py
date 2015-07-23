# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from log_refresh import LogRefresh
from ticket_check import PinnacleCheck,ZhiboCheck,SboCheck,load_account
import json
import cPickle
import re
import os
import datetime

webInfo = load_account('config.ini')       # load username and password
p_check = z_check = s_check = ''           # pinnacle, Zhibo, Sbo object, global
LOG_LIST = []                              # global, 所有log中是waiting状态的数据解析后都储存在这里


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

    return HttpResponse(json.dumps(LOG_LIST), content_type='application/json')

def ajax_refresh_log(request):

    global LOG_LIST

    rlog = LogRefresh()
    LOG_LIST = rlog.log_check()
    return HttpResponse(json.dumps(LOG_LIST), content_type='application/json')

def ajax_check(request,num):
    """依照单号检查账户账单"""

    global LOG_LIST

    i= int(num)

    #to find the account in the logList

    if LOG_LIST[i]['Account'] == 'Pinnacle':
        LOG_LIST[i]['Status'] = p_check.ticket_check(LOG_LIST[i]['Username'],LOG_LIST[i]['Ticket'])

    elif LOG_LIST[i]['Account'] == 'Zhibo':
        LOG_LIST[i]['Status'] = z_check.ticket_check(LOG_LIST[i]['Username'],LOG_LIST[i]['Ticket'])

    elif LOG_LIST[i]['Account'] == 'Sbo':
        LOG_LIST[i]['Status'] = s_check.ticket_check(LOG_LIST[i]['Username'],LOG_LIST[i]['Ticket'])

    return HttpResponse(json.dumps(LOG_LIST), content_type='application/json')


def ajax_check_all(request, account):
    """检查所有账户账单"""

    global LOG_LIST

    if account == 'All':
        for log in LOG_LIST:
            if log['Status'] == 'Waiting':
                if log['Account'] == 'Pinnacle':
                    LOG_LIST['Status'] = p_check.ticket_check(log['Username'], log['Ticket'])
                elif log['Account'] == 'Zhibo':
                    LOG_LIST['Status'] = z_check.ticket_check(log['Username'], log['Ticket'])
                elif log['Account'] == 'Sbo':
                    LOG_LIST['Status'] = s_check.ticket_check(log['Username'], log['Ticket'])

                print 'Checking '+log['Account']+' '+log['Ticket']

    elif account == 'Pinnacle':
        for log in LOG_LIST:
            if log['Status'] == 'Waiting' and log['Account'] == 'Pinnacle':
                    print 'Checking '+log['Account']+' '+log['Ticket']
                    log['Status'] = p_check.ticket_check(log['Username'], log['Ticket'])

    elif account == 'Zhibo':
        for log in LOG_LIST:
            if log['Status'] == 'Waiting' and log['Account'] == 'Zhibo':
                    print 'Checking '+log['Account']+' '+log['Ticket']
                    log['Status'] = z_check.ticket_check(log['Username'], log['Ticket'])

    elif account == 'Sbo':
        for log in LOG_LIST:
            if log['Status'] == 'Waiting' and log['Account'] == 'Zhibo':
                    print 'Checking '+log['Account']+' '+log['Ticket']
                    LOG_LIST['Status'] = s_check.ticket_check(log['Username'], log['Ticket'])

    #缓存当前数据
    cache=open('cache.txt','w+')
    cPickle.dump(LOG_LIST, cache)
    cache.close()

    return HttpResponse(json.dumps(LOG_LIST), content_type='application/json')

def ajax_save_log(request):
    """保存检查过的log文件"""

    WAITING_STATUS = '\xd7\xb4\xcc\xac:Waiting'            #Tag
    logname=datetime.date.today().strftime("%Y-%m-%d")
    newlogfile ='new_logs\\'+logname+'.log'                #新log地址
    logfile = LogRefresh.log_path + logname + '.log'
    try:
        if os.path.isfile(newlogfile):
            os.remove(newlogfile)
        log=open(logfile,'r')
        lines = log.readlines()
        for line in lines:
            line = line.split()
            if WAITING_STATUS in line:
                ticket = re.findall("\xb5\xa5\xba\xc5:(.*)", line[5])[0] #paser ticket
                for logline in LOG_LIST:
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

    return HttpResponse(json.dumps(LOG_LIST), content_type='application/json')

