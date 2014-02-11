#!/usr/bin/env python
## -*- coding: utf-8 -*-
import os
import tornado.ioloop
import tornado.web
import serial
import time
import threading

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        #self.set_cookie("cookie","cookieval")
        self.render(
            "home.html",
            title="PiServer",
            humidity=fresh_humidity
        )

def read_humidity():
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600)
        sensor = ser.readline()
    except:
        sensor = "not connected"
    return sensor

fresh_humidity = []

def keep_reading():
    while len(fresh_humidity) < 5:
        fresh_humidity.append(read_humidity())
        #fresh_humidity.pop(0)
        time.sleep(2)
        print(fresh_humidity)

bg = threading.Thread(group=None, target=keep_reading())
bg.run()

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