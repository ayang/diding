from tornado.util import ObjectDict


class InputField(ObjectDict):
    def __init__(self, name, type, label="", value="", placeholder="", error="", help="", **attribs):
        input_types = ("button", "checkbox", "file", "hidden", "image", "password", "radio", "reset", "submit", "text")
        self["name"] = name
        self["type"] = type if type in input_types else "text"
        self["label"] = label
        self["value"] = value
        self["placeholder"] = placeholder
        self["error"] = error
        self["help"] = help
        self.attribs = attribs
