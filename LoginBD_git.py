#coding=utf-8
import re
import urllib
import urllib2
import cookielib

tt = 1488365071918
gid = "17A6116-3D17-488A-86AB-2F5F3F8A4FD2"
#HOSUPPORT = 1
callback = "bd__cbs__3gmdau"


cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

bdMainUrl = "http://www.baidu.com"
resp_bdMainUrl = urllib2.urlopen(bdMainUrl)
#for index,cookie in enumerate(cj):
#    print "[",index,"]",cookie


bdTokenUrl = "https://passport.baidu.com/v2/api/?getapi&tpl=mn&apiver=v3&tt=%s&class=login&gid=%s&logintype=dialogLogin&callback=%s" %(tt,gid,callback)
resp_bdTokenUrl = urllib2.urlopen(bdTokenUrl)
html_bdTokenUrl = resp_bdTokenUrl.read()
token_bdTokenUrl = re.findall('token" : "+\w+",        "cookie',html_bdTokenUrl)
token = token_bdTokenUrl[0][10:42]
print "The token is: %s" %(token)
#for index,cookie in enumerate(cj):
#    print "[",index,"]",cookie

bdUBIUrl = "https://passport.baidu.com/v2/api/?loginhistory&token=%s&tpl=mn&apiver=v3&tt=%s&gid=%s&callback=%s" % (token,tt,gid,callback)
resp_bdUBIUrl = urllib2.urlopen(bdUBIUrl)
html_bdUBIUrl = resp_bdUBIUrl.read()
#for index,cookie in enumerate(cj):
#    print "[",index,"]",cookie

bdLoginUrl = "https://passport.baidu.com/v2/api/?login"
resp_bdLoginUrl = urllib2.urlopen(bdLoginUrl)
html_bdLoginUrl = resp_bdLoginUrl.read()
#for index,cookie in enumerate(cj):
#    print "[",index,"]",cookie

staticpage = "https://www.baidu.com/cache/user/html/v3Jump.html"
u_Url = "https://www.baidu.com/"

PostDict = {
"staticpage" : staticpage,
"charset" : "utf-8",
"token" : token,
"tpl" : "mn",
"subpro" : "",
"apiver" : "v3",
"tt" : tt,
"codestring" : "tcG1707c1cca700c105025614dd44015a3194994307f7047f55",
"safeflg" : "0",
"u" : u_Url,
"isPhone" : "",
"detect" : "1",
"gid" : gid,
"quick_user" : "0",
"logintype" : "dialogLogin",
"logLoginType" : "pc_loginDialog",
"idc" : "",
"loginmerge" : "true",
"splogin" : "rate",
"username" : "xxx",
"password" : "xxx",
"verifycode" : "%E4%BB%99%E4%BE%A0",
"mem_pass" : "on",
"rsakey" : "gcAbMRbjAb8Q2NCfV9ShDjybfXOdlMVA",
"crypttype" : "12",
"ppui_logintime" : "44333",
"countrycode" : "",
"dv" : "MDEwAAoAigAKA40AIwAAAF00AAcCAATLy8vLBwIABMvLy8sIAgAj0dOAgCwsLHZNGVgWUQNCD1APXwxcAztkO00oWjNVLG8AZAEMAgAf0-Pj4-Pzt-Oi7Kv5uPWq9aX2pvnBnsG0x6LQnv-S9wcCAATLy8vLDAIAH9Pi4uLi6kwYWRdQAkMOUQ5eDV0COmU6TzxZK2UEaQwNAgAFy8vNwsIHAgAEy8vLyxMCABrL3d3dtcG1xbaMo4z7jPvVt9a_266A44zhzgUCAATLy8vBAQIABsvPz8FW5BUCAAjLy8qQGpLgFgQCABbLy9nYudf3guyH6Ybxn7_JrN6txKvFFgIAIuqe9cXr2Oze59Lg2ODW5dzl3O_W4NHl3eXW7tzk3O7b6dsXAgAPycnc3Nb6mfXe-aXd6omuEAIAAcsGAgAoy8vL_Pz8_Pz8_Pm8vLy9mZmZnMrKysnJycnMmpqamEBAQEUjIyMhyQcCAATLy8vLCAIAIdPRmJjMzMzOXQlIBkETUh9AH08cTBMrdCtbOkk6TSJQNAkCACTT0enpwsLCwsLGoqL2t_m-7K3gv-Cw47Ps1IvUodK3xYvqh-INAgAdy8vN2MCU1Zvcjs-C3YLSgdGOtum2w7DVp-mI5YAHAgAEy8vLywwCAB_T5ubm5upGElMdWghJBFsEVAdXCDBvMEU2UyFvDmMGBwIABMvLy8sMAgAf0-rq6urkAlYXWR5MDUAfQBBDE0x0K3QBchdlK0onQgwCAB_T4uLi4u1iNnc5fixtIH8gcCNzLBRLFGESdwVLKkciDQIAHcvL3CQ8aClnIHIzfiF-Ln0tckoVSj9MKVsVdBl8DQIAHcvL09LKnt-R1oTFiNeI2IvbhLzjvMyt3q3atcejDQIAHcvL7PLqvv-x9qTlqPeo-Kv7pJzDnOyN_o36leeDCAIAHd_d5eWenp7DoPS1-7zur-K94rLhse7Widaw363ACQIAJtHT5uZ8fHx8fCPx8aXkqu2__rPss-Ow4L-H2IfxlOaP6ZDTvNi9CAIAI9HT5uZ8fHwTaz9-MHclZCl2KXkqeiUdQh1rDnwVcwpJJkInCQIAJtHT5uZ-fn5-fvn8_Kjpp-Cy877hvu697bKK1Yr8meuC5J3esdWwCAIAH93fgIB3d3foit6f0ZbEhciXyJjLm8T8o_yP-pj1nOgJAgAi3d-AgHd3d3d33f39qeim4bPyv-C_77zss4vUi_iN74Lrnw",
"callback" : callback
    }
PostData = urllib.urlencode(PostDict)
bdLoginUrl = "https://passport.baidu.com/v2/api/?login"

req_bdLoginUrl = urllib2.Request(bdLoginUrl,PostData)
req_bdLoginUrl.add_header('Content-Type', "application/x-www-form-urlencoded")
resp_bdLoginUrl = urllib2.urlopen(req_bdLoginUrl)
for index,cookie in enumerate(cj):
    print "[",index,"]",cookie
