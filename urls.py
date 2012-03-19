from tornado.web import URLSpec as s
from handlers.welcome import *
from handlers.auth import AuthHandler, LogoutHandler

url_patterns = [
    s(r"/", HomeHandler, name="home"),
    s(r"/login", AuthHandler, name="login"),
    s(r"/logout", LogoutHandler, name="logout"),
    s(r"/about", AboutHandler, name="about"),
    s(r"/topics", TopicsHandler, name="topics"),
    s(r"/topics/tagged/([^/\s]+)", TaggedTopicsHandler, name="taggedtopics"),
    s(r"/topic/new", NewTopicHandler, name="newtopic"),
    s(r"/topic/(\w+)", TopicHandler, name="topic"),
    s(r"/topic/(\w+)/edit", UpdateTopicHandler, name="edittopic"),
    s(r"/topic/(\w+)/reply", ReplyHandler, name="reply"),
    s(r"/tags", TagsHandler, name="tags"),
    s(r"/tag/([^/\s]+)", TagHandler, name="tag"),
    s(r"/users", UsersHandler, name="users"),
    s(r"/user/(\w+)", UserHandler, name="user"),
]
