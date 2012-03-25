import tornado.web
from models.topic import NodeManager


class HotNodes(tornado.web.UIModule):
    def render(self, count=20):
        nodes = NodeManager().all(limit=count)
        return self.render_string("module-hotnodes.html", nodes=nodes)
