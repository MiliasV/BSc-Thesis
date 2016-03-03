# Project-D
Diplomatiki


STEPS

(1)
tree_of_attack.py

This script takes as input a dataset that contains as relatonships with the form:

from As | to As | {0,1}   -> 0 for peering relationships, 1 for p2c realtionships (CAIDA dataset)

From this dataset it creates a valid tree of attack, depending on the victim and the malicious hosts 
we have define inside the script.

It returns the paths of the tree.

(2)
from_paths_to_vms.py

This script takes as input: file with the paths (list of lists) 
                            number of Vms (V)
  
  It makes a partition of the graph in V parts and it writes to a file a list 
  that contains edges and in which part its node of the edge is. 
  For example : [(123,256,1,4),..] means that node 123 is in Vm1, node 256 is in Vm4, and there is an 
  edge between them
  
  NEXT STEPS
  
  -Make a script that finds the match between Ips and Ases from those that are included in the dataset of 
  the Ddos attack of 2007 (August) (CAIDA dataset) so that we can build this specific tree of attack.
  For this goal we used a file that has the ips-asn mapping that existed in 01 August 2007  (from Delft university)

  -Make a script that takes as input a list of Vms and builds the overall topology by running a mininet script
  with the right arguments in each of the Vms.
  
  
  
  
