# -*- coding: utf-8 -*-
"""
Created on Wed May  6 21:10:42 2020

@author: dell
"""

import json
import os
import jieba
import collections


stopwords=[line.strip() for line in open('C:/Users/dell/Desktop/文本挖掘期末/hotel_comment/stopwords/stopword.txt', 'r',encoding='utf-8',errors='ignore').readlines()]
#结合了多个停用词表

def remove_characters(sentence):  #去停用词
    cleanwordlist=[word for word in sentence if word.lower() not in stopwords]
    filtered_text=' '.join(cleanwordlist)
    return filtered_text

def get_content(path):
    content=[]
    with open(path,'r', encoding='utf-8') as fp:
        con=json.load(fp)
        for i in range(0,len(con)):
            content.append(con[i]['content'].replace(' ','').replace('\n', '').replace('\r', ''))
    return(content)
    
def get_file_content(path):
    flist=os.listdir(path)
    flist=[os.path.join(path,x) for x in flist]
    corpus=[]
    for x in flist:
        corpus+=get_content(x)        
    return corpus

path='C:/Users/dell/Desktop/论文/data'
comment=get_file_content(path)


all_comment=''
for x in comment:
    all_comment+=x
split_words=list(jieba.cut(all_comment))



#filtered_corpus=remove_characters(split_words)  #去停用词
filtered_corpus=[word for word in split_words if word not in stopwords]

##词频统计
word_counts = collections.Counter(filtered_corpus) # 对分词做词频统计
word_counts_top10 = word_counts.most_common(100) # 获取前10最高频的词
f=open(r'C:\Users\dell\Desktop\论文\process\word.txt','w',encoding='utf_8')
print (word_counts_top10,file=f) # 输出检查
f.close()

##word2vec词向量模型
text = ' '.join(jieba.cut(all_comment))
fo = open('C:/Users/dell/Desktop/论文/process/comment_cut.txt', 'w', encoding='utf-8')
fo.write(text)
fo.close()

from gensim.models import word2vec
sentences =word2vec.Text8Corpus('C:/Users/dell/Desktop/论文/process/comment_cut.txt')
model = word2vec.Word2Vec(sentences, size=300)

model.wv.save_word2vec_format('C:/Users/dell/Desktop/py_anaconda/携程酒店爬虫/vectors_300d_word2vec.txt')
for key in model.most_similar('位置', topn=10):
    print(key)
