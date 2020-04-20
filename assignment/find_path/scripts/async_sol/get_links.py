import asyncio
import aiohttp


# sema = asyncio.BoundedSemaphore(7)
# sema,
async def make_request(session, title, cont=None):
    try:
        URL = "http://en.wikipedia.org/w/api.php"
        params = make_params(title, cont)
        async with session.get(URL, params=params, ssl=False) as response:
            res = await response.json()
            return res
    except Exception as e:
        print("tried to make request for ", title)
        print(e)

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
        for l in v["links"]:
            titles.add(l["title"])
    return  titles, cont

# async def get_links():
#     """Crawl & add concurrently to `queue` for multiple `urls`."""
#     try:
#         workers = [keep_getting_links() for _ in range(5)]
#         await asyncio.gather(workers)
#         # response = await make_request(session, title)
#         # titles, cont = parse_response(response)
#         # print("Read {0} links from {1}".format(len(titles), title))
#         # while cont != None:
#         #     response = await make_request(session, title, cont)
#         #     more_titles, cont = parse_response(response)
#         #     titles = titles.union(more_titles)
#         # await graph.search_links(title, titles)
#     except Exception as e:
#         print(e)
#         print("An exception occurred when getting links")



# def ():
#     try:
#         cont = ""
#         DATA = get_links(title)
#         return parse_links(title, DATA["titles"], DATA["cont"])
