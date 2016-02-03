#!/usr/bin/python  
import time
import re
import os
import sys
import json
import numpy as np
import itertools
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from pprint import pprint

#Author: Vasileios Milias

#nodes_per_Vm
nPv=5

def readmyfile(myfile):
    with open(myfile,"r") as f:
        lst = json.load(f)
    return lst

def numberOfNodes(eList):
    G=nx.DiGraph(eList)
    return len(G.nodes())

    

def reveList(eList):
    rev=[]
    for i in range(len(eList)):
        cur=reversed(eList[i])
        cur=tuple(cur)
        rev.append(cur)
    return rev    


def from_paths_to_graph(G,paths):
    Gp=nx.Graph()
    for path in paths:
        for i in range(len(path)-1):
            Gp.add_edge(path[i],path[i+1])
    return Gp


def list_of_vms(G,paths):
    #nodes that have been already placed into a Vm
    vms=[] 
    #as_to_vm_dict
    aTv={}
    #the number of vm that we are
    vm=0
    vm+=1
    l=[]
    count=0
    #no point of this
    flag=1
    for path in paths:
        if len(path)>=2 and path[0] not in aTv and path[1] not in aTv:
            l.append((path[0],path[1],0))
            aTv[path[0]]=vm
            aTv[path[1]]=vm
            count+=2
            path.pop(0)
            if len(path)>=2: 
                for node in path:
                    if count>=nPv:
                        break
                    elif path[1] not in aTv:
                        l.append((path[0],path[1],0))
                        aTv[path[1]]=vm
                        count+=1
    """
            paths= [x for x in paths if x != []]
            if paths==[]:
                break
            new=paths[0].pop(0)
            #print paths
            for lists in vms:
                if new in lists:
                    flag=0
            if new in l:
                flag=0
            if flag==1:    
                l.append(new)
                count+=1
        vms.append(l)
    """
    print "##########################################################"
    print l
    print "##########################################################"
    print paths
    return l

if __name__=='__main__':
    #input1 : file with paths in list of lists
    #input2 : number of Vms (=> list of Vms with credentials)
    
    start_time=time.time()
    paths=readmyfile(sys.argv[1])
    V=int(sys.argv[2])
    print paths 
    G=nx.Graph()
    G=from_paths_to_graph(G,paths)
    #for edge in G.edges():
        #l[k]=edge
    if ( (len(G.nodes())/nPv+1)>V ):
        print "#####You have to define a different number of nodes/Vm because you have not enouph Vms.You need %s more Vms"%(len(G.nodes())/nPv+1-V) 
                
    else:
        Vms=list_of_vms(G,paths)
    #data to edge list 
    #eList = convertToEdgeList(intL)
    
    #pos=nx.circular_layout(Gtree)
    #nx.draw(Gtree,pos)
    #nx.draw_networkx_labels(Gtree,pos)
    #plt.show()
    """
    debug
    print "######################################"
    print Gtree.edges(data=True)
    print "#####################################"
    print  Gtree.edges()
    print "#####################################"
    print Gtree.nodes()
    print nx.is_directed_acyclic_graph(Gtree) 
    print time.time()-start_time
    """
