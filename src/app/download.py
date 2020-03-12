import requests
import click
import json
import secrets
import os
from PIL import Image
from io import BytesIO
from pathlib import Path
from app.types.link import CatalogLinkType, ThreadLinkType

# TODO style the app's output (click.secho)
# TODO download images func <----- - speed it up - possibly use threading


def entry_point():
    cli()


@click.group()
def cli():
    pass


@cli.command()
@click.option('--link', '-l', type=CatalogLinkType(), help='Catalog link i.e. boards.4chan.org/BOARD/catalog')
@click.option('--test-run/--no-test-run', default='False', help='Implemented for test purposes')
def catalog(link, test_run):
    if not test_run:
        thread_dic = dispatch_catalog_link(link)
        thread_links = build_thread_links(thread_dic['th_list'], board=link['board'])
        image_links = build_image_links(thread_links, board=link['board'])
        download_images(image_links)


@cli.command()
@click.option('--link', '-l', type=ThreadLinkType(), help='Thread link i.e. boards.4chan.org/BOARD/thread/TH_NUM')
@click.option('--test-run/--no-test-run', default='False', help='Implemented for test purposes')
def thread(link, test_run):
    if not test_run:
        image_links = build_image_links(link['link'], board=link['board'], single=True)
        download_images(image_links)


def dispatch_catalog_link(link):
    thread_list = list()
    num_of_images = 0
    request = requests.get(link['link'])

    jsn = json.loads(request.content)
    for page in jsn:
        for thread_header in page['threads']:
            if thread_header['images'] > 0:
                num_of_images += thread_header['images']
                thread_list.append(thread_header['no'])

    return {'im_num': num_of_images, 'th_list': thread_list}


def download_images(links):
    try:
        os.mkdir(os.curdir+os.sep+'Downloads')
    except FileExistsError:
        pass
    with click.progressbar(links, label='Downloading images to hard disk') as links_bar:
        for link in links_bar:
            path = Path(os.curdir + os.sep + 'Downloads' + os.sep + link['filename'])
            i = Image.open(BytesIO(requests.get(link['link']).content))
            i.save(path)


def build_thread_links(numbers, board):
    thread_links = list()
    for number in numbers:
        thread_links.extend('https://a.4cdn.org/' + str(board) + '/thread/' + str(number) + '.json')
    return thread_links


def build_image_links(thread_list, board, single=False):
    image_links = list()
    if single:
        image_links.extend(get_image_link(thread_list, board))
    else:
        with click.progressbar(thread_list, label="Building image links") as th_list_bar:
            for thread in th_list_bar:
                image_links.extend(get_image_link(thread, board))
    return image_links


def get_image_link(link, board):
    links = list()
    request = requests.get(link)
    jsn = json.loads(request.content)
    for post in jsn['posts']:
        if post.get('filename'):
            if post.get('ext') == '.jpg' or post.get('ext') == '.png' or post.get('ext') == '.gif':
                links.append({'link': 'https://i.4cdn.org/' + str(board) + '/' + str(post.get('tim'))
                                      + str(post.get('ext')), 'filename': secrets.token_hex(8) + post.get('ext')})
    return links
