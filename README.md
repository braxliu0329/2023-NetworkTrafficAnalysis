## Table of Contents
  - [Project Description](#project-description)
  - [Requirements](#requirements)
  - [Stakeholders](#stakeholders)
  - [Group Members](#group-members)
  - [Supporting Mentor](#supporting-mentor)
  - [User Stories](#user-stories)
  - [Setup Instructions](#setup-instruction-for-development)
  - [Deployment Instructions](#deployment-instructions)
  - [License](#license)

## Project Description
  This project builds upon last year's Network Traffic Analysis, optimising their implementations of packet sniffing. The project as it existed last year was capable of detecting numerous attack methods,
  but with other methods becoming more prominent, this project aims to expand the scope of the previous version. This includes the development and optimisation of a pack sniffing tool for analysis of traffic patterns (including, but not exhaustive, of ARP poisoning, TCP SYN Flood, ICMP Flood and DoS attacks).

## Requirements
 - A working, better optimised version of the existing project designed to monitor data traffic across a network
 - Interception and logging of data packets
 - Analysis of data with consideration of previously unimplemented attack methods
 - An interactive, intuitive GUI

## Stakeholders
  Louis and Synoptix - Acting as the client behind this project and its main user. They will be expecting a system that allows monitoring and analysis of data packets over provided networks. They require a final, robust program that will allow them to test their network security by periodically scanning packets for any cyberattacks the company isn't aware of.

## Group Members
  - Ani Boja
  - Tony Liu
  - Tomos Sherlock
  - Joe Dobson

## Supporting Mentor
  - Oliver Gay

## User Stories
  - As the Synoptix information technology apartment, I want an automated system for monitoring and analyzing clients' private networks, so that I can check if data is being stolen or abused. My primary goal is to safeguard the network from potential malicious attacks.
  - As a Synoptix client, I want my network to be carefully analysed for potential threats, so that, in the case that the program detects an ongoing attack, the security is further escalated and IT is notified. I would like to use the program on our testing network in a passive way, the program will passively  monitor the network to automatically identify any ongoing network attacks that we are not aware of
  - As an experienced network analyst, I want to be able to scan a testing network in an active way, so that I can respond if we suspect there is some form of ongoing attack.
  - As a network engineer, I want a useful network analysis tool with an intuitive GUI, so that I can effectively use the interface to be able to dynamically capture, filter and sort packets. My primary goal is to be able to monitor and report suspicious packets within a network to direct investigations into the network's security.

## Minimum Viable Product Requirements  
 - The capabilities and features of the existing solution are preserved.
 - The code is well documented and commented.
 - The project's GUI is made more intuitive and organised.
 - The existing product is recreated in a different, better optimised language.

## Setup instruction for development
### Prerequisites

- Clone GitHub repository with the following command
```
git clone https://github.com/spe-uob/2023-NetworkTrafficAnalysis.git
```

#### Windows
- Download [Python](https://www.python.org/downloads/)
- Check the Python version with command (<3.9 recommended) and download Python libraries Scapy, Npcap, Pyqt5, MatPlotLib, pandas, and networkx with the command
```
python --version
pip install Scapy
pip install Pyqt5
pip install matplotlib
pip install pandas  
pip install networkx
```
Or download Scapy (https://scapy.readthedocs.io/en/latest/installation.html) with this link

- Download Npcap (https://npcap.com/#download) with this link


#### MacOS - Intel
- Download [Python](https://www.python.org/downloads/)

- Download library dependencies with the following command
```
pip install -r requirements.txt
```

#### MacOS - Arm64 (M1 / M2)
*The Scapy library is currently unavailable with local machine itself.*

- Download [Anaconda](https://www.anaconda.com/download/), create a virtual environment and download dependencies.
```
conda create -n <Environment name> python=<Version>
conda env list
activate <Environment name>
pip install -r requirements.txt
```


_When finished running the program, don't forget to deactivate the virtual environment using `deactivate`._

## Deployment Instructions

- Run main.py with command
```
python src/main.py
```

_(MacOS) When prompted to configure Python interpreter, select conda interpreter_

## License
Distributed under a *MIT License*
