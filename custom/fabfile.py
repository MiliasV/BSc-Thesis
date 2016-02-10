from fabric.api import * 
#cd,parallel,run,env,execute,task,sudo,open_shell
import networkx as nx

#env.hosts = ['snf-680603.vm.okeanos.grnet.gr']
#env.user = 'root'
#env.password = 'byslaf366'
env.hosts = ['mininet@192.168.56.101','mininet@192.168.56.102']
#env.hosts=['mininet@192.168.56.102']
#env.user = 'mininet'
env.passwords = {'mininet@192.168.56.101:22': 'mininet', 'mininet@192.168.56.102:22': 'mininet'}



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
	put('adjToNetwork.py','~/')
	put('exam.csv','~/')
	#put('~/USC-NSL-miniNExT-75c2781')
        # Simplest form:
        #environment = prompt('Please specify target environment: ')
        # With default, and storing as env.dish:
        #prompt('Specify favorite dish: ', 'dish', default='spam & eggs')
        #print("%s"%env.dish)
        #open_shell()
        #with hide('output'):
        #with
        run('sudo mn -c')
        with settings(warn_only=True):
            run('nohup sudo python  adjToNetwork.py exam.csv ')
            #run('disown')

if __name__=='__main__':
	execute(connection)
