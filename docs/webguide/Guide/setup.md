## Setup instructions
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

- In the root directory, run the build script
```
./build.sh
```

- Then run the shell script called nta
```
./nta.sh
```
- Use --help for usage instructions
```
./nta.sh --help
```
- To Use the CLI file analysis tool, navigate to `src` and run pcapAnalysis as follows:
```
cd src
./pcap_analysis
```
(Usage instructions should be explained by the command line)

_(MacOS) When prompted to configure Python interpreter, select conda interpreter_
