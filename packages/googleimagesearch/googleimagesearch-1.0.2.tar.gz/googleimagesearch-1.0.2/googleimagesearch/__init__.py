import requests
import re

URL = 'https://images.google.com/searchbyimage'
session = requests.session()
session.headers = {'User-Agent': 'Mozilla/5.0 Firefox/50.0'}


def patch(response):
    matches = re.findall('sbiq":"([^"]+)', response.text)
    response.name = matches[0] if matches else None
    return response


def search_url(url):
    return patch(session.get(URL, params={'image_url': url}))


def search_bytes(bytes):
    return patch(session.post(URL + '/upload', files={'encoded_image': bytes}))


def search_file(file):
    return search_bytes(open(file, 'rb').read())
