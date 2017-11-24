# -*- coding: utf-8 -*-
import datetime

from elasticsearch import Elasticsearch
from flask import Flask, jsonify, make_response, request
from flask_cors import *
from flask_mongoengine import *
from mongoengine.queryset.visitor import Q

app = Flask(__name__)
CORS(app)

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'futures_data',
    'host': '172.24.177.30',
    'port': 27017
}
db = MongoEngine(app)
now = datetime.datetime.now()
now_str = now.strftime('%Y-%m-%d')


@app.route("/")
def index():
    return "hello jasper~"


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/hotnews/api/v1.0/top', methods=['GET'])
@cross_origin()
def get_hot_news():
    now_str = '2017-11-22'
    hot_news = HotNews.objects(hot_news_date=now_str, news_type='sina').only('_id', 'news_short_title', 'news_keywords',
                                                                             'news_url',
                                                                             'hot_news_date').limit(4)
    return jsonify({'hotnews': hot_news})


@app.route('/hotnews/api/v1.0/topFutures', methods=['GET'])
@cross_origin()
def get_hot_futures_news():
    now_str = '2017-11-22'
    hot_futures_news = HotNews.objects(hot_news_date=now_str, news_type='futures').only('_id', 'news_short_title',
                                                                                        'news_keywords',
                                                                                        'news_url',
                                                                                        'hot_news_date').limit(4)
    return jsonify({'hotnews': hot_futures_news})


@app.route('/hotnews/api/v1.0/searchHot', methods=['GET'])
@cross_origin()
def search_hot_news():
    news_keywords = request.args.get("news_keywords")
    now = datetime.datetime.now()
    nowStr = now.strftime('%Y-%m-%d')
    nowStr = '2017-11-22'
    hot_news = HotNews.objects(news_keywords=news_keywords, hot_news_date=nowStr).only('news_list').limit(1)
    return jsonify({'hot_news': hot_news})


@app.route('/hotnews/api/v1.0/searchAll', methods=['GET'])
@cross_origin()
def search_all_news():
    news_keywords = request.args.get("news_keywords")
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=int(365))
    n_months = now - delta
    start_date = n_months.strftime("%Y-%m-%d %H:%M:%S")
    end_date = now.strftime("%Y-%m-%d %H:%M:%S")
    if is_valid_date(request.args.get("start_date")) and request.args.get("start_date") is not None:
        start_date = request.args.get("start_date") + " 00:00:00"
    if is_valid_date(request.args.get("end_date")) and request.args.get("end_date") is not None:
        end_date = request.args.get("end_date") + " 00:00:00"

    esc = ElasticSearchClass('172.24.177.30', '9200', '', '')
    res1 = esc.es.search("futures_data", size=30, body={
        # 'query': {
        #     # "terms": {"content": temp_list}, #字段匹配查询
        #     "match": {"title": news_keywords},  # 模糊查询
        # },
        "query": {
            "bool": {
                "must": [
                    {"match": {"title": news_keywords}},
                    # {"match": {"content": "Elasticsearch"}}
                ],
                "filter": [
                    # {"term": {"status": "published"}},
                    {"range":
                         {"date":
                              {"gte": start_date, "lte": end_date}
                          }
                     }
                ]
            }
        }
    })
    print '2搜索耗时：', res1['took'], '秒，结果数：', res1['hits']['total'], '条'
    return jsonify({'all_news': res1['hits']['hits']})


@app.route('/hotnews/api/v1.0/queryByType', methods=['GET'])
@cross_origin()
def query_by_type():
    futures_news_none = FuturesNews.objects(type_variety=0).only('spider_name', 'url', 'title', 'date', 'description',
                                                                 'type_up', 'type_down').limit(15)
    futures_news_iron = FuturesNews.objects(type_variety=1).only('spider_name', 'url', 'title', 'date', 'description',
                                                                 'type_up', 'type_down').limit(15)
    futures_news_bean = FuturesNews.objects(type_variety=2).only('spider_name', 'url', 'title', 'date', 'description',
                                                                 'type_up', 'type_down').limit(15)
    sina_news = SinaNews.objects().only('spider_name', 'url', 'title', 'date', 'description', 'positive',
                                        'negative').limit(15)
    futures_news = [{"futures_news_none": futures_news_none, "futures_news_iron": futures_news_iron,
                     "futures_news_bean": futures_news_bean, "sina_news": sina_news}]
    return jsonify({'futures_news': futures_news})


