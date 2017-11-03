# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 17:46:37 2017

@author: Ekko
"""
from urllib import request
from bs4 import BeautifulSoup
import requests
import pandas as pd
import jieba

#动漫 游戏 美食 命理 娱乐
def net_url_manager():
    net_url_tag=[]
    #动漫
    net_url_tag.append(['http://www.twgreatdaily.com/cat91/92','ackfun'])
    for i in range(7):
        net_url_tag.append(['https://life.tw/index.php?app=category&act=categorylist&no=72&page='+str(i+2),'ackfun'])
    #游戏
    for i in range(5):
        net_url_tag.append(['http://www.coco01.cc/category/categoryPostList?catId=83&page='+str(i+1),'game'])        
    #美食
    for i in range(5):
        net_url_tag.append(['http://www.coco01.cc/category/categoryPostList?catId=64&page='+str(i+1),'food'])        
    #命理
    for i in range(5):
        net_url_tag.append(['http://www.coco01.cc/category/categoryPostList?catId=67&page='+str(i+1),'lucky'])        
    #娱乐
    for i in range(5):
        net_url_tag.append(['http://www.coco01.cc/category/categoryPostList?catId=21&page='+str(i+1),'entertain'])
    return net_url_tag

def html_get(url_c):
    header_fox = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'} 
    reg=request.Request(url_c,headers=header_fox)
    with request.urlopen(reg) as f:
        return f.read().decode('utf-8')

def detail_url_manager1(n_url_tag):
    detail_url_tag=[]
    n=shape(n_url_tag)[0]
    detail_url_tag.extend(get_url1(n_url_tag[0]))
    for i in range(1,8):
        detail_url_tag.extend(get_url2(n_url_tag[i]))
    for i in range(8,n):
        detail_url_tag.extend(get_url3(n_url_tag[i]))
    return detail_url_tag

def get_url1(url_tag):
    url=url_tag[0]
    tag=url_tag[1]
    d_u_t=[]
    html_temp=html_get(url)
    soup=BeautifulSoup(html_temp,'lxml')
    print('net %s is processing'%url)
    for node in soup.find_all('div',class_="snippet"):
        node_temp=node.find('h3',class_="media-heading title")
        href_temp=node_temp.a['href']
        title_temp=node_temp.a.string
        detail_temp=detail_parse1(href_temp)
        d_u_t.append([href_temp,title_temp,tag,detail_temp])
    return d_u_t
        
def get_url2(url_tag):
    url=url_tag[0]
    tag=url_tag[1]
    d_u_t=[]
    html_temp=html_get(url)
    soup=BeautifulSoup(html_temp,'lxml')
    print('net %s is processing'%url)
    for node in soup.find_all('li',class_="shadow radius5"):
        href_temp="https://life.tw"+node.a['href']
        title_temp,detail_temp=detail_parse2(href_temp)
        d_u_t.append([href_temp,title_temp,tag,detail_temp])
    return d_u_t

def get_url3(url_tag):
    url=url_tag[0]
    tag=url_tag[1]
    d_u_t=[]
    html_temp=html_get(url)
    soup=BeautifulSoup(html_temp,'lxml')
    print('net %s is processing'%url)
    for node in soup.find_all('div',class_="col-md-4 col-xs-12 post-item"):
        href_temp="http://www.coco01.cc"+node.a['href']
        title_temp,detail_temp=detail_parse3(href_temp)
        d_u_t.append([href_temp,title_temp,tag,detail_temp])
    return d_u_t
    
def detail_parse1(href):
    text=str()
    print('parsing %s'%href)
    html_temp_detail=html_get(href)
    soup=BeautifulSoup(html_temp_detail,'lxml')
    node = soup.find('div',id="article-body")
    for p in node.find_all('p'):
        text+=(p.get_text())        
    return text

def detail_parse2(href):
    title=str()
    text=str()
    print('parsing %s'%href)
    html_temp_detail=html_get(href)
    soup=BeautifulSoup(html_temp_detail,'lxml')
    title=soup.find('div',class_="aricle-detail-top").h1.string
    text_node=soup.find('div',id="mainContent")
    for tp in text_node.find_all('p'):
        text+=tp.get_text()
    return title ,text

def detail_parse3(href):
    title=str()
    text=str()
    print('parsing %s'%href)
    html_temp_detail=html_get(href)
    soup=BeautifulSoup(html_temp_detail,'lxml')
    title =soup.find('h1',class_="post-title").get_text()
    text_node=soup.find('div',class_="post-html")
    for tp in text_node.find_all('p'):
        text+=tp.get_text()
    return title,text

if __name__=="__main__":
    net_url_tag=net_url_manager()
    detail_url_tag=detail_url_manager1(net_url_tag)
    detail_url_tag_pd=pd.DataFrame(detail_url_tag,columns=['url','titie','tag','conten'])
    (m,n)=shape(detail_url_tag_pd)
    for i in range(m):
        detail_url_tag_pd.ix[i,1]=detail_url_tag_pd.ix[i,1].strip()
        detail_url_tag_pd.ix[i,3]=detail_url_tag_pd.ix[i,3].strip()
    detail_url_tag_pd.to_csv('class_feeds_data.csv',index=False)

    