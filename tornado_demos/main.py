#!/usr/bin/env python

import concurrent.futures
import os.path

import pymongo
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

from handlers import apis, views

define("port", default=8889, help="run on the given port", type=int)
define("mongo_host", default="127.0.0.1", help="database host")
define("mongo_port", default=27017, help="database port")
define("db_name", default="esi", help="database name")
define("doc_name", default="test", help="database name")
define("mongo_user", default="blog", help="database user")
define("mongo_password", default="blog", help="database password")

# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", views.HomeHandler),
            (r"/top", views.TopHandler),
            (r"/p/(?P<paper_id>.*)", views.PaperHandler),
            (r"/v1/top", apis.TopHandler),
            (r"/v1/p/(?P<paper_id>.*)", apis.PaperHandler),
            # (r"/entry/([^/]+)", api.EntryHandler),

        ]
        settings = dict(
            blog_title=u"ESI Papers",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            debug=True,
            autosecape=None,
        )
        super(Application, self).__init__(handlers, **settings)

        # Have one global connection to the blog DB across all handlers
        client = pymongo.MongoClient(host=options.mongo_host, port=options.mongo_port)
        db = client[options.db_name]
        self.db = db


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
