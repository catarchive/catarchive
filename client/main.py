#!/usr/bin/env python3

import queue
import requests
import threading

import crawler
import classifier

# The initial links to crawl:
INITIAL = ['https://www.reddit.com/r/cats']

image_queue = queue.PriorityQueue()

def imager():
    """Imager thread to read from the image queue and classify images."""

    # Main imaging loop:
    while True:

        # Download the image from a url on the queue:
        url = image_queue.get()[1]
        image = requests.get(
            url,
            stream=True,
            headers={
                'User-Agent': crawler.web.UA
            },
            auth=('user', 'pass')
        )
        image.raw.decode_content = True

        if image.status_code != 200:
            print('bad status code', url)
            continue

        # Classify the image
        results = classifier.classify(image)
        if results[0]:
            print('imager: cat found!', results[1], url)
        else:
            print('imager: not a cat :(', results[1], url)

def main():
    """Main thread to crawl links from the link queue and add links to the
    image and linke queues."""

    # Create the link queue:
    link_queue = queue.PriorityQueue()
    for link in INITIAL:
        link_queue.put((0,link))

    # Main crawling loop:
    while True:

        # Crawl the next link in the queue:
        link = link_queue.get()[1]
        results = crawler.attempt(link)

        # Put the new links on the queue (prioritize urls with 'cat' in them):
        for new_link in results[0]:
            if 'cat' in new_link:
                link_queue.put((0, new_link))
            else:
                link_queue.put((1, new_link))

        # Put any new images on the imager's queue (prioritize urls with 'cat' in them):
        for image in results[1]:
            print('crawler: found an image', image)
            if 'cat' in image:
                image_queue.put((0, image))
            else:
                image_queue.put((1, image))

if __name__ == '__main__':

    # Start the imager thread:
    threading.Thread(target=imager, daemon=True).start()

    # Start crawling:
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
