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
`__init__` defines how the class initialises itself. This class keeps track of resulting IP addresses from all attack analyses, along with quarantined packets, dataframes for representing results and the provided packets. Most of these are initialised to empty arrays or default values, except for the data frame, flagged IPs and packets, which are set to their passed parameters.

`update_flagged_ips` is a function that uses the provided list of flagged IPs and updates the currently stored list of flagged IPs with any new additions.

### TCP Flood Detect
`tcp_flood_detect` scans all provided TCP packets for signs of a TCP Flood Attack. It is expected that the number of SYN packets on a network is around equal to the number of SYN-ACK packets. A disproportionately large number of SYN packets in comparison to SYN-ACK packets is evidence of a TCP Flood Attack.
```
  def tcp_syn_flood_detect(self):
        # creates canvas
        canvas = EmbeddedCanvas(self)

        # initialises suspicious address lists
        self.tcp_suspicious_addresses = []
        self.attacked_addresses = []

        # filters non-TCP packets out of dataframe
        tcp_packets = pd.DataFrame(self.dataframe[self.dataframe['Protocol'] == 'TCP'])

        # Returns None is no tcp packets are present
        if tcp_packets.empty:
            return None

        # dataframe with SYN packets
        tcp_syn_packets = pd.DataFrame(
            tcp_packets[tcp_packets["TCP_Flags"].apply(lambda x: True if str(x).find('S') != -1 else False)])

        # dataframe with syn-ack packets
        tcp_syn_ack_packets = pd.DataFrame(
            tcp_packets[tcp_packets["TCP_Flags"].apply(lambda x: True if str(x).find('SA') != -1 else False)])

        if tcp_syn_packets.empty or tcp_syn_ack_packets.empty:
            return None

        # addresses of syn and syn-ack packets
        syn_sources_addresses = pd.Series(tcp_syn_packets['SourceIP'])
        syn_ack_source_addresses = pd.Series(tcp_syn_ack_packets['SourceIP'])

        syn_dest_addresses = pd.Series(tcp_syn_packets['DestIP'])
        syn_ack_dest_addresses = pd.Series(tcp_syn_ack_packets['DestIP'])

        # concatenation of frequency of addresses
        syn_addresses = pd.concat([syn_sources_addresses.value_counts(), syn_dest_addresses.value_counts(),
                                   syn_ack_source_addresses.value_counts(), syn_ack_dest_addresses.value_counts()],
                                  axis=1).reset_index()
        syn_addresses.columns = ['Address', 'SendsSYN', 'ReceivesSYN', 'SendsSYN-ACK', 'ReceivesSYN-ACK']
        syn_addresses = syn_addresses.replace(np.nan, 0)

        # plots graph with these values
        tcpsyn_graph = syn_addresses.plot(ax=canvas.axes, x="Address",
                                          y=["SendsSYN", "ReceivesSYN", "SendsSYN-ACK", "ReceivesSYN-ACK"], kind="barh")
        tcpsyn_graph.set(title="TCP SYN Flood", xlabel="Packets")

        for index, row in syn_addresses.iterrows():
            address = row['Address']
            # add to attacked addresses if receives more SYN packets than SYN-ACK packets sent back
            if row['ReceivesSYN'] > 1.5 * row['SendsSYN-ACK']:
                self.attacked_addresses.append(address)
            # add to suspicious addresses if sends more SYN packets than SYN-ACK packets received
            if row['SendsSYN'] > 1.5 * row['ReceivesSYN-ACK']:
                if address not in self.suspicious_addresses:
                    self.suspicious_addresses.append(address)
                if address not in self.tcp_suspicious_addresses:
                    self.tcp_suspicious_addresses.append(address)
        # return the plotted graph
        return canvas
```
The method begins by creating a new canvas to contain a graphical representation of the TCP Flood analysis. It then filters
out all non-TCP packets provided. 

After initialising axes and labels of the graph, the analysis loops through all SYN
addresses provided and, if the address sends at least 50% more SYN packets than SYN-ACK packets, it is marked
as a suspicious address and plots it on the graph.

Similarly, any addresses that receive at least 50% more SYN packets than SYN-ACK packets are treated as attacked addresses,
and are also plotted on the graph. After scanning through all SYN packets, the method returns the plotted canvas to be displayed
on the GUI.