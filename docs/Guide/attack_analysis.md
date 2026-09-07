# NTAnalyser
NTAnalyser is a lightweight tool designed for network engineers to analyse packet data efficiently. It provides various analysis options such as protocol, IPv4, IPv6, MAC, source, and destination analysis. Use NTAnalyser to gain insights into your network traffic and troubleshoot issues effectively.

To start NTAnalyser, firs start the server with `build.sh`, then run the main packet capturing tool with the `--analysis` argument. NTAnalyser should open as a local webpage in the background. To begin analysis of captured packets, press the *start analysis* button.

## Source/Destination Analysis
<img src="https://github.com/TomosSherlock/NetworkTrafficAnalysis/assets/123552121/bda4d6a1-8601-44da-ba72-82790a4e6710" alt="address graph" align="left" style="padding-right:30px"/>NTAnalyser can chart the addresses of connected devices within the network. It tracks three different address formats. If any format doesn't show a graph, the software has not found any devices with that address format. Every node is a different address. Every edge between a node means that these two addresses have communicated with each other. These graphs are undirected, so it is not indicated whether a node is the receiver, sender, or both. Hovering over a node will display its address. A link is indicative of if a connection between these addresses has been made, not the number of times they have communicated. 

### IPv4 Analysis
These graphs can grow quite large, so scrolling may be needed. It is usual for an IPv4 graph to be more dense than its IPv6 counterpart, though this is not always the case.

### IPv6 Analysis 
IPv6 nodes are shown. These graphs can also grow quite large, but are usually less dense than IPv4 graphs.

### MAC Analysis
A visualisation of MAC nodes. A MAC graph is generally more sparse than an IPv6 or IPv4, since network interfaces may have multiple IPs, but will have only one MAC address.

## Frequency Analysis
The total number of captured packets packets is graphed for different protocols, source addresses and destination addresses:
![image](https://github.com/TomosSherlock/NetworkTrafficAnalysis/assets/123552121/e4f96f41-8aa3-4abf-8918-470077ee336d)
![image](https://github.com/TomosSherlock/NetworkTrafficAnalysis/assets/123552121/ef9bcabe-a599-4dab-867f-40e2b3afdddc)

## Attack Analysis
Captured packets can be scanned for potential cyberattacks. If an attack analysis finds the provided packets suspicious, it will generally mark the suspicious addresses and explain why they were marked as suspicious. Relevant graphs are also shown. Some analyses require a threshold. These thresholds have default values, and can be edited using the `configure analysis` button in the main GUI.

### ARP Poison
![image](https://github.com/TomosSherlock/NetworkTrafficAnalysis/assets/123552121/fb9451e8-1da2-4a6b-b565-2c7ebe03c239)

This analysis scans packets for signs of an ARP poisoning attack. Suspicious addresses are marked because the MAC addresses they originated from are associated with more than one IP address, which is erroneous and indicative of ARP Poisoning.

### TCP SYN Flood
![image](https://github.com/TomosSherlock/NetworkTrafficAnalysis/assets/123552121/bab52469-0fa6-4d47-aea7-73a8a26d1da4)

Scans for signs of a TCP SYN Flooding attack. Suspicious addresses are marked because they addresses send a greater amount of SYN requests than they receive SYN-ACK responses back, suggesting they are overloading asystem. The attacked addresses are marked because they  receive a greater amount of SYN requests than they send SYN-ACK responses back, which is indicative that these addresses are being overwhelmed by SYN requests and cant response fast enough.

### TCP Connect Scanning
![image](https://github.com/TomosSherlock/NetworkTrafficAnalysis/assets/123552121/28fc22cb-0c0d-4c55-bfd9-f4d9f0a0a792)

Scans packets for signs of a TCP Connection attack. Addresses are marked as suspicious if the address sends SYN flags without receiving SYN-ACK packets and if the same address sends more SYN packets than the within the time interval.

### DoS Detection
![image](https://github.com/TomosSherlock/NetworkTrafficAnalysis/assets/123552121/e9a57406-764e-4cf2-82cb-c2e3f37c8bb3)

Detects Denial of Service attacks by analysing the quantity of data packets sent by addresses. Suspicious addresses send a greater amount of traffic than the given threshold.

### HTTP Flood
![image](https://github.com/TomosSherlock/NetworkTrafficAnalysis/assets/123552121/eec089da-095f-4d39-96ed-e01860a85851)

Detects HTTP Flood attacks by analysing HTTP request packets. Suspicious addresses are marked because the HTTP Request packets sent from the addresses after a tcp connection is established are too high frequency.

### DNS Flood
![image](https://github.com/TomosSherlock/NetworkTrafficAnalysis/assets/123552121/bf4658c6-3c8e-48e1-b6f8-c7746c14a8c5)

Detects DNS Flood attacks by analysing DNS packets. Suspicious addresses are marked because the DNS packets sent from the addresses are too high frequency.

### SSL Stripping
![image](https://github.com/TomosSherlock/NetworkTrafficAnalysis/assets/123552121/8fe22074-8a09-4cef-b6da-ded4fa4fd6be)

Detects SSL Stripping attacks by analysing the frequency of SSL packets. Addresses are marked as suspicious source or destination addresses if they send/recieve more SSL packets than the provided threshold.

### UDP Flood
![image](https://github.com/TomosSherlock/NetworkTrafficAnalysis/assets/123552121/2ec9f644-c31f-4d11-9024-cf88a3bc30ac)

Detects UDP Flood attacks by analysing UDP packets. Addresses are marked as suspicious because the UDP packets sent from the addresses are too high frequency.

## Shutdown
The analyser can be manually shut down by navigating to the shutdown tab and refreshing the webpage.
