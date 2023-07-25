import csv
import random
import math
from itertools import combinations

#read nodes in original network	
def readOriginalCommunityNodes(nodesOriginalCommunities):

	f = open(nodesOriginalCommunities,"r")
	lines = f.readlines()

	#store all the nodes present in the original network structure			
	nodes = []
	for l in lines:
		nodesInGroup = l.split(' ')

		for node in nodesInGroup:
			if node != '\n':
				nodes.append(node.rstrip())

	f.close()

	return nodes



#read groups in the network
def readNetworkGroups(networkGroupsFile, listOfNodesFile):
		
	nodes = listOfNodesFile


	f = open(networkGroupsFile,"r")
	lines = f.readlines()

	w, h = 0, len(lines);
	networkGroups = [[0 for x in range(w)] for y in range(h)] # [[], [], []] if lines = 3, [[], []] if lines = 2
	
	#fill all nodes in a line in one []
	groupCnt = 0
	for l in lines:
		nodesInGroup = l.split(' ')
		for n in nodesInGroup:
			if n != '\n':
				networkGroups[groupCnt].append(n.rstrip())
		
		groupCnt += 1
	
	f.close()
	#-------------------------------------------------

	#count and add missing nodes from the networkGroup in current file
	missingNodesCnt = 0	
	missingNodes = []
	found = -1
	for node in nodes:
		found = -1
		for group in networkGroups:
			if node in group:
				found = 1

		if found == -1:		
			missingNodesCnt += 1
			missingNodes.append(node)

	#-------------------------------------------------

	#store groups present in file as it is and missing nodes as separate groups
	w, h = 0, len(lines)+missingNodesCnt;
	finalNetworkGroups = [[0 for x in range(w)] for y in range(h)]
	gCnt = 0
	for group in networkGroups:	
		for node in group:
			finalNetworkGroups[gCnt].append(node)

		gCnt += 1	

	nodeCnt = 0	
	for i in range(missingNodesCnt):
		finalNetworkGroups[gCnt].append(missingNodes[nodeCnt])		
		gCnt += 1
		nodeCnt += 1
	
	return finalNetworkGroups



def computeStructurePenalty(predictedCommunityStructure, networksGroupsDict, nodes, freqFrac, changedNodes):

	#print('---', predictedCommunityStructure)
	#print()
	# print("predictedCommunityStructure: ",predictedCommunityStructure)
	# print("changedNodes: ", changedNodes)
	penaltyScores = []	
	for n in nodes:
		if n not in changedNodes:
			# print("not in changedNodes", n)
			continue

		penalty = 0
		for predComm in predictedCommunityStructure:
			if predComm in nodes:
				if n == predComm:
					comm1 = [predComm]
			else:
				if n in predComm:
					comm1 = predComm
		# print(n, comm1)

		for comm, weight in networksGroupsDict.items():
			if comm in nodes:
				if n in comm:
					comm2 = [comm]
			elif n in comm:
				comm2 = comm
			else:
				continue
			#print(n, comm2)
			setUnion = set(comm1).union(set(comm2))
			setIntrs = set(comm1).intersection(set(comm2))
			if freqFrac == 'freq':
				penalty += (len(setUnion) - len(setIntrs)) * weight
			elif freqFrac == 'frac':
				penalty += (1 - (len(setIntrs)/len(setUnion))) * weight
				
			#print(n, set(comm1), set(comm2), len(setUnion), len(setIntrs),  weight, (len(setUnion) - len(setIntrs)) * weight, penalty)
		penaltyScores.append(penalty)

	#print()			
	return penaltyScores


def findPenaltyForEachNode(networksGroupsDict, nodes, freqFrac):
	#set every node in its own community
	predictedCommunities = []
	changedNodes = []
	nodePenalty = {}
	for n in nodes:
		predictedCommunities.append(n)
		changedNodes.append(n)
	
	# print("predictedCommunities: ",predictedCommunities)
	# print("changedNodes: ", changedNodes)

	penaltyScores = computeStructurePenalty(predictedCommunities, networksGroupsDict, nodes, freqFrac, changedNodes)		
	
	return penaltyScores




def freqFracBasedPredictions(networksGroupsDict, nodes, freqFrac):

	# print("starting freqFrac Function")
	penaltyScores = findPenaltyForEachNode(networksGroupsDict, nodes, freqFrac)
	# print("Penalty score: ",penaltyScores)

	cnt = 0			
	bestPenalty = 0
	for n in nodes:
		#print(n, penaltyScores[cnt])
		bestPenalty += penaltyScores[cnt]		
		cnt += 1

	# print(bestPenalty)

	predictedCommunities = []			
	for n in nodes:
		predictedCommunities.append(n)


	changing = 1
	cnt = 0
	bestPenaltyScores = penaltyScores
	while changing == 1:
		# print("while started")
		# print("Predicted Communities ")
		# print(predictedCommunities)
		# can delete visited communities 
		#  
		changing = 0	
		best_c1 = ''
		best_c2 = ''
		bestTempScores = []
		visitedCommunities = []
		for c1 in predictedCommunities:
			visitedCommunities.append(c1)
			for c2 in predictedCommunities:
				# print("C1: ", c1, "C2: ", c2)
				tempPredictedCommunities = predictedCommunities[:]
				tempPredictedCommunities.remove(c1)
				if c2 not in visitedCommunities:
					tempPredictedCommunities.remove(c2)
					tempComm = []
					if c1 not in nodes:
						for c1_node in c1:
							tempComm.append(c1_node)
					else:
						tempComm.append(c1)
			
					if c2 not in nodes:
						for c2_node in c2:
							tempComm.append(c2_node)
					else:
						tempComm.append(c2)

					tempPredictedCommunities.append(tempComm)
					#print(tempPredictedCommunities)
					newPenaltyScores = computeStructurePenalty(tempPredictedCommunities, networksGroupsDict, nodes, freqFrac, tempComm)
					#print(tempComm, newPenaltyScores, bestPenaltyScores, tempPredictedCommunities)
					penalty = 0
					for entry in newPenaltyScores:
						penalty += entry 
						
					pos1 = 0
					pos2 = 0
					for n in nodes:
						if n not in tempComm:
							penalty += bestPenaltyScores[pos1]
						pos1 += 1
					# print("Temp Comm: ", tempComm)
					# print("New Penalty Score: ", newPenaltyScores)
					# print("Penalty: ", penalty)
					# print("Best Penalty: ", bestPenalty)

					if penalty < bestPenalty:
						bestTempScores = newPenaltyScores
						best_c1 = c1
						best_c2 = c2
						bestTempComm = tempComm
						bestPenalty = penalty

						changing = 1	
		

		if changing == 1:
			#print(best_c1, best_c2, bestPenalty)					
			predictedCommunities.remove(best_c1)
			predictedCommunities.remove(best_c2)

			predictedCommunities.append(bestTempComm)
			#print(predictedCommunities)
			pos1 = 0
			pos2 = 0
			for n in nodes:
				if n in bestTempComm:
					bestPenaltyScores[pos1] = bestTempScores[pos2]
					pos2 += 1
				pos1 += 1

			#print(bestPenaltyScores)


	#print(freqFrac, 'communities:', predictedCommunities)			
	
	return predictedCommunities, str(bestPenalty)




