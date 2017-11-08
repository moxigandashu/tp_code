# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 14:28:03 2017

@author: 吴聪
"""
import jieba
import pandas as pd

#停用词表
def stop_word_list():
    with open('stop_words_tw.txt','r') as f:
        stop_list=[]
        for word in f.readlines():
            stop_list.append(word.strip('\n'))
        return stop_list
 
#分词
def jieba_cut(text):
    return list(jieba.cut(text))

#去除停用词
def stop_word_delete(stop_list,word_list):
    return [x for x in word_list if x not in stop_list]

#生成文档的词表
def vocab_list(dataset):
    vocabset=set()
    for document in dataset:
        vocabset=vocabset|set(document)
    return list(vocabset)

#将词列表转化成向量
def word_list_vec(vocablist,inputset):
    word_vec=zeros(len(vocablist))
    for word in inputset:
        if word in vocablist:
            word_vec[vocablist.index(word)]+=1
    return  word_vec

#朴素贝叶斯分类器
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
            
        elif classlist[i]=='entertain':
            p2+=trainMatrix[i]
            p2d+=sum(trainMatrix[i])
            
        elif classlist[i]=='food':
            p3+=trainMatrix[i]
            p3d+=sum(trainMatrix[i])
            
        elif classlist[i]=='game':
            p4+=trainMatrix[i]
            p4d+=sum(trainMatrix[i])
            
        elif classlist[i]=='lucky':
            p5+=trainMatrix[i]
            p5d+=sum(trainMatrix[i])
            
    p1vec=log(p1/p1d)
    p2vec=log(p2/p2d)
    p3vec=log(p3/p3d)
    p4vec=log(p4/p4d)
    p5vec=log(p5/p5d)
    return p1vec,p2vec,p3vec,p4vec,p5vec,p_ackfun,p_entertain,p_food,p_game,p_lucky

#分类器，输出概率最大的分类
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

def all_test_train(trainSet,testSet):
    #trainSet=list(range(n));testSet=[]
    trainSet=trainSet+testSet
    testSet=[]
    n_len=shape(trainSet)[0]    
    for i in range(int(n_len/2)):
        randIndex=int(random.uniform(0,len(trainSet)))
        testSet.append(trainSet[randIndex])
        del(trainSet[randIndex])
    trainSet_new=trainSet
    testSet_new=testSet
    popSet=[]
    error_rate_te=[];error_rate_tr=[]
    for i in range(8):
        if i%2==0:
            error_rate,testSet_new,pop_temp=over_test_drop(trainSet_new,testSet_new)
            
            if error_rate==0:break
            popSet.extend(pop_temp)
            error_rate_te.append(error_rate)
        else:
            error_rate,trainSet_new,pop_temp=over_test_drop(testSet_new,trainSet_new)
            
            if error_rate==0:break   
            popSet.extend(pop_temp)         
            error_rate_tr.append(error_rate)        
    print('error_rate_te:',error_rate_te)
    print('error_rate_tr:',error_rate_tr)
    te= error_rate_te;tr=error_rate_tr
    return te,tr,popSet,trainSet_new,testSet_new

def over_test_drop(tA,tB):
    tAMatrix=[];tAClasses=[]
    tB_new=[];tB_pop=[]
    for randIndex in tA:
            tAMatrix.append(wordMatrix[randIndex])
            tAClasses.append(classlist[randIndex])
    p1vec,p2vec,p3vec,p4vec,p5vec,p_ackfun,p_entertain,p_food,p_game,p_lucky=trainNB(tAMatrix,tAClasses)
    error_count=0
    all_count=len(tB)
    for randIndex in tB:
        class_pre=classifyNB(wordMatrix[randIndex],p1vec,p2vec,p3vec,p4vec,p5vec,p_ackfun,p_entertain,p_food,p_game,p_lucky)
        if class_pre!=classlist[randIndex]:
            error_count+=1
            print ('randIndex:',randIndex,'\t',class_pre,'\t',classlist[randIndex])
            tB_pop.append(randIndex)
        else:
            tB_new.append(randIndex)
    wrong_rate=error_count/all_count
    print('wrong_rate',wrong_rate,'\n')
    return   wrong_rate,tB_new,tB_pop
                          
    

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
    wordMatrix=[]
    for i in range(n):
        wordMatrix.append(word_list_vec(vocabset,word_list[i]))
    #class_tag=['ackfun', 'entertain', 'food', 'game', 'lucky']
    #分类与准确率

    #删除分类错误的文章      
    iteration=[]
    for j in range(10):    
        error_rate_A=[];error_rate_B=[];popSet=[]
        trainSet=list(range(n));testSet=[]
        for i in range(100):
            a,b,p,trainSet,testSet=all_test_train(trainSet,testSet)
            error_rate_A.append(a)
            error_rate_B.append(b)
            popSet.extend(p)
            if not a and not b:
                print('wrong rate is 0 at iteration %s'%(i+1))
                iteration.append(i)
                break
                

'''         
#循环交叉测试     
def test_main():
    wrong_rate=[]
    sum_rate=0
    for j in range(100):
        print ('iteration %d begin \n \t\t class_pre \t class_list'%(j+1))
        trainSet=list(range(n));testSet=[]
        for i in range(200):
            randIndex=int(random.uniform(0,len(trainSet)))
            testSet.append(randIndex)
            del(trainSet[randIndex])
        trainMatrix=[];trainClasses=[]
        for randIndex in trainSet:
            trainMatrix.append(wordMatrix[randIndex])
            trainClasses.append(classlist[randIndex])
        p1vec,p2vec,p3vec,p4vec,p5vec,p_ackfun,p_entertain,p_food,p_game,p_lucky=trainNB(trainMatrix,trainClasses)
        
        #test  
        error_count=0
        for randIndex in testSet:
            class_pre=classifyNB(wordMatrix[randIndex],p1vec,p2vec,p3vec,p4vec,p5vec,p_ackfun,p_entertain,p_food,p_game,p_lucky)
            if class_pre!=classlist[randIndex]:
                error_count+=1
                print ('randIndex:',randIndex,'\t',classifyNB(wordMatrix[randIndex],p1vec,p2vec,p3vec,p4vec,p5vec,p_ackfun,p_entertain,p_food,p_game,p_lucky),'\t',classlist[randIndex])
                classlist[randIndex]=class_pre                
        all_count=len(testSet)
        print('wrong_rate',error_count/all_count,'\n')
        sum_rate+=error_count/all_count
        wrong_rate.append(error_count/all_count)
    ave_rate=sum_rate/100
    return ave_rate


           
#测试        
def test_class_url(url):
    test_title,test_text=class_craw.detail_parse3(url)
    test_text=stop_word_delete(stop_list,list(jieba_cut(test_text)))
    test_vec=word_list_vec(vocabset,test_text)
    class_output=classifyNB(test_vec,p1vec,p2vec,p3vec,p4vec,p5vec,p_ackfun,p_entertain,p_food,p_game,p_lucky)  
    print(class_output)
    

def try1try():      
    wrong_rate1=[]
    wrong_rate2=[]
    for j in range(10):
        print ('iteration %d begin \n \t\t class_pre \t class_list'%(j+1))
        trainSet=list(range(n));testSet=[]
        for i in range(213):
            randIndex=random.randint(0,len(trainSet))
            testSet.append(trainSet[randIndex])
            del(trainSet[randIndex])
        wrong_rate1.append(over_test(trainSet,testSet))
        wrong_rate2.append(over_test(testSet,trainSet))   
        
    print('ave_rate1:',average(wrong_rate1))
    print('ave_rate2:',average(wrong_rate2))
    

def over_test(tA,tB):
    tAMatrix=[];tAClasses=[]
    for randIndex in tA:
            tAMatrix.append(wordMatrix[randIndex])
            tAClasses.append(classlist[randIndex])
    p1vec,p2vec,p3vec,p4vec,p5vec,p_ackfun,p_entertain,p_food,p_game,p_lucky=trainNB(tAMatrix,tAClasses)
    error_count=0
    all_count=len(tB)
    for randIndex in tB:
        class_pre=classifyNB(wordMatrix[randIndex],p1vec,p2vec,p3vec,p4vec,p5vec,p_ackfun,p_entertain,p_food,p_game,p_lucky)
        if class_pre!=classlist[randIndex]:
            error_count+=1
            print ('randIndex:',randIndex,'\t',class_pre,'\t',classlist[randIndex])
    wrong_rate=error_count/all_count
    print('wrong_rate',wrong_rate,'\n')
    return   wrong_rate      
    
 def test_rand_fun(testSet):
    a=0;b=0;c=0;d=0;e=0
    for i in testSet:
        if classlist[i]=='ackfun':a+=1
        elif classlist[i]=='entertain':b+=1
        elif classlist[i]=='food':c+=1
        elif classlist[i]=='game':d+=1
        elif classlist[i]=='lucky':e+=1
    print('a:%s,b:%s,c:%s,d:%s,e:%s'%(a,b,c,d,e))
'''    