import re

def parse_input(page):
        try:
            if "http" in page: 
                title = re.split('https:\/\/en.wikipedia.org\/wiki\/',page)[1]
                return re.sub("_", " ", title)
            else:
                return page
        except Exception as e:
            return "You must enter a valid wikipedia link."