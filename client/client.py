import queue
import requests
import threading
import sys
from urllib.parse import urlparse

custom = False

from .crawler import Crawler
from .crawler.web import UA
from .network import exceptions as netexcept

class Client:
    """Stores and controls the client's state."""

    def __init__(self, server, custom, good_domains, bad_domains):
        self.image_queue = queue.Queue()
        self.link_queue = queue.PriorityQueue()

        self.crawler = Crawler()
        self.server = server

        self.cats = set([])
        self.error_event = threading.Event()

        self.good_domains = good_domains
        self.bad_domains = bad_domains

        self.domain_priority = {}

        if custom:
            from . import custom_model
            self.classify = custom_model.classify
        else:
            from . import classifier
            self.classify = classifier.classify

    def calculate_priority(self, url):
        """Calculates the priority number of a url."""

        base = 750
        domain = urlparse(url).netloc

        if domain in self.bad_domains:
            base = 1250
        elif domain in self.good_domains:
            base = 50
        elif domain in self.crawler.tmr:
            base = 1000
        elif 'cat' in url:
            base = 749

        try:
            score = base + self.domain_priority[domain]
            if score < 0:
                self.domain_priority[domain] = -base + 1
        except KeyError:
            self.domain_priority[domain] = 0
            score = base

        return score if score > 0 else 0

    def crawler_thread(self):
        """Crawler thread to crawl links from the queue and add to the image queue."""

        while True:

            try:

                # Get the next item in the queue (index 1 because 0 is the priority #):
                priority, link = self.link_queue.get()
                if link in self.crawler.local_explored:
                    continue
                print('Crawler: Getting', link, priority)

                # Crawl the page:
                results = self.crawler.get_filtered_links(link)

                # Handle connection errors:
                if self.crawler.con_err:
                    print('Crawler: Connection error', link)
                    self.crawler.con_err = False
                    self.link_queue.task_done()

                    # Demote for conn err
                    try:
                        self.domain_priority[urlparse(link).netloc] += 100
                    except KeyError:
                        self.domain_priority[urlparse(link).netloc] = 48
                    continue

                # Page wasn't HTML:
                try:
                    if self.crawler.page.response.headers['Content-Type'][0:9] != 'text/html':
                        print('Crawler: Link not HTML', link, self.crawler.page.response.headers['Content-Type'])
                        continue
                except (KeyError, IndexError):
                    continue

                # Handle bad status codes
                sc = self.crawler.page.response.status_code
                if sc != 200:

                    # Demote for bad status
                    try:
                        self.domain_priority[urlparse(link).netloc] += 8
                    except KeyError:
                        self.domain_priority[urlparse(link).netloc] = 6

                    if sc == 429:
                        print('Crawler: Status code 429, adding back to queue', link)
                        self.link_queue.put((2, link))
                    else:
                        print('Crawler: Bad status code', sc, link)
                    self.link_queue.task_done()
                    continue

                # Demote domain
                try:
                    self.domain_priority[urlparse(link).netloc] += 4
                except KeyError:
                    # emphasize new domains
                    self.domain_priority[urlparse(link).netloc] = 0

                # Put the new links on the queue (prioritize urls with 'cat' in them):
                for new_link in results[0]:
                    if new_link not in self.crawler.local_explored:
                        self.link_queue.put((self.calculate_priority(new_link), new_link))

                # Put any new images on the image queue:
                for image in results[1]:

                    # Promote domain
                    self.domain_priority[urlparse(link).netloc] -= 6

                    print('Crawler: Found an image', image)
                    self.image_queue.put((image, link))

                self.link_queue.task_done()

            except Exception as e:
                print('Crawler: EXCEPTION:', e)
                continue

    def classifier_thread(self):
        """Classifier thread to read from the image queue and classify images."""

        # Main imaging loop:
        while True:

            try:

                # Download the image from a url on the queue:
                url, page_url = self.image_queue.get()
                print('Classifier: Downloading', url, 'from', page_url)
                try:
                    image = requests.get(
                        url,
                        stream=True,
                        headers={
                            'User-Agent': UA
                        },
                        timeout=3,
                        auth=('user', 'pass')
                    )
                    image.raw.decode_content = True
                    # 32 MB limit
                    try:
                        if int(image.headers['Content-Length']) > (1024 ** 2) * 32:
                            print('Classifier: Image too big', url)
                            continue
                    except (KeyError, IndexError):
                        pass
                except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                    print('Classifier: Could not connect', url)
                    self.image_queue.task_done()
                    continue

                # Handle bad status codes
                if image.status_code != 200:
                    print('Classifier: Bad status code', image.status_code, url)
                    self.image_queue.task_done()
                    continue

                # Classify the image:
                results = self.classify(image.raw)
                if results[0]:

                    # Promote original domain
                    self.domain_priority[urlparse(page_url).netloc] -= 32

                    print('Classifier: Cat found', results[1], url)
                    try:
                        self.server.imag(url)
                    except netexcept.SocketClosed:
                        print('Classifier: Error: Socket closed')
                        self.error_event.set()
                        sys.exit(1)
                    self.cats.add((url, page_url))
                else:
                    print('Classifier: Not a cat', results[1], url)

                    # Demote domain if image is very-not cat or very-cat
                    if not custom:
                        bad = 0
                        for i in results[1]:
                            if i[0] == 'website' or i[0] == 'menu' \
                            or i[0] == 'Band-Aid' or i[0] == 'sunscreen' \
                            or i[0] == 'packet' or i[0] == 'envelope' \
                            or i[0] == 'comic book':
                                    bad += 1
                            elif 'dog' in i[0] or 'Dog' in i[0] \
                            or 'bear' in i[0] or 'fox' in i[0] \
                            or 'Poodle' in i[0] or 'lynx' in i[0] \
                            or i[0] == 'leopard' or i[0] == 'snow leopard' \
                            or i[0] == 'jaguar' or i[0] == 'lion' \
                            or i[0] == 'tiger' or i[0] == 'cheetah':
                                bad -= 1
                        if bad > 0:
                                self.domain_priority[urlparse(page_url).netloc] += 10
                        elif bad < 0:
                                self.domain_priority[urlparse(page_url).netloc] -= 10

                self.image_queue.task_done()

            except Exception as e:
                print('Classifier: EXCEPTION:', e)
                continue

    def queuer_thread(self):
        """Queuer thread to request new URLs when the queue runs out."""

        while True:

            # Wait for the link queue to run out
            self.link_queue.join()
            print('Queuer: Requesting more URLs')

            # Get URLs from the server
            urls = []
            try:
                urls = self.server.urls()
            except netexcept.InvalidUrlsPacketReceived:
                print('Queuer: Error: Invalid URLS packet received', results[1], url)
                self.error_event.set()
                sys.exit(1)
            except netexcept.SocketClosed:
                print('Queuer: Error: Socket closed')
                self.error_event.set()
                sys.exit(1)
   
            print('Queuer: New URLs:', urls)

            # Add them to the queue
            for link in urls:
                self.link_queue.put((self.calculate_priority(link), link))

    def start(self):
        """Starts both threads and blocks until both queues are empty."""

        # Start the threads
        threading.Thread(target=self.crawler_thread, daemon=True).start()
        threading.Thread(target=self.classifier_thread, daemon=True).start()
        threading.Thread(target=self.queuer_thread, daemon=True).start()

        # Wait for an error event
        self.error_event.wait()
        raise KeyboardInterrupt()
