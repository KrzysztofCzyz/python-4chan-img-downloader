import json
from app.rules import *
from app.linkbuilder import LinkBuilder

known_rules = {
                "match": "MatchRule",
                "image-count": "ImageCountRule"
}


class BasicConfig(dict):

    def __init__(self):
        super().__init__()


base_config = BasicConfig()
builder = LinkBuilder()


class Config(dict):

    def __init__(self):
        super().__init__()
        self.type = "unset"

    def set_type(self, t):
        self.type = t


class ConfigGenerator:

    def __init__(self, arg):
        print(arg)
        with open(arg, mode='r') as fd:
            json_config = json.load(fd)
        self.job_configs = []

        # Base config
        self.populate_basic_config(base_config, json_config["basic"])

        # Link builder config
        c = BasicConfig()
        self.populate_basic_config(c, json_config["link-defs"])
        builder.configure(c)

        # Job config
        for rule_def in json_config["defs"]:
            self.populate_job_config(rule_def)

    @staticmethod
    def populate_basic_config(config, obj):
        config.update(obj)

    def populate_job_config(self, obj):
        conf = Config()
        job_type = obj.get("job-type")
        if job_type == 'board':
            conf.set_type("BOARD")
            rules = []
            for rule_msg in obj.get("rules"):
                rules.append(eval(known_rules[rule_msg.get("rule-type")] + "(\'" + rule_msg.get("rule-arg") + "\')"))
            conf["ruleset"] = rules
            conf["board"] = obj.get("board")
        self.job_configs.append(conf)

