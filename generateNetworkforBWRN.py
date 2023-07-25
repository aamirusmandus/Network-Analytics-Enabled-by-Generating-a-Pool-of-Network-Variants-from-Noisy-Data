import csv
import operator
import random
import math
import sys


networkEdgesFile = 'network.dat'

			
f = open(networkEdgesFile,"r")
lines = f.readlines()
communityCnt = 0 
mrfile = open("network.txt", "w+")
for l in lines:
	if "Nodes" not in l:
		nodesInCommunity = l.split('\t')
		mrfile.write(nodesInCommunity[0] + " " + nodesInCommunity[1] + " " + str(int(float((nodesInCommunity[2].rstrip()))*10)) + "\n")
mrfile.close()