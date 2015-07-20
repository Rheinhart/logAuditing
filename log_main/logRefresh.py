# -*- coding: utf-8 -*-
import sys
import re
import requests
import os
import time
import datetime
######
reload(sys)
######

log_path = os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))+u'\\负打负7-1'+'\\logs\\'
#log_path = os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))+'\\logs\\'
print log_path
rlist = []

class logRefresh():

    """读取log文件并解析,返回数据到rlist"""

    def __init__(self):

        self.data = {}
        self.date = datetime.date.today().strftime("%Y-%m-%d")
        self.time = ''
        self.info = '' #下注或者补单成功
        self.big = ''
        self.small=''
        self.income = 0
        self.deal = '' #成交
        self.game = ''
        self.odd = 0
        self.amount = 0
        self.ticket = 0
        self.account = 0
        self.username = ''
        self.balance = 0

    def __logcheck(self, logname, list):
        #Tag:
        ACCOUNT_PINNACLE = '\xd5\xcb\xbb\xa7:Pinnacle'  # account line[5]
        ACCOUNT_ZHIBO = '\xd5\xcb\xbb\xa7:Zhibo'  # account line[5]
        ACCOUNT_SBO = '\xd5\xcb\xbb\xa7:Sbo'  # account line[5]
        STATUS_SUCCESS = '\xd7\xb4\xcc\xac:Success'  # status line[4]
        STATUS_WAITING = '\xd7\xb4\xcc\xac:Waiting'  # status line[4]
        STATUS_REJECT = '\xd7\xb4\xcc\xac:\xd7\xa2\xd2\xe2\xb4\xcb\xb5\xa5\xb1\xbb\xbb\xae'  # 请注意！此单被划！
        WARN_SUCCESS = '\xa1\xbe\xb2\xb9\xb5\xa5\xb3' #WARN 补单成功
        INFO_SUCCESS = '\xa1\xbe\xcf\xc2\xd7\xa2\xb3' #INFO 下注成功
        DEAL_BIG = '\xb4\xf3\xc7\xf2' #成交 大球
        DEAL_SMALL = '\xd0\xa1\xc7\xf2' #成交 小球
        DEAL_HOME = '\xd6\xf7\xb6\xd3' #成交 主队
        DEAL_GUEST = '\xbf\xcd\xb6\xd3' #成交 客队
        TICKET = '\xb5\xa5\xba\xc5:'  # ticket id line[3]
        logfile = log_path + logname + '.log'
        tflag = True  # to judge if the ticket already in the list
        try:
            log = open(logfile, 'r')
            lines = log.readlines()
            hasInfo = False  # line number
            for line in lines:
                line = line.split()
                if WARN_SUCCESS in line[3] or INFO_SUCCESS in line[3]:# 判断是否为log球队信息行: info 下注成功, warn 补单
                    self.time = re.findall("([0-9]+\:[0-9]+\:[0-9]+)", line[1])[0]
                    if 'WARN' in line[2]:
                        self.income = re.findall("\xca\xd5\xc8\xeb(.*)", line[4])[0]  # paser 收入
                        #self.info =u'补单成功'
                    elif 'INFO' in line[2]:
                        self.income = re.findall("\xca\xd5\xc8\xeb:(.*)", line[4])[0]  # paser 收入
                        #self.info =u'下注成功'

                    game = re.findall("\xb6\xd3\xce\xe9:(.*)", line[5])[0]# paser 主队..and
                    games = ''
                    for i in range(6, len(line)-4):  # 合并比赛队伍到一个value
                        games +=' '+str(line[i])
                    self.game = game+games
                    self.prelevel = re.findall("\xd4\xa4\xc6\xda\xcb\xae\xce\xbb:(.*)", line[-4])[0]  # paser 预期水位
                    self.big = line[-2]  #paser 大或让球
                    self.small = line[-1] #paser 小或者受让

                if (ACCOUNT_PINNACLE in line) or (ACCOUNT_ZHIBO in line) or (ACCOUNT_SBO in line):
                    if STATUS_WAITING in line:
                        if DEAL_BIG in line[0]:
                            self.deal = u'大球'
                        elif DEAL_SMALL in line[0]:
                            self.deal = u'小球'
                        elif DEAL_HOME in line[0]:
                            self.deal = u'主队'
                        elif DEAL_GUEST in line[0]:
                            self.deal = u'客队'
                        self.deal += str(line[1])#成交额
                        self.odd = re.findall("\xc5\xe2\xc2\xca:(.*)", line[2])[0]  # paser 赔率
                        self.amount = re.findall("\xca\xfd\xb6\xee:(.*)", line[3])[0]  # paser 数额
                        self.score = re.findall("\xb1\xc8\xb7\xd6:(.*)", line[4])[0]  # paser 比分
                        self.ticket = re.findall("\xb5\xa5\xba\xc5:(.*)", line[5])[0]  # paser 账单
                        self.account = re.findall("\xd5\xcb\xbb\xa7:(.*)", line[7])[0]  # paser 账户
                        self.username = line[8]  # member用户名
                        self.balance = re.findall("\xd3\xe0\xb6\xee:(.*)", line[9])[0]  # paser 余额
                        self.data = {'Date':self.date, 'Time': self.time,'Game':self.game, 'Income': self.income, 'Waterlevel': self.prelevel, 'Deal': self.deal, 'Odd': self.odd,'Score':self.score, 'Amount':
                                         self.amount, 'Ticket': self.ticket, 'Status': 'Waiting', 'Account': self.account, 'Username': self.username, 'Balance': self.balance}
                        #print 'json:'
                        #print self.data
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

        print 'Checking:' + self.date
        self.__logcheck(self.date, rlist)
        return rlist


if __name__ == "__main__":

    waiting_list = []
    lRefresh = logRefresh()
    waiting_list = lRefresh.logCheck()
    #print waiting_list
