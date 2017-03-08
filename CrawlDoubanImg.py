# coding=utf-8
import re,os,sys
from urllib.request import *
from bs4 import BeautifulSoup

path = os.getcwd()
new_path = os.path.join(path,u'DBmeinv')
if not os.path.isdir(new_path):
    os.mkdir(new_path)

pageids = list(range(1,3940))
for pageid in pageids:
    url = 'http://www.dbmeinv.com/?pager_offset=%d' % pageid
    html = urlopen(url)
    soup = BeautifulSoup(html,'html.parser')

#girls = soup.find_all('img',class_='height_min')
    AllInfos = soup.find_all('img',class_='height_min')
    girls = []
    for AllInfo in AllInfos:
        girls.append(AllInfo.get('src'))

# print(girls)
# type(girls)

    index = 1
    for girl in girls:
        if index <= (len(girls)+1):
            try:
                urlretrieve(girl,new_path+'/'+'Page'+str(pageid)+'Pic'+str(index)+'.jpg')
                index +=1
            except Exception:
                print('download error.The %d pic' % index)
        else:
            print('download success')
pageid += 1
