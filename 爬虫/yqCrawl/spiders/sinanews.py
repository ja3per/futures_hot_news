# coding=utf-8


import time
from datetime import datetime
from yqCrawl.items import YqcrawlItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spider import CrawlSpider, Rule


class EastmoneySpider(CrawlSpider):
    name = 'sinanews'
    allowed_domains = ['news.sina.com.cn']
    start_urls = ['http://news.sina.com.cn/']
    dateFormat = '%Y-%m-%d %H:%M:%S'
    rules = (
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-10-31', )),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-10-30', )),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-10-29', )),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-10-28', )),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-10-27', )),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-10-26', )),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-10-25', )),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-10-24', )),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-10-23', )),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-10-22', )),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-10-21', )),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-10-20', )),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-10-19', )),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-10-18', )),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-10-17', )),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-10-16', )),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-11-15', )),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-10-14', )),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-10-13', )),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-10-12', )),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-10-11', )),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-10-10', )),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-10-09', )),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-10-08', )),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-10-07', )),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-10-06', )),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-10-05', )),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-10-04', )),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-10-03', )),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-10-02', )),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(allow=('http://news.sina.com.cn/.*%s.*' % '2017-10-01', )),
             callback='parse_item',
             follow=True),
    )

    def parse_item(self, response):
        div_title = response.xpath('//h1[@id="artibodyTitle"]/text()').extract()
        div_date = response.xpath('//meta[@name="weibo: article:create_at"]/@content').extract()
        content = response.xpath('string(//div[@id="artibody"])').extract_first(default="").strip()
        keywords = response.xpath('//meta[@name="keywords"]/@content').extract()
        description = response.xpath('//meta[@name="description"]/@content').extract()

        if len(div_title) > 0 and len(content) > 0:
            print(div_title, content)
            item = YqcrawlItem()
            item['spider_name'] = self.name
            item['url'] = response.url
            item['title'] = div_title[0]
            item['date'] = str(datetime.strptime(div_date[0], self.dateFormat))
            item['content'] = content
            item['keywords'] = keywords[0]
            item['description'] = description[0]

            yield item

