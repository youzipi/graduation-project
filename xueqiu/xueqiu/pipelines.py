# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import pymongo
from pymongo.errors import DuplicateKeyError


class CommentPipeline(object):
    settings = None
    collection = None

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        ext.settings = crawler.settings

        host = ext.settings['MONGO_HOST']
        port = ext.settings['MONGO_PORT']
        client = pymongo.MongoClient(host=host, port=port)

        db_name = ext.settings['MONGO_DBNAME']
        db = client[db_name]
        ext.collection = db['comment']

        return ext

    def process_item(self, item, spider):
        time_fields = ['created_at', 'edited_at']

        def str2time(comment):
            """
            js时间戳 转换为 date对象(同时也是MongoDB date对象)
            :param comment:
            :return:
            """
            # fromtimestamp
            # utcfromtimestamp 格林威治时间
            for field in time_fields:
                if comment.get(field) is not None:
                    comment[field] = datetime.datetime.fromtimestamp(float(comment[field]) / 1000)

            # comment['created_at'] = datetime.datetime.fromtimestamp(float(comment['created_at']) / 1000)
            # if comment.get('edited_at') is None:
            #     comment['edited_at'] = comment['created_at']
            return comment

        comments = item.get('list')
        symbol = item.get('symbol')
        for comment in comments:
            comment = str2time(comment)
            comment['symbol'] = symbol
            # todo 精简数据结构
            try:
                self.collection.insert_one(comment)
            except DuplicateKeyError:   # 该评论已存在
                pass

# todo comment 加一个pipeline 通过时间戳 或者 `id` 过滤 已存在的comment


class StockPipeline(object):
    settings = None
    collection = None

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        ext.settings = crawler.settings

        host = ext.settings['MONGO_HOST']
        port = ext.settings['MONGO_PORT']
        client = pymongo.MongoClient(host=host, port=port)

        db_name = ext.settings['MONGO_DBNAME']

        db = client[db_name]
        ext.collection = db['stocks']

        return ext

    def process_item(self, item, spider):
        stocks = item.get('stocks')
        for stock in stocks:
            self.collection.insert_one(stock)
