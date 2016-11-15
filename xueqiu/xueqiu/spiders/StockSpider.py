# coding=utf-8
import json
import logging
import logging.handlers

import re

import pymongo
import scrapy
from scrapy import Request, FormRequest, signals
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.project import get_project_settings

logger = logging.getLogger('xueqiu-comment')
logger.setLevel(logging.DEBUG)


class StockSpider(CrawlSpider):
    name = 'stock'
    main_page_url = 'https://xueqiu.com/'
    # https://xueqiu.com/stock/cata/stocklist.json?page=1&size=100&order=asc&orderby=code&type=11%2C12
    # size 最大为 100
    # orderby =code 股票编码
    # type = 11,12 深圳 上海
    stock_api = 'https://xueqiu.com/stock/cata/stocklist.json?size=100&order=asc&orderby=code&type=11%2C12&page={page}'
    count = 20
    # 最多只能访问100页
    page_count = 100



    def __init__(self, *a, **kw):
        settings = get_project_settings()
        # settings.set('ITEM_PIPELINES', {'StockPipeline': 1}, 20)

    def start_requests(self):
        return [Request(url=self.main_page_url, headers=self.settings['DEFAULT_REQUEST_HEADERS'],
                        callback=self.after_cookie)]

    def after_cookie(self, response):
        first_url = self.stock_api.format(page=1) + '&hl=0'
        yield Request(first_url, headers=self.settings['DEFAULT_REQUEST_HEADERS'], callback=self.handle)

    def handle(self, response):
        content = json.loads(response.body)
        stock_count = content.get('count').get('count')

        actual_page_count = (stock_count - 1) / self.count + 1

        _page_count = min(self.page_count, actual_page_count)
        for i in range(1, _page_count + 1):
            yield Request(self.stock_api.format(page=i),
                          headers=self.settings['DEFAULT_REQUEST_HEADERS'])

    def parse(self, response):
        # type:scrapy.http.Response
        content = json.loads(response.body)
        yield content
