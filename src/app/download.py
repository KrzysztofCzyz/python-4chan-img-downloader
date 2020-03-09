import requests
import click
import json
from PIL import Image
from io import BytesIO
from pathlib import Path
from app.types.link import LinkType

# TODO process indicator based on num of imgs - DONE
# TODO user interacion via click
# TODO change list to dics <filename(hex(8).ext), link>
# TODO style the app's output (click.style)
# TODO download images func <-----

@click.command()
def cli():
    parse()


@click.command()
@click.option('--link', type=LinkType(), help='Catalog link')
def parse(link):
    thread_dic = dispatch_link(link)
    thread_links = build_thread_links(thread_dic['th_list'], board=link['board'])
    image_links = build_image_links(thread_links, board=link['board'])


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
    iterator = 0
    with click.progressbar(length=len(links), label='Downloading images to hard disk') as links_bar:
        for link in links:
            path = Path('Downloads/' + link + '.jpg')
            i = Image.open(BytesIO(requests.get(link).content))
            i.save(path)
            iterator += 1
            links_bar.update(iterator)


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
                    image_links.append('https://i.4cdn.org/' + str(board) + '/' + str(post.get('tim'))
                                       + str(post.get('ext')))
    return image_links
