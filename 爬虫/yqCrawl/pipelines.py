# coding=utf-8

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis
import requests
import json
from pymongo import MongoClient

class YqcrawlPipeline(object):
    def __init__(self):
        pass
        # self.pool = redis.ConnectionPool(host='localhost', port=6379)
        self.pool = redis.ConnectionPool(host='172.24.177.30', port=6379)
        self.mongoClient = MongoClient('172.24.177.30', 27017)

    def process_item(self, item, spider):
        # 数据清理
        item['content'] = item['content'].replace('\r', '').replace('\n', '').replace('\t', '')
        item['split_words'] = []


        resp = requests.post('http://172.24.177.30:9200/futures_data/article/', data=json.dumps(dict(item)))
        respJson = json.loads(resp.text)

        item['es_id'] = respJson['_id']
        r = redis.Redis(connection_pool=self.pool)
        r.lpush(item['spider_name'], dict(item))

        db = self.mongoClient['futures_data']
        posts = db[item['spider_name']]
        posts.insert_one(dict(item))

        return item
