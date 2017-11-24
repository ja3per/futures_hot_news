# coding=utf-8


import time
from datetime import datetime
from yqCrawl.items import YqcrawlItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spider import CrawlSpider, Rule


class EastmoneySpider(CrawlSpider):
    name = 'eastmoney_x'
    allowed_domains = ['forex.eastmoney.com']
    start_urls = ['http://forex.eastmoney.com/']
    date = time.strftime('%Y%m%d', time.localtime())
    dateFormat = '%Y年%m月%d日 %H:%M'
    rules = (
        Rule(LinkExtractor(allow=('http://forex.eastmoney.com.*', )),
             callback='parse_item',
             follow=True),
    )

    def parse_item(self, response):
        div_title = response.xpath('//div[@class="newsContent"]/h1/text()').extract()
        div_date = response.xpath('//div[@class="time-source"]/div[@class="time"]/text()').extract()
        div_content = response.xpath('//div[@id="ContentBody"]').extract()
        content = response.xpath('string(//div[@id="ContentBody"])').extract_first(default="").strip()
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

