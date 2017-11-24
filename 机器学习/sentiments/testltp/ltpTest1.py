# -*- coding: utf-8 -*-
from pyltp import *
from nltk.parse import *

sents = SentenceSplitter.split('元芳你,怎么看？我就趴窗口上看呗！')  # 分句
print('\n'.join(sents))

model_path = '/Users/lindi/work/舆情/spider/ltp_data_v3.4.0/cws.model'
segmentor = Segmentor()
segmentor.load(model_path)

words = segmentor.segment('otcws是ltp分词模型的训练套件，用户可以使用otcws训练获得ltp的分词模型。otcws支持从人工切分数据中训练分词模型和调用分词模型对句子进行切分。人工切分的句子的样例如下.')
postagger = Postagger()
postagger.load('/Users/lindi/work/舆情/spider/ltp_data_v3.4.0/pos.model')
# postags = postagger.postag(words)
# for word, postag in zip(words, postags):
#     print(word+'/'+postag)

sents = SentenceSplitter.split('油脂与黑色系上涨 鸡蛋封死跌停')
print(sents[0])
words = segmentor.segment(sents[0])

postags = postagger.postag(words)

parser = Parser()
parser.load('/Users/lindi/work/舆情/spider/ltp_data_v3.4.0/parser.model')
arcs = parser.parse(words, postags)
arclen = len(arcs)
conll = ''
print(arcs[0])
for i in range(arclen):
    # if arcs[i].head == 0:
        # arcs[i].relation = 'ROOT'
    conll += '\t'+words[i]+'('+postags[i]+')\t'+postags[i]+'\t'+str(arcs[i].head)+'\t'+arcs[i].relation+'\n'
print(conll)
# conlltree = DependencyGraph(conll)
# tree = conlltree.tree()
# tree.draw()
