# coding=utf-8

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    # process.crawl('eastmoney')
    # process.crawl('qhrb')
    # process.crawl('jrj')
    # process.crawl('xinhua08')
    # process.crawl('hexun')
    # process.crawl('wallstreetcn')
    # process.crawl('7hcn')
    # process.crawl('eastmoney_f')
    # process.crawl('eastmoney_o')
    # process.crawl('eastmoney_s')
    # process.crawl('eastmoney_x')
    process.crawl('sinanews')
    process.start()
