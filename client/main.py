#!/usr/bin/env python3

import queue
import threading

import crawler

# The initial links to crawl:
INITIAL = ['https://www.reddit.com/r/cats']

# TODO: A better architecture for multi-threaded crawling.

def manager(init):
    """Constantly takes links from the queue and attempts to crawl them."""

    # Create the queue:
    q = queue.Queue()
    for link in init:
        q.put(link)

    # Main crawling loop:
    while True:
        link = q.get()
        for new_link in crawler.attempt(link):
            q.put(new_link)

if __name__ == '__main__':

    # Start the manager thread (multi-threading in the future):
    threading.Thread(target=manager,args=(INITIAL,)).start()
