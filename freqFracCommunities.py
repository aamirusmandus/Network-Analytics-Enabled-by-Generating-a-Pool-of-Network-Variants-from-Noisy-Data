import csv
import random
import math
import sys
import freqFrac_helperFunctions as ff
import time
nodesOriginalCommunitiesFile = sys.argv[1] #just to get the list of nodes in the community 
pathToGeneratedGroupsFiles = sys.argv[2] #list of possible community structures for the given network
numOfFiles = int(sys.argv[3]) #number of files present in argv[2]
nameOfFiles = sys.argv[4] #name of files present in argv[2] (i.e name of file = caviar, 
						  #the code will then attempt to open caviar1.txt.groupsLouvain.txt, caviar2.txt.groupsLouvain.txt and so on

#this will store all nodes in originalNetworkNodes
originalNetworkNodes = ff.readOriginalCommunityNodes(nodesOriginalCommunitiesFile)

#print(originalNetworkNodes)


#key = community, value = freq
networksGroupsDict = {}
#store all communities of all generated networks in a dictionary
#key: networkID, value: detected communities in network

for i in range(numOfFiles):
	filePath = pathToGeneratedGroupsFiles + nameOfFiles + str(i+1) + '.txt.groupsLouvain.txt'
	
	#networkGroups now contain groups(each line in file) in file and nodes that were missing in file but were there in nodes
	networkGroups = ff.readNetworkGroups(filePath, originalNetworkNodes)

	#store freq of groups in dict networkGroupsDict
	for group in networkGroups:
		group.sort()
		if tuple(group) in networksGroupsDict:
			networksGroupsDict[tuple(group)] += 1
		else:	
			networksGroupsDict[tuple(group)] = 1


#print(networksGroupsDict)	
start_time = time.time()
freqComm, freqScore = ff.freqFracBasedPredictions(networksGroupsDict, originalNetworkNodes, 'freq')	
freqComm.sort(key=len, reverse=True)



  
print()
print('frequency based communities:')
freqname = sys.argv[5] + "freq.txt"
mrfile = open(freqname, "w+")
finalComm = []
for comm in freqComm:
	print(comm)
	if isinstance(comm,str):
		mrfile.write(comm)
		mrfile.write('\n')
	else:
		commstr = ""
		for kli in range(len(comm)):
			if kli != len(comm)-1:
				commstr+=comm[kli]
				commstr+= " "
			else:
				commstr+=comm[kli]
				commstr+="\n"
		mrfile.write(commstr)

end_time = time.time()
print("total time ", end_time - start_time)
mrfile.close()
freqscorename = sys.argv[5] + "freqscore.txt"
mrfile = open(freqscorename, "w+")
mrfile.write(freqScore)
mrfile.close()

fracComm, fracScore = ff.freqFracBasedPredictions(networksGroupsDict, originalNetworkNodes, 'frac')	
fracComm.sort(key=len, reverse=True)

print()
print('fraction based communities:')
fracname = sys.argv[5] + "frac.txt"
mrfile = open(fracname, "w+")
for comm in fracComm:
	print(comm)
	if isinstance(comm,str):
		mrfile.write(comm)
		mrfile.write('\n')
	else:
		commstr = ""
		for kli in range(len(comm)):
			if kli != len(comm)-1:
				commstr+=comm[kli]
				commstr+= " "
			else:
				commstr+=comm[kli]
				commstr+="\n"
		mrfile.write(commstr)

mrfile.close()
fracscorename = sys.argv[5] + "fracscore.txt"
mrfile = open(fracscorename, "w+")
mrfile.write(fracScore)
mrfile.close()
end_time = time.time()
print("total time ", end_time - start_time)


