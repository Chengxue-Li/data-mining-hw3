import csv
import random
from itertools import combinations
from CommonUtil import Node, normalize, diff
class PageRankGraph():
    def __init__(self, rows, df, connectall = False, bidirected = False):
        data = dict()
        pr = dict()
        for i in range(0, len(rows)):
            for j in range(0, len(rows[i])):
                if not rows[i][j] in data:
                    data[rows[i][j]] = Node()
                    pr[rows[i][j]] = random.random()
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
                if bidirected:
                    data[rows[i][0]].add_children(rows[i][1])
                    data[rows[i][1]].add_parent(rows[i][0])
                    data[rows[i][1]].add_children(rows[i][0])
                    data[rows[i][0]].add_parent(rows[i][1])
                else:
                    data[rows[i][0]].add_children(rows[i][1])
                    data[rows[i][1]].add_parent(rows[i][0])
        normalize(pr)
        self.data = data
        self.pr = pr
        self.df = df
        self.n = len(data)
    def iterate(self):
        new_pr = dict()
        for key in self.data:
            sum = 0
            for parent in self.data[key].parents:
                sum += self.pr[parent] / len(self.data[parent].children)
            new_pr[key] = self.df / self.n + (1 - self.df) * sum
        normalize(new_pr)
        diff_pr = diff(new_pr, self.pr)
        self.pr = new_pr
        return diff_pr
#file_name = "hw3dataset/graph_4.txt"
#iteration_times = 1000
#damping_factor = 0.15
#rows = read_csv_file(file_name)
#graph = PageRankGraph(rows, damping_factor)
#for i in range(0, iteration_times):
#    graph.iterate()
#sorted_keys = sorted(graph.pr.keys(), key = lambda k: (graph.pr[k], k))
#for key in sorted_keys:
#    print(key, graph.pr[key])
