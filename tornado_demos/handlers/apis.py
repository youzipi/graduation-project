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


class TopCountHandler(ApiHandler):
    def get(self):
        post = self.db.test
        count = post.find().count()
        self.finish(unicode(count))


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


class AreaLinkHandler(ApiHandler):
    db_name = 'area_rank'

    def get(self):
        self.data
        research_areas = ['no-data']
        def _area_project(n, i):
            """
            {_id:computer science,count:2222},
            => {
                id:i,
                value:computer science,
                count:2222
            }
            """
            research_areas.append(n['_id'])
            n['value'] = n['_id']
            n['id'] = i
            del n['_id']

            return n

        def _link_project(n, i):
            n['id'] = i
            n['source'] = research_areas.index(n['source'])
            n['target'] = research_areas.index(n['target'])
            del n['_id']

            return n

        area_rank = self.post.find().sort('count', pymongo.DESCENDING)
        ar_len = self.post.find().count()
        area_rank1 = map(_area_project, area_rank, range(1, ar_len + 1))

        links = self.db['area_relation'].find()
        links_len = self.db['area_relation'].find().count()
        links1 = map(_link_project, links, range(1, links_len + 1))

        self.data['nodes'] = area_rank1
        self.data['links'] = links1

        if not self.data:
            self.write_json(status=-1, msg='no data', data=self.data)
        # self.finish(dumps(self.data))
        self.write_json(data=self.data)
