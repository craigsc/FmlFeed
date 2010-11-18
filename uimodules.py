import tornado.web
import utils

class Fml(tornado.web.UIModule):
	def render(self, post, homepage=True):
		return self.render_string("module-fml.html", post=post, idTo36=utils.idTo36, homepage=homepage)