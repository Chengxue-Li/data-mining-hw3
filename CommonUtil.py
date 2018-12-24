import csv
import random
def read_csv_file(file_name):
    with open(file_name) as file:
        rows = list(csv.reader(file))
    return rows
def normalize(d):
    total = 0
    for key in d:
        total += d[key]
    for key in d:
        d[key] /= total
def diff(d1, d2):
    result = 0
    for key in d1:
        result += (d1[key] - d2[key]) **2
    result /= len(d1)
    return result
class Node():
    def __init__(self):
        self.parents = list()
        self.children = list()
    def add_children(self, child):
        if not child in self.children:
            self.children.append(child)
    def add_parent(self, parent):
        if not parent in self.parents:
            self.parents.append(parent)
