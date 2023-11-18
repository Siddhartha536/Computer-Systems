from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
import sys
import time
import argparse
import subprocess


class NetworkTopo(Topo):
    def build(self, **_opts):
        
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        h1 = self.addSwitch('h1')
        h2 = self.addSwitch('h2')
        h3 = self.addSwitch('h3')
        h4 = self.addSwitch('h4')
        
        self.addLink(s1, s2, intfName1='s1-eth0', intfName2='s2-eth0')
        self.addLink(h1, s1, intfName2='s1-eth1')
        self.addLink(h2, s1, intfName2='s1-eth2')
        self.addLink(h3, s2, intfName2='s2-eth1')
        self.addLink(h4, s2, intfName2='s2-eth2')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Your script description')

    parser.add_argument('--config', choices=['b', 'c'], required=True,
                        help='Specify config option: b or c')
    parser.add_argument('--scheme', choices=['reno', 'vegas', 'cubic', 'bbr'], required=False,
                        help='Specify scheme option: reno, vegas, cubic, bbr')
    parser.add_argument('--loss', type=float, required=False,
                        help='Specify loss as a number')

    args = parser.parse_args()
    configValue = args.config
    schemeValue = args.scheme
    lossValue = args.loss
    


    topo = NetworkTopo()
    net = Mininet(topo=topo, waitConnected=True)
    net.start()

    schemeAsArg = ""
    if schemeValue:
        schemeAsArg = " -Z " + schemeValue

    #start h4 in server mode no matter what
    h1, h2, h3, h4 = net.getNodeByName('h1', 'h2', 'h3', 'h4')
    

    
if configValue == 'b':
    h4Server = h4.popen(['iperf', '-s', '-p', '5001'])

    h1Client = h1.popen(f'iperf -c {h4.IP()} -p 5001 {schemeAsArg}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = h1Client.communicate()
    print("h1Client Output:\n", output.decode())
    print("h1Client Error:\n", error.decode())
    h4Server.terminate()

else:
    h4Server = h4.popen(['iperf', '-s', '-p', '5001', '-P', '3'])

    def run_iperf_client(host, scheme_arg, output_file):
        iperf_command = f'iperf -c {h4.IP()} -p 5001 {scheme_arg} > {output_file} 2>&1 &'
        host.cmd(iperf_command)

    output_files = []
    for host in [h1, h2, h3]:
        output_file = f"{host.name()}_output.txt"
        output_files.append(output_file)
        run_iperf_client(host, schemeAsArg, output_file)

    # Wait for some time to ensure iperf clients have enough time to generate output
    time.sleep(5)

    # Terminate the iperf server
    h4Server.terminate()

    # Print the content of output files
    for output_file in output_files:
        with open(output_file, 'r') as file:
            print(f"Content of {output_file}:\n{file.read()}")

    CLI(net)
    
    net.stop()
