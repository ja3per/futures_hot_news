# coding=utf-8
import redis
import json
from snownlp import SnowNLP
from classify.VarietyClassifier import VarietyClassifier
from pyltp import *

class TrainFileBuilder(object):
    def __init__(self):
        pass
        self.pool = redis.ConnectionPool(host='172.24.177.30', port=6379)

    def makeTrainFile(self):
        r = redis.Redis(connection_pool=self.pool)
        list = r.lrange("eastmoney", 0, 8223)
        templist = []
        saveObj = []
        vclf = VarietyClassifier()
        vclf.loadModel('save/clf.pkl')
        with open('data/train1107.json', 'w', encoding='utf-8') as f:
            for article in list:
                temp = eval(article)
                title = temp['title']

                if title not in templist:
                    try:
                        saveTemp = dict()
                        keywords = temp['key_words'].replace(',', ' ')
                        type = vclf.predict(keywords)
                        if type != 0:
                            saveTemp['type'] = str(type)
                            saveTemp['keywords'] = keywords
                            saveTemp['title'] = title
                            saveTemp['url'] = temp['url']
                            saveTemp['description'] = temp['description']

                            # snowNlp = SnowNLP(saveTemp['description'])
                            print(saveTemp['title'])
                            # print(saveTemp['url'])
                            # print(saveTemp['description'])
                            # for sentence in snowNlp.sentences:
                            #     print(sentence)
                            # print('\n')

                            saveObj.append(saveTemp)
                        else:
                            continue
                    except Exception as ex:
                        print(ex)
                else:
                    print(title)

                templist.append(title)
            print(len(saveObj))
            json.dump(saveObj, f)

    def makeTypeFile(self):
        with open('data/train1107.json') as f:
            datas = json.load(f)

        with open('data/soybean.txt', 'w') as f:
            for data in datas:
                if data['type'] == '2':
                    f.write(data['title'] + '\n')
                    f.write(data['url'] + '\n')
                    f.write(data['keywords'] + '\n')
                    f.write(data['description'] + '\n')
                    snowNlp = SnowNLP(data['description'])
                    for sentence in snowNlp.sentences:
                        f.write(sentence + '\n')
                    f.write('\n')

        with open('data/iron.txt', 'w') as f:
            for data in datas:
                if data['type'] == '1':
                    f.write(data['title'] + '\n')
                    f.write(data['url'] + '\n')
                    f.write(data['keywords'] + '\n')
                    f.write(data['description'] + '\n')
                    snowNlp = SnowNLP(data['description'])
                    for sentence in snowNlp.sentences:
                        f.write(sentence + '\n')
                    f.write('\n')

    def test(self):
        with open('data/train1107.json', 'r') as f1:
            datas = json.load(f1)

        with open('data/train1110_505.json', 'w') as f:
            datasNew = []
            for index, data in zip(range(400, 500), datas[400: 500]):
                print(data['title'])
                uptype = input('类别(1正常,2上涨) index('+str(index)+'):')
                downtype = input('类别(1正常,2下跌) index('+str(index)+'):')
                print('\n')
                data['uptype'] = uptype
                data['downtype'] = downtype
                datasNew.append(data)
            json.dump(datasNew, f)

    def look(self):
        with open('data/train1110_501.json', 'r') as f:
            datas1 = json.load(f)

        with open('data/train1110_502.json', 'r') as f:
            datas2 = json.load(f)

        with open('data/train1110_503.json', 'r') as f:
            datas3 = json.load(f)

        with open('data/train1110_504.json', 'r') as f:
            datas4 = json.load(f)

        with open('data/train1110_505.json', 'r') as f:
            datas5 = json.load(f)


        list = []
        list.extend(datas1)
        list.extend(datas2)
        list.extend(datas3)
        list.extend(datas4)
        list.extend(datas5)

        with open('data/train1110_final.json', 'w') as f:
            json.dump(list, f)



if __name__ == '__main__':
    tfBuilder = TrainFileBuilder()
    # tfBuilder.makeTypeFile()
    # tfBuilder.makeTrainFile()
    tfBuilder.look()