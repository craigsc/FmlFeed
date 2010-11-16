#!/usr/bin/env python
import tornado.httpserver
import tornado.httpclient
import tornado.ioloop
import tornado.web
import tornado.options
import os.path

class MainHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		http = tornado.httpclient.AsyncHTTPClient()
		http.fetch("https://graph.facebook.com/search?q=fml&type=post",
			callback=self.on_response)
	
	def on_response(self, response):
		if (response.error): raise tornado.web.HTTPError(500)
		json = tornado.escape.json_decode(response.body)
		self.render("index.html", posts=json["data"], url=json["paging"]["next"])

settings = {
	"static_path": os.path.join(os.path.dirname(__file__), "static"),
	"template_path": os.path.join(os.path.dirname(__file__), "templates")
}

application = tornado.web.Application([
	(r"/", MainHandler),
], **settings)

if __name__ == "__main__":
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(8888)
	tornado.ioloop.IOLoop.instance().start()