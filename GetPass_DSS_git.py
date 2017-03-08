#coding=utf-8

import re
import cookielib
import urllib
import urllib2
import csv
from bs4 import BeautifulSoup
import re
import time

def make_cookie(name,value):
    return cookielib.Cookie(
        version=0,
        name=name,
        value=value,
        port=None,
        port_specified=False,
        domain="ip",
        domain_specified=True,
        domain_initial_dot=False,
        path="/",
        path_specified=True,
        secure=False,
        expires=None,
        discard=False,
        comment=None,
        comment_url=None,
        rest=None
        )
#利用cookielib自动管理cookies
cj = cookielib.CookieJar()
cj.set_cookie(make_cookie("xxx_password","xxx"))
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
#根据抓包，用到的urls
LoginURL = "http://ip/admin/login_login.action"
InfoUrl = "http://ip/admin/device/encoder_edit.action?id=2000"
#用户名，密码。幸亏没有验证码
username = "xxx"
passwd = "xxx"
#根据抓包，POST数据时的body如下
PostDict = {
    "userBean.loginName" : username,
    "userBean.loginPass" : passwd
    }
#将post时的body转码
PostData = urllib.urlencode(PostDict)
#先request，再response，最后获取cookie的JSESSIONID
req_LoginURL = urllib2.Request(LoginURL,PostData)
# req_LoginURL.add_header('Accept-Language', "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3")
resp_LoginURL = urllib2.urlopen(req_LoginURL)
html_LoginURL = resp_LoginURL.read()
#print html_LoginURL
#这是URL是返回整体设备列表的POST地址
MainUrl = "http://ip/admin/device/encoder_updatePaginationTable.action?nowTime="+str(long(1000 * time.time()))

#以下计算总共有763条记录，共43页，前42页每页18条数据，第43页有7条数据
PostDict = {
            "paginationParams.componentParams[0]":"001",
            "paginationParams.componentParams[1]": "",
            "paginationParams.componentParams[2]": "",
            "paginationParams.componentParams[3]": "",
            "paginationParams.componentParams[4]": "",
            "paginationParams.componentParams[5]": "0",
            "paginationParams.componentParams[6]": "",
            "paginationParams.pagesCount": "43",#这是以IP分类的设备的总页数
            "paginationParams.pageSize": "18",
            "paginationParams.updatedPage":2,#这是以IP分类的设备的当前页数
            "paginationParams.updatePage":"true"
        }

PostData = urllib.urlencode(PostDict)
req_MainUrl = urllib2.Request(MainUrl, PostData)
resp_MainUrl = urllib2.urlopen(req_MainUrl)
html_MainUrl = BeautifulSoup(resp_MainUrl, 'html.parser')

ip_total_record = int(html_MainUrl.select('.paginationTable > .page > span')[0].string)

ip_int_page = ip_total_record / 18
ip_total_page = ip_int_page + 1
ip_range = ip_total_page + 1
ip_alone_page_num = ip_total_record % 18
ip_alone_page_range = ip_alone_page_num + 1

