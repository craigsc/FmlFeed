#!/usr/bin/env python
import tornado.httpserver
import tornado.httpclient
import tornado.ioloop
import tornado.web
import tornado.options
import os.path
import uimodules
import utils

class HomeHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		http = tornado.httpclient.AsyncHTTPClient()
		http.fetch("https://graph.facebook.com/search?q=fml&type=post&limit=50",
			callback=self.on_response)
	
	def on_response(self, response):
		if (response.error): raise tornado.web.HTTPError(500)
		json = tornado.escape.json_decode(response.body)
		self.render("index.html", posts=json["data"], url=json["paging"]["next"])

class FmlHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self, fml_id):
		http = tornado.httpclient.AsyncHTTPClient()
		http.fetch("https://graph.facebook.com/" + utils.urlToId(fml_id),
			callback=self.on_response)
		
	def on_response(self, response):
		if (response.error): raise tornado.web.HTTPError(500)
		json = tornado.escape.json_decode(response.body)
		self.render("fml.html", post=json, idTo36=utils.idTo36)

settings = {
	"static_path": os.path.join(os.path.dirname(__file__), "static"),
	"template_path": os.path.join(os.path.dirname(__file__), "templates"),
	"ui_modules": uimodules,
}

application = tornado.web.Application([
	(r"/", HomeHandler),
	(r"/([a-y0-9]+z[a-y0-9]+)", FmlHandler),
], **settings)

if __name__ == "__main__":
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(8888)
	tornado.ioloop.IOLoop.instance().start()