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


@singleton
class TopicManager(DataManager):

    def get(self, id):
        topic = self.db.topic.find_one({"_id": ObjectId(id)})
        return topic

    def create(self, publisher, title, body, tag_list):
        topic = {
            "publisher": publisher,
            "title": title,
            "body": body,
            "tags": tag_list[:5],
            "create_time": datetime.utcnow(),
            "update_time": datetime.utcnow(),
            "last_reply_time": datetime.utcnow(),
            "last_reply_user": None,
            "replies_count": 0,
            "replies": [],
        }
        self.db.topic.insert(topic)
        tm = TagManager()
        for tag in tag_list:
            tm.increment(tag)
        return topic

    def update(self, id, title, body, tag_list):
        topic = self.get(id)
        topic["title"] = title
        topic["body"] = body
        topic["tags"] = tag_list[:5]
        topic["update_time"] = datetime.utcnow()
        self.db.topic.update(topic)
        return topic

    def delete(self, id):
        self.db.topic.remove({"_id": ObjectId(id)})

    def all(self, start=0, limit=0, sort_by=None):
        topics = self.db.topic.find(skip=start, limit=limit, sort=sort_by)
        return topics

    def tagged(self, tag, start=0, limit=0, sort_by=None):
        topics = self.db.topic.find({"tags": tag["name"]}, skip=start, limit=limit, sort=sort_by)
        return topics

    def count(self):
        count = self.topic.count()
        return count

    def reply(self, id, user, body):
        reply = {
            "user": user,
            "body": body,
            "time": datetime.utcnow(),
        }
        self.db.topic.update({"_id": ObjectId(id)}, {
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

    def create(self, name, wiki=None, icon=None):
        tag = {
            "name": name,
            "create_time": datetime.utcnow(),
            "update_time": datetime.utcnow(),
        }
        if wiki:
            tag.wiki = wiki
        if icon:
            tag.icon = icon
        self.db.tag.insert(tag)
        return tag

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

    def all(self, start=0, limit=0, sort_by=None):
        users = self.db.user.find(skip=start, limit=limit, sort=sort_by)
        return users

    def create(self, email, name):
        uid = self.db.counter.find_and_modify({"name": "user_id"}, {"$inc": {"c": 1}}, upsert=True)
        user = {
            "uid": uid["c"],
            "email": email,
            "name": name,
            "created_time": datetime.utcnow(),
            "last_accessed_time": datetime.utcnow(),
        }
        self.db.user.insert(user)
        return user

    def refresh(self, uid):
        self.db.user.update({"uid": uid}, {"last_accessed_time": datetime.utcnow()})

    def set_picture(self, uid, picture_url):
        return self.db.user.update({"uid": uid}, {"picture": picture_url})

    def set_profile(self, uid, profile):
        return self.db.user.update({"uid": uid}, {"profile": profile})
