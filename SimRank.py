import csv
import random
from itertools import combinations
from CommonUtil import read_csv_file, diff, Node
class SimRankGraph():
    def __init__(self, rows, c):
        data = dict()
        for i in range(0, len(rows)):
            for j in range(0, len(rows[i])):
                if not rows[i][j] in data:
                    data[rows[i][j]] = Node()
            data[rows[i][0]].add_children(rows[i][1])
            data[rows[i][1]].add_parent(rows[i][0])
        keys = data.keys()
        pairs = list(combinations(keys, 2))
        sim = dict()
        for pair in pairs:
            sim[tuple(sorted(pair))] = random.random()
        self.data = data
        self.sim = sim
        self.c = c
    def iterate(self):
        new_sim = dict()
        for pair in self.sim:
            a_parents = self.data[pair[0]].parents
            b_parents = self.data[pair[1]].parents
            if len(a_parents) * len(b_parents) == 0:
                new_sim[pair] = 0
                continue
            sum = 0
            for a_parent in a_parents:
                for b_parent in b_parents:
                    if a_parent == b_parent:
                        sum += 1
                    else:
                        sum += self.sim[tuple(sorted([a_parent, b_parent]))]
            new_sim[pair] = self.c / (len(a_parents) * len(b_parents)) * sum
        diff_sim = diff(new_sim, self.sim)
        self.sim = new_sim
        return diff_sim
#file_name = "hw3dataset/graph_4.txt"
#decay_factor = 0.8
#iteration_times = 10
#rows = read_csv_file(file_name)
#graph = SimRankGraph(rows, decay_factor)
#for i in range(0, iteration_times):
#    graph.iterate()
#sorted_keys = sorted(graph.sim.keys(), key = lambda k: (graph.sim[k], k))
#for key in sorted_keys:
#    print(key, graph.sim[key])
