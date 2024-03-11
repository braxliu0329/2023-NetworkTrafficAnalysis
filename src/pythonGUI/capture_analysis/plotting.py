import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import json
from scapy.layers.dns import DNS
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.inet6 import IPv6
from scapy.layers.l2 import ARP, Ether
import numpy as np

from pythonGUI.capture_analysis import dataframe_create


class Plotting:
    def __init__(self, data):
        dataframe_creator = dataframe_create.DataframeCreate(data)
        self.data_frame = dataframe_creator.data_frame

    def write_json(self, network, mode):
        nodes = []
        links = []
        for n in network.nodes():
            nodes.append({
                "id": n,
                "size": 24
            })
        for e in network.edges():
            links.append({
                "source": e[0],
                "target": e[1],
                "distance": 100
            })
        data = {
            "nodes": nodes,
            "links": links
        }
        with open(f"src/pythonGUI/plotData/{mode}.json", "w+") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def write_frequency_json(self, mode):
        keys = self.data_frame[mode].value_counts().keys()
        values = self.data_frame[mode].value_counts().values
        data = []
        if keys is not None and values is not None:
            for i in range(len(keys)):
                if mode == "SourceIP":
                    data.append({
                        "source": keys[i],
                        "frequency": int(values[i])
                    })
                elif mode == "DestIP":
                    data.append({
                        "dest": keys[i],
                        "frequency": int(values[i])
                    })
                elif mode == "Protocol":
                    data.append({
                        "protocol": keys[i],
                        "frequency": int(values[i])
                    })
                if mode == "Protocol":
                    data = {
                        "data": data
                    }
            with open(f"src/pythonGUI/plotData/{mode}.json", "w+") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
    
    def run_all(self):
        self.write_frequency_json("Protocol")

        ipv4_addresses = self.data_frame[self.data_frame["IP_Version"] == "IPv4"]
        # uses connections between source ip and destination ip to form edges
        network = nx.from_pandas_edgelist(ipv4_addresses, source='SourceIP', target='DestIP')
        self.write_json(network, "ipv4")

        ipv6_addresses = self.data_frame[self.data_frame["IP_Version"] == "IPv6"]
        network = nx.from_pandas_edgelist(ipv6_addresses, source='SourceIP', target='DestIP')
        self.write_json(network, "ipv6")
        # Remove all None entries from data_frame
        filtered_df = self.data_frame[~self.data_frame['SourceMac'].isnull()]
        network = nx.from_pandas_edgelist(filtered_df, source="SourceMac", target="DestMac")
        self.write_json(network, "mac")

        self.write_frequency_json("SourceIP")

        self.write_frequency_json("DestIP")

    

    def get_protocol(self, protocol, packet):
        if protocol in self.protocols.keys():
            protocol_name = self.protocols[protocol]
            # packets can have UDP and DNS layers
            if protocol_name == "UDP" and packet.haslayer(DNS):
                return "UDP/DNS"
            else:
                return protocol_name
        else:
            return protocol
