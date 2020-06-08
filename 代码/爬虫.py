# -*- coding: utf-8 -*-
"""
Created on Wed May  6 21:09:12 2020

@author: dell
"""

import requests
import json
import time
from fake_useragent import UserAgent

ua=UserAgent()

header = {
'User-Agent': ua.random
}

#proxies={
#        #'http':'119.101.52.243:20087',
#        'https':'27.40.91.56:22901'}

url='https://m.ctrip.com/restapi/soa2/16765/gethotelcomment?&_fxpcqlniredt=09031156110446310158'


def fetchCmts(page):
    formData = {
        'groupTypeBitMap': '2',
        'hotelId': '5090804',
        'pageIndex': str(page),
        'pageSize': '20',
        'travelType': '-1',
    }
    requests.packages.urllib3.disable_warnings()    
    res=requests.post(url,data=formData,headers=header,verify=False)
    res.raise_for_status()
    res.encoding = res.apparent_encoding

    json_data = json.loads(res.text)      #返回的是json文件
    if json_data['othersCommentList']==[]:
        data.append('null')               #做为循环终止的条件
    else:       
        for item in json_data['othersCommentList']:
            data.append({
                    'userName':item['userNickName'],                            #用户名
                    'travelType':item['travelType'],                            #出游类型
                    'ratingPoint': item['ratingPoint'],                         #评分
                    'checkInDate' : item['checkInDate'],                        #入住时间
                    'postDate' : item['postDate'],                              #发表时间
                    'imageNumber':len(item['imageList']),                       #该评论上传图片数
                    'usefulNumber':item['usefulNumber'],                        #有用数
                    'userCommentCount':item['userCommentCount'],                #该用户历史点评总数
                    'userCommentUsefulCount':item['userCommentUsefulCount'],    #该用户历史被点有用总数
                    'userImageCount':item['userImageCount'],                    #该用户历史上传图片总数
                    'content' : item['content']                                 #评论内容
                    })

startPage = 1
endPage =1000           

data=[]
for page in range(startPage, endPage + 1):
    fetchCmts(page)
    if data[-1]=='null':
        break
    time.sleep(8)
    
print("爬取完成")     #2191019     432451   1623771   434941  5982887  5312611  2335123  431959


path="".join(['C:/Users/dell/Desktop/论文/newdata/'+'如家酒店(大连星海公园店)'+'(共'+str(len(data)-1)+'条)'+'.json'])
with open(path, 'w', encoding='utf-8') as fp:
    json.dump(data[0:-1], fp, ensure_ascii=False, indent=4, sort_keys=False)