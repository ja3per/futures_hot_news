import numpy as np
import json
from pyltp import *
from gensim.models import Word2Vec

class Word2VecTest(object):

    def getWordVecs(self, wordList, model, t):
        # print(t, ' '.join(wordList))
        vecs = []
        for word in wordList:
            try:
                vecs.append(model[word])
            except KeyError:
                continue

        return np.array(vecs, dtype='float')

    def loadData(self):
        model_path = '/Users/lindi/work/舆情/spider/ltp_data_v3.4.0/cws.model'
        userdict_path = '/Users/lindi/work/舆情/spider/yqCrawl/sentiments/save/dict.txt'
        segmentor = Segmentor()
        segmentor.load_with_lexicon(model_path, userdict_path)
        posInput = []
        with open('data/train1108_final.json') as f:
            datas = json.load(f)

            for data in datas:
                if data['udtype'] == '2':
                    print(data['udtype'], data['title'])

            sentences = [segmentor.segment(article['title']) for article in datas]
            model = Word2Vec(sentences, size=200, workers=4, min_count=1)
            # print txtfile
            for data in datas:
                title = data['title']
                # resultList = [word for word in self.getWordVecs(segmentor.segment(title), model)]
                resultList = self.getWordVecs(segmentor.segment(title), model, data['udtype'])
                # for each sentence, the mean vector of all its vectors is used to represent this sentence
                if len(resultList) != 0:
                    resultArray = [word for word in sum(np.array(resultList))/len(resultList)]
                    # resultArray = sum(np.array(resultList))/len(resultList)
                    posInput.append({'x': resultArray,
                                     'y': data['udtype']})

            # print(posInput)
        return [pos['x'] for pos in posInput], [pos['y'] for pos in posInput]

if __name__ == '__main__':
    Word2VecTest().loadData()


