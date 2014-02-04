#!/usr/bin/env python
## -*- coding: utf-8 -*-
import os
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        page_arry = ["", ""]
        #self.set_cookie("cookie","cookieval")
        self.render("home.html",title="catfishes",storm_chasers=page_arry)

handlers = [
    (r"/", MainHandler),
]

settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),

)
application = tornado.web.Application(
    handlers, **settings)


if __name__ == '__main__':
    application.listen(os.environ.get('SERVER_PORT', 8080))
    tornado.ioloop.IOLoop.instance().start()