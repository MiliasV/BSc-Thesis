"""Custom topology 

All hosts connected via different switch to h1

host --- switch --- host1

"""
#!/usr/bin/python  

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.topolib import TreeTopo
from numpy import genfromtxt
import os
import sys
import time

class adjTopo(Topo):
	"building Topo from Adj Matrix m"
	def build(self,m):
		count=0
		rows=len(m)
		cols=len(m[0])
		nodes=rows 
		print nodes	
		"number of nodes is N (dimensions of A)"
		
		for i in range(0,rows):
			host=self.addHost('h%s'% (i))
		
		for i in range(0,rows):
			for j in range(i+1,cols): 
				"undirected network"
				if m[i][j]==1:
					switch = self.addSwitch('s%s' % (count))
					self.addLink(switch,'h%s' %(i))
					self.addLink(switch,'h%s' %(j))
					count+=1				

def testOne(A):
	topo = adjTopo(m=A)
	net = Mininet(topo)
	hosts=net.hosts
	net.start()
	CLI(net)
	net.stop()


if __name__=='__main__':
	global k
    	setLogLevel('info')
    	#num=int(sys.argv[1])
    	#simpleTest(num)
    	#m= [[0]*4 for x in range(4)]
   	#for i in range(0,2):
	#	for j in range(2,4):
	#		m[i][j]=1 
   	#m[3][1]=1
	
	m=genfromtxt(sys.argv[1], delimiter=',')
	print m
    	testOne(m)
