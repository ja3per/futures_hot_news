import numpy as np
import math
from pyltp import *
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt


class SVC_Genetic(object):
    CROSS_RATE = 0.8
    MUTATION_RATE = 0.003
    N_GENERATIONS = 200

    def __init__(self, pop):
        self.pop = pop
        self.POP_NUM = len(pop)
        self.DNA_SIZE = len(pop[0])

    # 初始化测试数据
    def initTrainData(self):
        with open('data/train1110_final.json') as f:
            datas = json.load(f)
            model_path = '/Users/lindi/work/舆情/spider/ltp_data_v3.4.0/cws.model'
            userdict_path = '/Users/lindi/work/舆情/spider/yqCrawl/sentiments/save/dict.txt'
            segmentor = Segmentor()
            segmentor.load_with_lexicon(model_path, userdict_path)
            X = [' '.join(segmentor.segment(article['title'])) for article in datas]

            vectorizer = TfidfVectorizer(min_df=1, strip_accents='unicode')
            self.X = vectorizer.fit_transform(X).toarray()
            self.y = [article['downtype'] for article in datas]


    # 解码DNA
    def decodeDNA(self, DNA):
        '''
        kernel（1-3位）：‘linear’, ‘poly’, ‘rbf’, ‘sigmoid’, ‘precomputed’ 默认 ‘rbf’
        probability（4位）：‘True’, ‘False’ 默认 ‘False’
        shrinking（5位）： ‘True’, ‘False’ 默认 ‘True’
        verbose（6位）： ‘True’, ‘False’ 默认 ‘False’
        decision_function_shape（7位）：‘ovo’, ‘ovr’ 默认 ‘ovr’
        '''
        kernelNum = math.pow(2, 2)*DNA[0] + math.pow(2, 1)*DNA[1] + math.pow(2, 0)*DNA[2]
        if kernelNum == 0:
            kernel = 'rbf'
        elif kernelNum == 1:
            kernel = 'linear'
        elif kernelNum == 2:
            kernel = 'poly'
        elif kernelNum == 3:
            kernel = 'sigmoid'
        elif kernelNum == 4:
            kernel = 'precomputed'

        cNum = math.pow(2, 2)*DNA[3] + math.pow(2, 1)*DNA[4] + math.pow(2, 0)*DNA[5]
        if cNum == 0:
            c = 1.2
        elif cNum == 1:
            c = 1.4
        elif cNum == 2:
            c = 1.6
        elif cNum == 3:
            c = 1.8
        elif cNum == 4:
            c = 2
        elif cNum == 5:
            c = 2.2
        elif cNum == 6:
            c = 2.4
        elif cNum == 7:
            c = 2.6

        return kernel, c


    # 适应性修正
    def fitnessDNA(self, pop):
        tempDict = dict()
        tempList = list()
        for index, DNA in zip(range(self.POP_NUM), pop):
            appendFlag = True
            kernelNum = math.pow(2, 2)*DNA[0] + math.pow(2, 1)*DNA[1] + math.pow(2, 0)*DNA[0]
            if kernelNum > 4:
                DNA = np.array([0, 0, 0] + list(DNA[3:]))
                pop[index] = DNA

            for key in tempDict.keys():
                if (pop[key] == DNA).all():
                    tempList.append(tempDict[key])
                    appendFlag = False

            if appendFlag:
                # 训练
                # print(DNA)
                kernel, c = self.decodeDNA(DNA)
                score = self.cross_score(kernel, c)
                tempList.append(score)
                tempDict[index] = score
                pass
        return np.array(tempList)

    def cross_score(self, kernel, c):
        # print(kernel, probability, shrinking, verbose, decision_function_shape)
        clf = SVC(kernel=kernel,
                  C=c,
                  # probability=probability,
                  # shrinking=shrinking,
                  # verbose=verbose,
                  # decision_function_shape=decision_function_shape
                  )

        scores = cross_val_score(clf, self.X, self.y, cv=3, scoring='accuracy')
        # print(np.mean(scores) * 100)
        return np.mean(scores) * 100

    def select(self, pop, fitness):
        idx = np.random.choice(np.arange(self.POP_NUM), size=self.POP_NUM, replace=True, p=fitness/fitness.sum())
        return pop[idx]

    def crossover(self, parent, pop_copy):
        if np.random.rand() < self.CROSS_RATE:
            i_ = np.random.randint(0, self.POP_NUM, size=1)                             # select another individual from pop
            cross_points = np.random.randint(0, 2, size=self.DNA_SIZE).astype(np.bool)   # choose crossover points
            parent[cross_points] = pop[i_, cross_points]                            # mating and produce one child
        return parent

    def mutate(self, child):
        for point in range(self.DNA_SIZE):
            if np.random.rand() < self.MUTATION_RATE:
                child[point] = 1 if child[point] == 0 else 0
        return child

    def drawImage(self, scores):
        plt.rcParams['font.sans-serif'] = ['SimHei']
        x = list(range(200))
        plt.plot(x, scores)
        plt.xlabel('增长代')
        plt.ylabel('准确率')
        plt.show()

if __name__ == '__main__':
    # DEFAULT_DNA = [[0, 0, 0, 0, 1, 0, 0]]
    DEFAULT_DNA = [[0, 0, 0, 0, 0, 0]]
    POP_NUM = 100
    N_GENERATIONS = 200

    pop = np.array(DEFAULT_DNA).repeat(POP_NUM, axis=0)
    svcGen = SVC_Genetic(pop)
    svcGen.initTrainData()

    scores = []

    for _ in range(N_GENERATIONS):
        fitness = svcGen.fitnessDNA(pop)
        scores.append(np.average(fitness))
        print(np.average(fitness))
        print("Most fitted DNA: ", pop[np.argmax(fitness), :])
        pop = svcGen.select(pop, fitness)
        pop_copy = pop.copy()
        for parent in pop:
            child = svcGen.crossover(parent, pop_copy)
            child = svcGen.mutate(child)
            parent[:] = child
        # print(pop)
    svcGen.drawImage(scores)
