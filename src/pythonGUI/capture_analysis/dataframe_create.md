# Dataframe create
Defines a class named `DataframeCreate`, aimed at creating a Pandas DataFrame from packets parsed by Scapy
for further analysis of network traffic. 

## Dependencies
```cython
         import matplotlib.pyplot as plt
         import pandas as pd
         import networkx as nx
         from scapy.layers.dns import DNS
         from scapy.layers.inet import IP, TCP, UDP, ICMP
         from scapy.layers.inet6 import IPv6
         
         from scapy.layers.l2 import ARP, Ether
         from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
         from scapy.packet import Raw
```
 - pandas - Utilized for structuring, manipulating, and analyzing the network packet data extracted by Scapy, 
 typically using DataFrame objects for efficient data handling.

 - scapy.layers.dns/inet/inet6 - Essential for parsing and manipulating network packets directly from pcap files or live network traffic, 
 extracting various protocol layers (IP, TCP, UDP, ICMP, etc.), and other packet details.

 - FigureCanvasQTAgg - It's used to integrate Matplotlib plots into a Qt5 application GUI, allowing for dynamic and interactive data visualization within the application.

 - Raw - Used to access and possibly manipulate the raw payload data of packets, which can be critical for analyzing packet contents beyond the standard protocol headers.

## Class Initialization Method
```cython
class DataframeCreate:
    def __init__(self, data):
        self.protocols = {1: "ICMP",
                          2: "IGMP",
                          6: "TCP",
                          17: "UDP",
                          58: "ICMPv6"}
        self.data_frame = self.create_data(data)
```
- `self.protocols`: A dictionary mapping protocol numbers to their corresponding string representations.

- `self.data_frame`: Generates a DataFrame using the `create_data` method, which takes a list of packets data as input.

## Create Data
```cython
         def create_data(self, packets):
             data = {"Number": [], "Time": [], "SourceMac": [], "DestMac": [], "IP_Version": [],
                     "SourceIP": [], "DestIP": [], "Protocol": [], "TCP_Flags" : [], "op" : [],
                     "hwsrc" : [], "ICMP_Type": [], "DNS_Type": [], "raw": [],
                     "SourcePort": [], "DestinationPort": []}
```
- Initializes a dictionary data containing multiple empty lists, which will serve as columns for the `DataFrame`. 
These include packet number, time, source/destination MAC addresses, IP version, source/destination IP addresses, 
protocol type, TCP flags, opcode, hardware source address, ICMP type, DNS type, raw payload data, source port, 
and destination port.
```cython
         for packet in packets:
             data["Number"].append(packet_number)
             if packet.haslayer(IP):
                 version = IP
             elif packet.haslayer(IPv6):
                 version = IPv6
             else:
                 version = ARP
```
- Iterates through each packet, populating the appropriate lists in the data dictionary based on the layers present in the packet 
```cython
         data["Time"].append(packet.time)
         if packet.haslayer(Ether):
             data["SourceMac"].append(packet.getlayer(Ether).src)
             data["DestMac"].append(packet.getlayer(Ether).dst)
             
         else:
             data["SourceMac"].append(None)
             data["DestMac"].append(None)
             
         if version == IP or version == IPv6:
             data["SourceIP"].append(packet.getlayer(version).src)
             data["DestIP"].append(packet.getlayer(version).dst)
             
             if version == IP:
                 data["IP_Version"].append("IPv4")
                 data["Protocol"].append(str(self.get_protocol(packet.getlayer(IP).proto, packet)))
                 
             elif version == IPv6:
                 data["IP_Version"].append("IPv6")
                 data["Protocol"].append(str(self.get_protocol(packet.getlayer(IPv6).nh, packet)))
             data["op"].append(None)
             data["hwsrc"].append(None)
             
         elif version == ARP:
             data["SourceIP"].append(packet.getlayer(ARP).psrc)
             data["DestIP"].append(packet.getlayer(ARP).pdst)
             data["Protocol"].append("ARP")
             data["op"].append(packet.getlayer(ARP).op)
             data["hwsrc"].append(packet.getlayer(ARP).hwsrc)
             data["IP_Version"].append(None)
```
- Determines how to extract source IP, destination IP, protocol, etc., based on whether the packet contains an IP, IPv6, or ARP layer.
```cython
         if packet.haslayer(TCP):
             tcp_layer = packet[TCP]
             data["TCP_Flags"].append(tcp_layer.flags)
             data["SourcePort"].append(tcp_layer.sport)
             data["DestinationPort"].append(tcp_layer.dport)
         
             if packet.haslayer(Raw):
                 data["raw"].append(packet[Raw].load)
             else:
                 data["raw"].append(None)
         else:
             tcp_layer = packet[TCP]
             data["TCP_Flags"].append(None)
             data["raw"].append(None)
             data["DestPort"].append(None)
```
- Extracts TCP flags and destination port for packets with a TCP layer

- Extracts the raw payload if the packet contains a Raw layer; otherwise, sets the raw payload column to None.
```cython
         if packet.haslayer(ICMP):
             data["ICMP_Type"].append(packet[ICMP].type)
         else:
             data["ICMP_Type"].append(None)

         if packet.haslayer(DNS):
             data["DNS_Type"].append(packet[DNS].qr)
         else:
             data["DNS_Type"].append(None)
```
- Extracts ICMP type and DNS type based on whether the packet contains the corresponding layer.

## Get Protocol
```cython
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
```
- Accepts a protocol number and a packet as parameters and returns the string representation of the protocol. 
If the protocol number is in the self. protocols dictionary, it returns the corresponding string; otherwise, 
it returns the string form of the protocol number.

- If the protocol is UDP and the packet contains a DNS layer, it returns "UDP/DNS" to indicate DNS traffic.

