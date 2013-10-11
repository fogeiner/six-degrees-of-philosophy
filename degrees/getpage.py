#!/usr/bin/env python
# -*- encoding: utf8 -*-

# Here are imports, do not worry about them
import setpath
from bs4 import BeautifulSoup
from json import loads
from urllib import urlopen, urlencode, unquote
from urlparse import urldefrag
from collections import OrderedDict

# optional helper functions should be written here
cache = {}

def urldecode(str):
    return unicode(unquote(str), 'utf-8')

def getJSON(page):
  params = urlencode({
    'format': 'json',
    'action': 'parse',
    'prop': 'text',
    'redirects': 'true',
    'page': page.encode('utf-8')})
  API = "http://en.wikipedia.org/w/api.php"
  print("Downloading... " + API + "?" + params)
  response = urlopen(API + "?" + params)
  return response.read().decode('utf-8')

def getRawPage(page):
  parsed = loads(getJSON(page))
  try:
    parse = parsed["parse"]
    title = parse["title"]
    content = parse["text"]["*"]
    return title, content
  except KeyError:
    # page does not exist
    return None, None

def getPage(page):
    if cache.has_key(page):
        return cache[page]
    title, content = getRawPage(page)
    hrefs = []
    if content is not None:
        soup = BeautifulSoup(content)
        for paragraph in soup.body.find_all('p', recursive=False):

            hrefs += [link.replace('_', ' ') for link in
                    [urldefrag(urldecode(link))[0][6:] for link in
                [link.get('href') for link in paragraph.find_all('a') if link.get('href').startswith('/wiki/')]]]

    hrefs = OrderedDict.fromkeys(hrefs).keys()
    hrefs = hrefs[:10]
    cache[page] = (title, hrefs)
    return cache[page]


if __name__ == '__main__':
  # This code is executed when running the file.
  # here are things that you could write here to test your functions:
  # print(getJSON("Telecom ParisTech"))
  # print(getRawPage("User:A3_nm/COMASIC"))
  # print(getRawPage("History"))
  print(getPage("Homer"))

