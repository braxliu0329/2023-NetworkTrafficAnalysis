# ARP Poisoning
_Address Resolution Protocol (ARP) Poisoning_, also known as _ARP Spoofing_, is a cyber attack where malicious _ARP packets_ are sent across a _Local Area Network (LAN)_ in an attempt to disrupt the network's _IP to MAC address table_.

## Threats

- Very easy to carry out 
    - the ARP protocol was designed for efficiency over security
    - the attacker only needs to have access to a machine within the LAN
- After the attack is carried out, all of the network's traffic between devices travels through the attacking computer
    - since these attacks occur on such a low level, users often don't realise they have been targeted by an ARP poisoning attack
    - ARP poisoning often leads to Man-in-the-Middle attacks
- ARP Poisoning can also be used to cause a denial-of-service condition by refusing to forward the target's packets to the network

## Prevention
ARP poisoning can be detected via a variety of softwares.
 - on most systems, the _"arp -a"_ command will display the current IP-to-MAC address table
 - tools such as X-ARP and arpwatch can be used to continuously monitor the network and alert the admin of signs of an ARP Poisoning attack
    - *might result in a false positive*

There are also several approaches to prevent these attacks:
 - By statically mapping all MAC addresses in a LAN to their respective IP addresses, these attacks are very effectively snuffed out
    - this is very administration-heavy, however
    - any change to the LAN will require manual updates of the ARP tables across _all_ hosts
 - Since ARP packets don't travel outside of the LAN, segmenting a network can result in less damaging ARP attacks.
  - Encryption can be used to mitigate the damage from ARP Poisoning attacks
    - a common result of Man-in-the-Middle attacks is the recording of passwords and sensitive information which, if encrypted, is less useful
 - By physically controlling who has access to devices in the LAN, ARP Poisoning attacks can be prevented as access to a device on the LAN is required
  - Ethernet switches often have built-in features to protect against ARP Poisoning
    - _Dynamic ARP Inspection (DAI)_ can be found on most modern switches
    - the validity of each ARP packet is checked, and packets that appear malicious are dropped
    - port security should also be enabled