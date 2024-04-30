from scapy.all import *
import time

# Target IP address and port
source_ip = '123.123.123.123'
target_ip = "10.0.0.2"  # Example IP, replace with your target IP
target_port = 80  # modify as needed

# Constructing UDP flood packets
packet_count = 10000  # Number of packets to send, adjust as necessary
packets_per_second = 1000
packets = []
start_time = time.time()

for i in range(packet_count):
    # Calculate the time to wait before sending the next packet to achieve desired packets per second
    time_to_wait = (start_time + (i + 1) / packets_per_second) - time.time()
    if time_to_wait > 0:
        time.sleep(time_to_wait)

    # Constructing a UDP packet with random data and current timestamp
    packet = IP(src=source_ip, dst=target_ip) / UDP(dport=target_port) / Raw(RandString(size=128))
    packets.append(packet)

# Saving to a pcap file
save_file = "../../test_pcaps/udp_flood2.pcap"
wrpcap(save_file, packets)

print(f"Generated a pcap file containing {packet_count} UDP flood attack packets at {packets_per_second} packets per second: {save_file}")
