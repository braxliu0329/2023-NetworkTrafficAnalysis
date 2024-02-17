from scapy.all import *

# Target IP address and port
source_ip = '123.123.123.123'
target_ip = "10.0.0.2"  # Example IP, replace with your target IP
target_port = 80  # modify as needed

# Constructing UDP flood packets
packet_count = 10000  # Number of packets to send, adjust as necessary
packets = []

for i in range(packet_count):
    packet = IP(src=source_ip, dst=target_ip) / UDP(dport=target_port)  # Constructing a UDP packet with random data
    packets.append(packet)

# Saving to a pcap file
save_file = "../test_pcaps/udp_flood.pcap"
wrpcap(save_file, packets)

print(f"Generated a pcap file containing {packet_count} UDP flood attack packets: {save_file}")
