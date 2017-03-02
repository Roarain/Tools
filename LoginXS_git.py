#coding=utf-8

import re
import cookielib
import urllib
import urllib2

#利用cookielib自动管理cookies
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
#根据抓包，用到的urls
OriUrl = "http://qd.xuegod.cn/web/login.php"
CookieUrl = "http://qd.xuegod.cn/web/useraction.php?a=dologin"
LoginUrl = "http://qd.xuegod.cn/index.php"
CheckInUrl = "http://qd.xuegod.cn/web/action.php?a=qiandao"
LogoutUrl = "http://qd.xuegod.cn/web/useraction.php?a=dologout"
#用户名，密码。幸亏没有验证码
username = "xxx"
passwd = "xxx"
#打开首页，读取页面源码
resp_OriUrl = urllib2.urlopen(OriUrl)
html_OriUrl = resp_OriUrl.read()
#根据抓包，可知POST此页面获取的PHPSESSID用于后面的login
resp_CookieUrl = urllib2.urlopen(CookieUrl)
html_CookieUrl = resp_CookieUrl.read()

#print html_OriUrl

#根据抓包，POST数据时的body如下
PostDict = {
    "qq" : username,
    "pass" : passwd
    }
#将post时的body转码
PostData = urllib.urlencode(PostDict)
#先request，再response，最后获取cookie的PHPSESSID
req_CookieUrl = urllib2.Request(CookieUrl,PostData)
resp_CookieUrl = urllib2.urlopen(req_CookieUrl)
html_CookieUrl = resp_CookieUrl.read()
#根据获取的PHPSESSID登陆
req_LoginUrl = urllib2.Request(LoginUrl,PostData)
#req_LoginUrl.add_header('Content-Type', "application/x-www-form-urlencoded")
#req_LoginUrl.add_header('Accept-Encoding', "gzip, deflate")
#req_LoginUrl.add_header('User-Agent', "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)")
#req_LoginUrl.add_header('Connection', "Keep-Alive")
#req_LoginUrl.add_header('Accept', "application/x-ms-application, image/jpeg, application/xaml+xml, image/gif, image/pjpeg, application/x-ms-xbap, */*")
#print req_LoginUrl.header_items()
resp_LoginUrl = urllib2.urlopen(req_LoginUrl)
html_LoginUrl = resp_LoginUrl.read()

#print html_LoginUrl

#登陆后继续利用PHPSESSID来签到
resp_CheckInUrl = urllib2.urlopen(CheckInUrl)
html_CheckInUrl = resp_CheckInUrl.read()

print html_CheckInUrl

for index,cookie in enumerate(cj):
    print "[",index,"]",cookie


#退出系统
resp_LogoutUrl = urllib2.urlopen(LogoutUrl)
html_LogoutUrl = resp_LogoutUrl.read()
#print html_LogoutUrl
