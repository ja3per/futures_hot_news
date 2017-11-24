from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
import json
from pyltp import *
from pymongo import MongoClient

class VarietyClassifier(object):
    def __init__(self):
        self.clfup = DecisionTreeClassifier(random_state=1)
        self.clfdown = DecisionTreeClassifier(random_state=1)
        self.vectorizer = TfidfVectorizer(min_df=0, strip_accents='unicode')
        self._loadModel()

    def _loadModel(self):
        with open('data/train1110_final.json') as f:
            model_path = '/Users/lindi/work/舆情/spider/ltp_data_v3.4.0/cws.model'
            userdict_path = '/Users/lindi/work/舆情/spider/yqCrawl/sentiments/save/dict.txt'
            segmentor = Segmentor()
            segmentor.load_with_lexicon(model_path, userdict_path)

            datas = json.load(f)
            self.X = [' '.join(segmentor.segment(article['title'])) for article in datas]
            self.yd = [article['downtype'] for article in datas]
            self.yu = [article['uptype'] for article in datas]

            self._traning()

    def _traning(self):
        self.X = self.vectorizer.fit_transform(self.X)
        self.clfdown.fit(self.X, self.yd)
        self.clfup.fit(self.X, self.yu)

    def _predict(self, keyword):
        X_test = self.vectorizer.transform([' '.join(keyword.split(','))])
        y_down = self.clfdown.predict(X_test)
        y_up = self.clfup.predict(X_test)

        return y_up, y_down

    def doVarietyClassifier(self, name):
        mongoClient = MongoClient('172.24.177.30', 27017)
        db = mongoClient['futures_data']
        posts = db['futures_news']
        for data in posts.find():
            try:
                print(data['title'])
                print(data['split_title'])
                type_up, type_down = self._predict(data['split_title'])
                print(type_up[0], type_down[0])
                posts.update({'_id': data['_id']}, {'$set': {"type_up": type_up[0], "type_down": type_down[0]}})
            except Exception as e:
                print(name, data['_id'], data['title'])
                continue

if __name__ == '__main__':
    clf = VarietyClassifier()
    clf.doVarietyClassifier('jrj')
    # clf.doVarietyClassifier('qhrb')
    # clf.doVarietyClassifier('xinhua08')