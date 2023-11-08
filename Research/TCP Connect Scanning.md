# TCP Connect Scanning:
TCP connect scanning is a network reconnaissance technique used by attackers to identify open ports on a target system. 
In a TCP connect scan, the attacker attempts to establish a full TCP connection with the target's ports to determine which ones are actively listening and, therefore, potentially vulnerable.

  - ## Outline
    In a TCP connect scan, the attacker initiates a standard three-way handshake by sending a TCP SYN (synchronize) packet to the target.
    If the port is open, the target responds with a SYN-ACK (synchronize-acknowledge) packet.
    The attacker then sends an ACK (acknowledge) packet to complete the handshake.
    By analyzing the responses, the attacker can identify open ports where the target system is actively accepting connections.
    Open ports often correspond to running services or applications.
  
  - ## Methods of Preventing TCP Connect Scanning:
  
    - ### Firewall configuration
      Use firewalls to restrict incoming connection requests to essential services.  
      Configure firewalls to block or log excessive connection attempts.
    - ### Intrusion Detection and Prevention Systems (IDPS)
      Implement IDPS solutions to detect and respond to patterns indicative of TCP connect scanning.  
      Set up alerting mechanisms for suspicious connection activities.
    - ### Rate Limiting
      Employ rate-limiting measures on network devices to control the rate of connection attempts.  
      Throttle or block repeated connection requests from the same source.
    - ### Network Segmentation
      Segment the network to limit the impact of successful scanning on specific areas.  
      Isolate critical systems from less critical ones.


