import asyncio
import aiohttp

'''

Some functions for making the request to media wiki api and parsing the response.

'''

# thought I would need a semaphore to limit the amount of connections to media wiki 
# was taken care of by aiohttps limit on a connector
# sema = asyncio.BoundedSemaphore(7)

async def make_request(session, title, cont=None):
    try:
        URL = "http://en.wikipedia.org/w/api.php"
        params = make_params(title, cont)
        async with session.get(URL, params=params, ssl=False) as response:
            res = await response.json()
            return res
    except:
        print("")
        # print(e)
         

def make_params(title, cont=None):
    params = {
        "action": "query",
        "format": "json",
        "prop": "links",
        "indexpageids": 1,
        "titles": title,
        "plnamespace": "0",
        'pllimit': "max",
        "formatversion": "2",
    }
    
    if cont != None:
        params["plcontinue"] = cont
    return  params

def parse_response(DATA): 
    titles = set()
    QUERY = DATA["query"]
    PAGES = QUERY["pages"]

    if "continue" in DATA:
        cont = DATA["continue"]["plcontinue"]
    
    elif "batchcomplete" in DATA and DATA["batchcomplete"]:
        cont = None 
    
    for v in PAGES:
        if "missing" in v and v["missing"]:
            return set(), cont
        elif "links" not in v:
            return set(), cont
        for l in v["links"]:
            titles.add(l["title"])
    return  titles, cont
