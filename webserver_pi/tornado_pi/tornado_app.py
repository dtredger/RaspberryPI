import tornado.web
import tornado.websocket
import tornado.ioloop

import os
import glob
import datetime
import sqlite3

HUMIDITY_LOG_LOCATION = '/500gb_hd/humidity_logs'
LOG_DATABASE_NAME = os.environ.get("LOG_DATABASE_NAME","/500gb_hd/temperature_humidity.db")
LOG_TABLE_NAME = 'temp_humidity'

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		# self.set_header('Access-Control-Allow-Origin', '*')
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
			title="Cuddlefish PiServer | Live Temp + Humidity",
			data_points=len(graph_data),
			graph_data=tornado.escape.json_encode(graph_data)
		)


class ApiHandler(tornado.web.RequestHandler):
	def get(self):
		self.set_header("Access-Control-Allow-Origin", "http://localhost:8080")
		self.set_header('Access-Control-Allow-Credentials', 'true')
		# sensor_data = get_humidity(HUMIDITY_LOG_LOCATION)
		# response = {'time': datetime.datetime.fromtimestamp(float(sensor_data[0])).strftime('%Y-%m-%d %H:%M:%S') + " UTC",
		# 			'data': {'temp': sensor_data[1].strip(),
		# 					'humidity': sensor_data[2].strip(),
		# 					'timestamp': sensor_data[0]
		# 					}
		# 			}
		response = {
			"name": "pretty-hrtime",
			"description": "process.hrtime() to words",
			"version": "0.2.2",
			"homepage": "https://github.com/robrich/pretty-hrtime",
			"repository": {
			"type": "git",
			"url": "git://github.com/robrich/pretty-hrtime.git"
			},
			"author": {
			"name": "Rob Richardson",
			"url": "http://robrich.org/"
			},
			"main": "./index.js",
			"keywords": [
			"hrtime",
			"benchmark"
			],
			"devDependencies": {
			"mocha": "^1.21.4",
			"should": "^4.0.4"
			},
			"scripts": {
			"test": "mocha"
			},
			"engines": {
			"node": ">= 0.8"
			},
			"licenses": [
			{
			  "type": "MIT",
			  "url": "http://github.com/robrich/orchestrator/raw/master/LICENSE"
			}
			],
			"readme": "[![Build Status](https://secure.travis-ci.org/robrich/pretty-hrtime.png?branch=master)](https://travis-ci.org/robrich/pretty-hrtime)\r\n[![Dependency Status](https://david-dm.org/robrich/pretty-hrtime.png)](https://david-dm.org/robrich/pretty-hrtime)\r\n\r\npretty-hrtime\r\n============\r\n\r\n[process.hrtime()](http://nodejs.org/api/process.html#process_process_hrtime) to words\r\n\r\nUsage\r\n-----\r\n\r\n```javascript\r\nvar prettyHrtime = require('pretty-hrtime');\r\n\r\nvar start = process.hrtime();\r\n// do stuff\r\nvar end = process.hrtime(start);\r\n\r\nvar words = prettyHrtime(end);\r\nconsole.log(words); // '1.2 ms'\r\n\r\nwords = prettyHrtime(end, {verbose:true});\r\nconsole.log(words); // '1 millisecond 209 microseconds'\r\n\r\nwords = prettyHrtime(end, {precise:true});\r\nconsole.log(words); // '1.20958 ms'\r\n```\r\n\r\nNote: process.hrtime() has been available since 0.7.6.\r\nSee [http://nodejs.org/changelog.html](http://nodejs.org/changelog.html)\r\nand [https://github.com/joyent/node/commit/f06abd](https://github.com/joyent/node/commit/f06abd).\r\n\r\nLICENSE\r\n-------\r\n\r\n(MIT License)\r\n\r\nCopyright (c) 2013 [Richardson & Sons, LLC](http://richardsonandsons.com/)\r\n\r\nPermission is hereby granted, free of charge, to any person obtaining\r\na copy of this software and associated documentation files (the\r\n\"Software\"), to deal in the Software without restriction, including\r\nwithout limitation the rights to use, copy, modify, merge, publish,\r\ndistribute, sublicense, and/or sell copies of the Software, and to\r\npermit persons to whom the Software is furnished to do so, subject to\r\nthe following conditions:\r\n\r\nThe above copyright notice and this permission notice shall be\r\nincluded in all copies or substantial portions of the Software.\r\n\r\nTHE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND,\r\nEXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF\r\nMERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND\r\nNONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE\r\nLIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION\r\nOF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION\r\nWITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\r\n",
			"readmeFilename": "README.md",
			"bugs": {
			"url": "https://github.com/robrich/pretty-hrtime/issues"
			},
			"_id": "pretty-hrtime@0.2.2",
			"dist": {
			"shasum": "8921ab783c2427820b4185d349845831fa3f1937"
			},
			"_from": "pretty-hrtime@^0.2.0",
			"_resolved": "https://registry.npmjs.org/pretty-hrtime/-/pretty-hrtime-0.2.2.tgz"
			}
		self.write(response)

