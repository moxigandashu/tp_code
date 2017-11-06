# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 19:20:29 2017

@author: 吴聪
"""
import os
import pandas as pd

#输入路径
xml_excel_path='G:/touchpal/code/xml_excel_exchange'
excel_path=xml_excel_path+'xml_excel_exchange.xlsx'
xml_path=xml_excel_path+'baikal_strings.xml'

os.chdir(xml_excel_path)
#读取文件
with open('baikal_strings.xml','rb') as f:
    s_xml=f.read().decode('utf-8')

s_excel=pd.read_excel('xml_excel_exchange.xlsx',0)

n=s_excel.shape[0]
for i in range(n):
    target_str=s_excel['中文名'][i]
    if s_xml.find(target_str)>=0:
        s_xml=s_xml.replace(target_str,s_excel['代码对应位'][i],1)
        
with open('new.xml','w',encoding='utf-8') as f:
    f.write(s_xml)
    
    

'''task:xml and csv exchange'''


import os 
import pandas as pd
from bs4 import BeautifulSoup

#set cwd
os.chdir(xml_excel_path)
#os.getcwd()

'''#xml--->csv'''
#open and read file.xml
soup=BeautifulSoup(open('baikal_strings.xml','r',encoding='utf-8'),'xml')
#get attribution and text
ref_table=[]
for item in soup.find_all('string'):
    ref_table.append([item.get('name'),item.get_text()])
#exchange into dataframe     
ref_table=pd.DataFrame(ref_table,columns=['code_str','name_str'])
#output to csv
ref_table.to_csv('ref_table.csv')


'''#csv--->xml'''
soup=BeautifulSoup(open('baikal_strings.xml','r',encoding='utf-8'),'xml')
ref_table=pd.read_csv('ref_table_TH.csv',encoding='gbk')
n =ref_table.shape[0]
for i in range(n):
    target_str=ref_table['code_str'][i]
    for item in soup.find_all('string',attrs={'name':target_str}):
        item.string=str(ref_table['TH'][i])
print(soup)
with open('baikal_string_TH.xml','w') as f:
    #f.write(soup.prettify())     
    f.write(str(soup))