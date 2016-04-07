from fabric.api import *
from fabric.tasks import execute
#cd,parallel,run,env,execute,task,sudo,open_shell
import networkx as nx
import sys
import os
from ast  import literal_eval
#env.hosts = ['snf-680603.vm.okeanos.grnet.gr']
#env.user = 'root'
#env.password = 'byslaf366'
#env.hosts=['mininet@192.168.56.102']
#env.user = 'mininet'
env.hosts=['mininet@192.168.56.101','mininet@192.168.56.102']

#env.hosts = ["mininet@192.168.56.101","mininet@192.168.56.102"]

env.passwords = {'mininet@192.168.56.101:22': 'mininet', 'mininet@192.168.56.102:22': 'mininet'}

ips=['192.168.56.101','192.100.56.102']


def showOvs():
        run('sudo ovs-vsctl show')

@parallel
def runOneLs():
    run('ls')


@parallel
def connection():
	#let's you interact with the remote VM from terminal
	#open_shell()
	#run('sudo mn')
	#with cd( '~/mininet/custom/'):
	#	run('ls')
	#put('adjToNetwork.py','~/')
	#put('exam.csv','~/')
	#put('~/USC-NSL-miniNExT-75c2781')
        # Simplest form:
        #environment = prompt('Please specify target environment: ')
        # With default, and storing as env.dish:
        #prompt('Specify favorite dish: ', 'dish', default='spam & eggs')
        #print("%s"%env.dish)
        #open_shell()
        #with hide('output'):
        #with
        #run('sudo mn -c')
        #put ('script.py','~/')
        #put ('list.txt','~/')
        #run('python script.py list.txt %s' %env.host)
	run('mkdir testing')
	run('cd testing')
        put('edges_mininet.txt','~/')
        put('min_builder.py','~/')
        run('sudo python min_builder.py %s edges_mininet.txt ' %env.host)
        #with settings(warn_only=True):
            #run('nohup sudo python  adjToNetwork.py exam.csv ')
            #run('disown')

if __name__=='__main__':
    
    f=open(sys.argv[1])
    line=f.readline()
    l=literal_eval(line)[:]
    #print l
    e={}
    count=0
    for i in range(len(ips)):
        e[i]=ips[i]

    l=[(edge[0],edge[1],e[edge[2]],e[edge[3]]) for edge in l] 
    file = open("edges_mininet.txt",'w+')
    for item in l:
        print>>file, item
    execute(connection)
    """
    print " "
    print '###############################'
    print l
    """
    """
    """
