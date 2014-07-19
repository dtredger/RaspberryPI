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
		if path[1:].isdigit():
			path = path[1:]
		else:
			path = '100'
		graph_data=read_database(path)
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
	# conn=sqlite3.connect(LOG_DATABASE_NAME)
	# cursor=conn.cursor()
	# cursor.execute("SELECT * FROM {0} ORDER BY timestamp desc limit {1}".format(LOG_TABLE_NAME, row_count))
	# rows=cursor.fetchall()
	# conn.close()
	rows=[(u'2014-07-19 20:22:16', 23, 72.1), (u'2014-07-19 20:22:12', 23, 72), (u'2014-07-19 20:22:09', 23, 71.8), (u'2014-07-19 20:21:54', 23, 71.8), (u'2014-07-19 20:21:47', 23, 72.3), (u'2014-07-19 20:21:44', 22.9, 72.3), (u'2014-07-19 20:21:40', 23, 72.3), (u'2014-07-19 20:21:37', 23, 72.3), (u'2014-07-19 20:21:33', 23, 72.4), (u'2014-07-19 20:21:26', 23, 72.3), (u'2014-07-19 20:21:22', 23, 72.4), (u'2014-07-19 20:21:19', 23, 72.4), (u'2014-07-19 20:21:15', 23, 72.4), (u'2014-07-19 20:21:08', 23, 72.3), (u'2014-07-19 20:21:05', 23, 72.3), (u'2014-07-19 20:21:01', 23, 72.3), (u'2014-07-19 20:20:50', 23, 72), (u'2014-07-19 20:20:47', 23, 72), (u'2014-07-19 20:20:43', 23, 71.9), (u'2014-07-19 20:20:36', 23, 71.8), (u'2014-07-19 20:20:33', 23, 71.7), (u'2014-07-19 20:20:25', 23, 71.8), (u'2014-07-19 20:20:15', 23, 72.4), (u'2014-07-19 20:20:11', 23, 72.4), (u'2014-07-19 20:20:08', 23, 72.5), (u'2014-07-19 20:20:04', 23, 72.4), (u'2014-07-19 20:19:57', 23, 72.3), (u'2014-07-19 20:19:53', 23, 72.3), (u'2014-07-19 20:19:43', 23, 72.3), (u'2014-07-19 20:19:39', 23, 72.3), (u'2014-07-19 20:19:36', 23, 72.2), (u'2014-07-19 20:19:29', 23, 72), (u'2014-07-19 20:19:21', 23, 71.7), (u'2014-07-19 20:19:18', 23, 71.6), (u'2014-07-19 20:19:14', 23, 71.5), (u'2014-07-19 20:19:11', 23, 71.6), (u'2014-07-19 20:19:07', 23, 71.8), (u'2014-07-19 20:19:04', 23, 72), (u'2014-07-19 20:19:00', 23, 72.3), (u'2014-07-19 20:18:56', 23, 72.2), (u'2014-07-19 20:18:53', 23, 72.2), (u'2014-07-19 20:18:49', 23, 72), (u'2014-07-19 20:18:42', 23, 71.8), (u'2014-07-19 20:18:39', 23, 71.9), (u'2014-07-19 20:18:28', 23, 72), (u'2014-07-19 20:18:24', 23, 71.7), (u'2014-07-19 20:18:21', 23, 71.6), (u'2014-07-19 20:18:17', 23, 71.4), (u'2014-07-19 20:18:14', 23, 71.4), (u'2014-07-19 20:18:10', 23, 71.3), (u'2014-07-19 20:18:07', 23, 71.4), (u'2014-07-19 20:18:00', 23, 71.8), (u'2014-07-19 20:17:56', 23, 72), (u'2014-07-19 20:17:49', 23, 72.1), (u'2014-07-19 20:17:42', 23, 71.9), (u'2014-07-19 20:17:35', 23.1, 71.8), (u'2014-07-19 20:17:31', 23, 71.7), (u'2014-07-19 20:17:27', 23.1, 71.7), (u'2014-07-19 20:17:20', 23, 71.6), (u'2014-07-19 20:17:17', 23, 71.9), (u'2014-07-19 20:17:06', 23.1, 72.3), (u'2014-07-19 20:17:03', 23.1, 72.4)]
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