#将所有763条数据抓取出来写入csv文件中
with open('ip.csv', 'wb') as f:
    csv_writer = csv.writer(f, delimiter=',')
    for ipid in range(1,ip_range):
        PostDict = {
            "paginationParams.componentParams[0]":"001",
            "paginationParams.componentParams[1]": "",
            "paginationParams.componentParams[2]": "",
            "paginationParams.componentParams[3]": "",
            "paginationParams.componentParams[4]": "",
            "paginationParams.componentParams[5]": "0",
            "paginationParams.componentParams[6]": "",
            "paginationParams.pagesCount": "43",#这是以IP分类的设备的总页数
            "paginationParams.pageSize": "18",
            "paginationParams.updatedPage":ipid,#这是以IP分类的设备的当前页数
            "paginationParams.updatePage":"true"
        }

        PostData = urllib.urlencode(PostDict)
        req_MainUrl = urllib2.Request(MainUrl, PostData)
        resp_MainUrl = urllib2.urlopen(req_MainUrl)
        html_MainUrl = BeautifulSoup(resp_MainUrl, 'html.parser')

        encoder_list = html_MainUrl.select('.paginationTable > .listdiv')
        if ipid <= ip_int_page:
            for encoder in encoder_list:
                    for i in range(1,19):
                        encoder_code = encoder.select('.encoder_code > span')[i].string
                        encoder_ip = encoder.select('.encoder_ip > span')[i].string
                        encoder_name = encoder.select('.encoder_name > span')[i].string
                        encoder_orgName = encoder.select('.encoder_orgName > span')[i].string
                        encoder_id = encoder.select('.operation > .editLink ')[i-1]['href'][76:-4]

                        InfoUrl = 'http://ip/admin/device/encoder_edit.action?id=%d' % int(encoder_id)
                        resp_InfoUrl = urllib2.urlopen(InfoUrl)
                        html_InfoUrl = resp_InfoUrl.read()
                        ipPort = re.findall(r'"deviceBean.ipPort" value="(.*?)"', html_InfoUrl)
                        loginName = re.findall(r'"deviceBean.loginName" value="(.*?)"',html_InfoUrl)
                        loginPass = re.findall(r'"deviceBean.loginPass" value="(.*?)"',html_InfoUrl)
                        channelsCount = re.findall(r'"deviceBean.encoderUnits\[0\].channelsCount" value="(.*?)"',html_InfoUrl)
                        if len(ipPort) == 1 and len(loginName)==1 and len(loginPass) == 1 and len(channelsCount) == 1:
                            print "开始抓取 IP分类 第",ipid,"页第",i,"条数据 ... ... ..."
                            csv_writer.writerow([encoder_id, encoder_ip, ipPort[0], loginName[0], loginPass[0],channelsCount[0] ,encoder_name, encoder_orgName])
                            print "结束抓取 IP分类 第", ipid, "页第", i, "条数据 ... ... ..."
        if ipid == ip_total_page:
            for encoder in encoder_list:
                for i in range(1, ip_alone_page_range):
                    encoder_code = encoder.select('.encoder_code > span')[i].string
                    encoder_ip = encoder.select('.encoder_ip > span')[i].string
                    encoder_name = encoder.select('.encoder_name > span')[i].string
                    encoder_orgName = encoder.select('.encoder_orgName > span')[i].string
                    encoder_id = encoder.select('.operation > .editLink ')[i - 1]['href'][76:-4]

                    InfoUrl = 'http://ip/admin/device/encoder_edit.action?id=%d' % int(encoder_id)
                    resp_InfoUrl = urllib2.urlopen(InfoUrl)
                    html_InfoUrl = resp_InfoUrl.read()
                    ipPort = re.findall(r'"deviceBean.ipPort" value="(.*?)"', html_InfoUrl)
                    loginName = re.findall(r'"deviceBean.loginName" value="(.*?)"', html_InfoUrl)
                    loginPass = re.findall(r'"deviceBean.loginPass" value="(.*?)"', html_InfoUrl)
                    channelsCount = re.findall(r'"deviceBean.encoderUnits\[0\].channelsCount" value="(.*?)"',
                                               html_InfoUrl)
                    if len(ipPort) == 1 and len(loginName) == 1 and len(loginPass) == 1 and len(channelsCount) == 1:
                        print "开始抓取 IP分类 第", ipid, "页第", i, "条数据 ... ... ..."
                        csv_writer.writerow(
                            [encoder_id, encoder_ip, ipPort[0], loginName[0], loginPass[0], channelsCount[0],
                             encoder_name, encoder_orgName])
                        print "结束抓取 IP分类 第", ipid, "页第", i, "条数据 ... ... ..."

# 获取IR类型的1028条数据，共58页，前57页，每页18条数据，第58页有2条数据
PostDict = {
            "paginationParams.componentParams[0]":"001",
            "paginationParams.componentParams[1]": "",
            "paginationParams.componentParams[2]": "",
            "paginationParams.componentParams[3]": "",
            "paginationParams.componentParams[4]": "",
            "paginationParams.componentParams[5]": "6",
            "paginationParams.componentParams[6]": "",
            "paginationParams.pagesCount": "58",#这是以IP分类的设备的总页数
            "paginationParams.pageSize": "18",
            "paginationParams.updatedPage":2,#这是以IP分类的设备的当前页数
            "paginationParams.updatePage":"true"
        }

PostData = urllib.urlencode(PostDict)
req_MainUrl = urllib2.Request(MainUrl, PostData)
resp_MainUrl = urllib2.urlopen(req_MainUrl)
html_MainUrl = BeautifulSoup(resp_MainUrl, 'html.parser')

IR_total_record = int(html_MainUrl.select('.paginationTable > .page > span')[0].string)

IR_int_page = IR_total_record / 18
IR_total_page = IR_int_page + 1
IR_range = IR_total_page + 1
IR_alone_page_num = IR_total_record % 18
IR_alone_page_range = IR_alone_page_num + 1


