from .graph  import Graph
from .get_links import get_all_links
import time

def main(source, destination):
    start_time = time.time()
    print("Start Time = ", start_time // 60 % 60)

    graph = Graph(source, destination)
    graph.add(source, get_all_links(source), '0')
    graph.add(destination, get_all_links(destination), '1')

    # check if dest is on src page
    if destination in graph.links(source):
        graph.set_previous(destination, source)
        return graph.get_path(destination)
    graph.prioritize(source)
    if (graph.found):
        return graph.done(time.time() - start_time)

    while (not graph.pq.empty()):
        if (graph.found):
            graph.done(time.time() - start_time)

        nxt = graph.pq.get()[1]
        print("checking: " + nxt)
        if destination in graph.links(nxt):
            graph.set_previous(destination, nxt)
            graph.make_path(destination)
            return graph.done(time.time() - start_time)
        else:
            graph.prioritize(nxt)
    return "No path found"
    
# if __name__ == "__main__":
#     main("Rami Malek", "Iran")



    