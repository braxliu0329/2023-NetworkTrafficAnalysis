## ICMP Floods
 - ## Outline
     An ICMP (ping) flood, is a DoS attack in which an attack attempts to overwhelm a system with ICMP echo-requests.
     Normally, ICMP echo-request and echo-reply messages are used to ping a network device in order to diagnose the health and connectivity of the device and the connection between       the sender and the device. By flooding the target with request packets, the network is forced to respond with an equal number of reply packets. This causes the target to become
     inaccessible to normal traffic.
  - ## What is ICMP (briefly)
    ICMP is a supporting internet protocl that differs from TCP and UDP, in that the latter protocols are used to exchange data between systems. Instead,
    ICMP is used for diagnostic purposes, sending error messages and requesting that the data be resent.
  - ## Detecting ICMP floods
    Ping floods are easier to detect based on the volume of ICMP traffic.
  - ## Mitigating ICMP floods
    - Traffic Rate limiting: Set a maximum number of ICMP echo requests that can be processed at any given time.
    - ICMP Protocol Blocking: Potentially a final effort in stopping an attack, blocking ICMP outright will stop the attack at the cost of being
      unable to troubleshoot legitimate issues with devices.
    - Blackhole Filtering: Routers and Firewalls can automatically detect requests from known DDoS botnets, and silently discard the requests.
   
      
  
