#!/usr/bin/env python3

import threading

import crawler

INITIAL = ['https://www.reddit.com/r/cat']

def manager():
    while True:
        link = crawler.link_queue.get()
        crawler.attempt(link)

if __name__ == '__main__':
    threading.Thread(target=manager).start()
    for link in INITIAL:
        crawler.link_queue.put(link)