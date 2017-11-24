# coding=utf-8


import time
from datetime import datetime
from yqCrawl.items import YqcrawlItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spider import CrawlSpider, Rule


class WallstreetcnSpider(CrawlSpider):
    name = 'wallstreetcn'
    allowed_domains = ['wallstreetcn.com']
    start_urls = ['https://wallstreetcn.com']
    date = time.strftime("%Y-%m-%d", time.localtime())
    dateFormat = '%Y-%m-%d %H:%M'
    rules = (
        Rule(LinkExtractor(allow=('.*wallstreetcn.com/articles/.*', )),
             callback='parse_item',
             follow=True),
    )

    def parse_item(self, response):
        div_title = response.xpath('//div[@class="article__heading__title"]/text()').extract()
        div_date = response.xpath('//div[@class="article__heading__meta"]/div[@class="meta-item article__heading__meta__left"]/span[@class="meta-item__text"]/text()').extract()
        div_content = response.xpath('//div[@class="node-article-content"]').extract()
        content = response.xpath('string(//div[@class="node-article-content"])').extract_first(default="").strip()
        keywords = response.xpath('//meta[@name="keywords"]/@content').extract()
        description = response.xpath('//meta[@name="description"]/@content').extract()

        # if len(div_title) > 0 and len(div_date) > 0 and len(div_content) > 0 and div_date[0][0: 10] == self.date:
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

