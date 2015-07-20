# -*- coding: utf-8 -*-
import sys
import re
import requests
import os
import time
import datetime
import ConfigParser
from bs4 import BeautifulSoup
import json
######
reload(sys)
######


class PinnacleCheck():

    def __init__(self,username,password):

        self.login_url = 'https://aaa.pinnaclesports.com/Login.aspx'
        self.login_session = requests.Session()
        self.username = username
        self.password = password
        self.isLogin = False

        #automatic login
        self.__loginmain()
        self.__kickoff()

    def __loginmain(self):
        '''login the main page'''

        login_header = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                  'Accept-Encoding':'gzip, deflate',
                  'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
                  'Cache-Control':'max-age=0',
                  'Connection':'keep-alive',
                  'Content-Type':'application/x-www-form-urlencoded',
                  'DNT':'1',
                  'Host':'aaa.pinnaclesports.com',
                  'Origin':'https://aaa.pinnaclesports.com',
                  'Referer':'https://aaa.pinnaclesports.com/Login.aspx',
                  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}


        postData = {'__VIEWSTATE':'/wEPDwUINDc3MzExNzIPZBYCAgMPZBYCAgEPZBYCAgMPEGQPFgECBxYBEAUEVGhhaQUCdGhnFgFmZGRevYPRLil7tSWwrGv94kOQWgS/Z/UdYWX+2Psw3JdwrQ==',
            '__VIEWSTATEGENERATOR':'C2EE9ABB',
            '__EVENTVALIDATION':'/wEdAA0XhIbGiuWL6wNXsuKKNl9+zyjSCk071VEBFi+Pn+x7Vbskj2bYtjy6x+ok0AhsxbmaWJgNYxXDKJmfHo3SUAtyDajVEjtqqAB+Fe3DJW2ReMqDhLSZLEX/ZvMqb4F5bexjIsOsOCcsfe6l6fcRigHQEAWAfkf0gHlvWmxI/1mZHAgsYlVDpoodEWRg9RRToQqwRQmdYVIGdQOw5ctONxUqR1LBKX1P1xh290RQyTesRVwK8/1gnn25OldlRNyIednDbiWC8p5oWQ9KZC32jRIUQPgwUS8va+KcSB9QJ0dkZouFlD3gerUhEyV9P/WYD/o=',
            'UPBF$LDDL':'en-GB',
            'UserName': self.username,
            'Password': self.password,
            'LB':'Login'}
        try:
            req = self.login_session.post(self.login_url, postData,headers=login_header)

        except Exception, e:
            print 'login fail: ', e
            return False

    def __kickoff(self):
        '''kick off other user and continue'''

        login_header = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                  'Accept-Encoding':'gzip, deflate',
                  'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
                  'Cache-Control':'max-age=0',
                  'Connection':'keep-alive',
                  'Content-Type':'application/x-www-form-urlencoded',
                  'DNT':'1',
                  'Host':'aaa.pinnaclesports.com',
                  'Origin':'https://aaa.pinnaclesports.com',
                  'Referer':'https://aaa.pinnaclesports.com/Login.aspx',
                  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}


        kickoff_url = 'https://aaa.pinnaclesports.com/AlreadyLoggedIn.aspx'

        postData = {'__VIEWSTATE':'/wEPDwULLTEzMDIzODIwMTNkZOmQJfUJyJT5fL5xtNAp2w1JEhyndb8AJjxA3GoJBox8',
        '__VIEWSTATEGENERATOR':'9461229B',
        '__EVENTVALIDATION':'/wEdAAXI5Cf5IjAXLSFBNsvmq/sRUbCimvzN/TczT4kz9qKpYnFNg25++/wnLLvx/zMOPgtg4wULag6puEpGFyFXlupb70/AcP6TbUveJn5MuDyMx7c9aL0zH/wbg+CtvVsRp1Fi1jTGdqVURYr7DEN6f2Fe',
        'LIHF': self.username,
        'LPHF': self.password,
        'COB':'Continue'}
        try:

            req = self.login_session.post(kickoff_url, postData,headers=login_header)
            self.pinnacle_balance = str(req.content)

            tag = 'Yesterday Total Balance'
            if  re.search(tag,self.pinnacle_balance):
                #login successful
                self.isLogin = True
                print 'Pinnacle login successful!\n'
                return True
            else:
                #login failure
                print 'login failure!\n'
                return False

            #req.close()
        except Exception, e:
            print 'login fail: ', e
            return False

    def __findticket(self,ticket):

        header = {'Content-Type':'application/x-www-form-urlencoded',
                  'Host':'aaa.pinnaclesports.com',
                  'Origin':'https://aaa.pinnaclesports.com',
                  'Referer':'https://aaa.pinnaclesports.com/FindTicket/FindTicket',
                  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}


        findticket_url = 'https://aaa.pinnaclesports.com/AlreadyLoggedIn.aspx'

        postData = {'__VIEWSTATE':'/wEPDwULLTEzMDIzODIwMTNkZA==',
                    'txtTicketNo':ticket,
                    'LDDL':'en-GB',
                    '__VIEWSTATEGENERATOR':'9461229B'}

        try:
            req = self.login_session.post(findticket_url, postData,headers=header)

            ticketinfo_url='https://aaa.pinnaclesports.com/Wagers/SearchTicket/'+str(ticket)
            ticketinfo = self.login_session.get(ticketinfo_url)
            tagIsTicket='Trans\.'
            tagHasNo = 'No data to display'
            tagReject ='Rejected'
            tagWaiting = 'Waiting'
            tagWin = 'Win'
            tagLoss = 'Loss'
            tagPending = 'Pending'
            isticket=re.findall(tagIsTicket,ticketinfo.content)
            if isticket:
                hasNo=re.findall(tagHasNo,ticketinfo.content)
                hasRejected=re.findall(tagReject,ticketinfo.content)
                hasSuccess = re.findall(tagWin,ticketinfo.content) or re.findall(tagLoss,ticketinfo.content) or re.findall(tagPending,ticketinfo.content)
                #hasWaiting = re.findall(tagWaiting,ticketinfo.content)
                if hasNo:
                      tag = 'no ticket'
                      return u'没有此单'
                else:
                    if hasRejected:
                        tag = str(ticket)+' has been rejected!'
                        return u'此单已划!'
                    elif hasSuccess:
                        tag = str(ticket)+' is Successfu!'
                        return 'Success'
                    else:
                        tag = str(ticket)+' is waiting!'
                        return 'Waiting'

            else:
                tag = 'not Pinnacle\'s ticket'
                return u'没有此单'
            print tag
        except Exception, e:
            print e
            return False

    def ticketCheck(self,nickname,ticket):

        try:
            checkT=self.__findticket(ticket)
            #print checkT
            return checkT
        except:
            return False


