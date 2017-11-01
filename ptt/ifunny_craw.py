# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 10:36:51 2017

@author: 吴聪
title : ifunny craw
"""
from urllib import request
from bs4 import BeautifulSoup
import requests
import pandas as pd
import jieba

def urlmanager(n):
    urls=[]
    for i in range(n):
        urls.append('http://ifunny.tw/category/12/'+str(i))
    return urls

def download1(url_c):
    reg=requests.get(url_c)
    return reg.text

def parse(html_c):
    href=[]
    src=[]
    title=[]
    soup=BeautifulSoup(html_c,'lxml')
    for node in soup.find_all('div',class_='item clearfix'):
        href.append(node.a['href'])
        src.append(node.find('img')['src'])
        title.append(node.find('p',class_='title').string.strip())
    return href,src,title

def get_src(src_url):
    header_fox = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'} 
    reg=request.Request(src_url,headers=header_fox)
    with request.urlopen(reg) as f:
        img=f.read()
    return img

    
if __name__=="__main__":
    par={'href':[],'src':[],'title':[]}
    n=int(input('input n:'))
    urls=urlmanager(n)
    for url in urls:
        html_c=download1(url)
        href,src,title=parse(html_c)
        par['href'].extend(href)
        par['src'].extend(src)
        par['title'].extend(title)
    data=pd.DataFrame(par)            
    text=','.join(data['title'])
    text_cut=','.join(jieba.cut(text))
    cab_list=text_cut.strip().split(',')
    
    cab_list_set=set(cab_list)
    cab_list_dic={}
    for cab in cab_list_set:
        cab_list_dic.update({cab:cab_list.count(cab)})
    sort_cab=sorted(cab_list_dic.items(),key=lambda item:item[1],reverse=True)

    sort_cab_pd=pd.DataFrame(sort_cab)
    sort_cab_pd.to_csv('cab.csv')
#img
    with open('1.jpg','wb') as w:
        w.write(img)

#N=50

#parse cont_detail
def get_deail_cont(url_dc):
    detail_c=[]
    cont=download1(url_dc)
    soup_c=BeautifulSoup(cont,'lxml')
    cont_div=soup_c.find('div',class_='Content-post')
    for node in cont_div.find_all('p'):
        detail_c.append(node.get_text())
    while '' in detail_c:
        detail_c.remove('')
    detail_c='\n'.join(detail_c)
    return detail_c

m=data.shape[0]
detail_cont=[]
for i in range(m):
    url=data['href'][i]
    print('process is parsing No.%d :%s'%(i,url)
    detail_cont.append(get_deail_cont(url))
detail_cont='\n'.join(detail_cont)
detail_text=[]
for i in range(m):
    detail_text.extend(detail_cont[i]) 
detail_text='\n'.join(detail_text)
detail_text_cut=','.join(jieba.cut(detail_text)).split(',')

detail_text_set=set(detail_text_cut)
detail_list_dic={}
for detail_cab in detail_text_set:
    detail_list_dic.update({detail_cab:detail_text_cut.count(detail_cab)})
sort_cab_detail=sorted(detail_list_dic.items(),key=lambda item:item[1],reverse=True)

sort_cab_detail_pd=pd.DataFrame(sort_cab_detail)
sort_cab_detail_pd.to_csv('cab_detail.csv')    
    
