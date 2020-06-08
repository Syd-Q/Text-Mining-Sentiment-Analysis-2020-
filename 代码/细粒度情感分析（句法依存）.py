# -*- coding: utf-8 -*-
"""
Created on Wed May  6 21:12:32 2020

@author: dell
"""

#载入情感词典
# 打开词典文件，返回列表
import pandas as pd
import json
def open_dict(Dict='hahah',path='C:/Users/dell/Desktop/文本挖掘期末/hotel_comment/emotion_dict/'):
    path = path + '%s.txt' %Dict
    dictionary = open(path, 'r', encoding='utf-8-sig',errors='ignore')#encoding='utf-8-sig',检查是否有文件头，并去掉
    dict = []
    for word in dictionary:
        word=word.strip('\n')
        word=word.strip(' ')
        dict.append(word)
    return dict
posdict = open_dict(Dict='posdict')#积极情感词典
negdict = open_dict(Dict='negdict')#消极情感词典
inversedict=open_dict(Dict='inversedict')
mostdict = open_dict(Dict='mostdict')
verydict= open_dict(Dict='verydict')
moredict = open_dict(Dict='moredict')
ishdict = open_dict(Dict='ishdict')
insufficientdict = open_dict(Dict='insufficientdict')


f=open('C:/Users/dell/Desktop/文本挖掘期末/hotel_comment/emotion_dict/酒店情感词典.txt','r',encoding='utf-8')
words = []
value=[]
for word in f.readlines():
    words.append(word.split(' ')[0])
    value.append(float(word.split(' ')[1].strip('\n')))
    
c={'words':words,
   'value':value}
fd=pd.DataFrame(c)
pos=fd['words'][fd.value>0]
posdict=posdict+list(pos)    ##加入酒店相关的正向情感词
neg=fd['words'][fd.value<0]
negdict=negdict+list(neg)    ##加入酒店相关的负向情感词
f.close()

alist=['环境', '卫生', '周边环境', '周围环境', '装修', '隔音', '卫生条件', '通风', '光线', '采光', '视野', '风景', '景观', '海景' ,'景色']
blist=['服务', '态度', '服务态度', '服务质量', '办事效率', '工作人员', '服务员', '服务生', '客服', '阿姨' ,'员工', '经理', '前台', '店家', '素质', '保洁', '接待', '打扫', '收拾', '整理']
clist=['设施', '配置', '家电', '设备', '物品', '家具', '用品', '生活用品', '基础设施', '用具', '装饰']
dlist=['价格', '价钱', '价位', '房价', '性价比', '费用', '房费']
elist=['交通', '位置', '地理', '地点', '地理位置', '地段', '周边', '周围', '附近', '出行', '公交', '公交车', '公交站', '公交车站', '地铁', '商业区', '市中心']
flist=['整体', '总体', '总的来说', '总之', '酒店', '公寓', '宾馆']
t_list=alist+blist+clist+dlist+elist+flist
q_list=posdict+negdict
x_list=inversedict+mostdict+verydict+moredict+ishdict+insufficientdict
q_list1=['便宜','划算','实惠','贵','优惠','不贵','物超所值','经济','涨价']#价格
q_list2=['方便','便利','便捷']#交通
q_list3=['卫生','干净','整洁','脏','舒适','舒服','潮湿','温馨','明亮','宽敞','干净利落','潮','暗','昏暗','漏水','反味','难闻','发霉']#环境
q_list4=['齐全','旧','陈旧','新','老旧','破旧','很全']#设施
q_list5=['热情','贴心','耐心','友善','冷漠','体贴','周到','亲切','细心','细致','和蔼']#服务





#句法分析
from pyltp import Parser#导入库Parser
from pyltp import Segmentor#导入Segmentor库
from pyltp import Postagger#导入Postagger库

def get_detail(sentence):
    math_path = r"C:\Users\dell\Desktop\py_anaconda\LTP_model\cws.model"#LTP分词模型库
    segmentor = Segmentor()#实例化分词模块
    segmentor.load(math_path)#加载分词库
    words = segmentor.segment(sentence)
    words=' '.join(words).split()

    math_path1 = r"C:\Users\dell\Desktop\py_anaconda\LTP_model\pos.model"#LTP词性标注模型库
    postagger = Postagger() #实例化词性模块
    postagger.load(math_path1)#加载词性库
    postags = postagger.postag(words)#这里的words是分词后的结果
    postags=' '.join(postags).split()#分割标注后的结果
    
    math_path2 = r"C:\Users\dell\Desktop\py_anaconda\LTP_model\parser.model"#LTP依存分析模型库
    parser = Parser() # 初始化实例
    parser.load(math_path2)#加载依存分析库
    arcs = parser.parse(words,postags)    
    head=[]
    relation=[]
    for arc in arcs:
        head.append(arc.head)
        relation.append(arc.relation)
    return head,relation,words,postags
    del head,relation,words,postags


def xiushi(word,words,relation,head):#找到情感词的修饰词
    j=0
    a=[]
    for i in words:
        if i in x_list and relation[j] in ['CMP','ADV'] and words[head[j]-1]==word:
            a.append(i)
        j+=1
    return a
                


#例子：服务很不好
    #非常宽敞 特别干净 面积真的很大 装修风格很简单但真的很好看 挺商务的 最近住过的大连酒店这里最喜欢了 住过港汇好多次了哈哈
    #性价比很高的酒店，住着很舒服，服务人员也都非常热情，周边交通也很方便