class ZhiboCheck():

    capchapage = "http://isn999.com/managersite/login/captcha"
    loginpage = "http://isn999.com/managersite/login/auth"
    outstandingpage = "http://isn999.com/managersite/betList/outstanding?userCode=%user%&winid=betList"
    finduserpage = "http://isn999.com/managersite/agentListing/list?_=1436537609675&loginLocale=ZH&parentCode=J102020I01T7&searchStatus=0&searchUserLevel=-1"
    refererpage = "http://isn999.com/managersite/login/manager?referAction=index"

    def __init__(self,username,password):
        self.web = requests.session()
        self.username = username
        self.password = password

    def __login(self):
        headerDict = {
            'Referer': 'Referer: ' + self.refererpage,
        }
        #Download the capcha image and decode by the dll
        r = self.web.get(self.capchapage,headers=headerDict)
        with open("Zhibo_capcha.jpg","wb") as output:
            output.write(r.content)
        output.close()
        os.startfile("Zhibo_capcha.jpg")
        #cap = antiCapcha.GetCode("capcha.jpg")
        cap = raw_input("please input the capcha:")
        #Login
        postDict = {
            'languageSelection':'2',
            'loginUsername': self.username,
            'loginPassword': self.password,
            'captcha':cap,
            'source':'managerSite',
        }
        r = self.web.post(self.loginpage,data=postDict,headers=headerDict)
        j = json.loads(r.text)
        if j.has_key('success'):
            #pass
            print "Login successful"
            return True
        elif j.has_key('errors'):
            print j['errors']['reason']
            return False
        else:
            print "Unknown error:"
            #print r.text
            return False

    def __finduser(self,nickname):
        #find the username according to the nickname
        user={"nickname":"","username":""}
        r = self.web.get(self.finduserpage)
        #print r.content
        soup = BeautifulSoup(r.text)
        my=soup.findAll("td",attrs={"class":"table-icon-cell"})
        for item in my:
            user['nickname']=re.findall(r'\bdata\-detail=\"[0-9a-zA-Z]*\-[0-9a-zA-Z]*\-(.*)\"\sonclick',str(item))[0]
            if user['nickname']==nickname:
                user['username']=re.findall(r'data\-detail=\"(.*)\-[0-9a-zA-Z]*\-[0-9a-zA-Z]*',str(item))[0]
                print user['nickname']+": "+user['username']+' found'
                return user['username']

        if not user['username']:
            print "<%s> has no corresponding username" % nickname
            return user['username']


    def __findticket(self, user, ticket_No):
        # Browse to the user page according to the user given
        r = self.web.get(self.outstandingpage.replace("%user%", user))
        for resp in r.history:
            if resp.status_code != requests.codes.ok:
                print "User <%s> not found" % user
                return u'无此用户'
        soup = BeautifulSoup(r.text)
        my_table = soup.find('table',id="tblBetList")
        rows = my_table.findChildren('tr')
        # The first row is the header and the last row is a hidden row
        rows = rows[1:-1]
        tickets = []
        for row in rows:
            # Parse the column one by one
            cells = row.findChildren('td')
            ticket = {}
            ticket['id'] = cells[0].text
            ticket['userid'] = cells[1].text
            ticket['username'] = cells[2].text
            # Slice the string to get the required text
            tmp = str(cells[3])
            ticket['ticketno'] = tmp[tmp.find(':')+1 : tmp.find('<br/>')]
            ticket['details'] = cells[4].text
            tmp = str(cells[5])
            ticket['odds'] = tmp[tmp.find('>')+1 : tmp.find('<br/>')]
            tmp = str(cells[6])
            ticket['amount'] = tmp[tmp.find('>')+1 : tmp.find('<br/>')]
            tmp = str(cells[7])
            ticket['status'] = tmp[tmp.find('>')+1 : tmp.find('<br/>')]
            tickets.append(ticket)
        # Search the tickets to match the ticket number
        for t in tickets:
            if t['ticketno'] == ticket_No:
                return 'Success'
        print "Ticket <%s> not found" % ticket_No
        return u'没有此单'

    def ticketCheck(self,nickname,ticket):

        r=self.__login()
        if r:
            try:
                user=self.__finduser(nickname)
                if user:
                    checkT=self.__findticket(user,ticket)
                    return checkT
            except:
                return False


