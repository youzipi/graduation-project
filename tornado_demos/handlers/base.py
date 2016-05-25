from tornado.web import RequestHandler
from bson.json_util import dumps

from .mixins import FlashMessageMixin


class BaseHandler(RequestHandler):
    @property
    def db(self):
        return self.application.db


class ApiHandler(BaseHandler, FlashMessageMixin):
    def write_json(self, data, status_code=200, msg='success'):
        self.finish(dumps({
            'code': status_code,
            'msg': msg,
            'data': data
        }
        ))


class ViewHandler(BaseHandler):
    view = ''

    def get(self, *args):
        self.render(self.view + ".html")


class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
