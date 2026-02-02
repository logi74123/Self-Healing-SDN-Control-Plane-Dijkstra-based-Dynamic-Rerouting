from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr, IPAddr
from collections import defaultdict
from copy import deepcopy
import os
import csv

log = core.getLogger()
delayFile = "delay.csv"

hosts = {'h1': ('10.0.0.1', '00:00:00:00:00:01'), 'h2': ('10.0.0.2', '00:00:00:00:00:02')}
host_to_switch = {'h1': 's1', 'h2': 's5'}

linkNames = {
	'g': ('s1', 's2'),
	'h': ('s1', 's3'),
	'i': ('s2', 's4'),
	'j': ('s4', 's5'),
	'k': ('s3', 's5'),
	}

portMappings = {
	's1': {'h1': 1, 's2': 2, 's3': 3},
	's2': {'s1': 1, 's4': 2},
	's3': {'s1': 1, 's5': 2},
	's4': {'s2': 1, 's5': 2},
	's5': {'h2': 1, 's4': 2, 's3': 3},
	}

class Dijkstra(EventMixin):
    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Enabling Dijkstra Module")
        self.delays = {}
        self.switches = set()
        self.neighbors = defaultdict(set)

        with open(delayFile, 'r') as csvfile:
            links = csv.reader(csvfile)
            next(links)
            for linkName, delay in links:
                s1, s2 = linkNames[linkName]
                self.delays[(s1, s2)] = int(delay)
                self.delays[(s2, s1)] = int(delay)
                self.switches.add(s1)
                self.switches.add(s2)
                self.neighbors[s1].add(s2)
                self.neighbors[s2].add(s1)

    def _dijkstra(self, source):
        distances = defaultdict(lambda: float('inf'))
        distances[source] = 0
        previous = {}
        unseen = deepcopy(self.switches)
        while unseen:
            u = min(unseen, key=lambda x: distances[x])
            unseen.remove(u)
            for v in self.neighbors[u]:
                alt = distances[u] + self.delays[(u, v)]
                if alt < distances[v]:
                    distances[v] = alt
                    previous[v] = u
        return distances, previous

    def _getPortMapping(self, source):
        distances, previous = self._dijkstra(source)
        ports = {}
        for h_name, s_name in host_to_switch.items():
            destSwitch = s_name
            if source == destSwitch:
                ports[h_name] = portMappings[source][h_name]
                continue
            
            # --- ADD THIS LOGGING LOGIC ---
            path = [destSwitch]
            curr = destSwitch
            while source != previous[curr]:
                curr = previous[curr]
                path.append(curr)
            path.append(source)
            path.reverse()
            log.info("Path from %s to %s: %s", source, h_name, " -> ".join(path))
            # ------------------------------

            ports[h_name] = portMappings[source][curr]
        return ports

    def _handle_ConnectionUp(self, event):
        switch = 's' + str(event.dpid)
        
        # 1. ADD THIS ARP RULE:
        # This tells the switch: "If you see ARP (0x0806), send it to all ports."
        msg_arp = of.ofp_flow_mod()
        msg_arp.match.dl_type = 0x0806 
        msg_arp.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
        event.connection.send(msg_arp)

        # 2. Keep your existing Dijkstra logic below:
        ports = self._getPortMapping(switch)
        for host, (ip, mac) in hosts.items():
            port = ports[host]
            msg = of.ofp_flow_mod()
            msg.match.dl_dst = EthAddr(mac)
            msg.actions.append(of.ofp_action_output(port=port))
            event.connection.send(msg)
            
        log.debug("Dijkstra installed on %s", dpidToStr(event.dpid))
def launch():
    core.registerNew(Dijkstra)