class SboCheck():

    domain = "https://agent.sbobet.com/"
    subdomain = ""
    mainpage = "https://agent.sbobet.com/default.aspx?lang=en"
    imgtextpage = "https://agent.sbobet.com/ImgTextRefresh.aspx"
    loginpage = "https://agent.sbobet.com/processlogin.aspx?lang=EN"
    refererpage = "https://agent.sbobet.com/default.aspx?lang=en"


    def __init__(self,username,password):

        self.web = requests.session()
        self.username = username
        self.password = password
        self.login()


    def login(self):
        headerDict = {
            'Referer': 'Referer: ' + self.refererpage,
        }
        r = self.web.get(self.mainpage,headers=headerDict)
        #Get the img src hidden in ImgTextRefresh.aspx
        r = self.web.get(self.imgtextpage,headers=headerDict)
        pos1 = r.text.find("imgtext")
        pos2 = r.text.find("default") + len("default")
        capcha = self.domain +  r.text[pos1:pos2]
        r = self.web.get(capcha,headers=headerDict)
        with open("Sbo_capcha.jpg","wb") as output:
            output.write(r.content)
        output.close()
        os.startfile("Sbo_capcha.jpg")
        print "enter captcha:"
        cap = input()
        postDict = {
            'hiduseDesktop':'no',
            'username': self.username,
            'password': self.password,
            'vcode':cap,
            'lang':'en',
        }
        r = self.web.post(self.loginpage,data=postDict,headers=headerDict)
        for resp in r.history:
            if resp.status_code != requests.codes.ok:
                print "Login failed (Wrong login info or verification is required)"
                return None
        #Get the params hidden in processlogin.aspx
        soup = BeautifulSoup(r.text)
        actionpage = soup.find("form", {"id":"f"})["action"]
        self.subdomain = actionpage[0:actionpage.find("welcome")]
        myid = soup.find("input", {"name":"id"})["value"]
        mykey = soup.find("input", {"name":"key"})["value"]
        getDict = {
            'id' : myid,
            'key' : mykey,
            'useDesktop' : 'no',
            'lang' : 'en'

        }
        welcomepage = self.subdomain + "welcome.aspx"
        #Redirect to the welcome page to get cookies
        r = self.web.get(welcomepage,params=getDict,headers=headerDict)
        print "Login successful"

    def getTicket(self, user, ticket_No):
        headerDict = {
            'Referer': 'Referer: ' + self.refererpage,
        }
        #Go to this page to get post params requried
        ospage1 = self.subdomain + "webroot/restricted/totalbet2/outstanding_new.aspx"
        r = self.web.get(ospage1,headers=headerDict)
        soup = BeautifulSoup(r.text)
        myids = soup.find("input", {"name":"ids"})["value"]
        myek = soup.find("input", {"name":"ek"})["value"]
        myp = soup.find("input", {"name":"p"})["value"]
        postDict = {
            'ids': myids,
            'ek': myek,
            'p': myp,
            'product': '1'
        }
        #Go to this page to get the list of user sid
        ospage2 = self.subdomain + "webroot/restricted/totalbet2/outstanding_frame_new.aspx"
        r = self.web.post(ospage2,data=postDict,headers=headerDict)
        SID = self.searchSID(r.text, user)
        if SID == None:
            print "User <%s> not found" % user
            return None
        postDict = {
            'ids': SID,
            'ek': myek,
            'p': myp,
            'prodcut': '1'
        }
        #Go to this page to get the list of ticket
        ospage3 = self.subdomain + "webroot/restricted/totalbet2/betlist_frame.aspx"
        r = self.web.post(ospage3,data=postDict,headers=headerDict)
        ticket = self.searchTicket(r.text, ticket_No)
        if ticket == None:
            print "Ticket <%s> not found" % ticket_No
            return None
        return ticket

    def searchSID(self, text, user):
        #Search User SID (changed everytime) from the user list table
        pos1 = text.find(user)
        #Return -1 if user cannot be found
        if pos1 < 0:
            return None
        pos2 = text.rfind("'r',",0,pos1) + 4
        pos3 = text.find(",", pos2)
        SID = text[pos2:pos3]
        return SID

    def searchTicket(self, text, ticket_No):
        #Search ticket info from the ticket list table
        pos1 = text.find(ticket_No)
        #Return -1 if ticket cannot be found
        if pos1 < 0:
            return None
        pos2 = text.rfind("f(",0,pos1) + 2
        pos3 = text.find(")", pos2)
        ticketStr = text[pos2:pos3].replace("'",'"')
        rawArray = json.loads(ticketStr)
        ticket = {
            "Type" : rawArray[2][3]
            , "Ratio" : rawArray[10]
            , "Amount" : rawArray[12]
            , "Status" : rawArray[14]
            , "TicketNo" : rawArray[5]
            , "User" : rawArray[4]
        }
        return ticket

def loadAccount(cfile):
    aList={}
    try:
        config=ConfigParser.SafeConfigParser()
        config.read(cfile)
        aList['Pinnacle_username'] = config.get('Pinnacle','Username')
        aList['Pinnacle_password'] = config.get('Pinnacle','Password')
        aList['Zhibo_username'] = config.get('Zhibo','Username')
        aList['Zhibo_password'] = config.get('Zhibo','Password')
        aList['Sbo_username'] = config.get('Sbo','Username')
        aList['Sbo_password'] = config.get('Sbo','Password')
        return aList
    except Exception, e:
        print 'read config.ini error'
        return False
