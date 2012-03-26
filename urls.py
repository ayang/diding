from tornado.web import URLSpec as s
from handlers.welcome import *
from handlers.auth import AuthHandler, LogoutHandler, GoogleAuthHandler, DoubanAuthHandler
from handlers.accounts import SignupHandler

url_patterns = [
    s(r"/", HomeHandler, name="home"),
    s(r"/login", AuthHandler, name="login"),
    s(r"/login/google", GoogleAuthHandler, name="login_google"),
    s(r"/login/douban", DoubanAuthHandler, name="login_douban"),
    s(r"/logout", LogoutHandler, name="logout"),
    s(r"/accounts/signup", SignupHandler, name="signup"),
    s(r"/about", AboutHandler, name="about"),
    s(r"/topics", TopicsHandler, name="topics"),
    s(r"/node/([^/\s]+)", NodeTopicsHandler, name="nodetopics"),
    s(r"/topic/new", NewTopicHandler, name="newtopic"),
    s(r"/topic/(\w+)", TopicHandler, name="topic"),
    s(r"/topic/(\w+)/edit", UpdateTopicHandler, name="edittopic"),
    s(r"/topic/(\w+)/reply", ReplyHandler, name="reply"),
    s(r"/nodes", NodesHandler, name="nodes"),
    s(r"/nodes/create", CreateNodeHandler, name="createnode"),
    s(r"/nodeinfo/([^/\s]+)", NodeHandler, name="node"),
    s(r"/users", UsersHandler, name="users"),
    s(r"/user/(\w+)", UserHandler, name="user"),
]
