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
nPv=6

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


def list_of_vms(G,paths,V):
    vms=[]
    #as_to_vm_dict
    aTv={}
    l=[]
    #no point of this
    flag=1
    for vm in range(V):
        paths= [x for x in paths if x != [] and len(x)>1]
        l=[]
        for path in paths:
            if len(path)>=2 and path[0] not in aTv and path[1] not in aTv and len(l)<nPv/2:
                l.append((path[0],path[1],0,vm))
                aTv[path[0]]=vm
                aTv[path[1]]=vm
                path.pop(0)
            if len(path)>=2: 
                for node in path:
                    if len(l)>=nPv/2:
                        break
                    elif path[1] not in aTv:
                        l.append((path[0],path[1],0,vm))
                        aTv[path[1]]=vm
                        path.pop(0)
        vms.append(l)
    
    count=0
    for path in paths:
        for i in range(len(path)-2):
            if count<V and len(vms[count])<nPv/2:
                if path[i+1] not in aTv:
                    vms[count].append((path[i],path[i+1],1,aTv[path[i]]))
                    count+=1
                    aTv[path[i+1]]=count
                    path.remove(path[i])
                elif path[i] not in aTv:
                    vms[count].append((path[i+1],path[i],1,aTv[path[i+1]]))
                    count+=1
                    aTv[path[i]]=count
                    path.remove(path[i])
                
            else:
                count+=1
    
    print len(aTv)
    print "##########################################################"
    print "VMS"
    print vms
    print "##########################################################"
    print "REMAIN PATHS"
    print paths
    print aTv
    return vms

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
        Vms=list_of_vms(G,paths,V)
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
