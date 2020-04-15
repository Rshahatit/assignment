#!/usr/bin/python3

"""
    get_links.py

    MediaWiki API Demos
    Demo of `Links` module: Get all links on the given page(s)

    MIT License
"""
import requests

def getLinks(title):
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "query",
        "format": "json",
        "prop": "links",
        "indexpageids": 1,
        "continue": "",
        "titles": title,
        "plnamespace": "0",
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    PAGES = DATA["query"]["pages"]
    titles = set()
    for k, v in PAGES.items():
        for l in v["links"]:
            titles.add(l["title"])
    return titles
