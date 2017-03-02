# coding=utf-8
from urllib.request import *
from bs4 import BeautifulSoup
import re

url = 'http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1480909756332_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=meijing+'
html = urlopen(url)
obj = BeautifulSoup(html,'html.parser')
index = 0
urls = re.findall(r'"objURL":"(.*?)"',str(obj))
for url in urls:
	if index <= 10:
		try:
			urlretrieve(url,'pic'+str(index)+'.png')
			#
			#第二个参数是文件保存路径, 
			#保存在和你这个脚本的同级目录下
			index += 1
		#try 和 except 是用来异常捕获
		except Exception:#Exception 处理所有异常
			print('下载失败,第%d张图片.'%index)
	else:
		print('下载完成')
		break

	#用来下载链接

