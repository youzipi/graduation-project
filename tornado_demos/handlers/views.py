import pymongo
from tornado.web import HTTPError
from bson.json_util import dumps

from .base import ViewHandler, AttributeDict


class HomeHandler(ViewHandler):
    def get(self):
        post = self.db.test
        papers = post.find().sort('citations', pymongo.DESCENDING).limit(10)

        if not papers:
            self.redirect("/compose")
            return
        self.render("home.html", papers=papers)


class TopHandler(ViewHandler):
    view = 'top'
    #
    # def get(self):
    #     self.render(self.view + '.vue')


class PaperHandler(ViewHandler):
    view = 'paper'

    def get(self, paper_id):
        post = self.db.test
        paper = post.find({'wos_no': paper_id})[0]
        paper = AttributeDict(paper)

        if not paper:
            # paper = {
            #     'msg': 'no paper match the id {0}'.format(paper_id),
            #     'data': None
            # }
            raise HTTPError(404)

        paper.year_citations = {int(k): v for k, v in paper.year_citations.iteritems()}

        self.render(self.view + '.html', paper=AttributeDict(paper))


class CrawlHandler(ViewHandler):
    view = 'crawl'


class CrawlStatusHandler(ViewHandler):
    view = 'crawl_status'


class AreaLinkHandler(ViewHandler):
    view = 'research_area_link'
