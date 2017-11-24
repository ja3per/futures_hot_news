from gensim.models import Word2Vec
import json
from pyltp import *

with open('data/train1108_final.json') as f:
    datas = json.load(f)
    model_path = '/Users/lindi/work/舆情/spider/ltp_data_v3.4.0/cws.model'
    userdict_path = '/Users/lindi/work/舆情/spider/yqCrawl/sentiments/save/dict.txt'
    segmentor = Segmentor()
    segmentor.load_with_lexicon(model_path, userdict_path)
    # segmentor.load(model_path)

    with open('data/positive_direction.txt') as fp:
        plist = fp.readlines()

    with open('data/negative_direction.txt') as fn:
        nlist = fn.readlines()

    for data in datas:
        # print(data['udtype'], data['title'])
        for word in segmentor.segment(data['title']):
            if word in plist and data['udtype'] != '2':
                print('非涨', data['title'])

            if word in nlist and data['udtype'] != '3':
                print('非跌', data['title'])


    sentences = [segmentor.segment(article['title']) for article in datas]
    print(len(sentences))
    model = Word2Vec(sentences, size=200, workers=4, min_count=1)
