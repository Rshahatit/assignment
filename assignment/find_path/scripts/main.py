from graph import Graph
from get_links import get_all_links


def main(source, destination):

    graph = Graph(source, destination)
    graph.add(source, get_all_links(source), '0')
    graph.add(destination, get_all_links(destination), '1')

    # check if dest is on src page
    if destination in graph.links(source):
        graph.set_previous(destination, source)
        return graph.get_path(destination)
    graph.prioritize(source)

    while (not graph.pq.empty()):
        if (graph.found):
            print(graph.path)
            print(graph)
            return graph.path

        nxt = graph.pq.get()[1]
        print("checking: " + nxt)
        if destination in graph.links(nxt):
            graph.set_previous(destination, nxt)
            graph.get_path(destination)
            print(graph.path)
            print(graph)
            return graph.path
        else:
            graph.prioritize(nxt)
    return "No path found"
    
# if __name__ == "__main__":
#     main(source, destination)

    