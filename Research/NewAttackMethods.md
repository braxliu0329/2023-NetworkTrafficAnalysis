# New Attack Methods
## UDP flood
Similar to ICMP flood, this involves overwhelming random ports on a remote host with a flood of User Datagram Protocol (UDP) packets, leading to denial of service.
- ### prevention
Implement rate limiting, configure routers and firewalls to filter unnecessary traffic, and use IDS/IPS for detection and mitigation.

## DNS amplification
This is a reflection-basedDDoS attack in which the attacker exploits vulnerabilities in the domain name system (DNS) server to turn initially small queries into much larger payloads, thereby overwhelming the target with a high volume of traffic.
- ### prevention
configure DNS servers to restrict recursive queries, implement  rate limiting and monitor for unusual DNS traffic

## SYN Flood

## SSL Stripping

## Packet Injection
