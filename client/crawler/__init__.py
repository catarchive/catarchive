import time
import queue
import requests
import threading

from . import web as w

link_queue = queue.Queue()

def attempt(link):

    p = w.Page(link)
    if p.url.netloc+p.url.path in w.local_explored:
        return

    try:
        p.get()
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        return

    if p.response.status_code == 429:
        print('429, sleeping for', p.response.headers['Retry-After'])
        time.sleep(int(p.response.headers['Retry-After']))
        attempt(link)

    w.local_explored.add(p.url.netloc+p.url.path)

    if p.response.status_code != 200:
        print('bad status code', p.response.status_code, link)
        return

    p.explore()

    for link in p.links:
        link_queue.put(link)

    for image in p.images:
        print(image)
