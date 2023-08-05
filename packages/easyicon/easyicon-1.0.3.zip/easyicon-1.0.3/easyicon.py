#coding:utf-8
#从www.easyicon.net网站批量下载图标文件
#autor:kancy 
#date:2016/12/27

import requests
import urllib.request
import time
import os
import sys
from bs4 import BeautifulSoup

#定义成员变量

#bPrintLog = True
bPrintLog = False

#控制打印日志
def _print(msg):
    if bPrintLog:
        print(msg)

#获取文件的url列表
def getEasyIconUrl(searchkey='heart',pageCount=1,fileType = "png"):
    
    #使用set集合去除重复数据
    iconlist=set([])
    currPage = 0
    baseimgurl='http://www.easyicon.net/iconsearch/{0}/{1}/'

    if len(searchkey)<=0:
        searchkey = 'heart'
    if len(fileType)<=0:
        fileType = 'png'
    if pageCount<=1:
        pageCount=1
        
    while pageCount>currPage:
        currPage = currPage + 1
        imgurl=baseimgurl.format(searchkey,currPage)
        print("正在请求",imgurl,"资源...")
        res = requests.get(imgurl)
        res.encoding='utf-8'
        soup = BeautifulSoup(res.text,'html.parser')

        for item in soup.select('.search_icon_detail ol li'):
            img = item.select('.d_link .k_left a')
            
            if len(img)>0:
                if fileType == "png":
                    iconlist.add(img[0]['href'])
                if fileType == "ico":
                    iconlist.add(img[1]['href'])
                if fileType == "icns":
                    iconlist.add(img[2]['href'])
                    
            if fileType == "gif":
                img = item.select('.pd_img .icon_img img')
                if len(img)>0:
                    iconlist.add("http:"+img[0]['src'])
                
                
    return iconlist

#获取带有规格尺寸的url
def _getSizeUrl(url,fileSize):
    returnValue = url
    if returnValue.split("/")[-4] != 'gif':
        returnValue = returnValue.rstrip("/")
        returnValue = returnValue[0:returnValue.rindex("/")]
        returnValue = returnValue + "/" + str(fileSize) + "/"
    return returnValue
    

#下载文件通过关键字和页数
#第一个参数：关键字,英文（必输）
#第二个参数：搜索到第几页，默认为1
#第三个参数：下载文件的类型，默认为png
#第四个参数：设置下载目录，默认为桌面
#第五个参数：文件的规格尺寸,如果不填，默认大小
def downloadIcon(searchkey,pageCount=1,fileType='png',localpath="C:/Users/Administrator/Desktop/{}",fileSize=0):
    #初始化
    if len(fileType)<=0:
        fileType = "png"

    localpath = localpath.format(fileType)
    if not os.path.exists(localpath):
        os.makedirs(localpath)

    #获取url列表
    iconlist = getEasyIconUrl(searchkey,pageCount,fileType)
        
    #循环下载文件
    fileCount = 0
    filename = time.strftime("%Y%m%d%H%M%S", time.localtime())+"-{0}.{1}"
    for url in iconlist:
        if fileSize > 0:
            url = _getSizeUrl(url,fileSize)
            
        _print("服务器地址："+url)
        localfilepath = localpath+"/"+filename.format(fileCount,fileType)
        urlfile = urllib.request.urlopen(url)
        with open(localfilepath,'wb') as localfile:
            localfile.write(urlfile.read())
            fileCount += 1
            _print("本地地址："+localfilepath+" "+str(fileCount)+"下载完成！")

    print("一共成功下载",fileCount,"个文件！") 

#下载文件
#downloadIcon("Pistol",5,"png","C:/Users/Administrator/Desktop/test",100)
#下载文件（默认大小）
#downloadIcon("Pistol",5,"png","C:/Users/Administrator/Desktop/test")
#下载文件（默认大小，默认路径）
#downloadIcon("Pistol",5,"png")
#下载文件（默认路径）
#downloadIcon("Pistol",5,"png",fileSize=200)
#下载文件（指定格式）
#downloadIcon("Pistol",5,"ico")
#下载文件（默认png格式）
#downloadIcon("Pistol",5)
#下载文件（默认搜索深度1）
#downloadIcon("Pistol")
#下载文件（指定关键字）
#downloadIcon("123",fileType='gif')

if __name__ =="__main__":
	bPrintLog = True
	downloadIcon("Heart",10,"png")
	
	while input("按任意键退出程序..."):
		sys.exit()



