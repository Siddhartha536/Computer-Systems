from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class LinuxRouter(Node):
    "A Node with IP forwarding enabled."

    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        # Enable forwarding on the router
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


class NetworkTopo(Topo):

    def build(self, **_opts):
        rA = self.addNode('rA', cls=LinuxRouter, ip='192.168.2.3/24')
        rB = self.addNode('rB', cls=LinuxRouter, ip='192.168.4.3/24')
        rC = self.addNode('rC', cls=LinuxRouter, ip='192.168.6.3/24')

        
        h1 = self.addHost('h1', ip='192.168.2.2/24',
                          defaultRoute='via 192.168.2.3')
        h2 = self.addHost('h2', ip='192.168.3.2/24',
                          defaultRoute='via 192.168.3.3')
        h3 = self.addHost('h3', ip='192.168.4.2/24',
                          defaultRoute='via 192.168.4.3')
        h4 = self.addHost('h4', ip='192.168.5.2/24',
                          defaultRoute='via 192.168.5.3')
        h5 = self.addHost('h5', ip='192.168.6.2/24',
                          defaultRoute='via 192.168.6.3')
        h6 = self.addHost('h6', ip='192.168.7.2/24',
                          defaultRoute='via 192.168.7.3')


        self.addLink(h1, rA, intfName2='rA-eth1',
                      params2={'ip': '192.168.2.3/24'})
        self.addLink(h2, rA, intfName2='rA-eth2',
                      params2={'ip': '192.168.3.3/24'})

    
        self.addLink(h3, rB, intfName2='rB-eth1',
                      params2={'ip': '192.168.4.3/24'})
        self.addLink(h4, rB, intfName2='rB-eth2',
                      params2={'ip': '192.168.5.3/24'})
        

        self.addLink(h5, rC, intfName2='rC-eth1',
                      params2={'ip': '192.168.6.3/24'})
        self.addLink(h6, rC, intfName2='rC-eth2',
                      params2={'ip': '192.168.7.3/24'})



        self.addLink(rA, rB, intfName1='rA-eth3', intfName2='rB-eth3',
              params1={'ip': '192.168.8.2/24'}, params2={'ip': '192.168.8.3/24'})
        self.addLink(rB, rC, intfName1='rB-eth4', intfName2='rC-eth3',
              params1={'ip': '192.168.9.2/24'}, params2={'ip': '192.168.9.3/24'})
        self.addLink(rA, rC, intfName1='rA-eth4', intfName2='rC-eth4',
              params1={'ip': '192.168.10.3/24'}, params2={'ip': '192.168.10.2/24'})


def run():
    topo = NetworkTopo()
    net = Mininet(topo=topo, waitConnected=True)
    net.start()
    
    # #rA->rB and rA->rC
    # #Static Routing For Router A
    # net['rA'].cmd('route add -net 192.168.4.0/24 gw 192.168.8.3 rA-eth3')
    # net['rA'].cmd('route add -net 192.168.5.0/24 gw 192.168.8.3 rA-eth3')
    # net['rA'].cmd('route add -net 192.168.6.0/24 gw 192.168.10.2 rA-eth4')
    # net['rA'].cmd('route add -net 192.168.7.0/24 gw 192.168.10.2 rA-eth4')

    # #Static Routing For Router B
    # net['rB'].cmd('route add -net 192.168.2.0/24 gw 192.168.8.2 rB-eth3')
    # net['rB'].cmd('route add -net 192.168.3.0/24 gw 192.168.8.2 rB-eth3')
    # net['rB'].cmd('route add -net 192.168.6.0/24 gw 192.168.9.3 rB-eth4')
    # net['rB'].cmd('route add -net 192.168.7.0/24 gw 192.168.9.3 rB-eth4')

    
    # #Static Routing For Router C
    # net['rC'].cmd('route add -net 192.168.2.0/24 gw 192.168.10.3 rC-eth4')
    # net['rC'].cmd('route add -net 192.168.3.0/24 gw 192.168.10.3 rC-eth4')
    # net['rC'].cmd('route add -net 192.168.4.0/24 gw 192.168.9.2 rC-eth3')
    # net['rC'].cmd('route add -net 192.168.5.0/24 gw 192.168.9.2 rC-eth3')


    #rA->rB->rC
    #for rA
    net['rA'].cmd('route add -net 192.168.4.0/24 gw 192.168.8.3 rA-eth3')
    net['rA'].cmd('route add -net 192.168.5.0/24 gw 192.168.8.3 rA-eth3')
    net['rA'].cmd('route add -net 192.168.6.0/24 gw 192.168.8.3 rA-eth3')
    net['rA'].cmd('route add -net 192.168.7.0/24 gw 192.168.8.3 rA-eth3')

    #for rB
    net['rB'].cmd('route add -net 192.168.6.0/24 gw 192.168.9.3 rB-eth4')
    net['rB'].cmd('route add -net 192.168.7.0/24 gw 192.168.9.3 rB-eth4')
    net['rB'].cmd('route add -net 192.168.2.0/24 gw 192.168.9.3 rB-eth4')
    net['rB'].cmd('route add -net 192.168.3.0/24 gw 192.168.9.3 rB-eth4')

    #for rC
    net['rC'].cmd('route add -net 192.168.2.0/24 gw 192.168.10.3 rC-eth4')
    net['rC'].cmd('route add -net 192.168.3.0/24 gw 192.168.10.3 rC-eth4')
    net['rC'].cmd('route add -net 192.168.4.0/24 gw 192.168.10.3 rC-eth4')
    net['rC'].cmd('route add -net 192.168.5.0/24 gw 192.168.10.3 rC-eth4')

    info(net['rA'].cmd('route'))
    info(net['rB'].cmd('route'))
    info(net['rC'].cmd('route'))
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
