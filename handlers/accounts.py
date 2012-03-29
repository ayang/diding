# -*- coding: utf-8 -*-
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
        name = self.get_argument('name', "")
        email = self.get_argument('email', "")
        password = self.get_argument('password', "")
        password2 = self.get_argument('password2', "")
        error = []
        user_manager = UserManager()
        if password != password2:
            self.form["password2"].error = True
            error.append("密码不匹配")
        if len(password) < 8:
            self.form["password"].error = True
            error.append("密码长度不够")
        if len(name) < 3:
            self.form["name"].error = True
            error.append("昵称太短")
        if len(email) < 6 or "@" not in email:
            self.form["email"].error = True
            error.append("Email格式不正确")
        elif user_manager.get_by_local_account(email):
            self.form["email"].error = True
            error.append(u"%s 电子邮件已经有人注册过了" % email)
        if error:
            self.form["name"].value = name
            self.form["email"].value = email
            self.render("accounts/signup.html", form=self.form, errors=error)
        else:
            account = {
                "name": name,
                "email": email,
                "password": user_manager.hash_password(password),
            }
            user = user_manager.create(email, name, {"local": account})
            userid = str(user["uid"])
            self.set_secure_cookie("user", userid)
            self.redirect(self.get_argument("next", "/"))
