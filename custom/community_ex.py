#!/usr/bin/python

from fabric.api import *
from numpy import genfromtxt
import numpy as np
#cd,parallel,run,env,execute,task,sudo,open_shell
import networkx as nx
import community
import matplotlib.pyplot as plt
from collections import defaultdict
import sys
import ast
def show_graph(adjacency_matrix):
	    # given an adjacency matrix use networkx and matlpotlib to plot the graph
	    rows, cols = np.where(adjacency_matrix == 1)
	    edges = zip(rows.tolist(), cols.tolist())
	    gr = nx.Graph()
	    gr.add_edges_from(edges)
	    # nx.draw(gr) #  include labels
	    f=plt.figure(1)
	    nx.draw_networkx(gr)
	    # now if you decide you don't want labels because your graph
	    # is too busy just do: nx.draw_networkx(G,with_labels=False)
	    f.show() 

if __name__=='__main__':
	N=int(sys.argv[1])
	sublist=[]
	print N
	#take adjacency matrix from csv file
	mydata = genfromtxt("/Users/thodoris/Documents/Matlab/Rgg_50.csv",delimiter=',')
	adjacency = mydata[1:,1:]
	#plot the initial graph
	#show_graph(adjacency)
	
	rows, cols = np.where(adjacency == 1)
	edges = zip(rows.tolist(), cols.tolist())
	G = nx.Graph()
	G.add_edges_from(edges)
	# nx.draw(gr) #  include labels
	#creating communities graph	
	part = community.best_partition(G)

	new_dict = defaultdict(list)

	for k, v in part.iteritems():
		new_dict[v].append(k)

	#creating the subgraphs
	for i,j in new_dict.iteritems():
		print i
		print j
		sublist.append(j)
	print len(sublist)
	number=len(sublist)/N #to kathe VM tha parei tosa communities
	count=-1
	while N<len(sublist):	
		count+=1
		print count,'+',count
		for i in xrange(number-1): #prosthetw ta communitites, 1/VM	
			if len(sublist)>count+1:
				sublist[count+1]=sublist[count]+sublist[count+1]
				#print len(sublist)
				sublist.pop(0)
				print sublist	
	
	for i in range(len(sublist)):
		sub=G.subgraph(sublist[i])	
		k=plt.figure(i+2)
		nx.draw_networkx(sub)
		k.show()
		print sublist
	#print new_dict[1]
	#print list(part.values())
	#print G.nodes()
	values = [part.get(node) for node in G.nodes()]
	g=plt.figure(1)
	nx.draw_spring(G, cmap = plt.get_cmap('jet'), node_color = values, node_size=30, with_labels=False)
	g.show()
	raw_input()
