import tornado.web
from models.message import TagManager


class HotTags(tornado.web.UIModule):
    def render(self, count=20):
        tags = TagManager().all(limit=count)
        return self.render_string("module-hottags.html", tags=tags)
