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
import os
import sys
import time

class allH1Topo(Topo):
    "h1 connected with different switch to each host"
    def build(self,n):
        for i in range(n):
            host=self.addHost('h%s' % (i+1))

        "switch = self.addSwitch('s1')"    
        
        for i in range(n-1):
            switch = self.addSwitch('s%s' % (i+2))
            self.addLink(switch,'h%s' % (i+2))
            self.addLink(switch,'h1')

def simpleTest(num):
    "Create and test a simple network"
    topo = allH1Topo(n=num)
    net = Mininet(topo)
    hosts=net.hosts
    k=1
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
    CLI(net)
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    
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
    
    net.stop()

    

if __name__=='__main__':
    global k
    setLogLevel('info')
    num=int(sys.argv[1])
    simpleTest(num)
