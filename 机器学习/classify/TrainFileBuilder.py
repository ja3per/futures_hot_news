import redis
import json

class TrainFileBuilder(object):
    def __init__(self):
        pass
        self.pool = redis.ConnectionPool(host='172.24.177.30', port=6379)

    def changeClassifier(self):
        saveObj = []
        a1Num = 0
        a2Num = 0

        otherNum = 0
        with open('train1103.json', 'r', encoding='utf-8') as f:
            list = json.load(f)

        with open('train1031_n.json', 'w', encoding='utf-8') as f:
            for article in list:
                saveTemp = dict()
                saveTemp['split_words'] = article['split_words']

                if saveTemp['split_words'].find('铁矿石') >= 0:
                    saveTemp['type'] = 1
                    a1Num += 1
                elif saveTemp['split_words'].find('豆粕') >= 0:
                    saveTemp['type'] = 2
                    a2Num += 1

                else:
                    if otherNum > 100:
                        continue
                    saveTemp['type'] = 0
                    otherNum += 1
                saveObj.append(saveTemp)

            print('铁矿石:', a1Num)
            print('豆粕:', a2Num)

            print('其他:', otherNum)
            print('总记录:', len(saveObj))
            json.dump(saveObj, f)

    def makeTrainFileFOSX(self):
        r = redis.Redis(connection_pool=self.pool)
        listf = r.lrange("eastmoney_f", 0, 326)
        listo = r.lrange("eastmoney_o", 0, 484)
        lists = r.lrange("eastmoney_s", 0, 332)
        listx = r.lrange("eastmoney_x", 0, 328)
        templist = []
        saveObj = []
        with open('train1031fosx.json', 'w', encoding='utf-8') as f:
            for article in listf:
                temp = eval(article)
                title = temp['title']

                if title not in templist:
                    try:
                        saveTemp = dict()
                        saveTemp['split_words'] = temp['split_words'].replace(',', ' ')
                        saveTemp['title'] = title
                        saveTemp['type'] = 0
                        saveObj.append(saveTemp)
                    except:
                        pass
                else:
                    print(title)

                templist.append(title)
            for article in listo:
                temp = eval(article)
                title = temp['title']

                if title not in templist:
                    try:
                        saveTemp = dict()
                        saveTemp['split_words'] = temp['split_words'].replace(',', ' ')
                        saveTemp['title'] = title
                        saveTemp['type'] = 1
                        saveObj.append(saveTemp)
                    except:
                        pass
                else:
                    print(title)

                templist.append(title)

            for article in lists:
                temp = eval(article)
                title = temp['title']

                if title not in templist:
                    try:
                        saveTemp = dict()
                        saveTemp['split_words'] = temp['split_words'].replace(',', ' ')
                        saveTemp['title'] = title
                        saveTemp['type'] = 2
                        saveObj.append(saveTemp)
                    except:
                        pass
                else:
                    print(title)

                templist.append(title)

            for article in listx:
                temp = eval(article)
                title = temp['title']

                if title not in templist:
                    try:
                        saveTemp = dict()
                        saveTemp['split_words'] = temp['split_words'].replace(',', ' ')
                        saveTemp['title'] = title
                        saveTemp['type'] = 3
                        saveObj.append(saveTemp)
                    except:
                        pass
                else:
                    print(title)

                templist.append(title)

            print(len(saveObj))
            json.dump(saveObj, f)

    def makeTrainFile(self):
        r = redis.Redis(connection_pool=self.pool)
        list = r.lrange("eastmoney", 0, 8223)
        templist = []
        saveObj = []
        with open('train1103.json', 'w', encoding='utf-8') as f:
            for article in list:
                temp = eval(article)
                title = temp['title']

                if title not in templist:
                    try:
                        saveTemp = dict()
                        saveTemp['key_words'] = temp['key_words'].replace(',', ' ')
                        saveTemp['title'] = title
                        saveTemp['url'] = temp['url']
                        saveTemp['split_words'] = temp['split_words']

                        if saveTemp['key_words'].find('铁矿石') >= 0:
                            saveTemp['type'] = 1
                            print('铁矿石')
                        elif saveTemp['key_words'].find('黑色系') >= 0:
                            saveTemp['type'] = 1
                            print('黑色系')
                        elif saveTemp['key_words'].find('豆粕') >= 0:
                            saveTemp['type'] = 2
                            print('豆粕')
                        else:
                            saveTemp['type'] = 0
                        saveObj.append(saveTemp)
                    except:
                        pass
                else:
                    print(title)

                templist.append(title)
            print(len(saveObj))
            json.dump(saveObj, f)


if __name__ == '__main__':
    tfBuilder = TrainFileBuilder()
    tfBuilder.makeTrainFile()
    # tfBuilder.changeClassifier()
    # tfBuilder.makeTrainFileFOSX()