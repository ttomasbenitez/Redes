from mininet.topo import Topo
from mininet.link import TCLink

class MyTopo( Topo ):
    "Simple topology example."

    def build( self ):
        "Create custom topo."

        # Add hosts and switches
        server = self.addHost('h1')
        client_1 = self.addHost('h2')
        client_2 = self.addHost('h3')
        client_3 = self.addHost('h4')
        switch = self.addSwitch('s1')
        #rightSwitch = self.addSwitch( 's4' )

        # Add links
        self.addLink(server, switch)
        self.addLink(switch, client_1, cls = TCLink , loss = 10)
        self.addLink(switch, client_2, cls = TCLink , loss = 10)
        self.addLink(switch, client_3, cls = TCLink , loss = 10)
        #self.addLink( rightSwitch, rightHost, cls = TCLink, loss = 30 )


topos = { 'mytopo': ( lambda: MyTopo() ) }