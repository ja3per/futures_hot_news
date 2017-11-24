from pymongo import MongoClient
from bson.objectid import ObjectId
from bs4 import BeautifulSoup
from urllib import request
import json
import math
from snownlp import SnowNLP
import numpy as np

def saveUrls():
    with open('aurls.txt', 'w') as f:
        mongoClient = MongoClient('172.24.177.30', 27017)
        db = mongoClient['futures_data']
        posts = db['sinanews']
        list = posts.find()
        templist = []
        for data in list:
            id = str(data['_id'])
            url = data['url']
            templist.append({'id': id, 'url': url})
            print(url)
        json.dump(templist, f)

def loadUrls():
    with open('aurls.txt') as f:
        li = json.load(f)
        return li

def getCUrl(url):
    tempUrl = 'http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=%s&newsid=%s&group=0&compress=0&ie=gbk&oe=gbk'
    response = request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'lxml')
    commentEl = soup.find('meta', attrs={'name': "comment"})['content']
    channel = commentEl.split(':')[0]
    newsid = commentEl.split(':')[1]
    return tempUrl % (channel, newsid)

def saveComments():
    index = 0
    mongoClient = MongoClient('172.24.177.30', 27017)
    db = mongoClient['futures_data']
    posts = db['comments']
    sinanews = db['sinanews']
    for data in loadUrls():
        try:
            index += 1
            tempList = []
            url = data['url']
            id = data['id']
            print(url)

            url = getCUrl(url)
            request.urlopen(url)
            response = request.urlopen(url+'&page=1&page_size=200')
            jsonStr = response.read()

            print(jsonStr[9:])
            jsonObj = json.loads(jsonStr[9:])

            tempList.extend(jsonObj['result']['cmntlist'])

            count = int(jsonObj['result']['count']['show'])
            pageNum = math.ceil(count / 200)
            if pageNum > 1:
                for page in range(2, pageNum + 1):
                    response = request.urlopen(url+('&page=%s&page_size=200' % page))
                    jsonStr = response.read()
                    jsonObj = json.loads(jsonStr[9:])
                    tempList.extend(jsonObj['result']['cmntlist'])
                    print('page: %s' % page)

            print(len(tempList))
            # break
            sentiments = []
            positive = 0
            negative = 0
            for temp in tempList:
                s = SnowNLP(temp['content'])
                sentiments.append(s.sentiments)
                if s.sentiments > 0.5:
                    positive += 1
                else:
                    negative += 1
            if len(sentiments) != 0:
                sentiment = np.mean(sentiments)
            else:
                sentiment = -1
            # saveObj = {'id': id, 'url': url, 'comment': tempList, 'sentiment': sentiment, 'positive': positive, 'negative': negative}
            print('第'+str(index)+'篇', sentiment, data['id'])
            # posts.insert_one(saveObj)
            sinanews.update({'_id': ObjectId(data['id'])}, {'$set': {'positive': positive, 'negative': negative}})
        except Exception as e:
            print(e)

def statistics():
    mongoClient = MongoClient('172.24.177.30', 27017)
    db = mongoClient['futures_data']
    posts = db['comments']
    posts2 = db['sinanews']
    # list = posts.find({'sentiment': {"$lte": 0.35}})
    list = posts.find()
    for data in list:

        if len(data['comment']) >= 50:
            print(data['id'])
            data2 = posts2.find_one({'_id': ObjectId(data['id'])})
            if data2 is not None:
                print(data2['title'], data['sentiment'])
                print(data2['url'])




if __name__ == '__main__':
    # saveUrls()
    # print(len(loadUrls()))
    # print(getCUrl('http://news.sina.com.cn/c/nd/2017-11-14/doc-ifynstfh7821553.shtml'))
    saveComments()
    # statistics()