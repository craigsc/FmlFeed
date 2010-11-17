import tornado.web

class Fml(tornado.web.UIModule):
	def render(self, post, homepage=True):
		return self.render_string("module-fml.html", post=post, homepage=homepage)