from bson.json_util import dumps

import pymongo

from .base import ApiHandler


class TopHandler(ApiHandler):
    def get(self):
        post = self.db.test
        papers = list(post.find().sort('citations', pymongo.DESCENDING).limit(10))

        if not papers:
            self.redirect("/compose")
            return
        # self.write_json(data=papers)
        self.finish(dumps(papers))


class PaperHandler(ApiHandler):
    def get(self, paper_id):
        post = self.db.test
        paper = post.find({'wos_no': paper_id})
        if not paper:
            paper = {
                'msg': 'no paper match the id {0}'.format(paper_id),
                'data': None
            }
        self.finish(dumps(paper))
