from bson.json_util import dumps

import pymongo
from scrapy import cmdline
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from crawler.esi.spiders.EsiSpider import EsiSpider
from crawler.service import start
from .base import ApiHandler


class TopHandler(ApiHandler):
    page_size = 10

    def get(self, page_num):
        page_num = int(page_num) or 0
        post = self.db.test
        papers = list(post.find().sort('citations', pymongo.DESCENDING)
                      .skip(self.page_size * (page_num - 1))
                      .limit(self.page_size))

        if not papers:
            self.redirect("/compose")
            return
        # self.write_json(data=papers)
        self.finish(dumps(papers))


class PaperHandler(ApiHandler):
    def get(self, paper_id):
        post = self.db.test  # type:pymongo.cursor.Cursor
        paper = post.find({'wos_no': paper_id})
        if not paper:
            paper = {
                'msg': 'no paper match the id {0}'.format(paper_id),
                'data': None
            }
        self.finish(dumps(paper))


class CrawlStartHandler(ApiHandler):
    def get(self):
        start()
        self.finish("success")
