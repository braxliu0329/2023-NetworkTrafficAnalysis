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
