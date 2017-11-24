from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import preprocessing
import numpy as np
import time
import json
import matplotlib.pyplot as plt
from pyltp import *
from gensim.models import Word2Vec
from word2vecTest import Word2VecTest

class ClassifierCompare(object):

    def loadData(self):
        with open('data/train1110_final.json') as f:
            model_path = '/Users/lindi/work/舆情/spider/ltp_data_v3.4.0/cws.model'
            userdict_path = '/Users/lindi/work/舆情/spider/yqCrawl/sentiments/save/dict.txt'
            segmentor = Segmentor()
            # segmentor.load(model_path)
            segmentor.load_with_lexicon(model_path, userdict_path)

            with open('data/positive_direction.txt') as fp:
                plist = [p.replace('\n', '') for p in fp.readlines()]

            with open('data/negative_direction.txt') as fn:
                nlist = [n.replace('\n', '') for n in fn.readlines()]

            datas = json.load(f)
            self.X = [' '.join(segmentor.segment(article['title'])) for article in datas]
            print(self.X)
            self.Xn = []
            for X in self.X:
                for x in X.split(' '):
                    if x in plist:
                        X = X.replace(x, '上涨')
                    elif x in nlist:
                        X = X.replace(x, '下跌')
                self.Xn.append(X)
            print(self.X)
            print(self.Xn)
            self.Xn = self.X


            self.y = [article['downtype'] for article in datas]


    def runClassifier(self, clf):
        scale = TfidfVectorizer(min_df=0, strip_accents='unicode')
        startTime = time.time()
        scaling_pipeline = Pipeline([('scale', scale), ('predict', clf)])
        scores = cross_val_score(scaling_pipeline, self.Xn, self.y, cv=10, scoring='accuracy')
        endTime = time.time()
        useTime = endTime - startTime
        return scores, useTime

    def drawAnalysePicture(self, classifiers):
        # 绘图
        width = 0.5
        plt.rcParams['font.sans-serif'] = ['SimHei']
        name_list = [classifier['name'] for classifier in classifiers]
        x = list(range(len(name_list)))
        num_right = [np.mean(classifier['scores']) * 100 for classifier in classifiers]

        num_userTime = [classifier['useTime'] * 1000 for classifier in classifiers]
        plt.subplot(211)
        plt.bar(x, num_right, width=width, label='准确率', tick_label=name_list)
        plt.ylabel('准确率')
        # plt.xticks(rotation=45)
        plt.legend()
        for a, b in zip(x, num_right):
            plt.text(a, b, '%.2f' % b + '%', ha='center', va='bottom')

        plt.subplot(212)
        plt.bar(x, num_userTime, width=width, label='用时(毫秒)', tick_label=name_list)
        plt.ylabel('用时(毫秒)')
        # plt.xticks(rotation=45)
        plt.legend()
        for a, b in zip(x, num_userTime):
            plt.text(a, b, '%.2fms' % b, ha='center', va='bottom')

        plt.show()

if __name__ == '__main__':
    compare = ClassifierCompare()
    compare.loadData()

    classifiers = []
    # classifiers.append({'name': '朴素贝叶斯', 'clf': MultinomialNB(alpha=0.01, fit_prior=False)})
    # classifiers.append({'name': '决策树', 'clf': DecisionTreeClassifier(random_state=1)})
    # classifiers.append({'name': '随机森林', 'clf': RandomForestClassifier(random_state=1)})
    classifiers.append({'name': '支持向量机', 'clf': SVC(kernel='linear')})
    # classifiers.append({'name': '神经网络', 'clf': MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)})
    # classifiers.append({'name': 'K邻', 'clf': KNeighborsClassifier()})
    # classifiers.append({'name': '逻辑回归', 'clf': LogisticRegression()})
    # classifiers.append({'name': '随机梯度下降', 'clf': SGDClassifier()})

    for classifier in classifiers:
        scores, useTime = compare.runClassifier(classifier['clf'])
        classifier['scores'] = scores
        classifier['useTime'] = useTime

    compare.drawAnalysePicture(classifiers)








