# coding=utf-8


import time
from datetime import datetime
from yqCrawl.items import YqcrawlItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spider import CrawlSpider, Rule


class JrjSpider(CrawlSpider):
    name = 'jrj'
    allowed_domains = ['futures.jrj.com.cn']
    start_urls = ['http://futures.jrj.com.cn']
    date = time.strftime("%Y/%m/%d", time.localtime())
    dateFormat = '%Y-%m-%d %H:%M:%S'
    rules = (
        # Rule(LinkExtractor(allow=('.*futures.jrj.com.cn.*%s.*' % date, )),
        Rule(LinkExtractor(allow=('http://futures.jrj.com.cn/2017/.*', )),
             callback='parse_item',
             follow=True),
    )

    def parse_item(self, response):
        div_title = response.xpath('//meta[@property="og:title"]/@content').extract()
        div_date = response.xpath('//meta[@property="og:release_date"]/@content').extract()
        div_content = response.xpath('//div[@class="titmain"]').extract()
        content = response.xpath('string(//div[@class="titmain"])').extract_first(default="").strip()
        keywords = response.xpath('//meta[@name="keywords"]/@content').extract()
        description = response.xpath('//meta[@name="description"]/@content').extract()

        if len(div_title) > 0 and len(div_date) > 0 and len(div_content) > 0:
            print(div_title, div_date, div_content)
            item = YqcrawlItem()
            item['spider_name'] = self.name
            item['url'] = response.url
            item['title'] = div_title[0]
            item['date'] = str(datetime.strptime(div_date[0], self.dateFormat))
            # item['div_content'] = div_content[0]
            item['content'] = content
            item['keywords'] = keywords[0]
            item['description'] = description[0]

            yield item

