from scapy.all import *
from scapy.layers.http import HTTPRequest
from scapy.layers.inet import IP, TCP

def generate_ssl_stripping_pcap(file_name="ssl_stripping.pcap"):
    packets = []

    # source ip address and destination ip address
    src_ip = "192.168.1.100"
    dst_ip = "192.168.1.1"

    # Create simulated HTTP traffic on port 443
    # Create 1000 packets
    for i in range(1000):
        packet = (IP(src=src_ip, dst=dst_ip) /
                  TCP(sport=12345, dport=443) /
                  HTTPRequest(
                      Method="GET",
                      Host="example.com",
                      Path="/",
                  ))
        packets.append(packet)

    # Write the generated packets into a PCAP file
    wrpcap(file_name, packets)

    print(f"Generated PCAP file {file_name} containing simulated SSL stripping traffic.")

# Invoke the function to generate the PCAP file
generate_ssl_stripping_pcap()
