from .get_links import get_all_links
from queue import PriorityQueue

class Graph():
    def __init__(self, source, destination):
        self.graph = {}
        self.start = source
        self.end = destination
        self.pq = PriorityQueue()
        self.found = False
        self.path = []
        self.seen = set()

    def __str__(self): 
        st = 'PATH: {0} \n'.format(str(self.path))
        for title in self.graph.keys():
            st += 'Title: ' + title + '\nprev: ' + self.graph[title]["previous"]  +  '\n' + str(len(self.links(title))) + '\n'
        st += "PQ approx length " + str(self.pq.qsize()) + "\n"
        st += "Checked this many pages: " + str(len(self.seen)) + "\n"
        return st

    def add(self, title, links, previous):
        self.graph[title] = {
            'links' : links, 
            'previous' : previous, 
            }

    def set_previous(self, title, previous):
        self.graph[title]["previous"] = previous
        print(self.graph[title])

    def prioritize(self, title):
        try:
            for link in self.links(title):
                print(title)
                if link in self.seen:
                    continue
                ls = get_all_links(link)
                self.add(link, ls, title)
                if (self.end in ls):
                    self.set_previous(self.end, link)
                    self.make_path(self.end)
                    print("FOUND!!!")
                    print(self.found)
                    print(self.end, link)
                    print(self.path)
                    return  
                # mul by -1 to give link with most common items "highest" priority
                priority = (-1 * len(ls.intersection(self.links(self.end))))
                print("getting links for: " + link + " priority " +  str(priority))   
                self.seen.add(link)         
                self.pq.put((priority, link))
        except Exception as e:
            print(e)
            print(self)
            return e

    def links(self, title):
        return self.graph[title]['links']

    def make_path(self, title):
        try:
            t = title 
            previous = self.graph[t]["previous"]
            path = [t]
            while(previous != '0'):
                path.append(previous)
                print(path)
                t = previous
                previous = self.graph[t]["previous"]
            if (title == self.end):
                self.found = True
            print("reversed " , path.reverse())
            self.path = path
            print(self.path)
        except Exception as e:
            print(e)
            print(path)
            return e
    
    def get_path(self, title):
        self.make_path(title)
        return self.path

    def dest(self):
        return self.end

    def done(self, duration):
        print(self.graph)
        print("Duration: ", duration)
        return self.graph.path
    