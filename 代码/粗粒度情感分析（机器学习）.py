# -*- coding: utf-8 -*-
"""
Created on Wed May  6 21:11:58 2020

@author: dell
"""

import json
import os
import jieba
import pandas as pd


stopwords=[line.strip() for line in open('C:/Users/dell/Desktop/文本挖掘期末/hotel_comment/stopwords/stopword.txt', 'r',encoding='utf-8',errors='ignore').readlines()]
#结合了多个停用词表

def remove_characters(sentence):  #去停用词
    cleanwordlist=[word for word in sentence if word.lower() not in stopwords]
    filtered_text=' '.join(cleanwordlist)
    return filtered_text

def text_normalize(text):
    text_split=[]
    for line in text:
        text_split.append(list(jieba.cut(line)))
    text_normal=[]
    for word_list in text_split:
        text_normal.append(remove_characters(word_list))
    return text_normal 

def get_content(path):
    content=[]
    with open(path,'r', encoding='utf-8') as fp:
        con=json.load(fp)
        for i in range(0,len(con)):
            content.append(con[i]['content'].replace(' ','').replace('\n', '').replace('\r', ''))
    return(content)

def get_rank(path):
    rank=[]
    with open(path,'r', encoding='utf-8') as fp:
        con=json.load(fp)
        for i in range(0,len(con)):
            rank.append(1 if con[i]['ratingPoint']>=4 else 0)
    return(rank)
    
def get_file_content(path):
    flist=os.listdir(path)
    flist=[os.path.join(path,x) for x in flist]
    corpus=[]
    lable=[]
    for x in flist:
        corpus+=get_content(x)    
    for x in flist:
        lable+=get_rank(x)        
    return corpus,lable

path='C:/Users/dell/Desktop/论文/data'
comment,lable=get_file_content(path)

c={'comment':comment,
   'value':lable}
df=pd.DataFrame(c)

x=df['comment']
y=df['value']

from sklearn.model_selection import train_test_split

#分割数据集
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=1/4, random_state=0)
X_train=text_normalize(X_train)
X_test=text_normalize(X_test)


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier 
from sklearn.linear_model import LogisticRegression


#TF-IDF计算权重
tfidf_vectorizer=TfidfVectorizer(min_df=1,norm='l2',smooth_idf=True,use_idf=True,ngram_range=(1,1))
tf_train_features= tfidf_vectorizer.fit_transform(X_train)
tf_test_features= tfidf_vectorizer.transform(X_test)

##预测函数
def train_predict_evaluate_model(classifier,train_features,train_labels,test_features,test_labels):
    classifier.fit(train_features,train_labels)
    predictions=classifier.predict(test_features)
    return predictions


##贝叶斯
mnb=MultinomialNB()
mnb_tf_pre=train_predict_evaluate_model(classifier=mnb,train_features=tf_train_features,train_labels=y_train,test_features=tf_test_features,test_labels=y_test)


##SVM
svm=SGDClassifier(loss='hinge',max_iter=1000)
svm_tf_pre=train_predict_evaluate_model(classifier=svm,train_features=tf_train_features,train_labels=y_train,test_features=tf_test_features,test_labels=y_test)


###ann

ann_model = MLPClassifier(hidden_layer_sizes=1, activation='logistic', solver='lbfgs', random_state=0)
ann_tf_pre=train_predict_evaluate_model(classifier=ann_model,train_features=tf_train_features,train_labels=y_train,test_features=tf_test_features,test_labels=y_test)


##逻辑回归
logreg = LogisticRegression(C=1,penalty='l2')
log_tf_pre=train_predict_evaluate_model(classifier=logreg,train_features=tf_train_features,train_labels=y_train,test_features=tf_test_features,test_labels=y_test)


print('贝叶斯准确率：',accuracy_score(y_test, mnb_tf_pre))

print('SVM准确率：',accuracy_score(y_test, svm_tf_pre))

print('ann准确率：',accuracy_score(y_test, ann_tf_pre))

print('逻辑回归准确率：',accuracy_score(y_test, log_tf_pre))


##好评率计算
path='C:/Users/dell/Desktop/论文/newdata'
comment,lable=get_file_content(path)

c={'comment':comment,
   'value':lable}
df=pd.DataFrame(c)

x=df['comment']
y=df['value']

X_train=text_normalize(x)
tf_train_features= tfidf_vectorizer.transform(X_train)
predictions=svm.predict(tf_train_features)

a=0
b=len(predictions)
for i in predictions:
    if i==1:
        a+=1

print(a/b)
