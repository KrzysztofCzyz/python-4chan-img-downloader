from pathlib import Path
import secrets
import os
from app.board import Board
from app import base_config, logger
from threading import Thread, Lock
from app.models import Picture


def download_image(link, path, lock):
    pic = Picture(link, path)
    pic.initialize(lock)


class DownloadManager:

    def __init__(self):
        self.links = []
        self.config = base_config

    def download(self, concurrent=True):
        self.prepare()
        base_path = self.config.get("download-path")+os.sep
        lock = Lock()
        for link in self.links:
            file_extension = link.split(r".")[-1]
            file_name = secrets.token_hex(8)
            full_path = Path(base_path+file_name+'.'+file_extension)
            t = Thread(target=download_image, args=(link, full_path, lock))
            t.run()

    def configure(self, config, reconfigure=False):
        if reconfigure:
            self.config = config
        else:
            self.config.update(config)

    def prepare(self):
        try:
            os.mkdir(self.config.get("download-path"))
            logger.log("Path created")
        except FileExistsError:
            logger.log("Path already exists, checking for hexes")

    def job_download_board_from_config(self, config, reconfigure=False):
        self.configure(base_config, reconfigure)
        board = Board()
        board.configure(config)
        board.dispatch()
        self.links = board.get_links()
        self.download()

