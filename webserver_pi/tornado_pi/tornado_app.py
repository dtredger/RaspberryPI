import os
import glob
import tornado.ioloop
import tornado.web
import datetime
import sqlite3
import json

HUMIDITY_LOG_LOCATION = '/500gb_hd/humidity_logs'
LOG_DATABASE_NAME = os.environ.get("LOG_DATABASE_NAME","/500gb_hd/temperature_humidity.db")
LOG_TABLE_NAME = 'temp_humidity'

class MainHandler(tornado.web.RequestHandler):
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

class GraphHandler(tornado.web.RequestHandler):
	def get(self, path='/100'):
		graph_data=read_database(path[1:])
		self.render(
			"graph.html",
			title="Cuddlefish PiServer",
			data_points=len(graph_data),
			graph_data=tornado.escape.json_encode(graph_data)
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

class v2ApiHandler(tornado.web.RequestHandler):
	def get(self):
		data = read_database()
		self.write(str(data))

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


def get_humidity(folder):
	os.chdir(folder)
	newest = max(glob.iglob('*.*'), key=os.path.getctime)
	file = open(newest, 'r')
	lines = file.readlines()
	file.close()
	# returns a line of csv like ['1395513142', ' T 19.2', ' H 31.1\n']	
	return lines[-1].split(',')

def read_database(row_count='100'):
	conn=sqlite3.connect(LOG_DATABASE_NAME)
	cursor=conn.cursor()
	cursor.execute("SELECT * FROM {0} ORDER BY datetime order by timestamp desc limit {1}".format(LOG_TABLE_NAME, row_count))
	rows=cursor.fetchall()
	conn.close()
	results = [list(row) for row in rows]
	for row in results:
		row[0] = str(row[0])
	return rows

handlers = [
	(r"/", MainHandler),
	(r"/datamountain", DataMountainHandler),
	(r"/graph(.*)", GraphHandler),
	(r"/api", ApiHandler),
	(r"/v2/api", v2ApiHandler),
	(r"/bear", GameHandler)
	# (r"/webhooks", WebhooksHandler),
]

settings = dict(
	template_path=os.path.join(os.path.dirname(__file__), "templates"),
	static_path=os.path.join(os.path.dirname(__file__), "static"),
)

application = tornado.web.Application(handlers, **settings)


if __name__ == '__main__':
	port = os.environ.get('SERVER_PORT', 8080)
	print "server starting on port %s" % port
	application.listen(port)
	tornado.ioloop.IOLoop.instance().start()
