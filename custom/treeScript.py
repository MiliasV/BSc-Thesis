"""Custom topology example

Two directly connected switches plus a host for each switch:

host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
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

class ExampleTopo (Topo):
    "fisrt example Topo"
    def __init__(self):
            # Initialize topology
            Topo.__init__( self )
            # Add hosts and switches
            leftHost = self.addHost('h1')
            rightHost = self.addHost('h2')
            upperHost = self.addHost('h3')
            downHost = self.addHost('h4')

            leftSwitch = self.addSwitch( 's1' )
            rightSwitch = self.addSwitch( 's2' )
            downSwitch = self.addSwitch( 's3' )
            aloneSwitch = self.addSwitch( 's4' )

            #Add links
            self.addLink(leftHost,leftSwitch)
            self.addLink(upperHost,leftSwitch)
            self.addLink(upperHost,rightSwitch)
            self.addLink(rightHost,rightSwitch)
            self.addLink(leftHost,downSwitch)
            self.addLink(rightHost,downSwitch)
            self.addLink(rightHost,aloneSwitch)
            self.addLink(leftSwitch,rightSwitch)
            self.addLink(leftSwitch,aloneSwitch)
            self.addLink(leftSwitch,downSwitch)
            self.addLink(downHost,downSwitch)	



def HTTPtest(net):
    "print 'Dumping host connections'"
    "dumpNodeConnections(net.hosts)"
    "print 'Testing network connectivity'"
    "net.pingAll()"
    hosts=net.hosts
    k=0
    a={}
    for i in hosts:
        "a[o]=h1 ,a[1]=h2 ..."
        a[k]=i
        print a[k]
        k +=1
    setLogLevel('debug')
    
    "h1 cleans the files before anyone writes them"
    a[0].cmd('rm -f outputcurl.txt')
    a[0].cmd('rm -f output_script.pcap')
    
    "h1 starts an Http server and writes output to Http.txt"
    
    a[0].cmd('python -u -m SimpleHTTPServer 80 >> Http.txt &')
    ">& /tmp/http.log &')"

    "Waiting for Http Server to start"
    time.sleep(4) 
    
    "h1 captures traffic "
    a[0].cmd('tcpdump -w output_script.pcap &')

    "time.sleep(5)"
    
    "all hosts curl to h1's server"
    for l in range(1,k):
        res=a[l].cmd('python curl_script.py 10.0.0.1 &')
        """
        res2=a[l].cmd('curl -w "@for_curl.txt" -o /dev/null -s', a[0].IP())
        res3=a[l].cmd('curl -w "@for_curl.txt" -o /dev/null -s', a[0].IP())
        print res2
        print res3
    """
    "time.sleep(10)"
    res=a[k-1].sendCmd('python curl_script.py 10.0.0.1 ')
    a[k-1].waitOutput()

if __name__=='__main__':
    global k
    setLogLevel('info')
    "Create network..."
    "topo = Tree"
    "arguments are for the depth and the fanout of the tree"
    tree4 = TreeTopo(depth=int(sys.argv[1]),fanout=int(sys.argv[2]))
    net = Mininet(topo=tree4,host=CPULimitedHost, link=TCLink)
    net.start()

    "...and run an http test"
    HTTPtest(net)
    net.stop()
