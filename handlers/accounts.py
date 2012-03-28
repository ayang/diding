# -*- coding: utf-8 -*-
import tornado.web
from models.topic import UserManager
from handlers.base import BaseHandler
from form import InputField


class SignupHandler(BaseHandler):
    def prepare(self):
        self.form = {
            "name": InputField("name", "text", "昵称", help="选一个合适的昵称，可以使用您的名字"),
            "email": InputField("email", "text", "电子邮件", help="请输入常用电子邮件，以便找回密码"),
            "password": InputField("password", "password", "密码", help="密码长一点才是王道，话说8位以下都Out了"),
            "password2": InputField("password2", "password", "密码(重复)", help="麻烦您再输一遍"),
        }

    def get(self):
        self.render("accounts/signup.html", form=self.form)

    def post(self):
        email = self.get_argument('email', "")
        password = self.get_argument('password', "")
        password2 = self.get_argument('password2', "")
        if password != password2:
            self.form["password2"].error = True
        self.form["email"].value = email
        self.render("accounts/signup.html", form=self.form)
