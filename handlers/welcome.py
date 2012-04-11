import tornado.web
from tornado.util import ObjectDict
from handlers.base import BaseHandler
from models.topic import TopicManager, NodeManager, UserManager

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


class NodeTopicsHandler(BaseHandler):
    def get(self, node_slug):
        node = NodeManager().get_by_slug(node_slug)
        if node is None:
            raise tornado.web.HTTPError(404)
        topics = TopicManager().filter_by_node(node["slug"])
        self.render("nodetopics.html", node=node, topics=topics)


class TopicHandler(BaseHandler):
    def get(self, tid):
        topic = TopicManager().get_by_tid(int(tid))
        if topic is None:
            raise tornado.web.HTTPError(404)
        self.render("topic.html", topic=topic)


class NewTopicHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        node_slug = self.get_argument("node", None)
        nodes = NodeManager().tree()
        self.render("newtopic.html", nodes=nodes, current_node_slug=node_slug)

    @tornado.web.authenticated
    def post(self):
        title = self.get_argument("title")
        body = self.get_argument("body")
        node_slug = self.get_argument("node")
        node = NodeManager().get_by_slug(node_slug)
        if node is None:
            raise tornado.web.HTTPError(404)
        topic = TopicManager().create(self.current_user, title, body, node)
        self.redirect("/topic/%s" % topic["tid"])


class UpdateTopicHandler(BaseHandler):
    def get(self, tid):
        topic = TopicManager().get_by_tid(int(tid))
        if topic is None:
            raise tornado.web.HTTPError(404)
        self.render("updatetopic.html", topic=topic)

    def post(self, tid):
        title = self.get_argument("title")
        body = self.get_argument("body")
        nodes = self.get_argument("nodes")
        node_list = nodes.split()
        topic = TopicManager().update(int(tid), title, body, node_list)
        if topic is None:
            raise tornado.web.HTTPError(404)
        self.redirect("/topic/%s" % topic["tid"])


class ReplyHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, tid):
        body = self.get_argument("reply")
        TopicManager().reply(int(tid), self.current_user, body)
        self.redirect(self.reverse_url("topic", int(tid)))


class NodeHandler(BaseHandler):
    def get(self, name):
        node = NodeManager().get_by_name(name)
        if node is None:
            raise tornado.web.HTTPError(404)
        self.render("node.html", node=node)


class NodesHandler(BaseHandler):
    def get(self):
        nodes = NodeManager().all()
        self.render("nodes.html", nodes=nodes)


class CreateNodeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        sections = NodeManager().sections()
        self.render("node-create.html", sections=sections)

    @tornado.web.authenticated
    def post(self):
        name = self.get_argument("name")
        slug = self.get_argument("slug")
        summary = self.get_argument("summary")
        icon = self.get_argument("icon", None)
        section = self.get_argument("section", "Default")
        user = self.current_user
        NodeManager().create(name, slug, user["uid"], icon=icon, summary=summary, section=section)
        self.redirect(self.reverse_url("nodetopics", slug))


class UsersHandler(BaseHandler):
    def get(self):
        users = UserManager().all()
        self.render("users.html", users=users)


class UserHandler(BaseHandler):
    def get(self, uid):
        user = UserManager().get_by_uid(int(uid))
        self.render("user.html", user=user)


@tornado.web.authenticated
class SetProfileHandler(BaseHandler):
    def get(self, uid):
        pass

    def post(self, uid):
        pass
