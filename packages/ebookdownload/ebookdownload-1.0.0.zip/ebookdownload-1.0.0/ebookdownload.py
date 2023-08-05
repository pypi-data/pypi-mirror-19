#coding:utf-8
 
import ezgui
import requests
import urllib.request
import time
import os
import sys
from bs4 import BeautifulSoup

#暂停
def pause():
    while input("输入任意键退出..."):
        exit()

#转码
def urlencode(url):
    url = "http://"+urllib.request.quote(url.lstrip("http://"))
    return url

#根据url下载文件
#ec：是否转url码 urllib.request.quote ...
def download1(url,filepath="C:/Users/Administrator/Desktop/dowanload",ec=True):
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    #下载文件
    localfilepath = filepath+url[url.rfind("/"):]

    #url转码
    if ec:
        url = urlencode(url)

    urlfile = urllib.request.urlopen(url)
    with open(localfilepath,'wb') as localfile:
        localfile.write(urlfile.read())
        print(localfilepath+" 下载完成！")

#根据url下载文件
#ec：是否转url码 urllib.request.quote ...
#buffer:512  缓存下载，加快下载速度
def download2(url,filepath="C:/Users/Administrator/Desktop/dowanload",ec=True,buffer=512):
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    #下载文件
    localfilepath = filepath+url[url.rfind("/"):]

    #url转码
    if ec:
        url = urlencode(url)

    urlfile = urllib.request.urlopen(url)
    
    start=time.time()
    with open(localfilepath,'wb') as localfile:
        data = urlfile.read(buffer)
        while data:
            localfile.write(data)
            data = urlfile.read(buffer)
    
    end = time.time()     
    print(localfilepath+" 下载完成，用时：","{0:.4f}".format(end-start),"秒")
		
#私有方法：获取图书的下载路径
#url：详情路径
#fileType：0-rar  , 1-txt ,2-epub
def _getQiSuBookUrl(url,fileType=0):
    downUrl = ""
    #请求资源
    r = requests.get(url)
    r.encoding="utf-8"
    s = BeautifulSoup(r.text,"html.parser")
    downlist = s.select(".show .showBox .showDown li a")
    downUrl = downlist[fileType]["href"]
    return downUrl


#下载奇书网图书：downQiSuBooks（小说类型，深度，最大下载数量,文件类型）
#typeNo:1-10
#pageCount：页数深度2+n
#maxCount：最大数量
#fileType：0-rar  , 1-txt ,2-epub
def downQiSuBooks(typeNo=1,pageCount=1,maxCount=1,fileType=0):
    basehome = "http://www.qisuu.com"
    baseurl = "http://www.qisuu.com/soft/sort0{0}/index_{1}.html"
    basedowndir = "C:/Users/Administrator/Desktop"

    #下载失败的列表
    downloadfaillist =[]
    
    #选择文件下载目录
    downdir = ezgui.diropenbox("选择下载目录","批量下载奇书网图书",basedowndir)
    if downdir=="":
        downdir = basedowndir
    
    for pageNo in range(1,pageCount+1):
        url = baseurl.format(typeNo,pageNo)
        if url.endswith("_1.html"):
            url = url.replace("index_1.html","index.html")

        #请求资源
        print ("正在请求",url,"...")
        print("-------------------------------------------------------------------------------")
        res = requests.get(url)
        res.encoding="utf-8" 
        soup = BeautifulSoup(res.text,"html.parser")

        #下载book
        for bookitem in soup.select(".list .listBox ul li"):
            bookurl = _getQiSuBookUrl(basehome+"/"+bookitem.select("a")[1]["href"],fileType)
             
            print("正在下载：",bookurl,"...")
            print("文件详情：",bookitem.select(".s")[0].text)
            print("简介：",bookitem.select(".u")[0].text)
            
            filepath = downdir+"/{0}/{1}".format(soup.select(".listTab h1")[0].text,"第{0}页".format(pageNo))
            try:
                download2(bookurl,filepath)
            except Exception as err:
                print (err)
                downloadfaillist.append(bookurl)
                pass
            print("-------------------------------------------------------------------------------")
            maxCount = maxCount-1
            if(maxCount==0):
                return downloadfaillist
            
    return downloadfaillist

if __name__ =="__main__":
    try:
        faillist = downQiSuBooks(3,11,3,1)
        print ("下载失败列表：","\n",faillist)
 
        
    except Exception as err:
        print (err)
        pass
    pause()

    
        
    
