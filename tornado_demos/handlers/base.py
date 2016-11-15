from tornado.web import RequestHandler
from bson.json_util import dumps

from .mixins import FlashMessageMixin


class BaseHandler(RequestHandler):
    @property
    def db(self):
        return self.application.db


class ApiHandler(BaseHandler, FlashMessageMixin):
    data = {}
    db_name = ''
    _post = None

    @property
    def post(self):
        if self._post is None:
            self._post = self.db[self.db_name]
        return self._post

    def write_json(self, data, status=1, msg='success'):
        self.finish(dumps({
            'status': status,
            'msg': msg,
            'data': data
        },
        ))


class ViewHandler(BaseHandler):
    view = ''

    def get(self, *args):
        self.render(self.view + ".html")


class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