with open('Initiative_registration.csv', 'wb') as f:
    csv_writer = csv.writer(f, delimiter=',')
    for IRid in range(1,IR_range):
        PostDict = {
            "paginationParams.componentParams[0]":"001",
            "paginationParams.componentParams[1]": "",
            "paginationParams.componentParams[2]": "",
            "paginationParams.componentParams[3]": "",
            "paginationParams.componentParams[4]": "",
            "paginationParams.componentParams[5]": "6",
            "paginationParams.componentParams[6]": "",
            "paginationParams.pagesCount": "58",#这是以IP分类的设备的总页数
            "paginationParams.pageSize": "18",
            "paginationParams.updatedPage":IRid,#这是以IP分类的设备的当前页数
            "paginationParams.updatePage":"true"
        }

        PostData = urllib.urlencode(PostDict)
        req_MainUrl = urllib2.Request(MainUrl, PostData)
        resp_MainUrl = urllib2.urlopen(req_MainUrl)
        html_MainUrl = BeautifulSoup(resp_MainUrl, 'html.parser')
        encoder_list = html_MainUrl.select('.paginationTable > .listdiv')

        if IRid <= IR_int_page:
            for encoder in encoder_list:
                for i in range(1,19):
                    encoder_code = encoder.select('.encoder_code > span')[i].string
                    encoder_ip = encoder.select('.encoder_ip > span')[i].string
                    encoder_name = encoder.select('.encoder_name > span')[i].string
                    encoder_orgName = encoder.select('.encoder_orgName > span')[i].string
                    encoder_id = encoder.select('.operation > .editLink ')[i-1]['href'][76:-4]

                    InfoUrl = 'http://ip/admin/device/encoder_edit.action?id=%d' % int(encoder_id)
                    resp_InfoUrl = urllib2.urlopen(InfoUrl)
                    html_InfoUrl = resp_InfoUrl.read()
                    registDeviceCode = re.findall(r'"deviceBean.registDeviceCode" value="(.*?)"', html_InfoUrl)
                    loginName = re.findall(r'"deviceBean.loginName" value="(.*?)"',html_InfoUrl)
                    loginPass = re.findall(r'"deviceBean.loginPass" value="(.*?)"',html_InfoUrl)
                    channelsCount = re.findall(r'"deviceBean.encoderUnits\[0\].channelsCount" value="(.*?)"',html_InfoUrl)

                    if len(loginName)==1 and len(loginPass) == 1 and len(registDeviceCode) == 1 and len(channelsCount) == 1:
                        print "开始抓取 主动注册 第",IRid,"页第",i,"条数据 ... ... ..."
                        csv_writer.writerow([encoder_id, encoder_ip, registDeviceCode[0], loginName[0], loginPass[0],channelsCount[0] ,encoder_name, encoder_orgName])
                        print "结束抓取 主动注册 第", IRid, "页第", i, "条数据 ... ... ..."
        if IRid == IR_total_page:
            for encoder in encoder_list:
                for i in range(1, IR_alone_page_range):
                    encoder_code = encoder.select('.encoder_code > span')[i].string
                    encoder_ip = encoder.select('.encoder_ip > span')[i].string
                    encoder_name = encoder.select('.encoder_name > span')[i].string
                    encoder_orgName = encoder.select('.encoder_orgName > span')[i].string
                    encoder_id = encoder.select('.operation > .editLink ')[i - 1]['href'][76:-4]

                    InfoUrl = 'http://ip/admin/device/encoder_edit.action?id=%d' % int(encoder_id)
                    resp_InfoUrl = urllib2.urlopen(InfoUrl)
                    html_InfoUrl = resp_InfoUrl.read()
                    registDeviceCode = re.findall(r'"deviceBean.registDeviceCode" value="(.*?)"', html_InfoUrl)
                    loginName = re.findall(r'"deviceBean.loginName" value="(.*?)"', html_InfoUrl)
                    loginPass = re.findall(r'"deviceBean.loginPass" value="(.*?)"', html_InfoUrl)
                    channelsCount = re.findall(r'"deviceBean.encoderUnits\[0\].channelsCount" value="(.*?)"',html_InfoUrl)

                    if len(loginName) == 1 and len(loginPass) == 1 and len(registDeviceCode) == 1 and len(channelsCount) == 1:
                        print "开始抓取 主动注册 第", IRid, "页第", i, "条数据 ... ... ..."
                        csv_writer.writerow([encoder_id, encoder_ip, registDeviceCode[0], loginName[0], loginPass[0], channelsCount[0],encoder_name, encoder_orgName])
                        print "结束抓取 主动注册 第", IRid, "页第", i, "条数据 ... ... ..."
