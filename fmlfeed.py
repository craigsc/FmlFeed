#!/usr/bin/env python
import tornado.httpserver
import tornado.httpclient
import tornado.ioloop
import tornado.web
from tornado.options import define, options
import tornado.options
import os.path
import uimodules
import utils
import memcache

class BaseHandler(tornado.web.RequestHandler):
	@property
	def mc(self):
		return self.application.mc

class HomeHandler(BaseHandler):
	@tornado.web.asynchronous
	def get(self):
		json = self.mc.get("newest")
		if not json:
			http = tornado.httpclient.AsyncHTTPClient()
			http.fetch("https://graph.facebook.com/search?q=fml&type=post&limit=50",
				callback=self.on_response)
		else:
			self.render("index.html", posts=json["data"], 
				url=json["paging"]["next"], valid=utils.valid)

	def on_response(self, response):
		if (response.error): raise tornado.web.HTTPError(500)
		json = tornado.escape.json_decode(response.body)
		self.mc.set("newest", json)
		self.render("index.html", posts=json["data"], url=json["paging"]["next"],
			valid=utils.valid)

class FmlHandler(BaseHandler):
	@tornado.web.asynchronous
	def get(self, fml_id):
		fmlId = utils.urlToId(fml_id)
		json = self.mc.get(fmlId)
		if not json:
			http = tornado.httpclient.AsyncHTTPClient()
			http.fetch("https://graph.facebook.com/" + fmlId,
				callback=self.on_response)
		else:
			self.render("fml.html", post=json, idTo36=utils.idToUrl)
		
	def on_response(self, response):
		if (response.error): raise tornado.web.HTTPError(500)
		json = tornado.escape.json_decode(response.body)
		self.mc.set(str(json["id"]), json)
		self.render("fml.html", post=json, idTo36=utils.idToUrl)
		
class AboutHandler(BaseHandler):
	def get(self):
		self.render("about.html")

class TeamHandler(BaseHandler):
	def get(self):
		self.render("team.html")	

define("port", default=8888, type=int, help="port to listen on")

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", HomeHandler),
			(r"/newest", HomeHandler),
			(r"/about", AboutHandler),
			(r"/team", TeamHandler),
			(r"/([a-y0-9]+z[a-y0-9]+)", FmlHandler),
		]
		settings = {
			"static_path": os.path.join(os.path.dirname(__file__), "static"),
			"template_path": os.path.join(os.path.dirname(__file__), "templates"),
			"ui_modules": uimodules,
			"debug": False,
		}
		tornado.web.Application.__init__(self, handlers, **settings)
		#global memcache instance
		self.mc = memcache.Client(['127.0.0.1:11211'], debug=0)

if __name__ == "__main__":
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
