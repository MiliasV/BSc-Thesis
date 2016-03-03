#/usr/bin/python  
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
import metis
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


def from_paths_to_graph(paths):
    G=nx.Graph()
    for path in paths:
        for i in range(len(path)-1):
            G.add_edge(path[i],path[i+1])
    return G

def list_of_vms(G,parts):
    l=[]
    vm={}
    count=0
    for n in G.nodes():
        vm[n]=parts[count]
        count+=1
    for e in G.edges():
        l.append((e[0],e[1],vm[e[0]],vm[e[1]]))

    #print vm
    #print l
    return l
    #for e in G.edges():
        

if __name__=='__main__':
    #input1 : file with paths in list of lists
    #input2 : number of Vms (=> list of Vms with credentials)
    
    start_time=time.time()
    paths=readmyfile(sys.argv[1])
    V=int(sys.argv[2])
    #print paths 
    G=nx.Graph()
    G=from_paths_to_graph(paths)
    
    #if ( (len(G.nodes())/nPv+1)>V ):
    #   print "#####You have to define a different number of nodes/Vm because you have not enouph Vms.You need %s more Vms"%(len(G.nodes())/nPv+1-V) 
    
    (edgecuts,parts)=metis.part_graph(G,V)
    #print edgecuts
    #print parts
    #print len(G.nodes())
    
    l = list_of_vms(G,parts)
    print l
    
    #Graphic representation
    count=0
    colors = ['red','blue','green','yellow','antiquewhite4','brown','cyan','violet','firebrick3','pink','black','purple']
    for n in G.nodes():
        G.node[n]['color']=colors[parts[count]]
        count+=1
     
    nx.write_dot(G,'200graph.dot')
    os.system("dot -Tpng 200graph.dot -o 200graph.png")
    #os.system("open graph.ps")

    #print time.time()-start_time
