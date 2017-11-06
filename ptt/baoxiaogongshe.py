# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 19:47:11 2017

@author: 吴聪
"""

from urllib import request
from bs4 import BeautifulSoup
import requests
import pandas as pd
import jieba

def url_manager(n):
    urls=[]
    for i in range(n):
        urls.append('http://www.bc3ts.com/category/categoryList?id=161&page='+str(i+1))
    return urls

def get_html(url_c):
    header_fox = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'} 
    reg=request.Request(url_c,headers=header_fox)
    with request.urlopen(reg) as f:
        return f.read().decode('utf-8')

def get_title(html_c):
    href=[]
    src=[]
    title=[]
    title_pre="http://www.bc3ts.com"
    soup=BeautifulSoup(html_c,'lxml')
    for node in soup.find_all('div',class_='col-md-4'):
        href.append(title_pre+node.find('div',class_="card mb-4")['href'])
        src.append(node.find('img')['src'])
        title.append(node.find('h5',class_='card-title').string)
    return href,src,title

if __name__=="__main__":
    urls=url_manager(2)
    par={'href':[],'src':[],'title':[]}
    for url in urls:
        href,src,title=get_title(get_html(url))
        par['href'].extend(href)
        par['src'].extend(src)
        par['title'].extend(title)

