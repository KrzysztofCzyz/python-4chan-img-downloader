import requests
import click
import json
import secrets
import os
from PIL import Image
from io import BytesIO
from pathlib import Path
from app.types.link import LinkType

# TODO process indicator based on num of imgs - DONE
# TODO user interacion via click - DONE
# TODO change list to dics <filename(hex(8).ext), link> - DONE
# TODO style the app's output (click.secho)
# TODO download images func <----- - DONE - works slow at the moment


@click.group()
def cli():
    pass


@cli.command()
@click.option('--link', type=LinkType(), help='Catalog link')
def catalog(link):
    thread_dic = dispatch_link(link)
    thread_links = build_thread_links(thread_dic['th_list'], board=link['board'])
    image_links = build_image_links(thread_links, board=link['board'])
    download_images(image_links)


def dispatch_link(link):
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
        thread_links.append('https://a.4cdn.org/' + str(board) + '/thread/' + str(number) + '.json')
    return thread_links


def build_image_links(thread_list, board):
    image_links = list()
    with click.progressbar(thread_list, label="Building image links") as th_list_bar:
        for thread in th_list_bar:
            request = requests.get(thread)
            jsn = json.loads(request.content)
            for post in jsn['posts']:
                if post.get('filename'):
                    if post.get('ext') == '.jpg' or post.get('ext') == '.png' or post.get('ext') == '.gif':
                        image_links.append({'link': 'https://i.4cdn.org/' + str(board) + '/' + str(post.get('tim'))
                                           + str(post.get('ext')), 'filename': secrets.token_hex(8)+post.get('ext')})
    return image_links
