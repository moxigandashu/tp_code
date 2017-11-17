# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 16:48:35 2017

@author: 吴聪
"""

import os 
import pandas as pd
from bs4 import BeautifulSoup

os_path="G:/touchpal/code/xml_excel_exchange/多语言翻译"
#set cwd
os.chdir(os_path)
#os.getcwd()

'''#xml--->csv'''
paths=["values-zh（简体中文）/cootek_internationalui_cc_strings.xml","values-zh（简体中文）/strings.xml",
      "values-en(英语)/cootek_internationalui_cc_strings.xml","values-en(英语)/strings.xml"]
def xml_csv(path):
    #open and read file.xml
    soup=BeautifulSoup(open(path,'r',encoding='utf-8'),'xml')
    #get attribution and text
    ref_table=[]
    for item in soup.find_all('string'):
        ref_table.append([item.get('name'),item.get_text()])
    #exchange into dataframe     
    ref_table=pd.DataFrame(ref_table,columns=['code_str','name_str'])
    #output to csv
    ref_table.to_csv(path+'ref_table.csv')


'''#csv--->xml'''
paths=['cootek_internationalui_cc_strings.xml','strings.xml']
ref_paths=['cootek_internationalui_cc_strings.xmlref_table.xlsx','strings.xmlref_table.xlsx']
ref_paths=['cootek_internationalui_cc_strings.xmlref_table.xlsx','strings.xmlref_table.csv']

def excel2xml(path,ref_path):
    soup=BeautifulSoup(open(path,'r',encoding='utf-8'),'xml')
    if(ref_path.split('.')[-1])=='xlsx':
        ref_table=pd.read_excel(ref_path)
    elif(ref_path.split('.')[-1])=='csv':
        ref_table=pd.read_csv(ref_path,encoding='gbk')
    tg_str=ref_table.columns[2]
    n =ref_table.shape[0]
    for i in range(n):
        target_str=ref_table['code_str'][i]
        for item in soup.find_all('string',attrs={'name':target_str}):
            item.string=str(ref_table[tg_str][i])
    print(soup)
    with open(path,'w') as f:
        #f.write(soup.prettify())     
        f.write(str(soup))