from .graph  import Graph
import asyncio 

"""
Starter of the async process. Intializes a graph object with the source and dest. 
Creates a list of workers for processing the queues that are created in the graph.
5 for getting the links from the api and 1 for checking what those workers return.
Time is stored in the beginning and elapsed time is calculated at the end.
""" 

async def main(source, destination):
    import time
    s = time.perf_counter()
    # print("Start Time = ", s)
    graph = Graph(source, destination)
    workers = [graph.search_links()]
    workers += [graph.keep_getting_links() for _ in range(7)]
    for res in asyncio.as_completed(workers):
        path = await res
        elapsed = time.perf_counter() - s
        if path == 0:
            return {"path": [], "duration": elapsed, "error": True, "message":"path does not exist with a depth of 15 from the source page"}
        # for c in asyncio.all_tasks():
        #     c.cancel()
        # print(f'Path from {source} to {destination}: {path} completed in {elapsed:0.2f} seconds')
        return {"path": path, "duration": round(elapsed,2), "error": False}

def start(source, destination):
    return asyncio.run(main(source, destination))
