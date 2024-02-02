# New Attack Methods
## UDP flood
Similar to ICMP flood, this involves overwhelming random ports on a remote host with a flood of User Datagram Protocol (UDP) packets, leading to denial of service.
- ### Prevention
Implement rate limiting, configure routers and firewalls to filter unnecessary traffic, and use IDS/IPS for detection and mitigation.

## DNS amplification
This is a reflection-basedDDoS attack in which the attacker exploits vulnerabilities in the domain name system (DNS) server to turn initially small queries into much larger payloads, thereby overwhelming the target with a high volume of traffic.
- ### Prevention
configure DNS servers to restrict recursive queries, implement  rate limiting and monitor for unusual DNS traffic

## SYN Flood
A SYN Flood attack is characterized by a high volume of TCP SYN packets directed at a target's port. 
- ### Prevention
Look for an unusually high number of TCP SYN packets (where the SYN flag is set but the ACK flag is not) compared to SYN-ACK packets.Analyze the distribution of source IPs. In some cases, SYN Flood attacks may originate from a limited set of IPs or use spoofed IP addresses.

## SSL Stripping
SSL Stripping involves downgrading HTTPS connections to HTTP.
- ### Prevention
Look for HTTP traffic on ports typically used for HTTPS (e.g., port 443). If there is HTTP traffic where you would expect HTTPS, it could be a sign of SSL Stripping.

## Packet Injection
Packet Injection involves inserting malicious packets into normal network traffic. 
- ### Prevention
Look for packets that do not fit the normal pattern of your network traffic. This might include unusual packet sizes, unexpected protocols, or strange payload data.
Repeated occurrences of specific packets or payloads that seem out of place can indicate injection.
