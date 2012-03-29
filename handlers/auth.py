# -*- coding: utf-8 -*-
import tornado.web
import tornado.auth
from tornado_third.douban import DoubanMixin
from models.topic import UserManager
from handlers.base import BaseHandler
from form import InputField


class GoogleAuthHandler(BaseHandler, tornado.auth.GoogleMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Google auth failed")
        user_manager = UserManager()
        author = user_manager.get_by_google_account(user["email"])
        if author is None:
            author = user_manager.create(user["email"], user["name"], {"google": user})
        else:
            user_manager.refresh(author["uid"])
        authorid = str(author["uid"])
        self.set_secure_cookie("user", authorid)
        self.redirect(self.get_argument("next", "/"))


class DoubanAuthHandler(BaseHandler, DoubanMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("oauth_token", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authorize_redirect()

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Douban auth failed")
        # do something else
        self.write(user)
        self.finish()


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))


class AuthHandler(BaseHandler):
    def prepare(self):
        self.form = {
            "email": InputField("email", "text", "电子邮件"),
            "password": InputField("password", "password", "密码"),
        }

    def get(self):
        self.render("login.html", form=self.form, next=self.get_argument("next", "/"))

    def post(self):
        email = self.get_argument("email", "")
        password = self.get_argument("password", "")
        user_manager = UserManager()
        user = user_manager.get_by_local_account(email)
        if user is not None:
            if user_manager.authenticate(user, password):
                userid = str(user["uid"])
                self.set_secure_cookie("user", userid)
                self.redirect(self.get_argument("next", "/"))
        return self.get()
