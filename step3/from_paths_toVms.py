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
nPv=10

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


def list_of_vms(paths):
    #nodes that have been already placed into a Vm
    nodes=[] 
    
    while paths:
        l=[]
        count=0
        while count<nPv:    
            flag=1
            paths= [x for x in paths if x != []]
            if paths==[]:
                break
            new=paths[0].pop(0)
            #print paths
            for lists in nodes:
                if new in lists:
                    flag=0
            if new in l:
                flag=0
            if flag==1:    
                l.append(new)
                count+=1
        nodes.append(l)
    print "##########################################################"
    print nodes
    return nodes

if __name__=='__main__':
    #input1 : file with paths in list of lists
    #input2 : number of Vms (=> list of Vms with credentials)
    
    start_time=time.time()
    paths=readmyfile(sys.argv[1])
    V=int(sys.argv[2])
    print paths 
    G=nx.Graph()
    G=from_paths_to_graph(G,paths)
    #print G.nodes() 
    if ( (len(G.nodes())/nPv+1)>V ):
        print "#####You have to define a different number of nodes/Vm because you have not enouph Vms.You need %s more Vms"%(len(G.nodes())/nPv+1-V) 
                
    else:
        Vms=list_of_vms(paths)
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
