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
  To be discussed with Synoptix

## Group Members
  - Ani Boja
  - Tony Liu
  - Tomos Sherlock
  - Joe Dobson

## Supporting Mentor
  - Oliver Gay

## User Stories
  1. As the Synoptix information technology apartment:
     - I want an automated system for monitoring and analyzing clients' private networks.
     - The purpose is to check if data is being stolen or abused.
     - The primary goal is to safeguard the network from potential threats.
  2. As a Synoptix client:
     - I want my network been carefully analysed.
     - I wish for the reporting of potential threats.
     - The objective is to ensure the security and smooth operation of my network.
  3. As a network engineer:
     - I want a useful network analysis tool with an intuitive GUI.
     - The purpose is to provide an interface to be able to dynamically capture, filter and sort packets.
     - The primary goal is to be able to monitor and report suspicious packets within a network to direct investigations into the network's security.
## Minimum Viable Product Requirements  
 - The capabilities and features of the existing solution are preserved
 - The code is well documented and commented
 - The project's GUI is made more intuitive and organised
 - Support for protection against a new form of cyberattack

## Setup instruction for development
### Prerequisites

- Clone GitHub repository with the following command
```
git clone https://github.com/spe-uob/2022-NetworkTrafficAnalysis.git
```

#### Windows
- Download [Python](https://www.python.org/downloads/)
- Check the python version with command (<3.9 recommended)
```
python --version
```

- Download Python libraries Scapy, Npcap, Pyqt5, MatPlotLib, pandas, and networkx with the command
```
pip install Scapy
pip install Npcap
pip install Pyqt5
pip install matplotlib
pip install pandas  
pip install networkx
```
Or download [Scapy and Npcap](https://scapy.readthedocs.io/en/latest/installation.html) with this link


#### MacOS - Intel
- Download [Python](https://www.python.org/downloads/)

- Download library dependencies with the following command
```
pip install -r requirements.txt
```

#### MacOS - Arm64 (M1 / M2)
*The Scapy library is currently unavailable with local machine itself.*

- Download [Anaconda](https://www.anaconda.com/download/)

- Create a virtual enviroment
```
conda create -n <Environment name> python=<Version>
```
- Check if the environment is initialised
```
conda env list
```
- Activate the environment
```
activate <Environment name>
```
or
```
source activate <Environment name>
```

- Download library dependencies with the following command
```
pip install -r requirements.txt
```


_When finished running the program, don't forget to deactivate the virtual environment._
```
deactivate
```

## Deployment Instructions

- Run main.py with command
```
python code/pythonGUI/main.py
```

_(MacOS) When prompted to configure Python interpreter, select conda interpretor_

## License
  To be discussed with Synoptix
