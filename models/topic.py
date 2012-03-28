from datetime import datetime
from pymongo import Connection
from pymongo.objectid import ObjectId


def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


class DataManager:
    def __init__(self):
        self.db = Connection().diding


def extract(d, keys):
    return dict((k, d[k]) for k in keys if k in d)


@singleton
class UserManager(DataManager):

    def get(self, id):
        user = self.db.user.find_one({"_id": ObjectId(id)})
        return user

    def get_by_uid(self, uid):
        user = self.db.user.find_one({"uid": uid})
        return user

    def get_by_email(self, email):
        user = self.db.user.find_one({"email": email})
        return user

    def get_by_local_account(self, email):
        return self.db.user.find_one({"accounts.local.email": email})

    def get_by_google_account(self, email):
        return self.db.user.find_one({"accounts.google.email": email})

    def all(self, start=0, limit=0, sort_by=None):
        users = self.db.user.find(skip=start, limit=limit, sort=sort_by)
        return users

    def create(self, email, name, accounts, **kwargs):
        uid = self.db.counter.find_and_modify({"name": "user_id"}, {"$inc": {"c": 1}}, upsert=True)
        user = {
            "uid": uid["c"],
            "email": email,
            "name": name,
            "created_time": datetime.utcnow(),
            "last_accessed_time": datetime.utcnow(),
            "accounts": accounts,
            "access": ["createtopic"],
        }
        user.update(**kwargs)
        self.db.user.insert(user)
        return user

    def refresh(self, uid):
        self.db.user.update({"uid": uid}, {"$set": {"last_accessed_time": datetime.utcnow()}})

    def set_picture(self, uid, picture_url):
        return self.db.user.update({"uid": uid}, {"$set": {"picture": picture_url}})

    def set_profile(self, uid, profile):
        return self.db.user.update({"uid": uid}, {"$set": {"profile": profile}})


@singleton
class NodeManager(DataManager):

    def get(self, id):
        node = self.db.node.find_one({"_id": ObjectId(id)})
        return node

    def get_by_slug(self, slug):
        node = self.db.node.find_one({"slug": slug})
        return node

    def create(self, name, slug, uid, **kwargs):
        node = {
            "name": name,
            "slug": slug,
            "create_time": datetime.utcnow(),
            "update_time": datetime.utcnow(),
            "creater_id": uid,
            "summary": "",
            "icon": "",
        }
        node.update(**kwargs)
        self.db.node.insert(node)
        return node

    def update(self, slug, **kargs):
        self.db.node.update({"slug": slug}, kargs)

    def add_topic(self, slug, topic_id):
        self.db.node.update({"slug": slug}, {"$push": {"topics": topic_id}})

    def remove_topic(self, slug, topic_id):
        self.db.node.update({"slug": slug}, {"$pull": {"topics": topic_id}})

    def increment(self, slug):
        self.db.node.update({"slug": slug}, {"$inc": {"topic_count": 1}})

    def all(self, start=0, limit=0, sort_by=None):
        nodes = self.db.node.find(skip=start, limit=limit, sort=sort_by)
        return nodes

    def tree(self):
        nodes = self.db.node.group(['section'], None,
                        {'list': []},
                        'function(obj, prev) {prev.list.push(obj)}'
                        )
        return nodes

    def sections(self):
        sections = self.db.section.find().sort("order", 1)
        return sections

    def count(self):
        count = self.nodes.count()
        return count


@singleton
class TopicManager(DataManager):

    def get(self, id):
        topic = self.db.topic.find_one({"_id": ObjectId(id)})
        return topic

    def get_by_tid(self, tid):
        return self.db.topic.find_one({"tid": tid})

    def create(self, publisher, title, body, node, **kwargs):
        tid = self.db.counter.find_and_modify({"name": "topic_id"}, {"$inc": {"c": 1}}, upsert=True)
        topic = {
            "tid": tid,
            "node": extract(node, ("name", "slug")),
            "publisher": publisher,
            "title": title,
            "body": body,
            "create_time": datetime.utcnow(),
            "update_time": datetime.utcnow(),
            "last_reply_time": datetime.utcnow(),
            "last_reply_user": None,
            "replies_count": 0,
            "replies": [],
        }
        topic.update(**kwargs)
        self.db.topic.insert(topic)

        return topic

    def update(self, id, title, body, **kwargs):
        topic = self.get(id)
        topic["title"] = title
        topic["body"] = body
        topic["update_time"] = datetime.utcnow()
        topic.update(**kwargs)
        self.db.topic.update(topic)
        return topic

    def delete(self, tid):
        self.db.topic.remove({"tid": tid})

    def all(self, start=0, limit=0, sort_by=None):
        topics = self.db.topic.find(skip=start, limit=limit, sort=sort_by)
        return topics

    def filter_by_node(self, node_slug, start=0, limit=0, sort_by=None):
        topics = self.db.topic.find({"node.slug": node_slug}, skip=start, limit=limit, sort=sort_by)
        return topics

    def count(self):
        count = self.topic.count()
        return count

    def reply(self, tid, user, body):
        reply = {
            "user": user,
            "body": body,
            "time": datetime.utcnow(),
        }
        self.db.topic.update({"tid": tid}, {
            "$push": {"replies": reply},
            "$set": {"last_reply_time": datetime.utcnow(), "last_reply_user": user},
            "$inc": {"replies_count": 1}
            })
        return reply


@singleton
class TagManager(DataManager):

    def get(self, id):
        tag = self.db.tag.find_one({"_id": ObjectId(id)})
        return tag

    def get_by_name(self, tagname):
        tag = self.db.tag.find_one({"name": tagname})
        return tag

    def create(self, name, summary=None, icon=None):
        tag = {
            "name": name,
            "create_time": datetime.utcnow(),
            "update_time": datetime.utcnow(),
            "summary": summary,
            "icon": icon,
        }
        self.db.tag.insert(tag)
        return tag

    def update(self, name, **kargs):
        self.db.tag.update({"name": name}, kargs)

    def increment(self, name):
        tag = self.get_by_name(name)
        if not tag:
            tag = self.create(name)
        self.db.tag.update(tag, {"$inc": {"topic_count": 1}})

    def all(self, start=0, limit=0, sort_by=None):
        tags = self.db.tag.find(skip=start, limit=limit, sort=sort_by)
        return tags

    def count(self):
        count = self.tags.count()
        return count
