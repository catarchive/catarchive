import queue
import requests
import threading
from urllib.parse import urlparse

try:
    from . import crawler
    from . import classifier
except ImportError:
    import crawler
    import classifier

class Client:
    """Stores and controls the client's state."""

    def __init__(self, initial, server):
        self.image_queue = queue.Queue()
        self.link_queue = queue.PriorityQueue()
        for link in initial:
            self.link_queue.put((0,link))
        self.crawler = crawler.Crawler()
        self.cats = set([])
        self.server = server

    def calculate_priority(self, link):
        """Calculates the priority number of a link."""

        if urlparse(link).netloc in self.crawler.tmr:
            return 2
        if 'cat' in link:
            return 0
        return 1

    def crawler_thread(self):
        """Crawler thread to crawl links from the queue and add to the image queue."""

        while True:

            # Get the next item in the queue (index 1 because 0 is the priority #):
            link = self.link_queue.get()[1]
            if link in self.crawler.local_explored:
                continue
            print('CA: Crawler: Getting', link)

            # Crawl the page:
            results = self.crawler.get_filtered_links(link)

            # Handle connection errors:
            if self.crawler.con_err:
                print('CA: Crawler: Connection error', link)
                self.crawler.con_err = False
                self.link_queue.task_done()
                continue

            # Page wasn't HTML:
            try:
                if self.crawler.page.response.headers['Content-Type'][0:10] != 'text/html;':
                    continue
            except IndexError:
                continue

            # Handle bad status codes
            sc = self.crawler.page.response.status_code
            if sc != 200:
                if sc == 429:
                    print('CA: Crawler: Status code 429, adding back to queue', link)
                    self.link_queue.put((2, link))
                else:
                    print('CA: Crawler: Bad status code', sc, link)
                self.link_queue.task_done()
                continue

            # Put the new links on the queue (prioritize urls with 'cat' in them):
            for new_link in results[0]:
                if new_link not in self.crawler.local_explored:
                    self.link_queue.put((self.calculate_priority(new_link), new_link))

            # Put any new images on the image queue:
            for image in results[1]:
                print('CA: Crawler: Found an image', image)
                self.image_queue.put(image)

            self.link_queue.task_done()

    def classifier_thread(self):
        """Classifier thread to read from the image queue and classify images."""

        # Main imaging loop:
        while True:

            # Download the image from a url on the queue:
            url = self.image_queue.get()
            print('CA: Classifier: Downloading', url)
            try:
                image = requests.get(
                    url,
                    stream=True,
                    headers={
                        'User-Agent': crawler.web.UA
                    },
                    timeout=3,
                    auth=('user', 'pass')
                )
                image.raw.decode_content = True
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                print('CA: Classifier: Could not connect', url)
                self.image_queue.task_done()
                continue

            # Handle bad status codes
            if image.status_code != 200:
                print('CA: Classifier: Bad status code', image.status_code, url)
                self.image_queue.task_done()
                continue

            # Classify the image:
            results = classifier.classify(image.raw)
            if results[0]:
                print('CA: Classifier: Cat found', results[1], url)
                self.server.imag(url)
                self.cats.add(url)
            else:
                print('CA: Classifier: Not a cat', results[1], url)

            self.image_queue.task_done()

    def start(self):
        """Starts both threads and blocks until both queues are empty."""

        threading.Thread(target=self.crawler_thread, daemon=True).start()
        threading.Thread(target=self.classifier_thread, daemon=True).start()
        self.link_queue.join()
        self.image_queue.join()
