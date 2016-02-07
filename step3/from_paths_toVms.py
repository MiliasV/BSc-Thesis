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

#Author: Vasileios Milias

#nodes_per_Vm
nPv=4

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
    #inputs graph,paths,number of vms,runs for aTv>=2
    #output list with the edges that go in every Vm.
    #Format of output: [ [(node1,node2,{0,1},vm),(...)],[..],..]
    #if the third elem. of tuple is 0 the nodes are both in this vm
    #                            is 1 the first node is in this vm and the 
    #                            second in the vm indicated by the 4th elem
    vms=[]
    #as_to_vm_dict
    aTv={}
    #how many nodes have been inserted to the vm
    vm_nodes={}
    for vm in range(V):
        vm_nodes[vm]=0
    l=[]
    #no point of this
    flag=1
    e=G.edges()

    #here we put as many edges as we can without "breaking" them in half (vm to vm) 
    #thelei ftiaximo. Den pairnei ola ta zeygaria pou mporei
    for vm in range(V):
        paths= [x for x in paths if x != [] and len(x)>1]
        l=[]
        for path in paths:
            if len(path)>=2 and path[0] not in aTv and path[1] not in aTv and len(l)<nPv/2:
                l.append((path[0],path[1],0,vm))
                e=[x for x in e if ( (x[0]!=path[0] or x[1]!=path[1]) and (x[0]!=path[1] or x[1]!=path[0]) )]
                aTv[path[0]]=vm
                aTv[path[1]]=vm
                vm_nodes[vm]+=2
                print "%s,%s, added (%s,%s)"%(vm,vm_nodes,path[0],path[1])
                path.pop(0)
            if len(path)>=2: 
                for node in path:
                    if len(l)>nPv/2:
                        break
                    elif aTv[path[0]]==vm and path[1] not in aTv:
                        l.append((path[0],path[1],0,vm))
                        e=[x for x in e if ( (x[0]!=path[0] or x[1]!=path[1]) and (x[0]!=path[1] or x[1]!=path[0]) )]
                        aTv[path[1]]=vm
                        vm_nodes[vm]+=1
                        path.pop(0)
        vms.append(l)

    #here we put the rest of the breaking edges
    for edge in e:
        if edge[0] in aTv:
            vm0=aTv[edge[0]]
        if edge[1] in aTv:
            vm1=aTv[edge[1]]
       
        if edge[0] in aTv and edge[1] not in aTv:
            #if i can put it in the same vm
            if vm_nodes[aTv[edge[0]]]<nPv:
                vms[aTv[edge[0]]].append((edge[1],edge[0],0,aTv[edge[0]]))
                aTv[edge[1]]=aTv[edge[0]]
                vm_nodes[aTv[edge[0]]]+=1
                e=[x for x in e if ( (x[0]!=edge[0] or x[1]!=edge[1]) and (x[0]!=edge[1] or x[1]!=edge[0]) )]

            else:
                for Vm in vm_nodes:
                    if vm_nodes[Vm]<nPv:
                        vms[Vm].append((edge[1],edge[0],1,vm0))
                        vm_nodes[Vm]+=1
                        vms[vm0].append((edge[0],edge[1],1,Vm))
                        aTv[edge[1]]=Vm
                        e=[x for x in e if ( (x[0]!=edge[0] or x[1]!=edge[1]) and (x[0]!=edge[1] or x[1]!=edge[0]) )]
                        break

        elif edge[1] in aTv and edge[0] not in aTv:
            
            if vm_nodes[aTv[edge[1]]]<nPv:
                vms[aTv[edge[1]]].append((edge[0],edge[1],0,aTv[edge[1]]))
                aTv[edge[0]]=aTv[edge[1]]
                vm_nodes[aTv[edge[1]]]+=1
                e=[x for x in e if ( (x[0]!=edge[0] or x[1]!=edge[1]) and (x[0]!=edge[1] or x[1]!=edge[0]) )]
            else:
                for Vm in vm_nodes:
                    if vm_nodes[Vm]<nPv:
                        vms[Vm].append((edge[0],edge[1],1,vm1))
                        vm_nodes[Vm]+=1
                        vms[vm1].append((edge[1],edge[0],1,Vm))
                        aTv[edge[0]]=Vm
                        e=[x for x in e if ( (x[0]!=edge[0] or x[1]!=edge[1]) and (x[0]!=edge[1] or x[1]!=edge[0]) )]
                        break
       
        elif edge[0] in aTv and edge[1] in aTv:
            vms[vm0].append((edge[0],edge[1],1,vm1))
            vms[vm1].append((edge[1],edge[0],1,vm0))
            e=[x for x in e if ( (x[0]!=edge[0] or x[1]!=edge[1]) and (x[0]!=edge[1] or x[1]!=edge[0]) )]
        """
        elif nPv==1:
            count=0
            for node in G.nodes():
                aTv[node]=count
                count+=1
            for edge in e:
                #nPv=1
                print edge
                count=0
                vm0=aTv[edge[0]]    
                vm1=aTv[edge[1]]
                for Vm in range(len(vm_nodes)-1):
                    if vm_nodes[Vm]<nPv:
                        vms[Vm].append((edge[0],edge[1],1,vm1))
                        vm_nodes[Vm]+=1
                    if vm_nodes[Vm+1]<nPv:
                        vms[Vm+1].append((edge[1],edge[0],1,vm0))
                        vm_nodes[Vm+1]+=1
                        break
                    #e=[x for x in e if ( (x[0]!=edge[0] or x[1]!=edge[1]) and (x[0]!=edge[1] or x[1]!=edge[0]) )]
           """ 

                    


           #e.remove((path[0],path[1]))
    
    print len(aTv)
    print "##########################################################"
    print "VMS"
    print vms
    print "##########################################################"
    print "REMAIN PATHS"
    print paths
    print "##########################################################"
    print "as to Vm dictionary"
    print aTv
    print "##########################################################"
    print "REMAIN EDGES"
    print e
    print "##########################################################"
    print "size of VM"
    print vm_nodes
    print "##########################################################"
    print "starting edges"
    print G.edges()
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
    #else:
    #    Vms=list_of_vms(G,paths,V)
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
