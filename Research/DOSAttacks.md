# Dos Attacks
DoS attacks(denial-of-service) attack meant to shut down a machine or network, making it inaccessible to its intended users. DoS attacks accomplish this by flooding the target with traffic, or sending it information that triggers a crash. In both instances, the DoS attack deprives legitimate users of the service or resource they expected.
Though DoS attacks do not typically result in the theft or loss significant info or other assets, they can cost the victim a great deal of time and money to handle.
There are two general methods of DoS attacks: flooding services or crashing services

- Buffer overflow attacks
- ICMP flood
- SYN flood
  
Other DoS attacks simply exploit vulnerabilities that cause the target system or service to crash. In these attacks, input is sent that takes advantages of bugs in the target that subsequently crash or severely destabilize the system.

# DDoS Attacks
A DDoS attacks occurs when multiple systems orchestrate a synchronized DoS attack to a single target.
DDoS attacks have the following properties:
- Location of the attack is difficult to detect
- He can leverage the greater volume of machine to execute a seriously disruptive attack
- More difficult to shut down multiple machines than one

e.g The Google Attack in 2020, Security Reliability Engineering team in google measured a record-breaking UDP amplification attack sourced out of several Chinese ISPs, which remains the largest bandwidth attack.Mounted from three Chinese ISPs, the attack on thousands of Google’s IP addresses lasted for six months and peaked at a breath-taking 2.5Tbps! 


# How to prevent DoS attacks
- Monitor traffic
  - Organizations can enroll in a service that detects or redirects the abnormal traffic flows typically associated with a DoS attack, while allowing normal traffic to proceed on the network

- Load balancing
  - Distributing traffic across multiple servers, a DoS attack can be prevented from overwhelming a single server or resource. Load balancing can be achieved using hardware or software solutions

- IP blocking
  - Blocking traffic from known or suspected malicious sources can prevent DoS traffic from reaching its target

- Rate limiting
  - Limiting the rate of traffic to reach a server or resource can prevent a DoS attack from overwhelming it



