from get_links import getLinks
from checker import check
from queue import PriorityQueue

def main(source, destination):

    graph = {}
    graph['path'] = [source]
    pq = PriorityQueue()

    src_titles = getLinks(source)
    graph['source'] = src_titles
    if check(src_titles, destination):
        graph['path'].append(destination)
        print(graph['path'])
        return graph['path']

    #des_titles = getLinks(destination)

main('Rami Malek', '2018 in film')
    