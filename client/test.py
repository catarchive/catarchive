from classifier import classify
import requests

r = requests.get('https://greerpage.com/static/images/img1.jpg', stream=True)
print(classify(r, is_url=True))
