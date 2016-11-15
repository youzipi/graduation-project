# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

from scrapy import Request
from scrapy.exceptions import DropItem

from .settings import file_handler
from items import EsiItem

import pymongo

logger = logging.getLogger("pipiline")
logger.addHandler(file_handler)


class EsiPipeline(object):
    settings = None
    collection = None

    # def __init__(self):
    #     pass

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        ext.settings = crawler.settings

        host = ext.settings['MONGO_HOST']
        port = ext.settings['MONGO_PORT']
        client = pymongo.MongoClient(host=host, port=port)

        db_name = ext.settings['MONGO_DBNAME']
        doc_name = ext.settings['MONGO_DOCNAME']
        db = client[db_name]
        ext.collection = db[doc_name]

        return ext

    # def __init__(self):
    #     host = settings['MONGO_HOST']
    #     port = settings['MONGO_PORT']
    #     client = pymongo.MongoClient(host=host, port=port)
    #
    #     db_name = 'esi'
    #     doc_name = 'test'
    #     db = client[db_name]
    #     self.collection = db[doc_name]

    def process_item(self, item, spider):
        logger.debug(("item=", item))
        esi_info = dict(item)

        if esi_info.get('title') is None:
            self.collection.update_one(
                {'wos_no': esi_info.get('wos_no')},
                {"$set":
                     {'citations': item.get('citations')}
                 }
            )
        else:
            self.collection.insert(esi_info)


class YearCitationsPipeline(object):
    settings = None
    collection = None

    # def __init__(self):
    #     host = settings['MONGO_HOST']
    #     port = settings['MONGO_PORT']
    #     client = pymongo.MongoClient(host=host, port=port)
    #
    #     db_name = 'esi'
    #     doc_name = 'test'
    #     db = client[db_name]
    #     self.collection = db[doc_name]

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        ext.settings = crawler.settings

        host = ext.settings['MONGO_HOST']
        port = ext.settings['MONGO_PORT']
        client = pymongo.MongoClient(host=host, port=port)

        db_name = ext.settings['MONGO_DBNAME']
        doc_name = ext.settings['MONGO_DOCNAME']
        db = client[db_name]
        ext.collection = db[doc_name]

        return ext

    def process_item(self, item, spider):
        """

        :param item:
        :param spider:
        :return:
        """
        if item.get('citations', 0) != None:
            return item
        logger.debug(("item=", item))
        esi_info = dict(item)
        # self.post.insert(esi_info)
        if self.collection.find({'wos_no': item.get('wos_no')}).clean() == 1:
            # if exist,update citations
            self.collection.update_one({'wos_no': esi_info.get('wos_no')},
                                       {"$set": {'citations': item.get('citations')}})

            # elif item.get('title') is None:
            # pass
            # if has no wos_info, send a request to wos
            # yield Request(item['wos_link'], callback=spider.parse_wos_page, meta={'item': item})
            # request = Request(item['wos_link'], callback=spider.parse_wos_page, meta={'item': item})
            # return request
        else:
            self.collection.insert_one(esi_info)
            # self.post.update_one({'wos_no': esi_info.get('wos_no')}, {"$set": esi_info}, upsert=True)
            # return item


class DuplicatesPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item.get('wos_no') in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item.get('wos_no'))
            return item
