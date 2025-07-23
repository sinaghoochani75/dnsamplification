#!/usr/bin/python3
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.cli import CLI

from p4_mininet import P4Switch, P4Host

import argparse
from time import sleep

parser = argparse.ArgumentParser(description="Sina Mininet")
parser.add_argument(
    "--behavioral-exe",
    help="Path to behavioral executable",
    type=str,
    action="store",
    required=True,
)
parser.add_argument(
    "--thrift-port",
    help="Thrift server port for table updates",
    type=int,
    action="store",
    default=9090,
)
parser.add_argument(
    "--num-hosts",
    help="Number of hosts to connect to switch",
    type=int,
    action="store",
    default=2,
)
parser.add_argument(
    "--json", help="Path to JSON config file", type=str, action="store", required=True
)
parser.add_argument(
    "--pcap-dump",
    help="Dump packets on interfaces to pcap files",
    type=str,
    action="store",
    required=False,
    default=False,
)

args = parser.parse_args()


class SinaHost(P4Host):
    def start(self):
        super().start()
        print(f"{self.name} started! ({self.IP()})")


class SinaTopo(Topo):
    def __init__(self, sw_path, json_path, thrift_port, pcap_dump, n, **opts):
        super().__init__(self, **opts)

        switch = self.addSwitch(
            "s1",
            sw_path=sw_path,
            json_path=json_path,
            thrift_port=thrift_port,
            pcap_dump=pcap_dump,
        )

        for h in range(n):
            host = self.addHost(
                f"h{h + 1}", ip=f"10.0.{h}.10/24", mac=f"00:04:00:00:00:{h:02x}"
            )
            self.addLink(host, switch)


def main():
    num_hosts = args.num_hosts

    topo = SinaTopo(
        args.behavioral_exe,
        args.json,
        args.thrift_port,
        args.pcap_dump,
        num_hosts,
    )
    net = Mininet(topo=topo, host=SinaHost, switch=P4Switch, controller=None)
    net.start()

    sw_mac = [f"00:aa:bb:00:00:{n:02x}" for n in range(num_hosts)]

    sw_addr = [f"10.0.{n}.1" for n in range(num_hosts)]

    for n in range(num_hosts):
        h = net.get(f"h{n + 1}")
        h.setARP(sw_addr[n], sw_mac[n])
        h.setDefaultRoute(f"dev eth0 via {sw_addr[n]}")

    for n in range(num_hosts):
        h = net.get(f"h{n + 1}")
        h.describe()

    sleep(1)

    print("Ready !")

    CLI(net)
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    main()
