#!/usr/bin/python  
import time
import re
import os
import sys
import numpy as np
import itertools
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from pprint import pprint

#Author: Vasileios Milias
def readmyfile(myfile):
    #reads file in format: fromAs|toAs|{0,-1}
    #OUTPUT L:
    #L's lines are edges with the format
    #L[*][0] = from    
    #L[*][1] = to    
    #L[*][2] = {0,-1} where 0 = undirected edge
    #                      -1 = directed edge  
    wordList=[]
    with open(myfile) as f:
        line=f.readlines()
        for i in range(len(line)-1):
            if line[i+1][0]!='#':
                wordList.append(re.split(r'\|',line[i+1].rstrip('\t')))
    return wordList


def numberOfNodes(eList):
    G=nx.DiGraph(eList)
    return len(G.nodes())

def convertToWeightedEdgeList(L):
    #here we make the edgeList from the format : fromAs|toAs|{0,-1}
    #For undirected edges we add a new edge with weight 0
    #For directed edges we add a new edge fromAS->toAs with weight 1
    #and another edge toAs->fromAs with weight 2
    #p2c ->weight 1, c2p ->weight 2, p2p -> weight 0
    mylist=[]
    for i in range(len(L)):
        #if undirected edge
        if L[i][2]==0: 
            #L[i][2]=1
            newElem=(L[i][0],L[i][1],0)
            mylist.append(newElem)
            newElem=(L[i][1],L[i][0],0)
            mylist.append(newElem)
        #if directed edge    
        else:
            newElem=(L[i][0],L[i][1],1)
            mylist.append(newElem)
            newElem=(L[i][1],L[i][0],2)
            mylist.append(newElem)
    return mylist        


def convertToEdgeList(L):
    #here we make the edgeList from the format : fromAs|toAs|{0,-1}
    #For undirected edges i add a new edge from the opposite side.
    mylist=[]
    for i in range(len(L)):
        #if undirected edge
        if L[i][2]==0: 
            #L[i][2]=1
            newElem=(L[i][0],L[i][1])
            mylist.append(newElem)
            newElem=(L[i][1],L[i][0])
            mylist.append(newElem)
        #if directed edge    
        else:
            newElem=(L[i][0],L[i][1])
            mylist.append(newElem)
    return mylist        


#from edge list to adjacency list
def fromEdgeToAdj(eList):
    u=[]
    v=[]
    adjList = {}
    for edge in eList:
        u=edge[0]
        v=edge[1]
        if u not in adjList:
            adjList[u]=[]
        adjList[u].append(v)
    return adjList
    #printAdjList(adjList)
    
    

def reveList(eList):
    rev=[]
    for i in range(len(eList)):
        cur=reversed(eList[i])
        cur=tuple(cur)
        rev.append(cur)
    return rev    


def bfs_as_relationships(G,victim,mh):
    #bfs and as-relationships properties
    #inputs: weighted graph with as-relationships with the format: 
    #                           p2c -> w=1, c2p -> w=2 ,p2p -> w=1
    #        victim, malicious hosts
    paths=[]
    for m in mh:
        print m
        stack=[(m,[m])]
        while stack:
            (vertex,path)=stack.pop(0)
            for next in set(G.neighbors(vertex)) - set(path):
                if len(path)>1:

                    if (
                            ( 
                              ( (G[path[len(path)-2]][path[len(path)-1]]["weight"]==1) and ( (G[vertex][next]["weight"]==(1)) )) or
                              ( (G[path[len(path)-2]][path[len(path)-1]]["weight"]==0) and ( (G[vertex][next]["weight"]==(2 or 0)) )) or
                              ( (G[path[len(path)-2]][path[len(path)-1]]["weight"]==2) and G[vertex][next]["weight"]==2 )  
                            )  and
                            len(path)<7
                         ): 
                        if next==victim:
                            L=path
                            L.append(next)
                            paths.append(L)
                            stack=[]
                            break 
                        else:
                            stack.append((next,path +[next])) 
                elif next==victim:
                    L=path
                    L.append(next)
                    paths.append(L)
                    stack=[]
                    break 
                else:
                    
                    stack.append((next,path+[next]))
    
    for path in paths:
        L=[]
        for i in range(len(path)-1):
            L.append(G[path[i]][path[i+1]]["weight"])
        print L
    if len(mh)==len(paths):
        print "All paths exist"
    else:
        print "%s paths don't exist" %(len(mh)-len(paths))
    return paths

def from_paths_to_graph(G,paths):
    Gp=nx.DiGraph()
    for path in paths:
        for i in range(len(path)-1):
            Gp.add_edge(path[i],path[i+1],weight=G[path[i]][path[i+1]]["weight"])
    return Gp


if __name__=='__main__':
    #input : file with dataset : fromAs|toAs|{0,-1}
    
    start_time=time.time()
    L=readmyfile(sys.argv[1])
    
    #strings to ints
    intL = [list(map(int, row)) for row in L]
    
    #data to edge list 
    #eList = convertToEdgeList(intL)
    
    wList = convertToWeightedEdgeList(intL)
    G=nx.DiGraph()
    G.add_weighted_edges_from(wList)
    as_paths =( bfs_as_relationships(G,174,
                                    [6453, 701,209, 6730, 10026,
                                    1239, 1267, 1916, 2497, 3209, 
                                    196615, 5412, 3320, 3340, 42, 
                                    3357]) )
    
    
    print as_paths                            
    Gtree=from_paths_to_graph(G,as_paths)
    pos=nx.circular_layout(Gtree)
    nx.draw(Gtree,pos)
    nx.draw_networkx_labels(Gtree,pos)
    plt.show()
    print "######################################"
    print Gtree.edges(data=True)
    print "#####################################"
    print  Gtree.edges()
    print "#####################################"
    print Gtree.nodes()
    print nx.is_directed_acyclic_graph(Gtree) 
    print time.time()-start_time
