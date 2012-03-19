import tornado.web
from tornado.util import ObjectDict
from handlers.base import BaseHandler
from models.topic import TopicManager, TagManager, UserManager

import logging
logger = logging.getLogger('boilerplate.' + __name__)


class HomeHandler(BaseHandler):
    def get(self):
        topics = TopicManager().all(sort_by=[("update_time", 1)])
        self.render("home.html", topics=topics)


class AboutHandler(BaseHandler):
    def get(self):
        self.render("about.html")


class TopicsHandler(BaseHandler):
    def get(self):
        topics = TopicManager().all()
        self.render("topics.html", topics=topics)


class TaggedTopicsHandler(BaseHandler):
    def get(self, tagname):
        tag = TagManager().get_by_name(tagname)
        if tag is None:
            raise tornado.web.HTTPError(404)
        topics = TopicManager().tagged(tag)
        self.render("taggedtopics.html", tag=tag, topics=topics)


class TopicHandler(BaseHandler):
    def get(self, id):
        topic = TopicManager().get(id)
        if topic is None:
            raise tornado.web.HTTPError(404)
        self.render("topic.html", topic=topic)


class NewTopicHandler(BaseHandler):
    def get(self):
        self.render("newtopic.html")

    def post(self):
        title = self.get_argument("title")
        body = self.get_argument("body")
        tags = self.get_argument("tags")
        tag_list = tags.split()
        topic = TopicManager().create(self.current_user, title, body, tag_list)
        self.redirect("/topic/%s" % topic["_id"])


class UpdateTopicHandler(BaseHandler):
    def get(self, id):
        topic = TopicManager().get(id)
        if topic is None:
            raise tornado.web.HTTPError(404)
        self.render("updatetopic.html", topic=topic)

    def post(self, id):
        title = self.get_argument("title")
        body = self.get_argument("body")
        tags = self.get_argument("tags")
        tag_list = tags.split()
        topic = TopicManager().update(id, title, body, tag_list)
        if topic is None:
            raise tornado.web.HTTPError(404)
        self.redirect("/topic/%s" % topic["_id"])


class ReplyHandler(BaseHandler):
    def post(self, id):
        body = self.get_argument("reply")
        TopicManager().reply(id, self.current_user, body)
        self.redirect(self.reverse_url("topic", id))


class TagHandler(BaseHandler):
    def get(self, name):
        tag = TagManager().get_by_name(name)
        if tag is None:
            raise tornado.web.HTTPError(404)
        self.render("tag.html", tag=tag)


class TagsHandler(BaseHandler):
    def get(self):
        tags = TagManager().all()
        self.render("tags.html", tags=tags)


class UsersHandler(BaseHandler):
    def get(self):
        users = UserManager().all()
        self.render("users.html", users=users)


class UserHandler(BaseHandler):
    def get(self, uid):
        user = UserManager().get_by_uid(int(uid))
        self.render("user.html", user=user)


class SetProfileHandler(BaseHandler):
    def get(self, uid):
        pass

    def post(self, uid):
        pass
