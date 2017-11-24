# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YqcrawlItem(scrapy.Item):
    # 爬虫名称
    spider_name = scrapy.Field()
    # URL链接
    url = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 日期
    date = scrapy.Field()
    # 内容
    content = scrapy.Field()
    # 原内容
    # div_content = scrapy.Field()
    # 关键词
    keywords = scrapy.Field()
    # 概述
    description = scrapy.Field()
    # 分词列
    split_words = scrapy.Field()
