from .get_links import make_request, make_params, parse_response
# from queue import PriorityQueue
import asyncio
import aiohttp

"""
as we wait for the responses from the wiki api i want to have titles to be queued up to be check

so there is a difference between titles to visit and titles to check. titles to visit are sent to the get links function
whats the difference... 
well we will be getting titles to check througout but while those are seemingly streaming in as they complete their IO operations
we want to check the ones that it already got.
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
        self.previous = {source : '0'}
        self.event = asyncio.Event()
        # session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=5))
        # self.session = session
        self.titles_to_fetch.put_nowait(source)

        #self.titles_to_visit.put_nowait(source)

    def __str__(self): 
        st = 'PATH: {0} \n'.format(str(self.path))
        for title in self.graph.keys():
            st += 'Title: ' + title + '\nprev: ' + self.previous[title]  +  '\n' + str(len(self.links(title))) + '\n'
        st += "Checked this many pages: " + str(len(self.seen)) + "\n"
        return st

    def add(self, title, links):
        self.graph[title] = {
            'links' : links,  
            }

    def set_previous(self, title, previous):
        self.previous[title] = previous

    # async def search(self):
    #     try:
    #         # while not self.titles_to_visit.empty():
    #             # await self.event.wait()
    #             # if self.found:
    #             #     return self.path
    #             await get_links()
    #             # current = await self.titles_to_visit.get()
    #             # if current not in self.seen:
    #                 # conn = aiohttp.TCPConnector(limit=8)
    #                 # async with self.session as session:
    #                     # await get_links(session, current, self)
    #                     # self.seen.add(current)
    #     except Exception as e:
    #         print(e)

    async def search_links(self):
        while True:
            title, links = await self.titles_to_visit.get()
            self.add(title, links)
            self.seen.add(title)
            print("checking", title)
            if self.end in self.links(title):
                    self.set_previous(self.end, title)
                    self.make_path(self.end)
                    print("FOUND")
                    print(self)
                    # self.session.close()
                    return self.path
            for link in links:
                if link not in self.seen and link != title:
                    self.previous[link] = title
                    await self.titles_to_fetch.put(link)

    async def keep_getting_links(self):
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=5)) as session:
                while True:
                        if self.found:
                            await session.close()
                        title = await self.titles_to_fetch.get()
                        response = await make_request(session, title)
                        titles, cont = parse_response(response)
                        print("Read {0} links from {1}".format(len(titles), title))
                        while cont != None:
                            response = await make_request(session, title, cont)
                            more_titles, cont = parse_response(response)
                            titles = titles.union(more_titles)
                        await self.titles_to_visit.put((title, titles))
        except Exception as e:
            print(e)
            print("An exception occurred when getting links")
    


                
    def links(self, title):
        return self.graph[title]['links']

    def make_path(self, title):
        try:
            t = title 
            previous = self.previous[t]
            path = [t]
            while(previous != '0'):
                path.append(previous)
                t = previous
                print(previous, "might be looping")
                previous = self.previous[t]
            self.found = True
            path.reverse()
            self.path = path
        except Exception as e:
            print(e)
            return e
    
    def get_path(self, title):
        self.make_path(title)
        return self.path

    def done(self, duration):
        print(self.graph)
        print("Duration: ", duration)
        return self.graph.path
    