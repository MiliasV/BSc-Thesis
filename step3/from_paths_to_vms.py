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
    k=[]
    vm={}
    count=0
    for n in G.nodes():
        vm[n]=parts[count]
        count+=1
    for e in G.edges():
        l.append((e[0],e[1],vm[e[0]],vm[e[1]]))
    for e in l:
        if e[0]==701:
            k.append((e[1],e[0],vm[e[1]],vm[e[0]]))
        else:
            k.append((e[0],e[1],vm[e[0]],vm[e[1]]))

    #print vm
    #print l
    return k
    #for e in G.edges():
        

if __name__=='__main__':
    #input1 : file with paths in list of lists
    #input2 : number of Vms (=> list of Vms with credentials)
    
    start_time=time.time()
    paths=readmyfile(sys.argv[1])
    V=int(sys.argv[2])
    with open(sys.argv[3]) as f:                                               
        mH=f.read().splitlines()                                               
        mH.remove('None')                                                          
        mH=map(int,mH)
    #print paths 
    G=nx.Graph()
    #print len(paths)
    G=from_paths_to_graph(paths)
    (edgecuts,parts)=metis.part_graph(G,V)
    #print '#############################################################'
    #print nx.average_shortest_path_length(G,weight=None)
    #print edgecuts
    #print parts
    #print len(G.nodes())
    file=open("new_edges.txt",'w+')
    l = list_of_vms(G,parts)
    print >> file,l
    #for item in l:
        #print>>file, item
    file.close()
    #print l
 
    #Graphic representation
    count=0
    colors = ['darkkhaki','darkorange','darkslategray2','darkviolet','dimgrey','khaki','lightcoral','lightpink4','blue','green','yellow','antiquewhite4','brown','cyan','violet','firebrick3','pink','black','purple']
    for n in G.nodes():
        G.node[n]['color']=colors[parts[count]]
        count+=1
        print G.node[n]
        if n in mH:
            G.node[n]['color']='red'

     
    #pos=nx.circular_layout(G)
    nx.write_dot(G,'new_edges.dot')
    os.system("sed -i -e 's/--/->/g' new_edges.dot")
    os.system("python dottoxml.py new_edges.dot new_edges.graphml")
    #os.system("dot -Tpng 10circlegraph.dot -o 10circlegraph.png")
    #os.system("open graph.ps")
    
    #print time.time()-start_time
