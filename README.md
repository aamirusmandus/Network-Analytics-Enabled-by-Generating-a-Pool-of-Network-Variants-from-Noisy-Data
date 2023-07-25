# Network-Analytics-Enabled-by-Generating-a-Pool-of-Network-Variants-from-Noisy-Data

1) LFR Benchmark Network Generation:
   
   Please use the Git repo of the authors of the LFR papers: https://github.com/eXascaleInfolab/LFR-Benchmark_UndirWeightOvp to generate LFR Benchmark Networks with the desired properties.
   
   We used: "./lfrbench_udwov -N 27 -k 4.52 -maxk 13 -muw 0.29 -mut 0.23 -minc 2 -maxc 3 -C 0.52" for the Caviar network and "./lfrbench_udwov -N 104 -k 2.88 -maxk 30 -muw 0.145 -mut 0.173 -minc 2 -maxc 3 -C 0.118" for the Sicilian network.

   
   If your desired network does not have ground truth communities available to compute muw, mut, minc, and maxc, we suggest running community detection like Louvain on the network 100 times and using the most common result to compute these parameters.



2) Prepare for BWRN:
   
   Run generateNetworkforBWRN.py to convert the network file into the format readable by the BWRN. Please edit the variable networkEdgesFile to point to the network.dat file output by the LFR code.

   BWRN will take a community structure file as input and attempt to keep this structure while shaking. If you want to use the groundtruth provided by the LFR generator then run generateCommunityforBWRN.py to convert the community file into the format readable by the BWRN code. Please edit the variable networkCommunityFile to point to the community.dat file output by the LFR code.

   However since using the ground truth would make our experiment trivial, we use the most common output of Louvain community detection run 100 times on the network.txt file produced by generateNetworkforBWRN.py.



3) Run BWRN:
   
   "python3 networkGeneratorSBM.py auto BWRN 0.875 noRandomize network.txt community.txt outputfoldername/bwrn 1000"
   
   This will run the BWRN code to generate 1000 shaken versions of the original edgelist.

   Please see the previous paper https://www.sciencedirect.com/science/article/pii/S0020025521010884 (A network generator for covert network structures) for more details about BWRN.


   The first argument specifies using auto mode instead of manual
   
   The second argument specifies using the BWRN mode instead of WRG.
   
   The third argument specifies p of 0.875
   
   The fourth argument specifies not to randomize the names of nodes
   
   The fifth argument specifies the edgelist file created in step 3
   
   The sixth argument specifies the community file created in step 3.
   
   The seventh argument specifies the folder to output into and the naming of the files e.g. bwrn1.txt, bwrn2.txt, etc.
   
   The eigth argument specifies the number of files to produce.



4) Run Louvain:
   
   Use louvainCommunityDetection.py to run the Louvain community detection algorithm on each of the 1000 bwrn produced weighted edgelists and output the results in the format readable by our code with filenames bwrn1.txt.groupsLouvain.txt, bwrn2.txt.groupsLouvain.txt, etc.
   
   You can edit runLouvain.sh to do this automatically.

   
   The first argument specifies the file names of the bwrn files
   
   The second argument specifies the output file names



5) Find the set of communities with the lowest fraction or frequency-based Shannon entropy:

   "python3 freqFracCommunities.py outputfoldername/bwrn1.txt.groupsLouvain.txt outputfoldername/ 1000 bwrn outputfoldername/"
   
   This will run the entropy minimization code and produce freq.txt, freqscore.txt, frac.txt, and fracscore.txt in the given outputfoldername.
   
   freq.txt and frac.txt contain the set of communities with the lowest frequency and fraction-based Shannon entropy.
   
   freqscore.txt and fracscore.txt contain the total Shannon entropy of the final respective community structures.
   
   
   The first argument points to a single community structure file which is only used to get the list of nodes in the network.
   
   The second argument specifies the folder to search for bwrn louvain outputs.
   
   The third argument specifies the number of bwrn louvain outputs.
   
   The fourth argument specifies the name of the bwrn louvain files before ".txt.groupsLouvain.txt"

   The fifth argument specifies the folder to place the output files in.



6) Repeat to further minmize: 

   Repeat steps 3-5 replacing the argument "community.txt" to BWRN with either the frac.txt or freq.txt depending on which heuristic you want to minmize.

   Check if the new score in fracscore.txt or freqscore.txt is lower than it was after the first iteration. If so, repeat steps 3-5 again. Continue until the entropy stops decreasing for at least 2 rounds in a row.


7) Compute NMI score:

   You can use communityComparison.py to compute the NMI score between the groundtruth community structure and an output community structure. Edit the file and file2 variables to point to your desired community structure files e.g. groundTruth.txt and frac.txt. The order does not matter.

If you have any questions please contact me (Aamir Mandviwalla) at mandva@rpi.edu
