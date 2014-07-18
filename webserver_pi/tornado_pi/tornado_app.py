import tornado.web
import tornado.websocket
import tornado.ioloop

import os
import glob
import datetime

HUMIDITY_LOG_LOCATION = '/500gb_hd/humidity_logs'

# cribbed auth methods #
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_cookie("greetings")
        if not user_json:
            return None
        return tornado.escape.json_decode(user_json)


def authenticated(func):
    def wrapped_get(self, fn=None):
    	# craps out: claims func should have 1 arg
        # if 'localhost' in self.request.host:
        #     return func(self, fn)
        # else:
        return tornado.web.authenticated(func)(self, fn)
    return wrapped_get



class MainHandler(tornado.web.RequestHandler):

	@authenticated
	def get(self):
		if not self.get_cookie("greetings"):
			self.set_cookie('greetings', 'human', 
							domain=None,
							expires=datetime.datetime.utcnow() + datetime.timedelta(days=365)
							)
		self.render(
			"home.html",
			title="Cuddlefish PiServer",
		)


class DataMountainHandler(tornado.web.RequestHandler):

	def get(self):
		sensor_data=get_humidity(HUMIDITY_LOG_LOCATION)
		self.render(
			"data.html",
			title="Cuddlefish PiServer",
			time=datetime.datetime.fromtimestamp(float(sensor_data[0])).strftime('%Y-%m-%d %H:%M:%S') + " UTC",
			temperature=sensor_data[1],
			humidity=sensor_data[2]
		)


class ApiHandler(tornado.web.RequestHandler):

	def get(self):
		sensor_data = get_humidity(HUMIDITY_LOG_LOCATION)
		response = {'time': datetime.datetime.fromtimestamp(float(sensor_data[0])).strftime('%Y-%m-%d %H:%M:%S') + " UTC",
					'data': {'temp': sensor_data[1].strip(),
							'humidity': sensor_data[2].strip(),
							'timestamp': sensor_data[0]
							}
					}
		self.write(response)


class v2_ApiHandler(tornado.web.RequestHandler):

	def get(self):
		data = {
			0: {
		        "age": 0, 
		        "id": "motorola-xoom-with-wi-fi",
		        "imageUrl": "img/phones/motorola-xoom-with-wi-fi.0.jpg",
		        "name": "Motorola XOOM\u2122 with Wi-Fi",
		        "snippet": "The Next,NextXOOM with Wi-Fi,the world's first tablet powered by Android 3.0 (Honeycomb)."
		    },
		    1: {
		        "age": 1,
		        "id": "motorola-xoom",
		        "imageUrl": "img/phones/motorola-xoom.0.jpg",
		        "name": "MOTOROLA XOOM\u2122",
		        "snippet": "Theience the future with MOTOROLA XOOM,the world's first tablet powered by Android 3.0 (Honeycomb)."
		    }
		}    
		self.write(data)


# TODO - github is capable of sending JSON on certain events
# class WebhooksHandler(tornado.web.RequestHandler):
#     def get(self):

class GameHandler(tornado.web.RequestHandler):

	def get(self):
		if not self.get_cookie("game"):
			self.set_cookie('game', 'playa', 
							domain=None,
							expires=datetime.datetime.utcnow() + datetime.timedelta(days=365)
							)
		self.render('bear.html')


class WebSocketHandler(tornado.websocket.WebSocketHandler):

	def open(self):
		print 'connected'
		self.write_message('you connected')

	def on_message(self, message):
		self.write_message(message)
		
	def on_close(self):
		print 'conn closed'



def get_humidity(folder):
	os.chdir(folder)
	newest = max(glob.iglob('*.*'), key=os.path.getctime)
	file = open(newest, 'r')
	lines = file.readlines()
	file.close()

	# returns a line of csv like ['1395513142', ' T 19.2', ' H 31.1\n']	
	return lines[-1].split(',')




handlers = [
	(r"/", MainHandler),
	(r"/datamountain", DataMountainHandler),
	(r"/api", ApiHandler),
	(r"/bear", GameHandler),
	# (r"/webhooks", WebhooksHandler),
	(r"/websocket", WebSocketHandler),
	(r"/v2/api", v2_ApiHandler),
]

settings = dict(
	template_path=os.path.join(os.path.dirname(__file__), "templates"),
	static_path=os.path.join(os.path.dirname(__file__), "static"),
	login_url="/bear", #tornado @authenticated redirects to here
)

application = tornado.web.Application(handlers, **settings)


if __name__ == '__main__':
	port = os.environ.get('SERVER_PORT', 8080)
	print "server starting on port %s" % port
	application.listen(port)
	tornado.ioloop.IOLoop.instance().start()
