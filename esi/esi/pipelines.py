# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

from scrapy.exceptions import DropItem

from items import EsiItem
from scrapy.conf import settings

# import pymongo

logger = logging.getLogger("pipiline")


class EsiPipeline(object):
    def __init__(self):
        host = settings['MONGO_HOST']
        port = settings['MONGO_PORT']
        # conn = pymongo.MongoClient(host=host, port=port)

        db_name = 'esi'
        doc_name = 'test'
        # db = conn[db_name]
        # self.post = db[doc_name]

    def process_item(self, item, spider):
        # logger.debug(("item=", item))
        esi_info = dict(item)
        # self.post.insert(esi_info)
        # self.post.update_one({'wos_no': esi_info['wos_no']}, {"$set": esi_info}, upsert=True)
        return item


class DuplicatesPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['wos_no'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['wos_no'])
            return item
