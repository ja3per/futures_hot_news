# coding=utf-8


import time
from datetime import datetime
from yqCrawl.items import YqcrawlItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spider import CrawlSpider, Rule


class SevenhcnSpider(CrawlSpider):
    name = '7hcn'
    allowed_domains = ['www.7hcn.com']
    start_urls = ['http://www.7hcn.com']
    date = time.strftime("%Y-%m-%d", time.localtime())
    dateFormat = '时间：%Y-%m-%d %H:%M:%S'
    rules = (
        Rule(LinkExtractor(allow=('.*www.7hcn.com/article/.*', )),
             callback='parse_item',
             follow=True),
    )

    def parse_item(self, response):
        div_title = response.xpath('//title/text()').extract()
        div_date = response.xpath('//div[@class="fix box-share"]/span[1]/text()').extract()
        div_content = response.xpath('//div[@class="box-show"]').extract()
        content = response.xpath('string(//div[@class="box-show"])').extract_first(default="").strip()
        keywords = response.xpath('//meta[@name="keywords"]/@content').extract()
        description = response.xpath('//meta[@name="description"]/@content').extract()

        if len(div_title) > 0 and len(div_date) > 0 and len(div_content) > 0 and div_date[0][3: 13] == self.date:
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

