import time
import requests
import threading

from . import web as w

local_explored = set([])
images = set([])

def attempt(link):
    """Attempt to crawl a single webpage. Any other links are returned, 
    and the images are printed."""

    # Ensure the page hasn't already been explored:
    if link in local_explored:
        return []

    # Instantiate the page class:
    p = w.Page(link)

    # Try to get the webpage:
    try:
        p.get()
    # Return if there was a connect error or if the request timed out:
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        return []

    # Sleep for the appropriate time and reattempt if the status code was 429:
    if p.response.status_code == 429:
        print('429, sleeping for', p.response.headers['Retry-After'])
        time.sleep(int(p.response.headers['Retry-After']))
        attempt(link)

    # Add the link to the explored set:
    local_explored.add(link)

    # Return if the status code was not 200:
    if p.response.status_code != 200:
        print('bad status code', p.response.status_code, link)
        return []

    # The explore method will set p.links and p.images.
    p.explore()

    # Print out the images:
    for image in p.images:
        if image not in local_explored:
            print(image)
            images.add(image)

    # Return any links to crawl.
    return p.links
