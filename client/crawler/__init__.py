import requests
from urllib.parse import urlparse

from . import web

class Crawler:
    """Stores the explored pages and has methods for crawling pages."""

    def __init__(self):
        self.local_explored = set([])
        self.local_images = set([])
        self.page = web.Page('')
        self.con_err = False
        self.tmr = set([])

    def get_filtered_links(self, link):
        """Get the unexplored links and images from a single webpage."""

        # Instantiate the page class:
        self.page = web.Page(link)

        # Try to get the webpage:
        try:
            self.page.get()
        # Return if there was a connect error or if the request timed out:
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            self.con_err = True
            self.local_explored.add(link)
            return ([], [])

        # Return without marking as explored for 429:
        if self.page.response.status_code == 429:
            self.tmr.add(self.page.url.netloc)
            return ([], [])
        else:
            if self.page.url.netloc in self.tmr:
                self.tmr.remove(self.page.url.netloc)

        # Add the link to the explored set:
        self.local_explored.add(link)

        # Only follow HTML:
        try:
            if self.page.response.headers['Content-Type'][0:10] != 'text/html;':
                return ([], [])
        except IndexError:
            return ([], [])

        # Return if the status code was not 200:
        if self.page.response.status_code != 200:
            return ([], [])

        # The explore method will set self.page.links and self.page.images.
        self.page.explore()

        # Filter the links:
        valid_links = []
        for link in self.page.links:
            if link not in self.local_explored:
                if link.split('.')[-1] == 'pdf' or link.split('.')[-1] == 'gz' or link.split('.')[-1] == 'zip':
                    if len(link.split('/')[-1].split('.')) != 0:
                        continue
                valid_links.append(link)

        # Filter the images:
        valid_images = []
        for image in self.page.images:
            if image not in self.local_images:
                # We only care about jpegs.
                if image.split('.')[-1] != 'jpg' and image.split('.')[-1] != 'jpeg':
                    if '?' in image:
                        if image.split('.')[-1].split('?')[0] != 'jpg' and image.split('.')[-1].split('?')[0] != 'jpeg':
                            continue
                    elif len(image.split('/')[-1].split('.')) != 0:
                        continue
                valid_images.append(image)
                self.local_images.add(image)

        # Return any links to crawl.
        return (valid_links, valid_images)
