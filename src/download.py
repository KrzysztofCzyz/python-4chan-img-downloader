import requests
import click
import json
import re
from PIL import Image
from io import BytesIO
from pathlib import Path
#TODO process indicator based on num on imgs
#TODO user interacion via click
#TODO change list to dics <filename(hex(8).ext), link>


def download_images(links):
    for link in links:
        path = Path('Downloads/' + link + '.jpg')
        i = Image.open(BytesIO(requests.get(link).content))
        i.save(path)


def build_thread_links(numbers, board):
    thread_links = list()
    for number in numbers:
        thread_links.append('https://a.4cdn.org/' + str(board) + '/thread/' + str(number) + '.json')
    return thread_links


def build_image_links(thread_list, board):
    image_links = list()
    for thread in thread_list:
        request = requests.get(thread)
        jsn = json.loads(request.content)
        for post in jsn['posts']:
            if post.get('filename'):
                image_links.append('https://i.4cdn.org/' + str(board) + '/' + str(post.get('tim')) + '.'
                                   + str(post.get('ext')))
    return image_links


@click.command()
@click.argument('link')
def parse(link):
    link_match = regexp.match(link)

    if not link_match:
        return

    thread_list = list()
    request = requests.get(link)

    jsn = json.loads(request.content)
    for page in jsn:
        for thread_header in page['threads']:
            if thread_header['images'] > 0:
                thread_list.append(thread_header['no'])

    thread_links = build_thread_links(thread_list, board=link_match.group(1))
    build_image_links(thread_links, board=link_match.group(1))


@click.command()
def cli():
    regexp = re.compile(r'\Ahttp[?s]://a.4cdn.org/(\w+)/catalog.json\Z', re.IGNORECASE)
    parse()

# https://i.4cdn.org/[board]/[4chan image ID].[file extension]
