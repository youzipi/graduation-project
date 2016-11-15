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
from scrapy.xlib.pydispatch import dispatcher

logger = logging.getLogger('xueqiu-comment')
logger.setLevel(logging.DEBUG)


class CommentSpider(CrawlSpider):
    name = 'comment'
    main_page_url = 'https://xueqiu.com/'
    # https://xueqiu.com/statuses/search.json?source=user&sort=time&count=10&symbol=SZ300104&page=1
    # count z最大为20
    # source = user,all,...
    comment_api = 'https://xueqiu.com/statuses/search.json?source=user&sort=time&count=20&symbol={symbol}&page={page}'
    symbol = 'SZ300104'
    sort = 'time'
    count = 20
    # 最多只能访问100页
    page_count = 100

    total_new_count = 0  # 所有目标股票新增评论数 todo

    def __init__(self, *a, **kw):
        self.settings = get_project_settings()
        host = self.settings['MONGO_HOST']
        port = self.settings['MONGO_PORT']
        client = pymongo.MongoClient(host=host, port=port)

        db_name = self.settings['MONGO_DBNAME']
        db = client[db_name]
        self.collection = db['stocks']
        # self.stocks = self.collection.find()
        self.stocks = self.collection.find({'count': {"gt": 2000}}).sort('count', pymongo.DESCENDING).limit(
            20)  # 946/3631
        # self.stocks = self.collection.find({'symbol': 'SZ002264'})

        dispatcher.connect(self.after_closed, signals.spider_closed)

    def after_closed(self):
        print "total_new_count={0}".format(self.total_new_count)

    def start_requests(self):
        return [Request(url=self.main_page_url, headers=self.settings['DEFAULT_REQUEST_HEADERS'],
                        callback=self.after_cookie)]

    def after_cookie(self, response):
        """
        访问单个股票评论列表的第一页,获取新增评论数量
        :param response:
        :return:
        """
        for stock in self.stocks:
            symbol = stock.get('symbol')

            first_url = self.comment_api.format(symbol=symbol, page=1) + '&hl=0'  # 避开重复url 导致handle()中第一页的请求不会被执行
            yield Request(first_url, headers=self.settings['DEFAULT_REQUEST_HEADERS'], callback=self.handle,
                          meta={'stock': stock})

    def handle(self, response):
        stock = response.meta.get('stock')
        symbol = stock.get('symbol')
        stored_count = 0 if stock.get('count') is None else int(stock.get('count'))  # 已存储数量

        content = json.loads(response.body)
        comments_count = int(content.get('count'))  # 总评论数,已被删除的评论也会纳入统计
        max_page = int(content.get('maxPage'))  # 可访问评论页数
        # comments_count = 0
        # if comments_count_str is not None:
        #     comments_count = int(comments_count_str)  # 最新的数量
        new_count = comments_count - stored_count

        # self.collection.update_one({'symbol': symbol},
        #                            {"$set": {'count': comments_count}})
        # logger.debug('symbol={0},new_count={1},total_count={2}'.format(symbol, 0, stored_count))

        # if new_count <= 0:
        if new_count <= 0 or comments_count < 1000:  # 没有新的评论 或者 总评论<1000
            logger.debug('symbol={0},new_count={1},stored_count={2}'.format(symbol, 0, stored_count))
            return
        else:
            # 有新的评论
            self.total_new_count += new_count
            logger.debug('symbol={0},new_count={1},stored_count={2}'.format(symbol, new_count, stored_count))
            actual_page_count = (new_count - 1) / self.count + 1

            _page_count = min(self.page_count, actual_page_count, max_page)
            for i in range(1, _page_count + 1):
                # logger.debug('iii={0}'.format(i))
                yield Request(self.comment_api.format(symbol=symbol,
                                                      page=i),
                              headers=self.settings['DEFAULT_REQUEST_HEADERS'])
            self.collection.update_one({'symbol': symbol},
                                       {"$set": {'count': comments_count}})

    def parse(self, response):
        # type:scrapy.http.Response
        content = json.loads(response.body)
        yield content
