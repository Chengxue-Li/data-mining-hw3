import matplotlib.pyplot as plt
import scipy
import numpy as np
import csv
import time
import scipy.cluster.hierarchy as sch
from PageRank import PageRankGraph
from SimRank import SimRankGraph
from CommonUtil import read_csv_file
from HITS import HITSGraph

hw3_dataset_files = ["hw3dataset/graph_1.txt",
"hw3dataset/graph_2.txt",
"hw3dataset/graph_3.txt",
"hw3dataset/graph_4.txt",
"hw3dataset/graph_5.txt",
"hw3dataset/graph_6.txt"]
hw1_dataset_file = "hw3dataset/data.ntrans_5.tlen_10.nitems_1.5.csv"
iteration_times_plot = 20
iteration_times_total = 10000
damping_factor = 0.15
decay_factor = 0.8
datasets = []
diff_converge = 10 ** -30
# read all files
for file in hw3_dataset_files:
    datasets.append(read_csv_file(file))
write_to_csv = [None] * len(datasets)
# PageRank
print("PageRank")
fig = plt.figure(figsize=(12,7))
fig.subplots_adjust(wspace = 0.4, hspace = 0.4)
for i in range(0, len(datasets)):
    print("Running graph " + str(i + 1) + "...")
    page_rank_graph = PageRankGraph(datasets[i], damping_factor)
    diff_pr = [0] * iteration_times_plot
    first = True
    start = time.time()
    for j in range(0, iteration_times_total):
        d = page_rank_graph.iterate()
        if j < iteration_times_plot:
            diff_pr[j] = d
        if d < diff_converge and first:
            print("iteration times: " + str(j + 1))
            end = time.time()
            print("time: "+str(1000*(end-start))+"msec")
            first = False
        if d < diff_converge and j >= iteration_times_plot:
            print("converge!")
            break
    write_to_csv[i] = [None, [], [], []]
    write_to_csv[i][0] = list(page_rank_graph.pr.keys())
    write_to_csv[i][0].sort(key = lambda k: int(k))
    for key in write_to_csv[i][0]:
        write_to_csv[i][1].append(page_rank_graph.pr[key])
#   sorted_keys = sorted(page_rank_graph.pr.keys(), key = lambda k: (page_rank_graph.pr[k], k))
#    for key in sorted_keys:
#        print(key, page_rank_graph.pr[key])
    plt.subplot(231 + i)
    plt.plot(range(1, iteration_times_plot + 1), diff_pr)
    plt.yscale('log')
    #plt.ylim(10 ** -35, 10 ** -1)
    plt.title("graph " + str(i + 1))
    plt.xlabel('iteration times')
    plt.ylabel('mean variance')
plt.show()

# HITS
print("HITS")
fig = plt.figure(figsize=(12,7))
fig.subplots_adjust(wspace = 0.4, hspace = 0.4)
for i in range(0, len(datasets)):
    print("Running graph " + str(i + 1) + "...")
    hits_graph = HITSGraph(datasets[i])
    diff_auth_hub = [0] * iteration_times_plot
    first = True
    start = time.time()
    for j in range(0, iteration_times_total):
        d = hits_graph.iterate()
        if j < iteration_times_plot:
            diff_auth_hub[j] = d
        if d[0] < diff_converge and d[1] < diff_converge and first:
            print("iteration times: " + str(j + 1))
            end = time.time()
            print("time: " + str(1000*(end-start))+"msec")
            first = False
        if d[0] < diff_converge and d[1] < diff_converge and j >= iteration_times_plot:
            print("converge!")
            break
    for key in write_to_csv[i][0]:
        write_to_csv[i][2].append(hits_graph.auth[key])
        write_to_csv[i][3].append(hits_graph.hub[key])
