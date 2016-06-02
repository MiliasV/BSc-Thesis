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
from random import randint

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


def convertToWeightedEdgeList(L):
    #here we make the edgeList from the format : ProviderAs|CustomerAs|{0,-1}
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

    
def bfs_as_relationships(G,victim,mh):
    #bfs and as-relationships properties
    #inputs: weighted graph with as-relationships with the format: 
    #p2c ->weight 1, c2p ->weight 2, p2p -> weight 0
    #victim, malicious hosts
    paths=[]
    for m in mh:
        #print m
        stack=[(m,[m])]
        while stack:
            (vertex,path)=stack.pop(0)
            for next in set(G.neighbors(vertex)) - set(path):
                if len(path)>1:

                    if (
                            ( 
                              ( (G[path[len(path)-2]][path[len(path)-1]]["weight"]==2) and ( (G[vertex][next]["weight"]==(2 or 0)) )) or
                              ( (G[path[len(path)-2]][path[len(path)-1]]["weight"]==0) and ( (G[vertex][next]["weight"]==( 1)) )) or
                              ( (G[path[len(path)-2]][path[len(path)-1]]["weight"]==1) and G[vertex][next]["weight"]==(1) )  
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
    return paths



if __name__=='__main__':
    #input : file with dataset : fromAs|toAs|{0,-1}
    
    L=readmyfile(sys.argv[1])
    intL = [list(map(int, row)) for row in L]
    
    with open(sys.argv[2]) as f:
        mh=f.read().splitlines()
    mh.remove('None')
    mH=map(int,mh)
    smallmH=[]
    for i in range(3):
        smallmH.append(mH[i])
    
    wList = convertToWeightedEdgeList(intL)
    G=nx.DiGraph()
    G.add_weighted_edges_from(wList)
    as_paths = bfs_as_relationships(G,701,smallmH)
    print as_paths


