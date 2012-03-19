# -*- coding: utf-8 -*-
import json
import tornado.web
from models.topic import UserManager

import logging
logger = logging.getLogger('boilerplate.' + __name__)


class BaseHandler(tornado.web.RequestHandler):
    """A class to collect common handler methods - all other handlers should
    subclass this one.
    """

    def load_json(self):
        """Load JSON from the request body and store them in
        self.request.arguments, like Tornado does by default for POSTed form
        parameters.

        If JSON cannot be decoded, raises an HTTPError with status 400.
        """
        try:
            self.request.arguments = json.loads(self.request.body)
        except ValueError:
            msg = "Could not decode JSON: %s" % self.request.body
            logger.debug(msg)
            raise tornado.web.HTTPError(400, msg)

    def get_json_argument(self, name, default=None):
        """Find and return the argument with key 'name' from JSON request data.
        Similar to Tornado's get_argument() method.
        """
        if default is None:
            default = self._ARG_DEFAULT
        if not self.request.arguments:
            self.load_json()
        if name not in self.request.arguments:
            if default is self._ARG_DEFAULT:
                msg = "Missing argument '%s'" % name
                logger.debug(msg)
                raise tornado.web.HTTPError(400, msg)
            logger.debug("Returning default argument %s, as we couldn't find "
                    "'%s' in %s" % (default, name, self.request.arguments))
            return default
        arg = self.request.arguments[name]
        logger.debug("Found '%s': %s in JSON arguments" % (name, arg))
        return arg

    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id:
            return None
        return UserManager().get_by_uid(int(user_id))

    @property
    def db(self):
        return self.application.db

    def markup(self, content):
        from markdown import markdown
        return markdown(content, output_format="html5", safe_mode="escape")

    def pretty_date(self, time=False):
        """
        Get a datetime object or a int() Epoch timestamp and return a
        pretty string like 'an hour ago', 'Yesterday', '3 months ago',
        'just now', etc
        """
        from datetime import datetime
        now = datetime.utcnow()
        if type(time) is int:
            diff = now - datetime.fromtimestamp(time)
        elif isinstance(time, datetime):
            diff = now - time
        elif not time:
            diff = now - now
        second_diff = diff.seconds
        day_diff = diff.days

        if day_diff < 0:
            return ''

        if day_diff == 0:
            if second_diff < 10:
                return u"刚才"
            if second_diff < 60:
                return str(second_diff) + u" 秒钟前"
            if second_diff < 120:
                return  u"1 分钟前"
            if second_diff < 3600:
                return str(second_diff / 60) + u" 分钟前"
            if second_diff < 7200:
                return u"1 小时前"
            if second_diff < 86400:
                return str(second_diff / 3600) + u" 小时前"
        if day_diff == 1:
            return u"昨天"
        if day_diff < 7:
            return str(day_diff) + u" 天前"
        if day_diff < 31:
            return str(day_diff / 7) + u" 周前"
        if day_diff < 365:
            return str(day_diff / 30) + u" 月前"
        return str(day_diff / 365) + u" 年前"

    def gravatar(self, email, size=48):
        import hashlib
        digest = hashlib.md5(email.strip().lower()).hexdigest()
        p = "http://www.gravatar.com/avatar/%s?s=%d&d=identicon"
        return p % (digest, int(size))

    def render_string(self, template_name, **kwargs):
        args = dict(
            markup=self.markup,
            pretty_date=self.pretty_date,
            gravatar=self.gravatar,
        )
        args.update(kwargs)
        return super(BaseHandler, self).render_string(template_name, **args)
