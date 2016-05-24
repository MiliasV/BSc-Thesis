from fabric.api import *
from fabric.tasks import execute
#cd,parallel,run,env,execute,task,sudo,open_shell
import networkx as nx
import sys
import os
from ast  import literal_eval
#env.hosts = ['snf-680603.vm.okeanos.grnet.gr']
#env.user = 'mininet'
#env.password = 'byslaf366'
#env.hosts=['mininet@192.168.56.102']
#env.user = 'mininet'
env.disable_known_hosts=True
env.warn_only=True
#env.hosts=['mininet@192.168.56.102','mininet@192.168.56.101','mininet@83.212.102.97']
env.hosts=['mininet@83.212.108.121','mininet@83.212.102.97','mininet@83.212.108.122','mininet@83.212.108.123','mininet@83.212.108.124']

#env.hosts = ["mininet@83.212.102.97","mininet@147.102.13.61","mininet@192.168.56.103"]

#env.passwords = {'mininet@192.168.56.101:22': 'mininet', 'mininet@192.168.56.102:22': 'mininet','mininet@192.168.56.103:22' : 'mininet','mininet@83.212.102.97:22': 'byslaf366'}
env.passwords = {'mininet@83.212.102.97:22': 'byslaf366','mininet@83.212.108.121:22': 'byslaf366','mininet@83.212.108.122:22': 'byslaf366','mininet@83.212.108.123:22': 'byslaf366','mininet@83.212.108.124:22': 'byslaf366'}
                 

#ips=['83.212.102.97','192.168.56.102','192.168.56.101']
ips=['83.212.102.97','83.212.108.121','83.212.108.122','83.212.108.123','83.212.108.124']
     
     
#'83.212.102.97',
     


def showOvs():
        run('sudo ovs-vsctl show')

@hosts('mininet@83.212.102.123')
def victimServer():
    run('sudo mn -c')
    run('mkdir -p testing')
    put('edges_mininet.txt','~/testing/')
    put('min_builder.py','~/testing/')
    put('allMh.txt','~/testing/')
    print '############################ %s ################'%env.host
    run('cd testing && sudo python min_builder.py %s edges_mininet.txt allMh.txt &' %env.host , pty=False)

@parallel
def runOneLs():
    run('ls')

@parallel
@hosts('mininet@83.212.108.122','mininet@83.212.108.121','mininet@83.212.102.97','mininet@83.212.108.123')
#@hosts('mininet@83.212.108.121')
def connection():
        run('sudo mn -c')
        run('mkdir -p testing')
        put('edges_mininet.txt','~/testing/')
        put('min_builder.py','~/testing/')
        put('allMh.txt','~/testing/')
        print '############################ %s ################'%env.host
        run('cd testing && sudo python min_builder.py %s edges_mininet.txt allMh.txt' %env.host , pty=False)

if __name__=='__main__':
   
    f=str(sys.argv[1])
    num=int(sys.argv[2])
    mH=sys.argv[3]
    os.system("python from_paths_to_vms.py %(file)s %(number)s %(mh)s" %{"file":f, "number":num,"mh":mH})
    f1=open("new_edges.txt",'r')
    #f1=open(sys.argv[3])
    line=f1.readline()
    l=literal_eval(line)[:]
    print l
    e={}
    count=0
    for i in range(len(ips)):
        e[i]=ips[i]

    l=[(edge[0],edge[1],e[edge[2]],e[edge[3]]) for edge in l] 
    file = open("edges_mininet.txt",'w+')
    for item in l:
        print>>file, item
    file.close()
    f1.close()
    #execute(victimServer)
    execute(connection)
