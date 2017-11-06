# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 11:25:58 2017

@author: 吴聪
"""
#引入需要用到的包os和pandas
import os 
import pandas as pd

flagpath='G:/touchpal/code/flags/xhdpi' #文件夹所在的路径
flagpath='G:/touchpal/code/flags/xxhdpi'
countrypath='G:/touchpal/code/flags/country_ code.csv' #国家简称与国家代码对应表格路径

filelist=os.listdir(flagpath) #获取所有文件名
country_code=pd.read_csv(countrypath) #读取表格

for files in filelist:
    olddir=os.path.join(flagpath,files) #修改前文件路径及文件名
    filename=os.path.splitext(files)[0] #得到文件名
    filetype=os.path.splitext(files)[1] #得到文件类型
    newfilename=filename #先用旧的文件名覆盖新文件名，防止没有新文件名
    m=shape(country_code)[0] #获取国家简称与国家代码对应表格（DataFrame)行数
    for i in range(m):
        if country_code['Alpha_code'][i]==filename: #匹配与转化
            newfilename=country_code['Numeric code'][i] #匹配成功复制新文件名
    newname=str(newfilename)+filetype #连接文件名与文件类型
    newdir=os.path.join(flagpath,newname) #新的文件路径及文件名
    os.rename(olddir,newdir) #重命名，覆盖原先的文件名


#两个表格匹配
import pandas as pd

isopath='G:/touchpal/code/iso3166.csv'
countrypath='G:/touchpal/code/country.csv'

iso=pd.read_csv(isopath,encoding='cp1252')

del(iso['Alpha-3 code'])

country_code=pd.read_csv(countrypath,header=None)
country_code.columns=['prefix','alpha2']

m=shape(country_code)[0]
n=shape(iso)[0]

country_code['c_code']=NAN
            
for i in range(m):
    for j in range(n):
        if (country_code['alpha2'][i]==iso['Alpha-2 code'][j]):
            country_code.c_code[i]=iso['Numeric code'][j]
            
            
#将国旗文件名命名为小写
import os 
import pandas as pd

flagpath='G:/touchpal/code/flags_v3/xhdpi' #文件夹所在的路径
flagpath='G:/touchpal/code/flags_v3/xxhdpi'
countrypath='G:/touchpal/code/flags_v3/country_code.csv' #国家简称与国家代码对应表格路径

filelist=os.listdir(flagpath) #获取所有文件名
country_code=pd.read_csv(countrypath,encoding='cp1252') #读取表格

for files in filelist:
    olddir=os.path.join(flagpath,files) #修改前文件路径及文件名
    filename=os.path.splitext(files)[0] #得到文件名
    filetype=os.path.splitext(files)[1] #得到文件类型
    newfilename=filename #先用旧的文件名覆盖新文件名，防止没有新文件名
    m=shape(country_code)[0] #获取国家简称与国家代码对应表格（DataFrame)行数
    for i in range(m):
        if country_code['Alpha_code'][i]==filename: #匹配与转化
            newfilename=country_code['Numeric code'][i] #匹配成功复制新文件名
    newname=str(newfilename)+filetype #连接文件名与文件类型
    newdir=os.path.join(flagpath,newname) #新的文件路径及文件名
    os.rename(olddir,newdir) #重命名，覆盖原先的文件名