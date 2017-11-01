# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 17:55:24 2017

@author: 吴聪
"""


from urllib import request
#requsts bug exits
import requests
header_fox={
    'Host':'www.ptt.cc',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
    'Accept':'text/html,application/xhtml+xm…plication/xml;q=0.9,*/*;q=0.8',
    'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding':'gzip, deflate, br',
    'Content-Type':'application/x-www-form-urlencoded',
    'Content-Length':'44',
    'Referer':'https://www.ptt.cc/ask/over18?from=%2Fbbs%2FGossiping%2Findex.html',
    'Cookie':'__cfduid=d0eaf3895448295178e0fa917e84c5b9f1508123835; _ga=GA1.2.1279473261.1508123843; _gid=GA1.2.919937539.1509335528; _gat=1',
    'Connection':'keep-alive',
    'Upgrade-Insecure-Requests':'1'
}

html_cont=requests.post('https://www.ptt.cc/ask/over18?from=%2Fbbs%2FGossiping%2Findex.html',headers=header_fox)
#req=request.Request('https://www.ptt.cc/bbs/Gossiping/index25075.html')
#req.add_header(header_fox)
#with request.urlopen(req) as f:
#    html_cont=f.read()

class Spidermain(object):
    def __init__(self):
        self.downloader=Download()
        self.parser=Parser()
        self.outputer=Output()
    def craw(self):
        try:
            url='https://www.ptt.cc/bbs/Gossiping/index25061.html'
            html_cont=download(url)
            print(html_cont)
        except:
            print('somethingwrong')

class Download(object):
    def download(self,cu_url):
        if cu_url is None:
            return None
        with request.urlopen(cu_url) as f:
            res=f.read()
            return res.decode('utf-8')

class Parser(object):
    def parse1(self,url, html_cont):
        soup=BeautifulSoup(html_cont,'html.parser')
        newhref=self.get_newhref(url,soup)
        return newhref

class Output(object):
    pass

if __name__ == '__main__':
    obj_spider=Spidermain()
    obj_spider.craw()
    
    
import urllib.request
url='https://www.ptt.cc/bbs/Gossiping/index25090.html'
header_fox={
        'Host': 'www.ptt.cc',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '44',
        'Referer': 'https://www.ptt.cc/ask/over18?from=%2Fbbs%2FGossiping%2Findex.html',
        'Cookie': '__cfduid=d0eaf3895448295178e0fa917e84c5b9f1508123835; _ga=GA1.2.1279473261.1508123843; _gid=GA1.2.919937539.1509335528; _gat=1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
        }
req=urllib.request.Request(url,headers=header_fox)
with urllib.request.urlopen(req) as f:
    html_cont=f.read()
    print(html_cont)

import socket
import time  
timeout = 20    
socket.setdefaulttimeout(timeout)#这里对整个socket层设置超时时间。后续文件中如果再使用到socket，不必再设置  
sleep_download_time = 10  
time.sleep(sleep_download_time) #这里时间自己设定  

url='https://www.ptt.cc/ask/over18?from=%2Fbbs%2FGossiping%2Findex.html'
header_chrome={
        'authority':'www.ptt.cc',
        'method':'POST',
        'path':'/ask/over18',
        'scheme':'https',
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'zh-CN,zh;q=0.8',
        'cache-control':'max-age=0',
        'content-length':'44',
        'content-type':'application/x-www-form-urlencoded',
        'cookie':'__cfduid=d17692bda6cbfb7675d71d76f2e6d25a81507883342; over18=1; _ga=GA1.2.1945062127.1507883344; _gid=GA1.2.543515921.1509339206',
        'origin':'https://www.ptt.cc',
        'referer':'https://www.ptt.cc/ask/over18?from=%2Fbbs%2FGossiping%2Findex.html',
        'upgrade-insecure-requests':'1',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
                               }

req=urllib.request.Request(url,headers=header_chrome)
with urllib.request.urlopen(req) as f:
    html_cont=f.read()
    print(html_cont)


url='https://www.ptt.cc/bbs/C_Chat/index12511.html'
req=urllib.request.Request(url)
with urllib.request.urlopen(req) as f:
    html_cont=f.read()
    print(html_cont)

#requests 
import requests

url = 'https://www.ptt.cc/bbs/C_Chat/index.html'
response = requests.get(url)
response.encoding='utf-8'

print(response.text)



#parse ptt
import requests
from bs4 import BeautifulSoup
import pandas as pd

def urlmanager(n):
    start= 12511
    pre_str='https://www.ptt.cc/bbs/C_Chat/index'
    urls=[]
    for i in range(n):
        cur_index=start-i
        urls.append(pre_str+str(cur_index)+'.html')
    return urls

def download(url_c):
    req=requests.get(url_c)
    #req.encoding='utf-8'
    return req.text

def parse(html_c):
    title_cur=[]
    html_cur=[]
    soup=BeautifulSoup(html_c,'lxml')
    for node in soup.find_all('div',class_='title'):
        if node.find('a'):
            title_cur.append(node.string())
            html_cur.append(node.a['href'])
        else:
            title_cur.append(node.string())
            html_cur.append('NULL')
    return title_cur,html_cur

def jb_cut(sent):
    return (jieba.cut(sent))

def gen2list(gen):
    return (','.join(gen)) 
   
if __name__ == '__main__':
    title=[]
    html=[]
    n=5
    urls=urlmanager(n)
    for i in range(n):
        url_c=urls[i]
        print(url_c)
        html_c=download(url_c)
        title_cur,html_cur=parse(html_c)
        title.extend(title_cur)
        html.extend(html_cur)
    data=pd.DataFrame([title,html]).T
    data.columns=['title','html']
                     
    m=data.shape[0]
    cab_list=[]
    cab=[]
    for i in range(m):
        cab_list.append(','.join(jb_cut(data['title'][i])))
    for i in range(m):
        cab.extend(cab_list[i])
    cab.strip()
        

        

        
            

        