import re

def parse_input(page):
    if "http://en.wikipedia.org/wiki/" in page or "https://en.wikipedia.org/wiki/" in page: 
        title = re.split(r'https:\/\/en.wikipedia.org\/wiki\/',page)[1]
        return re.sub("_", " ", title)
    elif "http" in page:
        return 0
    else:
        return page
    