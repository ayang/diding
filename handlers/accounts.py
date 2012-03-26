import tornado.web
from models.topic import UserManager
from handlers.base import BaseHandler


class SignupHandler(BaseHandler):
	def get(self):
		self.render("accounts/signup.html")


	def post(self):
		pass
