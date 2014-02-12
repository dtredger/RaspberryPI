#!/usr/bin/env python
## -*- coding: utf-8 -*-
import os
import tornado.ioloop
import tornado.web
import datetime


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        if not self.get_cookie("greetings"):
            self.set_cookie('greetings',
                'human', domain=None,
                expires=datetime.datetime.utcnow() + datetime.timedelta(days=365)
            )
        self.render(
            "home.html",
            title="PiServer",
        )


class DataMountainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "data.html",
            title="PiServer",
            humidity=get_humidity()
        )


def get_humidity(filename):
    file = open(filename, 'r')
    lines = file.readlines()
    file.close()
    return lines[-1]




handlers = [
    (r"/", MainHandler),
    (r"/datamountain", DataMountainHandler),
]

settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
)


application = tornado.web.Application(
    handlers, **settings)


if __name__ == '__main__':
    port = os.environ.get('SERVER_PORT', 8080)
    print "server starting on port %s" % port
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()