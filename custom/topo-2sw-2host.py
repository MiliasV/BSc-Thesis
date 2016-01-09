"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        leftHost = self.addHost( 'h1' )
        rightHost = self.addHost( 'h2' )
        leftSwitch = self.addSwitch( 's3' )
        rightSwitch = self.addSwitch( 's4' )

        # Add links
        self.addLink( leftHost, leftSwitch )
        self.addLink( leftSwitch, rightSwitch )
        self.addLink( rightSwitch, rightHost )
	
	#commands
	h1=hosts[1]
	result=h1.cmd("ping -c 2",h2.IP())
	print result

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


		
topos = { 'mytopo': ( lambda: MyTopo() ),'example': (lambda:ExampleTopo())}
