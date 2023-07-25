import numpy as np
from sklearn import metrics
import sys


# change these to be the 2 community files you want to compare
# expectation is the file has 1 community per line and spaces separating the nodes in each community


file2 = np.loadtxt("frac.txt", dtype=str, delimiter="\n")
file = np.loadtxt("groundTruth.txt", dtype=str, delimiter="\n")

readComms = []
for j in range(len(file2)):
    readComms.append([])
    for component in file2[j].split(" "):
        if(len(component)>0):
            readComms[j].append(component)

predNodes = set()
for comm in readComms:
    for c in comm:
        predNodes.add(c)

comms = []
for j in range(len(file)):
    comms.append([])
    for component in file[j].split(" "):
        if(len(component)>0):
            comms[j].append(component)

actualNodes = set()
for comm in comms:
    for c in comm:
        actualNodes.add(c)


missingNodes = list((set(actualNodes)).difference(set(predNodes)))
for nodes in missingNodes:
    new_comm = []
    new_comm.append(nodes)
    readComms.append(new_comm)

labels_true = []
labels_pred = []

for p in range(len(comms)):
    for o in range(len(comms[p])):
        labels_true.append(p)
        
for p in range(len(readComms)):
    for o in range(len(readComms[p])):
        labels_pred.append(p)
    

    

print(round(metrics.normalized_mutual_info_score(labels_true, labels_pred),3))