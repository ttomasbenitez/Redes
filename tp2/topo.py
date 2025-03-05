from mininet.topo import Topo
from mininet.link import TCLink

MAX_HOSTS = 4

SWITCHES_OBLIGATORIOS = 2

MIN_SWITCHES_MEDIADORES = 2

class MyTopo( Topo ):
    "Simple topology example."

    def __init__(self, agregar_switches = MIN_SWITCHES_MEDIADORES):
        Topo.__init__(self)
        self.number_switches = agregar_switches
        #print(number_switches)

        hosts = []
        switches = []

        # Add hosts and switches
        for i in range(MAX_HOSTS):
            hosts.append(self.addHost('h'+str(i + 1)))

        for i in range(self.number_switches + SWITCHES_OBLIGATORIOS):
            switches.append(self.addSwitch('s'+str(i + 1)))
        

        # Add links default
        self.addLink(hosts[0], switches[0])
        self.addLink(hosts[1], switches[0])
        self.addLink(hosts[2], switches[self.number_switches + SWITCHES_OBLIGATORIOS - 1])
        self.addLink(hosts[3], switches[self.number_switches + SWITCHES_OBLIGATORIOS - 1])
        

        # #Add Links tunel

        for i in range(self.number_switches + SWITCHES_OBLIGATORIOS - 1):
            #print(i)
            self.addLink(switches[i] , switches[i + 1])

topos = { 'mytopo': MyTopo}