@app.route('/hotnews/api/v1.0/mediaNewsCount', methods=['GET'])
@cross_origin()
def query_media_news_count():
    type_variety = request.args.get("type_variety")
    variety_group_count = FuturesNews.objects.aggregate(
        {'$match': {
            'type_variety': int(type_variety)
        }},
        {
            '$group': {'_id': '$spider_name', 'count': {'$sum': 1}}
        })
    total_group_count = FuturesNews.objects.aggregate(
        {
            '$group': {'_id': '$spider_name', 'count': {'$sum': 1}}
        })
    return jsonify({'variety_group_count': list(variety_group_count), 'total_group_count': list(total_group_count)})


@app.route('/hotnews/api/v1.0/dailyNewsCount', methods=['GET'])
@cross_origin()
def query_daily_news_count():
    # type_variety = request.args.get("type_variety")
    count_days = request.args.get("count_days")
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=int(count_days))
    n_days = now - delta
    # from_date = datetime.datetime.strptime("2017-11-1", "%Y-%m-%d")
    daily_news_count = FuturesNews.objects(Q(date__gte=n_days)).aggregate(
        {
            '$group': {'_id': '$date_str', 'count': {'$sum': 1}}
        },
        {
            '$sort': {'_id': 1}
        }
    )
    return jsonify({'total_news_count': list(daily_news_count)})


@app.route('/hotnews/api/v1.0/wordCloud', methods=['GET'])
@cross_origin()
def query_word_cloud():
    limit = request.args.get("limit")
    variety_type = request.args.get("variety_type")
    word_cloud = FuturesNewsWordCloud.objects(variety_type=variety_type).limit(int(limit))
    return jsonify({"word_cloud": word_cloud})


# 判断是否是一个有效的日期字符串
def is_valid_date(date_str):
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except:
        return False


class FuturesNews(db.Document):
    meta = {
        'collection': 'futures_news',
        'ordering': ['-date'],
        'strict': False
    }

    _id = db.ObjectIdField()
    spider_name = db.StringField()
    url = db.StringField()
    title = db.StringField()
    date = db.DateTimeField()
    description = db.StringField()
    type_variety = db.IntField()
    type_up = db.StringField()
    type_down = db.StringField()
    date_str = db.StringField()


class FuturesNewsWordCloud(db.Document):
    meta = {
        'collection': 'futures_news_word_cloud',
        'ordering': ['-value'],
        'strict': False
    }

    _id = db.ObjectIdField()
    name = db.StringField()
    value = db.StringField()
    variety_type = db.IntField()


class SinaNews(db.Document):
    meta = {
        'collection': 'sinanews',
        'ordering': ['-date'],
        'strict': False
    }

    _id = db.ObjectIdField()
    spider_name = db.StringField()
    url = db.StringField()
    title = db.StringField()
    date = db.StringField()
    description = db.StringField()
    type_variety = db.IntField()
    type_up = db.StringField()
    type_down = db.StringField()
    positive = db.IntField()
    negative = db.IntField()


class HotNews(db.Document):
    meta = {
        'collection': 'hot_news',
        'ordering': ['-hot_ratio'],
        'strict': False
    }

    _id = db.ObjectIdField()
    news_type = db.StringField()
    news_order = db.StringField()
    news_count = db.StringField()
    hot_ratio = db.StringField()
    news_title = db.StringField()
    news_short_title = db.StringField()
    news_url = db.StringField()
    news_from = db.StringField()
    hot_news_date = db.StringField()
    news_keywords = db.StringField()
    news_list = db.ListField(db.StringField())


class HotNewsFutures(db.Document):
    meta = {
        'collection': 'hot_news_futures',
        'ordering': ['-hot_ratio'],
        'strict': False
    }

    _id = db.ObjectIdField()
    news_type = db.StringField()
    news_order = db.StringField()
    news_count = db.StringField()
    hot_ratio = db.StringField()
    news_title = db.StringField()
    news_short_title = db.StringField()
    news_url = db.StringField()
    news_from = db.StringField()
    hot_news_date = db.StringField()
    news_keywords = db.StringField()
    news_list = db.ListField(db.StringField())


class ElasticSearchClass(object):
    def __init__(self, host, port, user, passwrod):
        self.host = host
        self.port = port
        self.user = user
        self.password = passwrod
        self.connect()

    def connect(self):
        self.es = Elasticsearch(hosts=[{'host': self.host, 'port': self.port}],
                                http_auth=(self.user, self.password))

    def count(self, indexname):
        """
        :param indexname:
        :return: 统计index总数
        """
        return self.es.count(index=indexname)

    def delete(self, indexname, doc_type, id):
        """
        :param indexname:
        :param doc_type:
        :param id:
        :return: 删除index中具体的一条
        """
        self.es.delete(index=indexname, doc_type=doc_type, id=id)

    def get(self, indexname, id):
        return self.es.get(index=indexname, id=id)

    def search(self, indexname, size=10):
        try:
            return self.es.search(index=indexname, size=size, sort="@timestamp:desc")
        except Exception as err:
            print(err)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
