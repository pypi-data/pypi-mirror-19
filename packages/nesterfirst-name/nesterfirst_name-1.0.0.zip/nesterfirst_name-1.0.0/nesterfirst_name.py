# -*- coding: cp936 -*-

import urllib
import re

#��������ҳ����Ϣ
def getHtml(url):
    #urlopen()������һ��url
    page =urllib.urlopen(url)
    html=page.read()
    code=page.getcode()
    print code
    return html

#��ȡ����ҳ������Ҫɸѡ��ͼƬ����
def getImg(html):
    reg = r'src="(.+?\.jpg)"'
    imgre =re.compile(reg)
    imglist =re.findall(imgre,html)
    x=0
    for imgurl in imglist:
        urllib.urlretrieve(imgurl,'%s.jpg'%x)
        x+=1
    return imglist

html=getHtml("http://tieba.baidu.com/p/4894181088")
print (getImg(html))
#print html


