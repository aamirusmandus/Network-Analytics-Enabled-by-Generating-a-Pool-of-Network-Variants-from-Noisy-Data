import csv
import operator
import random
import math
import sys
import numpy as np
import ast

import collections
networkCommunityFile = 'community.dat'


communities = collections.defaultdict(list)			
f = open(networkCommunityFile,"r")
lines = f.readlines()
communityCnt = 0 
for l in lines:

	nodesInCommunity = l.split('\t')
	nodesInCommunity[1].strip()
	# print(nodesInCommunity[1])
	communities[nodesInCommunity[1]].append(nodesInCommunity[0])


mrfile = open("groundTruth.txt", "w+")
for commune in communities.values():
    for iaz in range(len(commune)):
        if(iaz<(len(commune)-1)):
            mrfile.write(str(commune[iaz]) + " ")
        else:
            mrfile.write(str(commune[iaz]))
    mrfile.write("\n")
mrfile.close()
