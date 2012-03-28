from tornado.util import ObjectDict


class InputField(ObjectDict):
    def __init__(self, name, type, label="", value="", placeholder="", error="", help=""):
        self["name"] = name
        self["type"] = type
        self["label"] = label
        self["value"] = value
        self["placeholder"] = placeholder
        self["error"] = error
        self["help"] = help
