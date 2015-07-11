# -*- coding: utf-8 -*-
import sys
import re
import requests
import os
import time
import datetime
import cPickle
######
reload(sys)
######

log_path = os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))+u'\\负打负更新'+'\\logs\\'
print log_path
rlist = []

class logRefresh():

    """Automatically get the data of Balance Sheet"""

    def __init__(self):

        self.data = {}
        self.date = datetime.date.today().strftime("%Y-%m-%d")
        self.time = ''
        self.info = ''
        self.income = u'读取错误'
        self.bigdeal = 0
        self.smalldeal = 0
        self.deal = ''
        self.game = ''
        self.odd = 0
        self.amount = 0
        self.ticket = 0
        self.account = 0
        self.username = ''
        self.balance = 0

    def __logcheck(self, logname, list):

        ACCOUNT_PINNACLE = '\xd5\xcb\xbb\xa7:Pinnacle'  # account line[5]
        ACCOUNT_ZHIBO = '\xd5\xcb\xbb\xa7:Zhibo'  # account line[5]
        ACCOUNT_SBO = '\xd5\xcb\xbb\xa7:Sbo'  # account line[5]
        STATUS_SUCCESS = '\xd7\xb4\xcc\xac:Success'  # status line[4]
        STATUS_WAITING = '\xd7\xb4\xcc\xac:Waiting'  # status line[4]
        STATUS_REJECT = '\xd7\xb4\xcc\xac:\xd7\xa2\xd2\xe2\xb4\xcb\xb5\xa5\xb1\xbb\xbb\xae'  # 请注意！此单被划！
        TICKET = '\xb5\xa5\xba\xc5:'  # ticket id line[3]
        # self.login_name = '' #line[6]
        logfile = log_path + logname + '.log'
        tflag = True  # to judge if the ticket already in the list
        try:
            log = open(logfile, 'r')
            lines = log.readlines()
            hasInfo = False  # line number
            for line in lines:
                line = line.split()
                if 'INFO' in line:  # 判断是否为log球队信息行: info 下注成功, warn 补单
                    length = len(line)
                    if length > 4:
                        #print line
                        self.income = re.findall(
                            "\xca\xd5\xc8\xeb:(.*)", line[4])[0]  # paser 收入
                        # paser 主队..and
                        game = re.findall("\xb6\xd3\xce\xe9:(.*)", line[5])[0]
                        for i in range(6, length - 2):  # 合并比赛队伍到一个value
                            self.game = game + ' ' + str(line[i])
                        self.info = self.game
                        self.prelevel = re.findall("\xd4\xa4\xc6\xda\xcb\xae\xce\xbb:(.*)", line[-2])[0]  # paser 预期水位

                if 'WARN' in line:  # 判断是否为log球队信息行: info 下注成功, warn 补单
                    #print line
                    self.info=' '.join(line[5:-2])
                    self.time = line[1]
                    length = len(line)
                    if length > 4:
                        #print line
                        self.prelevel = re.findall("\xd4\xa4\xc6\xda\xcb\xae\xce\xbb:(.*)", line[-2])[0]  # paser 预期水位

                if (ACCOUNT_PINNACLE in line) or (ACCOUNT_ZHIBO in line) or (ACCOUNT_SBO in line):
                    if STATUS_WAITING in line:
                        #print line
                        self.bigdeal = re.findall("\xb3\xc9\xbd\xbb:\xb4\xf3(.*)", line[0])  # paser 大成交
                        self.smalldeal = re.findall("\xb3\xc9\xbd\xbb:\xd0\xa1(.*)", line[0])  # paser 小成交
                        self.odd = re.findall("\xc5\xe2\xc2\xca:(.*)", line[1])[0]  # paser 赔率
                        self.amount = re.findall("\xca\xfd\xb6\xee:(.*)", line[2])[0]  # paser 数额
                        self.ticket = re.findall("\xb5\xa5\xba\xc5:(.*)", line[3])[0]  # paser 张单
                        self.account = re.findall("\xd5\xcb\xbb\xa7:(.*)", line[5])[0]  # paser 账户
                        self.username = line[6]  # member用户名
                        self.balance = re.findall("\xd3\xe0\xb6\xee:(.*)", line[7])[0]  # paser 余额
                        if self.bigdeal:
                            self.deal = u'大' + self.bigdeal[0]
                        elif self.smalldeal:
                            self.deal = u'小' + self.smalldeal[0]
                        self.data = {'Date':self.date, 'Time': self.time,'Info':self.info, 'Income': self.income, 'Waterlevel': self.prelevel, 'Deal': self.deal, 'Odd': self.odd, 'Amount':
                                         self.amount, 'Ticket': self.ticket, 'Status': 'Waiting', 'Account': self.account, 'Username': self.username, 'Balance': self.balance}

                        for var in list:
                            if var['Ticket'] == self.ticket:
                                tflag = False
                        if tflag:
                            list.append(self.data)
                        tflag = True


            return True

        except IOError:
            print('File Error!')
            return False
        finally:
            log.close()

    def logCheck(self):

        try:
            print 'Checking:' + self.date
            self.__logcheck(self.date, rlist)
            return rlist
        except:
            print ' Open Log file false!'
            return False

if __name__ == "__main__":

    waiting_list = []
    lRefresh = logRefresh()
    waiting_list = lRefresh.logCheck()
    #print waiting_list
