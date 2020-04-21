from .utils import make_request, make_params, parse_response
import asyncio
import aiohttp

"""
Graph Object that stores the state of the graph, contains the wokers that retrieve the links, and search through those links.
Keeps track of state: titles_to_visit and titles_to_fetch are the async queues that give jobs to both search links and keep getting links
seen is used to stop any cyles.
previous is used to follow a path back to the source once we've found the destination. 
"""
class Graph():
    def __init__(self, source, destination):
        self.graph = {}
        self.start = source
        self.end = destination
        self.titles_to_visit = asyncio.Queue()
        self.titles_to_fetch = asyncio.Queue()
        self.found = False
        self.path = []
        self.seen = set()
        #initlizing with the source page to start searching
        self.titles_to_fetch.put_nowait((source, 0))
        self.previous = {source : ('0', 0)}
        # Attempted:
        # I was going to broadcast an event that the dest was found but found a way around it.
        # self.event = asyncio.Event() 
        # I was going to pass the same session to each worker, but it was closing after a single connection with the context manager syntax
        # session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=5)) 
        # self.session = session

    def __str__(self): 
        st = 'PATH: {0} \n'.format(str(self.path))
        for title in self.seen:
            st += 'Title: ' + title + '\nprev: ' + self.get_prev(title) + '\n'
        st += "Checked this many pages: " + str(len(self.seen)) + "\n"
        return st
    
    '''
    Constantly pops items from the Titles to visit queue ->
    checks if the destination title is on that page ->
    if not, adds all the titles on that page into the titles to fetch queue'''
    async def search_links(self):
        while True:
            title, links = await self.titles_to_visit.get()
            # self.add(title, links)
            self.seen.add(title)
            # print("checking", title)
            if self.end in links:
                    self.set_previous(self.end, title, 0)
                    self.make_path(self.end)
                    print(f'Checked this many pages: {str(len(self.seen))} \n')
                    return self.path
            new_depth = self.get_depth(title) + 1
            # print(new_depth)
            for link in links:
                if link not in self.seen and link != title:
                    self.set_previous(link, title, new_depth)
                    await self.titles_to_fetch.put((link, new_depth))

    ''' 
    Constantly pops items from the Titles to fetch queue ->
    Ensures that we get all the links for the page even if it has to make more than one request
    due to a 500 limit response. 
    Adds the title with its links into the titles to visit queue'''
    
    async def keep_getting_links(self):
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=5)) as session:
                while True:
                        if self.found:
                            await session.close()
                            return self.path
                        title, depth = await self.titles_to_fetch.get()
                        if depth >= 15:
                            # await session.close()
                            return 0
                        response = await make_request(session, title)
                        if response == None:
                            continue
                        titles, cont = parse_response(response)
                        # print("Read {0} links from {1}".format(len(titles), title))
                        while cont != None:
                            response = await make_request(session, title, cont)
                            more_titles, cont = parse_response(response)
                            titles = titles.union(more_titles)
                        await self.titles_to_visit.put((title, titles))
        except:
            print("")
            # print("An exception occurred when getting links")
    
    def add(self, title, links):
        self.graph[title] = {
            'links' : links,  
            }

    def set_previous(self, title, previous, depth):
        self.previous[title] = (previous, depth)

    def get_prev(self, title):
        return self.previous[title][0]

    def get_depth(self, title):
        return self.previous[title][1]

    def links(self, title):
        return self.graph[title]['links']

    def make_path(self, title):
        try: 
            previous = self.get_prev(title)
            path = [title]
            while(previous != '0'):
                path.append(previous)
                title = previous
                previous = self.get_prev(title)
            self.found = True
            path.reverse()
            self.path = path
        except:
            print("")
            # return e
    
    def get_path(self, title):
        self.make_path(title)
        return self.path
    