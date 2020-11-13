#!/bin/env python
from app.downloadmanager import DownloadManager
import pathlib
from app.config import ConfigGenerator
import argparse
import sys


def parse_args():
    parser = argparse.ArgumentParser(description='Download images via CLI')
    parser.add_argument('--config', help='alternative config', default=str(pathlib.PosixPath.cwd())+"/defs.json",
                        action='store')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    c = ConfigGenerator(args.config)
    dm = DownloadManager()
    for job in c.job_configs:
        dm.job_download_board_from_config(job)
