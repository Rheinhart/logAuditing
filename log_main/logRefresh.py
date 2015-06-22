# -*- coding: utf-8 -*-
import sys
import re
import requests
import os
import time
import datetime

log_path = sys.path[0]+'\\logs\\'
list = []
class logRefresh():

        """Automatically get the data of Balance Sheet"""
        def __init__(self):

            self.dict ={'时间':'','队伍':'',}

        def _logcheck(self,logname,list):

            ACCOUNT_PINNACLE= '\xd5\xcb\xbb\xa7:Pinnacle' #account line[5]
            STATUS_SUCCESS ='\xd7\xb4\xcc\xac:Success'  #status line[4]
            STATUS_WAITING ='\xd7\xb4\xcc\xac:Waiting'  #status line[4]
            STATUS_REJECT ='\xd7\xb4\xcc\xac:\xd7\xa2\xd2\xe2\xb4\xcb\xb5\xa5\xb1\xbb\xbb\xae' #请注意！此单被划！
            TICKET = '\xb5\xa5\xba\xc5:' #ticket id line[3]
            #self.login_name = '' #line[6]
            logfile=log_path+logname+'.log'
            #newlogfile = re.findall(r'(.*)\.log',logname)[0]+'m.log'
            try:
                log=open(logfile,'r')
                lines =  log.readlines()
                for line in lines:
                    line = line.split()
                    if ACCOUNT_PINNACLE in line:
                        if STATUS_WAITING in line:
                            #print line
                            ticket = re.findall("\xb5\xa5\xba\xc5:(.*)",line[3])[0] #paser ticket
                            if ticket not in list:
                                list.append(ticket)
                                #print waiting_list
                    line.append('\n')
                    line='\t'.join(line)

                return True

            except IOError:
                print('File Error!')
            finally:
                log.close()

        def logCheck(self):
            data = datetime.date.today().strftime("%Y-%m-%d")
            log = data
            try:
                print 'Checking:'+log
                self._logcheck(log,list)
                return list
            except:
                return False






