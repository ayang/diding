import tornado.web
from models.topic import UserManager
from handlers.base import BaseHandler
from form import InputField


class SignupHandler(BaseHandler):
    def prepare(self):
        self.form = {
            "email": InputField("email", "text"),
            "password": InputField("password", "password"),
            "password2": InputField("password2", "password"),
        }

    def get(self):
        self.render("accounts/signup.html")

    def post(self):
        email = self.get_argument('email', "")
        password = self.get_argument('password', "")
        password2 = self.get_argument('password2', "")
        if password != password2:
            self.form["password2"].error = True
        self.form["email"].value = email
        self.render("accounts/signup.html")
