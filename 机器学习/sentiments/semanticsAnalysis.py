# -*- coding: utf-8 -*-
from pyltp import *
from nltk.parse import *

class semanticsAnalysis(object):
    def __init__(self):
        # 分词初始化
        self.segmentor = Segmentor()
        self.segmentor.load('/Users/lindi/work/舆情/spider/ltp_data_v3.4.0/cws.model')

        # 词性标注初始化
        self.postagger = Postagger()
        self.postagger.load('/Users/lindi/work/舆情/spider/ltp_data_v3.4.0/pos.model')

        # 语义分析初始化
        self.parser = Parser()
        self.parser.load('/Users/lindi/work/舆情/spider/ltp_data_v3.4.0/parser.model')

    def splitWord(self, sentence):
        return self.segmentor.segment(sentence)

    def postagWords(self, words):
        postags = self.postagger.postag(words)

    def parser(self, words, postags):
        arcs = self.parser.parse(words, postags)


