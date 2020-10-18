import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

UA = 'CatArchiveBot/0.1.0 (+https://github.com/catarchive)'

local_explored = set([])

class AlwaysRobot:
    def can_fetch(self, foo, bar):
        return True

class Page:
    def __init__(self, url):
        self.url = urlparse(url)
        self.raw_url = url
    def get(self):
        self.response = requests.get(
            self.raw_url,
            headers={
                'User-Agent': UA
            },
            timeout=2,
            auth=('user', 'pass')
        )
    def explore(self):
        page_data = BeautifulSoup(self.response.text, 'html.parser')
        links = [link.get('href') for link in page_data.find_all('a')]
        images = [image.get('src') for image in page_data.find_all('img')]

        try:
            self.robots = RobotFileParser(url=self.url.scheme+'://'+urlparse(seed_url).netloc+'/robots.txt')
            self.robots.read()
        except:
            self.robots = AlwaysRobot()

        self.links = []
        for link in links:
            # handle relative urls    
            try:
                if link[0] == '/':
                    if link[1] == '/':
                        link = 'http:' + link
                    else:
                        link = self.url.scheme + '://' + self.url.netloc + link
                elif link[0] == '#':
                    continue
                elif len(link) > 3 and link[0:4] != 'http':
                    if len(link) > 6 and link[0:7] == 'mailto:':
                        continue
                    if len(link) > 10 and link[0:11] == 'javascript:':
                        continue
                    link = self.url.scheme + '://' + self.url.netloc + '/' + link
                elif len(link) < 4:
                    link = self.url.scheme + '://' + self.url.netloc + '/' + link
            except:
                continue

            parsed = urlparse(link)
            robots = self.robots
            if parsed.netloc != self.url.netloc:
                try:
                    robots.set_url(self.url.scheme+'://'+urlparse(seed_url).netloc+'/robots.txt')
                    robots.read()
                except:
                    robots = AlwaysRobot()

            if robots.can_fetch(UA, link):
                self.links.append(link)

        self.images = []
        for image in images:
            # handle relative urls    
            try:
                if image.rsplit('.')[-1] != 'jpg' and image.rsplit('.')[-1] != 'jpeg':
                    if len(image.rsplit('.')) != 0:
                        continue
                if image[0] == '/':
                    if image[1] == '/':
                        image = 'http:' + image
                    else:
                        image = self.url.scheme + '://' + self.url.netloc + image
                elif len(image) > 3 and image[0:4] != 'http':
                    image = self.url.scheme + '://' + self.url.netloc + '/' + image
                elif len(image) < 4:
                    image = self.url.scheme + '://' + self.url.netloc + '/' + image
            except:
                continue

            parsed = urlparse(image)
            if parsed.netloc+parsed.path in local_explored:
                continue
            robots = self.robots
            if parsed.netloc != self.url.netloc:
                try:
                    robots.set_url(self.url.scheme+'://'+urlparse(seed_url).netloc+'/robots.txt')
                    robots.read()
                except:
                    robots = AlwaysRobot()

            if robots.can_fetch(UA, image):
                self.images.append(image)
                local_explored.add(parsed.netloc+parsed.path)

