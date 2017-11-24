#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import redis
from redisearch import Query
from redisearch import Client
from redisearch import TextField
#
# # Creating a client with a given index name
# client = Client('myIndex')
#
# # Creating the index definition and schema
# client.create_index((TextField('title', weight=5.0), TextField('body')))
#
# # Indexing a document
# client.add_document('doc1', title = 'RediSearch', body = 'Redisearch impements a search engine on top of redis')
#
# # Simple search
# res = client.search("search engine")
#
# # Searching with snippets
# res = client.search("search engine", snippet_sizes = {'body': 50})
#
# # Searching with complext parameters:
# q = Query("search engine").verbatim().no_content().paging(0,5)
# res = client.search(q)
#
#
# # the result has the total number of results, and a list of documents
# print res.total # "1"
# print res.docs[0].title
#

if __name__ == '__main__':
    r = redis.Redis(host='172.24.177.30', port=6379, db=0)   #如果设置了密码，就加上password=密码
    # r.set('foo', 'baba')   #或者写成 r['foo'] = 'bar'
    # print r.llen('hexun')
    print r.lindex('irons',1)
    # print r.lrange('eastmoney',3500,3600)