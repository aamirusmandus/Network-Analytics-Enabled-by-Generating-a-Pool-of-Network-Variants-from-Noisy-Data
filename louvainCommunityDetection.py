import sys
from community import community_louvain
import networkx as nx


G = nx.Graph()
filename = sys.argv[1]
    
with open(filename) as f:
	for line in f:
		values = line.split(" ")
		source = values[0]
		target = values[1]

		weighty = float(values[2].strip("\n"))
		if G.has_edge(target, source):
			G[target][source]["weight"] += weighty
		else:	
			G.add_edge(source,target, weight=weighty)

partitions = community_louvain.best_partition(G, weight='weight')

for comm in set(partitions.values()):
	for node in partitions.keys():
		if partitions[node] == comm:
			print(node, end=" ")

	print()     

			
