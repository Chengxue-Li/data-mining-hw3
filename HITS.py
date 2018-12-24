import random
from itertools import combinations
from CommonUtil import Node, normalize, diff
class HITSGraph():
    def __init__(self, rows, connectall = False, bidirected = True):
        data = dict()
        auth = dict()
        hub = dict()
        for i in range(0, len(rows)):
            for j in range(0, len(rows[i])):
                if not rows[i][j] in data:
                    data[rows[i][j]] = Node()
                    auth[rows[i][j]] = random.random()
                    hub[rows[i][j]] = random.random()
            if connectall:
                pairs = list(combinations(rows[i], 2))
                for pair in pairs:
                    if bidirected:
                        data[pair[0]].add_parent(pair[1])
                        data[pair[1]].add_children(pair[0])
                        data[pair[0]].add_children(pair[1])
                        data[pair[1]].add_parent(pair[0])
                    else:
                        data[pair[0]].add_parent(pair[1])
                        data[pair[1]].add_children(pair[0])
            else:
                data[rows[i][0]].add_children(rows[i][1])
                data[rows[i][1]].add_parent(rows[i][0])
        normalize(auth)
        normalize(hub)
        self.data = data
        self.auth = auth
        self.hub = hub
    def iterate(self):
        new_auth = dict()
        new_hub = dict()
        for key in self.data:
            new_auth[key] = 0
            new_hub[key] = 0
            for parent in self.data[key].parents:
                new_auth[key] += self.hub[parent]
            for child in self.data[key].children:
                new_hub[key] += self.auth[child]
        normalize(new_auth)
        normalize(new_hub)
        diff_auth = diff(new_auth, self.auth)
        diff_hub = diff(new_hub, self.hub)
        self.auth = new_auth
        self.hub = new_hub
        return diff_auth, diff_hub
#file_name = "hw3dataset/graph_4.txt"
#iteration_times = 1000
#rows = read_csv_file(file_name)
#graph = HITSGraph(rows)
#for i in range(0, iteration_times):
#    graph.iterate()
#sorted_keys = sorted(graph.hub.keys(), key = lambda k: (graph.hub[k], k))
#for key in sorted_keys:
#    print(key, graph.hub[key])
