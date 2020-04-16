from queue import PriorityQueue
from get_links import get_all_links

class Graph():
    def __init__(self, source, dest):
        self.graph = {}
        self.start = source
        self.end = dest
        self.pq = PriorityQueue()
        self.found = False
        self.path = []
        self.seen = set()

    def __str__(self): 
        st = 'PATH: {0} \n'.format(str(self.path))
        for title in self.graph.keys():
            st += 'Title: ' + title + '\nprev:    \n' + str(self.links(title)) + '\n'
        st += str(len(self.pq)) + "\n"
        st += str(self.seen) 
        return st

    def add(self, title, links, previous):
        self.graph[title] = {
            'links' : links, 
            'previous' : previous, 
            }

    def set_previous(self, title, previous):
        self.graph[title]["previous"] = previous

    def prioritize(self, title):
        for link in self.links(title):
            if link in self.seen:
                continue
            ls = get_all_links(link)
            self.add(link, ls, title)
            if (self.end in ls):
                self.set_previous(self.end, link)
                self.path = self.get_path(self.end)
                print(graph)
                return  
            # mul by -1 to give link with most common items "highest" priority
            priority = (-1 * len(ls.intersection(self.links(self.dest()))))
            print("getting links for: " + link + " priority " +  str(priority))   
            self.seen.add(link)         
            self.pq.put((priority, link))

    def links(self, title):
        return self.graph[title]['links']

    def get_path(self, title):
        previous = self.graph[title]["previous"]
        path = []
        while(previous != '0'):
            path.append(previous)
            title = previous
            previous = self.graph[title]["previous"]
        if (title == self.end):
            self.found = True
        path.reverse()
        self.path = path
        return path

    def dest(self):
        return self.end
    
    