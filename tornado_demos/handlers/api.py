from bson.json_util import dumps
from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    @property
    def db(self):
        return self.application.db

    def write_json(self, data, status_code=200, msg='success'):
        self.finish(dumps({
            'code': status_code,
            'msg': msg,
            'data': data
        }
        ))


import pymongo

import tornado


class HomeHandler(BaseHandler):
    def get(self):
        post = self.db.test
        papers = post.find().sort('citations', pymongo.DESCENDING).limit(10)

        if not papers:
            self.redirect("/compose")
            return
        # self.render("home.html", papers=papers)
        self.render("home.html", papers=papers)


class TopHandler(BaseHandler):
    def get(self):
        post = self.db.test
        papers = list(post.find().sort('citations', pymongo.DESCENDING).limit(10))

        if not papers:
            self.redirect("/compose")
            return
        # self.write_json(data=papers)
        self.finish(dumps(papers))
