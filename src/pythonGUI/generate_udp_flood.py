from scapy.all import *

# 目标IP地址和端口
source_ip = '123.123.123.123'
target_ip = "10.0.0.2"  # 示例IP，请替换成你的目标IP
target_port = 80  # 示例端口，请根据需要修改

# 构造UDP洪水包
packet_count = 10000  # 发送包的数量，根据需要调整
packets = []

for i in range(packet_count):
    packet = IP(src=source_ip, dst=target_ip) / UDP(dport=target_port)  # 构造包含随机数据的UDP包
    packets.append(packet)

# 保存到pcap文件
save_file = "../test_pcaps/udp_flood.pcap"
wrpcap(save_file, packets)

print(f"已生成包含{packet_count}个UDP洪水攻击数据包的pcap文件：{save_file}")
