import requests
import json
from app.config import builder


extensions = [".jpg", ".png", ".gif"]


class Thread:
    def __init__(self, board, no):
        self.link = builder.build_thread_link(board, no)
        self.links = []
        self.board = board

    def dispatch(self):
        request = requests.get(self.link)
        jsn = json.loads(request.content)
        for post in jsn.get('posts'):
            if post.get('filename'):
                if post.get('ext') in extensions:
                    self.links.append(builder.build_image_link(self.board, post.get('tim'), post.get('ext')))


class Board:

    def __init__(self):
        self.link = ""
        self.board = ""
        self.threads = []
        self.rules = []

    def configure(self, config, reconfigure=False):
        if reconfigure:
            self.threads = []
        self.rules = config["ruleset"]
        self.board = config["board"]
        self.link = builder.build_board_link(self.board)

    def dispatch(self):
        request = requests.get(self.link)
        jsn = json.loads(request.content)
        for page in jsn:
            for thread_header in page['threads']:
                flag = True
                for rule in self.rules:
                    if not rule.check(thread_header):
                        flag = False
                        break
                if flag:
                    self.threads.append(Thread(self.board, thread_header['no']))
        for t in self.threads:
            t.dispatch()

    def get_links(self):
        result = []
        for t in self.threads:
            result.extend(t.links)
        return result
