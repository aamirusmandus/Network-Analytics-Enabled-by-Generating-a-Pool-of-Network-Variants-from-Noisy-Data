#!/bin/sh

for i in {1..100}
do
	echo $i

	python louvainCommunityDetection.py outputfoldername/bwrn$i.txt > outputfoldername/bwrn$i.txt.groupsLouvain.txt 


done
