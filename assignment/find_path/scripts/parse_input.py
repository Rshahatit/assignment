import re

def parse_input(page):
        try:
            if "http" in page:
                return re.split('https:\/\/en.wikipedia.org\/wiki\/',page)[1]
        except Exception as e:
            return "You must enter a valid wikipedia link."