import requests

def get_links(title, cont=""):
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"
    PARAMS = {
        "action": "query",
        "format": "json",
        "prop": "links",
        "indexpageids": 1,
        "titles": title,
        "plnamespace": "0",
        'pllimit': "max",
        "formatversion": "2",
    }
    if len(cont) != 0:
        PARAMS["plcontinue"] = cont

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    titles = set()
    QUERY = DATA["query"]
    PAGES = QUERY["pages"]

    if "continue" in DATA:
        cont = DATA["continue"]["plcontinue"]
    elif "batchcomplete" in DATA and DATA["batchcomplete"]:
        cont = "" 
    for v in PAGES:
        if "missing" in v and v["missing"]:
            return {"titles": set(), "cont": cont}
        for l in v["links"]:
            titles.add(l["title"])
    print("Read {0} links from {1}".format(len(titles), title))
    return  {"titles": titles, "cont": cont}
    
def parse_links(title, titles, cont):
    master_titles = titles

    if len(cont) == 0:
        return master_titles
    else:
        while(len(cont) != 0):
            res = get_links(title, cont)
            master_titles = master_titles.union(res["titles"])
            cont = res["cont"]
    return master_titles

def get_all_links(title):
    try:
        cont = ""
        DATA = get_links(title)
        return parse_links(title, DATA["titles"], DATA["cont"])
    except Exception as e:
        print(e)
        print("An exception occurred when getting links")