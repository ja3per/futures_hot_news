import json
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

class tt(object):
    def loadData(self):
        with open('data/train1109.json') as f:
            with open('data/positive_direction.txt') as fp:
                plist = [p.replace('\n', '') for p in fp.readlines()]

            with open('data/negative_direction.txt') as fn:
                nlist = [n.replace('\n', '') for n in fn.readlines()]

            datas = json.load(f)
            self.X = [article['split_title'] for article in datas]
            self.Xn = []
            for X in self.X:
                for x in X.split(' '):
                    if x in plist:
                        X = X.replace(x, '上涨')
                    elif x in nlist:
                        X = X.replace(x, '下跌')
                self.Xn.append(X)

            print(self.Xn)
            # self.Xn = self.X

            self.y = [article['udtype'] for article in datas]

    def train(self):
        self.scale = TfidfVectorizer(min_df=0, strip_accents='unicode')
        self.Xn = self.scale.fit_transform(self.Xn)
        self.clf = SGDClassifier()
        self.clf.fit(self.Xn, self.y)
        print('||'.join(self.scale.get_feature_names()))

    def test(self, line, y):
        nline = self.scale.transform([line])
        ny = self.clf.predict(nline)
        if ny[0] != y:
            # pass
            print(line, y, ny[0])

    def runTest(self):
        with open('data/positive_direction.txt') as fp:
            plist = [p.replace('\n', '') for p in fp.readlines()]

        with open('data/negative_direction.txt') as fn:
            nlist = [n.replace('\n', '') for n in fn.readlines()]

        with open('data/train1109.json') as f:
            datas = json.load(f)
            for data in datas:
                titles = data['split_title']
                for title in data['split_title'].split(' '):
                    if title in plist:
                        titles = titles.replace(title, '上涨')
                    if title in nlist:
                        titles = titles.replace(title, '下跌')
                    # if title == '商品':
                    #     titles = titles.replace(title, '')
                self.test(titles, data['udtype'])

if __name__ == '__main__':
    ttt = tt()
    ttt.loadData()
    ttt.train()
    ttt.runTest()
    # ttt.test('铁矿石 大幅 上涨', '3')