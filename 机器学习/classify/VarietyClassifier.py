import json
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib
from pymongo import MongoClient

class VarietyClassifier(object):
    def __init__(self):
        self.clf = DecisionTreeClassifier(random_state=1)
        self.vectorizer = TfidfVectorizer(min_df=0, strip_accents='unicode')
        with open('save/train1103.json', 'r', encoding='utf-8') as f:
            self.datas = json.load(f)
            self.X = [article['key_words'] for article in self.datas]
            self.vectorizer.fit_transform(self.X)
        self._loadModel()

    def _loadModel(self):
        self.clf = joblib.load('save/clf.pkl')

    def _predict(self, keyword):
        X_test = self.vectorizer.transform([' '.join(keyword.split(','))])
        y_test = self.clf.predict(X_test)

        return y_test[0]

    def doVarietyClassifier(self, name):
        mongoClient = MongoClient('172.24.177.30', 27017)
        db = mongoClient['futures_data']
        posts = db[name]
        for data in posts.find():
            try:
                type_variety = self._predict(data['split_keywords'])
                posts.update({'_id': data['_id']}, {'$set': {"type_variety": int(type_variety)}})
            except Exception as e:
                print(name, data['_id'], data['title'], e)
                continue


if __name__ == '__main__':
    clf = VarietyClassifier()
    clf.doVarietyClassifier('7hcn')
    clf.doVarietyClassifier('eastmoney')
    clf.doVarietyClassifier('hexun')
    clf.doVarietyClassifier('jrj')
    clf.doVarietyClassifier('qhrb')
    clf.doVarietyClassifier('wallstreetcn')
    clf.doVarietyClassifier('xinhua08')