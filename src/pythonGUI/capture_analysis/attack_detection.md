# Attack Detection
Attack Detection is the main file responsible for analysing captured data packets for cyberattacks. It is tested by
`attack_analysis_tests.py` interacts with the GUI with files such as `dataframe_create.py` to display its analyses.
## Dependencies
```
import numpy as np
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import dataframe_create
```
Attack detection imports the following libraries and code:
 - numpy - allows for faster mathematical operations across the many data packets analysed.
 - pandas - used to package dataframes for use by `dataframe_create.py`
 - matplotlib - an object-oriented plotting library used to initialise graphs used by `dataframe_create.py` to display analyses.
 - dataframe_create - another file made for this project used to display attack analysis data.

## Embedded Canvas
```
# small object used to create embedded graphs onto GUI
class EmbeddedCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # set graph parameters and data to initialise the embedded graph
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(EmbeddedCanvas, self).__init__(fig)
```
`EmbeddedCanvas` initialises a Figure for use by `dataframe_create.py`.

## Attack Detection
`AttackDetection` is a class that wraps around all the detection methods within this file.
```
class AttackDetection:
    # initialise attack detection variables
    def __init__(self, data, flagged_IPs):
        # initialise all flagged ip addresses as empty
        self.arp_suspicious_addresses = None
        self.icmp_suspicious = None
        self.dns_response_suspicious = None
        self.dns_request_suspicious = None
        self.dos_suspicious_addresses = None
        self.http_suspicious = None
        self.tcp_suspicious_addresses = None
        self.tcp_scanning_suspicious = None
        
        # initialise quarantined packets as empty
        self.quarantined_packets = None
        
        # create a dataframe with the attack analysis data
        dataframe_creator = dataframe_create.DataframeCreate(data)
        self.dataframe = dataframe_creator.data_frame

        # initialise all general addresses
        self.blocked_addresses = []
        self.suspicious_addresses = flagged_IPs
        self.attacked_addresses = []
        
        # initialise the packets to the provided data
        self.packets = data

    # updates this class' flagged ip addresses with any new ips in the provided list of addresses
    def update_flagged_ips(self, ips):
        for ip in ips:
            if ip not in self.suspicious_addresses:
                self.suspicious_addresses.append(ip)
```
`__init__` defines how the class initialises itself. This class keeps track of resulting IP addresses from all attack analyses, along with quarantined packets, dataframes for representing results and the provided packets. Most of these are initialised to empty arrays or default values, with the exception of the data frame, flagged IPs and packets, which are set to their passed parameters.

`update_flagged_ips` is a function that uses the provided list of flagged IPs and updates the currently stored list of flagged IPs with any new additions.