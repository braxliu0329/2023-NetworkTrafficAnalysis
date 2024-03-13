import binascii

from scapy.layers.dns import DNS
from scapy.layers.inet import IP, TCP, UDP
from scapy.all import *
from scapy.layers.inet6 import IPv6
from scapy.layers.l2 import ARP
import pandas as pd


from .Packet_Capture import *
# import Packet_Capture
from scapy.all import *


# object with commands accessible from the user interface
class GUIActions:
    def __init__(self):
        self.captured_packets = None
        self.running = True
        self.sniffer = Sniffer()

        self.protocols = {1: "ICMP",
                          2: "IGMP",
                          6: "TCP",
                          17: "UDP",
                          58: "ICMPv6"}

    # calls method to start sniffer
    def start_sniffer(self, status, window):
        self.sniffer.run_sniffer(status, window)

    # returns sniffed packets from sniffer
    def get_sniffed_packets(self):
        return self.sniffer.sniffed_packets

    # Method to filter collected packets,
    def filter_packets(self, protocol):
        filtered_packets = []
        sniffed_packets = self.get_sniffed_packets()
        self.sniffer.set_protocol(protocol)
        # if no filter specified returns all packets
        if protocol == "":
            self.sniffer.filtered_packets.clear()
            return sniffed_packets
        else:
            # checks if each packet has that protocol and appends to list if so
            for packet in sniffed_packets:
                if packet.haslayer(protocol):
                    filtered_packets.append(packet)
                    self.sniffer.filtered_packets = filtered_packets
            return filtered_packets

    def filter_packets_source_address(self, source_address):
        filtered_packets = []
        sniffed_packets = self.get_sniffed_packets()
        # if no filter specified returns all packets
        if source_address == "":
            self.sniffer.filtered_packets.clear()
            return sniffed_packets
        else:
            # Iterate through all sniffed packets and check if their source address matches the given address
            # Supports both IP and ARP packets
            for packet in sniffed_packets:
                if packet.haslayer(IP) and packet[IP].src == source_address:
                    filtered_packets.append(packet)
                elif packet.haslayer(ARP) and packet[ARP].psrc == source_address:
                    filtered_packets.append(packet)
            return filtered_packets

    def filter_packets_destination_address(self, destination_address):
        filtered_packets = []
        sniffed_packets = self.get_sniffed_packets()
        # if no filter specified returns all packets
        if destination_address == "":
            self.sniffer.filtered_packets.clear()
            return sniffed_packets
        else:
            # Iterate through all sniffed packets and check if their destination address matches the given address
            # Supports both IP and ARP packets
            for packet in sniffed_packets:
                if packet.haslayer(IP) and packet[IP].dst == destination_address:
                    filtered_packets.append(packet)
                elif packet.haslayer(ARP) and packet[ARP].pdst == destination_address:
                    filtered_packets.append(packet)
            return filtered_packets

    def filter_packet_combined(self, protocol, source_address, dst_address):
        filtered_packets = []
        sniffed_packets = self.get_sniffed_packets()
        self.sniffer.set_protocol(protocol)
        # If neither protocol nor source address is specified, return all sniffed packets
        if protocol == "" and source_address == "" and dst_address == "":
            filtered_packets = sniffed_packets

        # If only protocol is specified, filter packets by the specified protocol
        elif source_address == "" and dst_address == "":
            filtered_packets = self.filter_packets(protocol)

        # If only source address is specified, filter packets by the specified source address
        elif protocol == "" and dst_address == "":
            filtered_packets = self.filter_packets_source_address(source_address)

        # If only destination address is specified, filter packets by the specified source address
        elif protocol == "" and source_address == "":
            filtered_packets = self.filter_packets_destination_address(dst_address)

        elif protocol == "":
            filtered_packets_source = self.filter_packets_source_address(source_address)
            for packet in filtered_packets_source:
                if packet.haslayer(IP) and packet[IP].dst == dst_address:
                    filtered_packets.append(packet)
                elif packet.haslayer(ARP) and packet[ARP].pdst == dst_address:
                    filtered_packets.append(packet)

        elif source_address == "":
            filtered_packets_protocol = self.filter_packets(protocol)
            for packet in filtered_packets_protocol:
                if packet.haslayer(IP) and packet[IP].dst == dst_address:
                    filtered_packets.append(packet)
                elif packet.haslayer(ARP) and packet[ARP].pdst == dst_address:
                    filtered_packets.append(packet)

        elif dst_address == "":
            filtered_packets_protocol = self.filter_packets(protocol)
            for packet in filtered_packets_protocol:
                if packet.haslayer(IP) and packet[IP].src == source_address:
                    filtered_packets.append(packet)
                elif packet.haslayer(ARP) and packet[ARP].psrc == source_address:
                    filtered_packets.append(packet)
        else:
            filtered_packets_protocol = self.filter_packets(protocol)
            for packet in filtered_packets_protocol:
                ip_match = packet.haslayer(IP) and packet[IP].src == source_address and packet[IP].dst == dst_address
                arp_match = packet.haslayer(ARP) and packet[ARP].psrc == source_address and packet[ARP].pdst == dst_address

                if ip_match or arp_match:
                    filtered_packets.append(packet)
        return filtered_packets

    # Methods to read and write pcap files
    def read_pcap(self, file, window):
        self.sniffer.sniff_read(file, window)

    def write_pcap(self, filename):
        # writes each packet captured to a pcap file
        for packet in self.sniffer.sniffed_packets:
            if packet not in self.sniffer.ignored_packets:
                wrpcap(filename, packet, append=True)

    # returns protocol depending on protocol number
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