class v2ApiHandler(tornado.web.RequestHandler):
	def get(self):
		self.set_header('Access-Control-Allow-Origin', '*')
		self.set_header('Access-Control-Allow-Credentials', 'true')
		data = read_database()
		self.write(str(data))

# TODO - github is capable of sending JSON on certain events
# class WebhooksHandler(tornado.web.RequestHandler):
#     def get(self):

# class GameHandler(tornado.web.RequestHandler):
# 	def get(self):
# 		if not self.get_cookie("game"):
# 			self.set_cookie('game', 'playa', 
# 							domain=None,
# 							expires=datetime.datetime.utcnow() + datetime.timedelta(days=365)
# 							)
# 		self.render('bear.html')


# class WebSocketHandler(tornado.websocket.RequestHandler):

# 	def open(self):
# 		print 'connected'
# 		self.write_message('you connected')

# 	def on_message(self, message):
# 		self.write_message(message)
		
# 	def on_close(self):
# 		print 'conn closed'

class TimelapseHandler(tornado.web.RequestHandler):
	def get(self):
		folder="/Users/dylantredger/rpi_photes"
		image_uri= folder + "/" + get_newest_picture(folder)
		self.render("picture.html",
			image_uri=image_uri,
			image_url="file://{0}".format(image_uri),
			title="Cuddlefish PiServer | Timelapse Photos"
			)

class FileHandler(tornado.web.StaticFileHandler):
    def initialize(self, path):
        self.dirname, self.filename = os.path.split(path)
        super(FileHandler, self).initialize(self.dirname)

    def get(self, path=None, include_body=True):
        # Ignore 'path'.
        super(FileHandler, self).get(self.filename, include_body)



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
	cursor.execute("SELECT * FROM {0} ORDER BY timestamp desc limit {1}".format(LOG_TABLE_NAME, row_count))
	rows=cursor.fetchall()
	conn.close()
	results = [list(row) for row in rows]
	for row in results:
		row[0] = str(row[0])
	return rows

def get_newest_picture(folder):
	original_path = os.getcwd()
	os.chdir(folder)
	newest = max(glob.iglob('*.*'), key=os.path.getctime)
	os.chdir(original_path)
	return newest


handlers = [
	(r"/", MainHandler),
	(r"/datamountain", DataMountainHandler),
	(r"/graph(.*)", GraphHandler),
	(r"/api", ApiHandler),
	(r"/v2/api", v2ApiHandler),
	(r"/timelapse", TimelapseHandler),
	(r"/file", FileHandler, {'path': '/Users/dylantredger'}),
	(r"/pic/(.*)", tornado.web.StaticFileHandler, {'path':'/Users/dylantredger/rpi_photes/'})
	# (r"/bear", GameHandler)
	# (r"/webhooks", WebhooksHandler),
	# (r"/websocket", WebSocketHandler),
]

settings = dict(
	template_path=os.path.join(os.path.dirname(__file__), "templates"),
	static_path=os.path.join(os.path.dirname(__file__), "static")
	# login_url="/bear", #tornado @authenticated redirects to here
)

application = tornado.web.Application(handlers, **settings)


if __name__ == '__main__':
	port = os.environ.get('SERVER_PORT', 8000)
	print "server starting on port %s" % port
	application.listen(port)
	tornado.ioloop.IOLoop.instance().start()