#    print("auth")
#    sorted_keys = sorted(hits_graph.auth.keys(), key = lambda k: (hits_graph.auth[k], k))
#    for key in sorted_keys:
#        print(key, hits_graph.auth[key])
#    print("hub")
#    sorted_keys = sorted(hits_graph.hub.keys(), key = lambda k: (hits_graph.hub[k], k))
#    for key in sorted_keys:
#        print(key, hits_graph.hub[key])
    plt.subplot(231 + i)
    plt.plot(range(1, iteration_times_plot + 1), diff_auth_hub)
    plt.yscale('log')
    #plt.ylim(10 ** -26, 10 ** -1)
    plt.title("graph " + str(i + 1))
    plt.xlabel('iteration times')
    plt.ylabel('mean variance')
plt.show()

for i in range(0, len(write_to_csv)):
    with open("result/graph_"+str(i+1)+"_hits_pagerank.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["node", "pr", "auth", "hub"])
        for j in range(0, len(write_to_csv[i][0])):
            writer.writerow([write_to_csv[i][0][j], write_to_csv[i][1][j],
            write_to_csv[i][2][j], write_to_csv[i][3][j]])
# SimRank
print("SimRank")
iteration_plot_data = []
heatmap_data = []
for i in range(0, 5):
    print("Running graph " + str(i + 1) + "...")
    sim_rank_graph = SimRankGraph(datasets[i], decay_factor)
    diff_sim = [0] * iteration_times_plot
    first = True
    start=time.time()
    for j in range(0, iteration_times_total):
        d = sim_rank_graph.iterate()
        if j < iteration_times_plot:
            diff_sim[j] = d
        if d < diff_converge and first:
            print("iteration times: " + str(j + 1))
            end = time.time()
            print("time: " + str(1000*(end-start))+"msec")
            first=False
        if d < diff_converge and j >= iteration_times_plot:
            print("converge!")
            break
    iteration_plot_data.append(diff_sim)
    # heatmap
    keys = list(sim_rank_graph.data.keys())
    matrix = [[0]*len(keys) for x in range(0, len(keys))]
    for j in range(0, len(keys)):
        for k in range(0, len(keys)):
            if j == k:
                matrix[j][k] = 1
            else:
                matrix[j][k] = sim_rank_graph.sim[tuple(sorted([keys[j], keys[k]]))]
    d = sch.distance.pdist(matrix)
    L = sch.linkage(d, method = 'complete')
    ind = sch.fcluster(L, 0.5 * d.max(), 'distance')
    keys = [keys[i] for i in list((np.argsort(ind)))]
    for j in range(0, len(keys)):
        for k in range(0, len(keys)):
            if j == k:
                matrix[j][k] = 1
            else:
                matrix[j][k] = sim_rank_graph.sim[tuple(sorted([keys[j], keys[k]]))]
    heatmap_data.append([matrix, keys])
    with open("result/graph_"+str(i+1)+"_simrank.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([""] + keys)
        for j in range(0, len(keys)):
            writer.writerow([keys[j]]+matrix[j]);
# plot iteration convergence
fig = plt.figure(figsize=(13,7))
fig.subplots_adjust(wspace = 0.4, hspace = 0.4)
for i in range(0, 5):
    plt.subplot(231 + i)
    plt.plot(range(1, iteration_times_plot + 1), iteration_plot_data[i])
    plt.yscale('log')
    #plt.ylim(10 ** -17, 1)
    plt.title("graph " + str(i + 1))
    plt.xlabel('iteration times')
    plt.ylabel('mean variance')

# plot sim heatmap
fig = plt.figure(figsize=(13,7))
for i in range(0, 5):
    ax = fig.add_subplot(231 + i)
    plt.title("graph " + str(i + 1))
    a = ax.matshow(heatmap_data[i][0])
    cbar = fig.colorbar(a)
    cbar.set_clim(vmin = 0, vmax = 1)
    cbar.set_ticks(np.linspace(0., 1., num=11, endpoint=True))
    cbar.draw_all()
    ax.xaxis.set_ticks_position('bottom')
    if len(heatmap_data[i][1]) < 10:
        ax.set_xticklabels([""] + heatmap_data[i][1])
        ax.set_yticklabels([""] + heatmap_data[i][1])
    else:
        plt.axis("off")
plt.show()

# hw1 dataset
# bidirected
hw1_dataset = read_csv_file(hw1_dataset_file)
diff_pr = []
page_rank_graph = PageRankGraph(hw1_dataset, damping_factor, connectall = True, bidirected = True)
print("hw1 dataset PageRank")
for i in range(0, iteration_times_total):
    d = page_rank_graph.iterate()
    if i < iteration_times_plot:
        diff_pr.append(d)
    if d < diff_converge and i >= iteration_times_plot:
        print("converge!")
        break
hits_graph = HITSGraph(hw1_dataset, connectall = True, bidirected = True)
diff_auth_hub = []
print("hw1 dataset HITS")
for i in range(0, iteration_times_total):
    d = hits_graph.iterate()
    if i < iteration_times_plot:
        diff_auth_hub.append(d)
    if d[0] < diff_converge and d[1] < diff_converge and i >= iteration_times_plot:
        print("converge!")
        break

fig = plt.figure(figsize=(8,3.5))
fig.subplots_adjust(wspace = 0.4, hspace = 0.4)
# plot PageRank
plt.subplot(121)
plt.plot(range(1, iteration_times_plot + 1), diff_pr)
plt.yscale('log')
plt.title("PageRank")
plt.xlabel('iteration times')
plt.ylabel('mean variance')
# plor HITS
plt.subplot(122)
plt.plot(range(1, iteration_times_plot + 1), diff_auth_hub)
plt.yscale('log')
plt.title("HITS")
plt.xlabel('iteration times')
plt.ylabel('mean variance')
plt.show()
keys = list(page_rank_graph.data.keys())
keys.sort(key = lambda k: int(k))
with open("result/hw1dataset_hits_pagerank_bidirected.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["node", "pr", "auth", "hub"])
    for key in keys:
        writer.writerow([key, page_rank_graph.pr[key], hits_graph.auth[key], hits_graph.hub[key]])
# directed
hw1_dataset = read_csv_file(hw1_dataset_file)
diff_pr = []
page_rank_graph = PageRankGraph(hw1_dataset, damping_factor, connectall = True, bidirected = False)
print("hw1 dataset PageRank")
for i in range(0, iteration_times_total):
    d = page_rank_graph.iterate()
    if i < iteration_times_plot:
        diff_pr.append(d)
    if d < diff_converge and i >= iteration_times_plot:
        print("converge!")
        break
hits_graph = HITSGraph(hw1_dataset, connectall = True, bidirected = False)
diff_auth_hub = []
print("hw1 dataset HITS")
for i in range(0, iteration_times_total):
    d = hits_graph.iterate()
    if i < iteration_times_plot:
        diff_auth_hub.append(d)
    if d[0] < diff_converge and d[1] < diff_converge and i >= iteration_times_plot:
        print("converge!")
        break

fig = plt.figure(figsize=(8,3.5))
fig.subplots_adjust(wspace = 0.4, hspace = 0.4)
# plot PageRank
plt.subplot(121)
plt.plot(range(1, iteration_times_plot + 1), diff_pr)
plt.yscale('log')
plt.title("PageRank")
plt.xlabel('iteration times')
plt.ylabel('mean variance')
# plor HITS
plt.subplot(122)
plt.plot(range(1, iteration_times_plot + 1), diff_auth_hub)
plt.yscale('log')
plt.title("HITS")
plt.xlabel('iteration times')
plt.ylabel('mean variance')
plt.show()
keys = list(page_rank_graph.data.keys())
keys.sort(key = lambda k: int(k))
with open("result/hw1dataset_hits_pagerank_directed.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["node", "pr", "auth", "hub"])
    for key in keys:
        writer.writerow([key, page_rank_graph.pr[key], hits_graph.auth[key], hits_graph.hub[key]])
