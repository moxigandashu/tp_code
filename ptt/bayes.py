# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 14:28:03 2017

@author: 吴聪
"""
import jieba
import pandas as pd

def stop_word_list():
    with open('stop_words_tw.txt','r') as f:
        stop_list=[]
        for word in f.readlines():
            stop_list.append(word.strip('\n'))
        return stop_list
    
def jieba_cut(text):
    return list(jieba.cut(text))

def stop_word_delete(stop_list,word_list):
    return [x for x in word_list if x not in stop_list]

def vocab_list(dataset):
    vocabset=set()
    for document in dataset:
        vocabset=vocabset|set(document)
    return list(vocabset)

def word_list_vec(vocablist,inputset):
    word_vec=zeros(len(vocablist))
    for word in inputset:
        word_vec[vocablist.index(word)]+=1
    return  word_vec

def trainNB(trainMatrix,classlist):
    n_doc=len(trainMatrix)
    n_word=len(trainMatrix[0])
    p_ackfun=classlist.count('ackfun')/n_doc
    p_entertain=classlist.count('entertain')/n_doc
    p_food=classlist.count('food')/n_doc
    p_game=classlist.count('game')/n_doc
    p_lucky=classlist.count('lucky')/n_doc
    #
    p1=ones(n_word);p2=ones(n_word);p3=ones(n_word);p4=ones(n_word);p5=ones(n_word)
    p1d=p2d=p3d=p4d=p5d=2;
    for i in range(n_doc):
        if classlist[i]=='ackfun':
            p1+=trainMatrix[i]
            p1d+=sum(trainMatrix[i])
            print(1)
        elif classlist[i]=='entertain':
            p2+=trainMatrix[i]
            p2d+=sum(trainMatrix[i])
            print(2)
        elif classlist[i]=='food':
            p3+=trainMatrix[i]
            p3d+=sum(trainMatrix[i])
            print(3)
        elif classlist[i]=='game':
            p4+=trainMatrix[i]
            p4d+=sum(trainMatrix[i])
            print(4)
        elif classlist[i]=='lucky':
            p5+=trainMatrix[i]
            p5d+=sum(trainMatrix[i])
            print(5)
    p1vec=log(p1/p1d)
    p2vec=log(p2/p2d)
    p3vec=log(p3/p3d)
    p4vec=log(p4/p4d)
    p5vec=log(p5/p5d)
    return p1vec,p2vec,p3vec,p4vec,p5vec,p_ackfun,p_entertain,p_food,p_game,p_lucky

def classifyNB(vec2classify,p1vec,p2vec,p3vec,p4vec,p5vec,p_ackfun,p_entertain,p_food,p_game,p_lucky):
    p1=sum(vec2classify*p1vec)+log(p_ackfun)
    p2=sum(vec2classify*p2vec)+log(p_entertain)
    p3=sum(vec2classify*p3vec)+log(p_food)
    p4=sum(vec2classify*p4vec)+log(p_game)
    p5=sum(vec2classify*p5vec)+log(p_lucky)
    p_list=[p1,p2,p3,p4,p5]
    #return p_list.index(max(p_list))+1
    class_tag=['ackfun', 'entertain', 'food', 'game', 'lucky']
    return class_tag[p_list.index(max(p_list))]
    #return p1,p2,p3,p4,p5                             
    
    

if __name__=="__main__":
    stop_list=stop_word_list()
    doclist=[];classlist=[];word_list=[]
    data=pd.read_csv('class_feeds_data.csv',encoding='gbk')
    doclist=data['content']
    classlist=list(data['tag'])
    n=len(doclist)
    for i in range(n):
        word_list.append(stop_word_delete(stop_list,list(jieba_cut(doclist[i]))))
    vocabset=vocab_list(word_list)
    trainMatrix=[]
    for i in range(n):
        trainMatrix.append(word_list_vec(vocabset,word_list[i]))
    #class_tag=['ackfun', 'entertain', 'food', 'game', 'lucky']
    
    p1vec,p2vec,p3vec,p4vec,p5vec,p_ackfun,p_entertain,p_food,p_game,p_lucky=trainNB(trainMatrix,classlist)
    
        
      
        
        
    
    