#!/usr/bin/python  
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.topolib import TreeTopo
import os
import sys
import time
import json
import ast 


"""Custom topology 

Building topology depending on edge-list

"""
class allH1Topo(Topo):
    def build(self,l):
        #dictionary for the names of the hosts&switches
        sh={}
        for e in l:
	    print e
	    #flag= 0 {same vm}, 1 {first node in other vm}, 2 {second node in other vm}
	    flag=0
	    
            if e[2]==vm:
		if e[0] not in sh:
                    if e[0] in mH:
                            host=self.addHost('h_%s' % (e[0]))
                            if dV[e[0]]==1:
                            	s1=self.addSwitch('s_%s' % (e[0]))
                            	self.addLink(s1,host)
                            	sh[e[0]]='s_'+str(e[0])
                    else:
                        #creation of non-malicious host->switch
                        s1=self.addSwitch('s_%s' %(e[0]))
                        sh[e[0]]='s_'+str(e[0])
		
			
            else:
                flag=1
                #s1=self.addSwitch('s_%s' %(e[0]))
                sh[e[0]]='s_'+str(e[0])
                vm2=e[2]
                    
            if e[3]==vm:
                if e[1] not in sh:
                    if e[1] in mH:
			    host=self.addHost('h_%s' % (e[1]))
                            #if dV[e[0]]==1:
                            s2=self.addSwitch('s_%s' % (e[1]))
                            self.addLink(s2,host)
                            sh[e[1]]='s_'+ str(e[1])
		            #print str[e[1]]
			    #else:
                    else:
                        #creation of non-malicious host->switch
                        s2=self.addSwitch('s_%s' %(e[1]))
                        sh[e[1]]='s_'+ str(e[1])
            else:
                flag=2
                #s2=self.addSwitch('s_%s' %(e[1]))
                sh[e[1]]='s_'+ str(e[1])
                vm2=e[3]

            if flag==0:
                self.addLink(sh[e[0]],sh[e[1]])
	    elif flag==1:
		vDict[sh[e[1]]]=[vm2,sh[e[0]]+sh[e[1]]]
	    else:
		vDict[sh[e[0]]]=[vm2,sh[e[0]]+sh[e[1]]]
        "switch = self.addSwitch('s1')"    
"""
-Creates the custom topology allH1Topo
-h1 runs SimpleHTTPServer
-All hosts run curl to h1 
-results on output_script.pcap, outputcurl.txt
"""

def Test(num):
    "Create and test a simple network"
    topo = allH1Topo(l=num)
    net = Mininet(topo)
    hosts=net.hosts
    switches=net.switches
    net.start()
    for switch in switches:
	if str(switch) in vDict:
		switch.cmd('ovs-vsctl add-port switch vxlan%(number)s -- set interface vxlan%(number)s type=gre options:remote_ip=%(vm2)s options:key=%(number)s'% {"number":vDict[str(switch)][1],"vm2":vDict[str(switch)][0]})
		print "olaaa"
    		switch.cmdPrint('ovs-vsctl show')		
    
    CLI(net)
    net.stop()
   
    """ 
    a={}
   
    "a[1]=h1, a[2]=h2..."
    setLogLevel('debug')

    for i in hosts:
        if i==hosts[0]:
            a[k]=i
            for l in range(len(hosts)-1):
                a[k].cmd('ifconfig h1-eth%(s1)s 10.0.%(s2)s.1/24' % {"s1":l ,"s2":l+2})
        else:
            a[k]=i
            a[k].cmd('ifconfig h%(s1)s-eth0 10.0.%(s2)s.2/24' % {"s1":k ,"s2":k})
        k+=1
    net.start()
    n=2
    for switch in switches:
        switch.cmd('ovs-vsctl add-port "s%(number)s" vxlan%(number)s -- set interface vxlan%(number)s type=vxlan options:remote_ip=%(vm2)s options:key=%(number)s'% {"number":n,"vm2":vm2})
        n+=1
    #print "Dumping host connections"
    #dumpNodeConnections(net.hosts)
    
    "h1 cleans the files before anyone writes them"
    a[1].cmd('rm -f outputcurl.txt')
    a[1].cmd('rm -f output_script.pcap')
    
    "h1 starts an Http server and writes output to Http.txt"
    
    a[1].cmd('python -u -m SimpleHTTPServer 80 >> Http.txt &')
    ">& /tmp/http.log &')"

    "Waiting for Http Server to start"
    time.sleep(4) 
    
    "h1 captures traffic "
    a[1].cmd('tcpdump -i any -w output_script.pcap &')
    
    for l in range(2,k-1):
        res=a[l].cmd('python curl_script.py 10.0.%s.1 &' %(l))
    
    res=a[k-1].sendCmd('python curl_script.py 10.0.%s.1 ' %(k-1))
    a[k-1].waitOutput()
    
    #CLI(net)
    net.stop()

    
"""
if __name__=='__main__':
    l=[]
    #input1=this vm's ip
    #input2=edges/vms
    flag=0
    vDict={}
    vm=str(sys.argv[1])
    #print vm
    #edges=eval(open(sys.argv[2]))
    mH=[701,7481]
    with open(sys.argv[2]) as f:
    	edges = [ast.literal_eval(line) for line in f]    
    dV={}
    for e in edges:
        if vm in e:
            l.append(e)
            if e[0] in dV:
                dV[e[0]]+=1
            else:
                dV[e[0]]=1
            if e[1] in dV:
                dV[e[1]]+=1
            else:
                dV[e[1]]=1
            #print e
    setLogLevel('info')
    print l
    Test(l)
