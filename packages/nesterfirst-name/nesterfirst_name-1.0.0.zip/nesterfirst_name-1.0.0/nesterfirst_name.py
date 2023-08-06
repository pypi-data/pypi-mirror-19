# -*- coding: cp936 -*-

import urllib
import re

#下载整个页面信息
def getHtml(url):
    #urlopen()方法打开一个url
    page =urllib.urlopen(url)
    html=page.read()
    code=page.getcode()
    print code
    return html

#获取整个页面中需要筛选的图片链接
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


