from .graph  import Graph
import asyncio 

"""
Make a consumer that also produces

the consumer consumes the source first and then queues those links to be processed by another consumer which puts those linkes back in the queue
to be processed by that same consumer that retrieved them from the api.

""" 

# async def cons_title_prod_links(q, cons_links_prod_titles, previous):
#     title = await q.get()
#     links = await get_all_links(title)
#     cons_links_prod_titles(title, links, previous, q)
    

# async def cons_links_prod_titles(title, links, previous, q):
#     graph.add(title, links, previous)
#     for link in links:

async def main(source, destination):
    import time
    s = time.perf_counter()
    # start_time = time.time()
    print("Start Time = ", s)
    graph = Graph(source, destination)
    workers = [graph.search_links()]
    workers += [graph.keep_getting_links() for _ in range(5)]
    # workers.append(keep_getting_links())
    for res in asyncio.as_completed(workers):
        path = await res
        elapsed = time.perf_counter() - s
        # for c in asyncio.all_tasks():
        #     c.cancel()
        path = f'Path from {source} to {destination}: {path} completed in {elapsed:0.2f} seconds'
        print(f'Path from {source} to {destination}: {path} completed in {elapsed:0.2f} seconds')

        return path
    # task = asyncio.create_task(graph.search())
    # for res in asyncio.as_completed(task):
    #     path = await res
    # path = await graph.search()
    # for c in asyncio.all_tasks(asyncio.get_running_loop()):
    #     c.cancel()
    elapsed = time.perf_counter() - s
    path = f'Path from {source} to {destination}: {path} completed in {elapsed:0.2f} seconds'
    print(f'Path from {source} to {destination}: {path} completed in {elapsed:0.2f} seconds')
    return path
def start(source, destination):
    return asyncio.run(main(source, destination))

    
# start("Rami Malek", "Iran")
    
# asyncio.as_completed()
# start = time.perf_counter()
# asyncio.run(main(**ns.__dict__))
# elapsed = time.perf_counter() - start
# print(f"Program completed in {elapsed:0.5f} seconds.")