def get_list(sentence):
    i=0
    d_list=[]    
    head,relation,words,postags=get_detail(sentence)

    for word in words:
        if word in t_list and relation[i] in ['SBV','VOB','FOB'] and words[head[i]-1] in q_list:
            d={'属性词':word,'情感词':words[head[i]-1],'修饰词':xiushi(words[head[i]-1],words,relation,head)}
            d_list.append(d)
        if word in q_list and relation[i] in ['ATT','CMP'] and words[head[i]-1] in t_list:
            d={'属性词':words[head[i]-1],'情感词':word,'修饰词':xiushi(word,words,relation,head)}
            d_list.append(d)
        if word in t_list and relation[i] in ['COO'] and words[head[i]-1] in q_list:
            d={'属性词':word,'情感词':words[head[i]-1],'修饰词':xiushi(words[head[i]-1],words,relation,head)}
            d_list.append(d)
        if word in q_list and relation[i] in ['COO'] and words[head[i]-1] in t_list:
            d={'属性词':words[head[i]-1],'情感词':word,'修饰词':xiushi(word,words,relation,head)}
            d_list.append(d)
        i+=1
    
    ##潜在属性词抽取
    q_word=[]#抽取过的情感词集和
    for d in d_list:
        q_word.append(d['情感词'])
    
    for word in words:
        if word not in q_word and word in q_list1:
            d={'属性词':'价格','情感词':word,'修饰词':xiushi(word,words,relation,head)}
            d_list.append(d)
        if word not in q_word and word in q_list2:
            d={'属性词':'交通','情感词':word,'修饰词':xiushi(word,words,relation,head)}
            d_list.append(d)
        if word not in q_word and word in q_list3:
            d={'属性词':'环境','情感词':word,'修饰词':xiushi(word,words,relation,head)}
            d_list.append(d)
        if word not in q_word and word in q_list4:
            d={'属性词':'设施','情感词':word,'修饰词':xiushi(word,words,relation,head)}
            d_list.append(d)
        if word not in q_word and word in q_list5:
            d={'属性词':'服务','情感词':word,'修饰词':xiushi(word,words,relation,head)}
            d_list.append(d)
    return(d_list)
    del d_list,head,relation,words,postags,q_word



#倾向分析
#定义判断奇偶的函数
def judgeodd(num):
    if num%2==0:
        return 'even'
    else:
        return 'odd'

def score(alist,d_list):
    totalcount=0
    a=0
    for d in d_list:
        count=0
        if d['属性词'] in alist:
            a+=1
            if d['情感词'] in posdict:
                c = 0 #情感词前否定词的个数
                for w in d['修饰词']:
                    if w in inversedict:
                        c += 1 
                if judgeodd(c) == 'odd':
                    count=-1
                else:
                    count=1
            else:
                c=0
                for w in d['修饰词']:
                    if w in inversedict:
                        c += 1 
                if judgeodd(c) == 'odd':
                    count=1
                else:
                    count=-1
        totalcount+=count
    if a==0:
        return 20
    else:
        return totalcount
    del d_list,totalcount


def s_sentence(d_list):
    score_dict={'环境':20,
                '服务':20,
                '设施':20,
                '价格':20,
                '交通':20,
                '整体':20,} 
    totalcount1=score(alist,d_list)#环境
    if totalcount1==20:
        score_dict['环境']=0##表示没有相关评论
    elif totalcount1>0:
        score_dict['环境']=1
    elif totalcount1<=0:
        score_dict['环境']=-1
        
    totalcount2=score(blist,d_list)#服务
    if totalcount2==20:
        score_dict['服务']=0##表示没有相关评论
    elif totalcount2>0:
        score_dict['服务']=1
    elif totalcount2<=0:
        score_dict['服务']=-1    
    
    totalcount3=score(clist,d_list)#设施
    if totalcount3==20:
        score_dict['设施']=0##表示没有相关评论
    elif totalcount3>0:
        score_dict['设施']=1
    elif totalcount3<=0:
        score_dict['设施']=-1    

    totalcount4=score(dlist,d_list)#价格
    if totalcount4==20:
        score_dict['价格']=0##表示没有相关评论
    elif totalcount4>0:
        score_dict['价格']=1
    elif totalcount4<=0:
        score_dict['价格']=-1    

    totalcount5=score(elist,d_list)#交通
    if totalcount5==20:
        score_dict['交通']=0##表示没有相关评论
    elif totalcount5>0:
        score_dict['交通']=1
    elif totalcount5<=0:
        score_dict['交通']=-1    

    totalcount6=score(flist,d_list)#整体
    if totalcount6==20:
        score_dict['整体']=0##表示没有相关评论
    elif totalcount6>0:
        score_dict['整体']=1
    elif totalcount6<=0:
        score_dict['整体']=-1    
       
    return score_dict
    del score_dict,totalcount1,totalcount2,totalcount3,totalcount4,totalcount5,totalcount6
    


#抽取出词对
import gc
content=[]
score_list=[]
with open(r'C:\Users\dell\Desktop\论文\newdata\如家酒店(大连星海公园店)(共357条).json','r', encoding='utf-8') as fp:
    con=json.load(fp)
    for i in range(0,len(con)):
        content.append(con[i]['content'].replace(' ','').replace('\n', '').replace('\r', ''))

for sentence in content[0:50]:
    d_list=get_list(sentence)
    score_dict=s_sentence(d_list)
    score_list.append(score_dict)
    del score_dict,d_list
    gc.collect()


fo = open('C:/Users/dell/Desktop/论文/newdata/score.json', 'r', encoding='utf-8')
#json.dump(score_list[0:10],fo,ensure_ascii=False, indent=4, sort_keys=False)
#fo.write(score_list)
con=json.load(fo)
con.append(score_list)
json.dump(con,fo,ensure_ascii=False, indent=4, sort_keys=False)
fo.close()

import gc
gc.collect()