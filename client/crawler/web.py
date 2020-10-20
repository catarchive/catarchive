import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

UA = 'CatArchiveBot/0.1.0 (+https://github.com/catarchive)'

class Page:
    """Represents a webpage with methods for crawling."""

    def __init__(self, url):
        self.url = urlparse(url)
        self.raw_url = url
        self.links = []
        self.images = []

    def get(self):
        """Sends the request to get the page and stores the response as self.response."""

        self.response = requests.get(
            self.raw_url,
            headers={
                'User-Agent': UA
            },
            timeout=3,
            auth=('user', 'pass')
        )

    def explore(self):
        """Parses out links and images from the webpage and stores them in self.links and self.images, respectively.""" 

        # Use Beautiful Soup to parse the HTML and get the href of a tags and src of img tags:
        page_data = BeautifulSoup(self.response.text, 'html.parser')
        links = [link.get('href') for link in page_data.find_all('a')]
        images = [image.get('src') for image in page_data.find_all('img')]

        for link in links:
            # Format the url:
            link = self.format_url(link)
            if link == '':
                continue

            # Append each valid link to self.links:
            self.links.append(link)

        for image in images:
            # Format the url:
            image = self.format_url(image)
            if image == '':
                continue

            # Append each valid image to self.images:
            self.images.append(image)

    def format_url(self, link):
            """Handle the many different ways to format links."""

            if link == None or link == '':
                return ''

            if link[0] == '/':
                # Links starting with //:
                if len(link) > 1 and link[1] == '/':
                    return 'http:' + link
                # Links starting with /:
                else:
                    return self.url.scheme + '://' + self.url.netloc + link
            # Ignore ID links:
            elif link[0] == '#':
                return ''
            elif (len(link) > 4 and link[0:5] != 'http:') and (len(link) > 5 and link[0:6] != 'https:'):
                # Ignore mailto links:
                if len(link) > 6 and link[0:7] == 'mailto:':
                    return ''
                # Ignore javascript links:
                if len(link) > 10 and link[0:11] == 'javascript:':
                    return ''
                # Bad protocol:
                if '://' in link:
                    return ''
            # Relative-directory links:
            # TODO: Better relative links (see https://kb.iu.edu/d/abwp).
            # Relative urls are dumb! Use absolute ones please.
                return self.url.scheme + '://' + self.url.netloc + self.url.path + '/' + link
            elif len(link) < 5:
                return self.url.scheme + '://' + self.url.netloc + self.url.path + '/' + link
            # The link is fine:
            else:
                return link
