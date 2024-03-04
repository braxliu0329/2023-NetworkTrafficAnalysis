# Attack Detection
Attack Detection is the main file responsible for analysing captured data packets for cyberattacks. It is tested by
`attack_analysis_tests.py` interacts with the GUI with files such as `dataframe_create.py` to display its analyses.
## Dependencies
```cython
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
```cython
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
```cython
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

### TCP Flood Detection
`tcp_flood_detect` scans all provided TCP packets for signs of a TCP Flood Attack. It is expected that the number of SYN packets on a network is around equal to the number of SYN-ACK packets. A disproportionately large number of SYN packets in comparison to SYN-ACK packets is evidence of a TCP Flood Attack.
```cython
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

### TCP Connect Scanning Detection
`tcp_connect_scanning_detect` scans all provided TCP packets for signs of a TCP Connection attack. This detection requires two conditions to flag an address as suspicious:
 - it has sent SYN flags without receiving SYN-ACK packets
 - it sends more SYN packets than the threshold within a decided time interval _(currently 5)_
```cython
def tcp_connect_scanning_detect(self, threshold):
        # create an empty canvas to store data points
        canvas = EmbeddedCanvas()
        # initialise suspicious addresses as an empty list
        self.tcp_scanning_suspicious = []
        # Sets interval time
        interval = 5

        # get all tcp packets
        tcp_packets = pd.DataFrame(self.dataframe[self.dataframe['Protocol'] == 'TCP'])
        # if there are no tcp packets, return nothing as there is no possibility of a tcp connect attack
        if tcp_packets.empty:
            return None

        # get all syn packets
        tcp_syn_packets = pd.DataFrame(
            tcp_packets[tcp_packets["TCP_Flags"].apply(lambda x: True if str(x).find('S') != -1 else False)])
        # get all syn-ack packets
        tcp_syn_ack_packets = pd.DataFrame(
            tcp_packets[tcp_packets["TCP_Flags"].apply(lambda x: True if str(x).find('SA') != -1 else False)])
        # if there are no syn or syn-ack packets, return nothing
        if tcp_syn_packets.empty or tcp_syn_ack_packets.empty:
            return None

        # get all syn source addresses
        syn_sources_addresses = pd.Series(tcp_syn_packets['SourceIP'])
        # get all syn-ack destination addresses
        syn_ack_dest_addresses = pd.Series(tcp_syn_ack_packets['DestIP'])

        # combine syn source and syn-ack destination addresses into one dataframe
        syn_addresses = pd.concat([syn_sources_addresses.value_counts(), syn_ack_dest_addresses.value_counts()],
                                  axis=1).reset_index()
        syn_addresses.columns = ['Address', 'SendsSYN', 'ReceivesSYN-ACK']
        # if there are empty addresses, set the data to 0
        syn_addresses = syn_addresses.replace(np.nan, 0)
        # create empty data slots for the syn rate
        syn_rate = {'Address': [],
                    'SYN_rate': []}
        # combine all unique addresses
        src_addr = tcp_syn_packets['SourceIP'].unique()

        # loop through each unique address
        for add in src_addr:
            # get all packets that match this address' source ip
            packet_ip = self.dataframe[self.dataframe['SourceIP'] == add]
            # initialise time difference
            time_diff = 0
            if len(packet_ip) > 1:
                time_diff = packet_ip['Time'].iloc[-1] - packet_ip['Time'].iloc[0]

            # Added time_diff condition to mitigate the rate soaring
            # if the time difference is too short
            if time_diff <= 1 or len(packet_ip) == 1:
                rate = len(packet_ip)
                syn_rate['Address'].append(add)
                syn_rate['SYN_rate'].append(int(rate))
            else:
                rate = len(packet_ip) / time_diff
                syn_rate['Address'].append(add)
                syn_rate['SYN_rate'].append(int(rate))

        # get a dataframe of all syn time differences
        syn_rate_df = pd.DataFrame.from_dict(syn_rate)
        # if this dataframe is empty, return None as a tcp connect attack is unfeasible
        if syn_rate_df.empty:
            return None
        # create the graph to display the data points
        tcp_con_graph = syn_rate_df.plot(ax=canvas.axes, x="Address", kind='barh', legend=False)
        tcp_con_graph.axvline(threshold, color='r', linestyle='--')
        tcp_con_graph.set(xlabel="SYN sending rate (packets/sec)")

        # initialise lists to contain the tcp connection count and time
        tcp_connection_count = {}
        tcp_connection_time = {}

        # The detection requires two steps to be suspicious:
        # 1. If the address sends SYN flags without receiving SYN-ACK packets
        # 2. If the same address sends more SYN packets than the threshold within the time interval
        for index, row in syn_addresses.iterrows():
            if row['SendsSYN'] > 0 and row['ReceivesSYN-ACK'] == 0:
                src_ip = row['Address']
                # DataFrame of packets that has src_ip as the Source IP
                tcp_ip = pd.DataFrame(tcp_packets[tcp_packets["SourceIP"]
                                      .apply(lambda x: True if str(x).find(src_ip) != -1 else False)])
                # Initialising the SYN packet count
                tcp_connection_count[src_ip] = 0
                for i, r in tcp_ip.iterrows():

                    # Initialising with time of the first occurrence of the src_ip
                    if src_ip not in tcp_connection_time.keys():
                        tcp_connection_time[src_ip] = r['Time']

                    # If the number of SYN packet excels the threshold,
                    # Check whether the time elapsed if less than interval.
                    # If so, the packet is classified as suspicious
                    if tcp_connection_count[src_ip] >= threshold:
                        if r['Time'] - tcp_connection_time[src_ip] <= interval:
                            if src_ip not in self.tcp_scanning_suspicious:
                                self.tcp_scanning_suspicious.append(src_ip)
                            if src_ip not in self.suspicious_addresses:
                                self.suspicious_addresses.append(src_ip)
                        # If not, reset the time period by the latest occurrence
                        else:
                            tcp_connection_count[src_ip] = 0
                            tcp_connection_time[src_ip] = r['Time']
                    tcp_connection_count[src_ip] += 1

        # return the dataframe to be displayed
        return canvas
```
The method begins by creating a new canvas to contain a graphical representation of the TCP Connection analysis. It then filters
out all non-TCP packets provided.

After initialising axes and labels of the graph, the analysis loops through all SYN addresses provided and, if the address has sent
a SYN flag without receiving SYN packets, and it has sent more SYN packets within the time interval, it is marked
as a suspicious address and plots it on the graph.

After finishing analyses, the final state of the canvas is returned to graphically represent the suspicious addresses.

### ARP Poison Detection
`arp_poison_detect` scans all provided TCP packets for signs of an ARP Poisoning Attack. It is expected that each packet's mac address has one associated ip address. If this is not the case, the address is marked as suspicious for ARP Poisoning.
```cython
def arp_poison_detect(self):
        # initialise this arp suspicious addresses
        self.arp_suspicious_addresses = []
        # create an empty canvas to store data points
        canvas = EmbeddedCanvas()

        # dataframe with only ARP packets
        arp_packets = pd.DataFrame(self.dataframe[self.dataframe['Protocol'] == 'ARP'])

        # Returns empty canvas if no arp packets are present since no analysis can be performed
        if arp_packets.empty:
            return None

        # reset the indexes on the arp packets
        arp_packets.reset_index()
        # initialise suspicious addresses and the ip_mac addresses
        ip_mac = {}
        suspicious_addresses = []

        # iterates through each ARP packet
        for index, arp_packet in arp_packets.iterrows():
            # stores each source ip and mac address
            source_IP = arp_packet['SourceIP']
            source_mac = arp_packet['hwsrc']
            # if source mac not already in dictionary an entry is created
            if source_mac not in ip_mac:
                ip_mac[source_mac] = [source_IP]
            else:
                # if ip address is not associated with mac address add to its list
                if source_IP not in ip_mac[source_mac]:
                    ip_mac.setdefault(source_mac, []).append(source_IP)

        # initialises mac address frequency dictionary to be made into dataframe
        mac_freq_table = {"MAC_addresses": [],
                          "Frequency": []}

        # initialise lists of mac addresses and their frequencies
        mac_addr_list = []
        mac_addr_freq_list = []

        # loop through all mac addresses
        for mac_addr in ip_mac:
            mac_addr_list.append(mac_addr)
            # add number of ip addresses associated with that mac address
            mac_addr_freq_list.append(len(ip_mac[mac_addr]))
            # if that mac address is associated with more than one ip address than it is marked as suspicious
            if len(ip_mac[mac_addr]) > 1:
                suspicious_addresses.extend(ip_mac[mac_addr])

        # add lists to dictionary, one address at a time
        for index, mac_addr in enumerate(mac_addr_list):
            mac_freq_table["MAC_addresses"].append(mac_addr)
            mac_freq_table["Frequency"].append(mac_addr_freq_list[index])

        # initialise the dataframe with appropriate axes and titles
        table_dataframe = pd.DataFrame.from_dict(mac_freq_table)
        arp_graph = table_dataframe.plot(ax=canvas.axes, kind='barh', x='MAC_addresses', legend=False)
        arp_graph.set(xlabel="Frequency", title="ARP Poison")
        arp_graph.locator_params(axis="x", integer=True, tight=True)
        # threshold here is 1 since any mac address having more than one ip address is suspicious
        arp_graph.axvline(1, color='r', linestyle='--')
        # removes any repeated addresses
        self.arp_suspicious_addresses = list(dict.fromkeys(suspicious_addresses))

        # adds suspicious addresses to main suspicious address list
        for address in self.arp_suspicious_addresses:
            if address not in self.suspicious_addresses:
                self.suspicious_addresses.append(address)

        # return the canvas to graphically display the suspicious addresses
        return canvas
```
The method begins by creating a new canvas to contain a graphical representation of the ARP Poisoning analysis. It then filters
out all non-ARP packets provided.

After initialising axes and labels of the graph, the analysis loops through all ARP mac addresses provided and, if the address has more than one associated ip addresses, it is marked as a suspicious address and is plotted on the graph.

After finishing analyses, the final state of the canvas is returned to graphically represent the suspicious addresses.

### Threshold DOS Detection
`threshold_dos_detect` is a simple DOS detection function that, given a threshold, ensures that each unique IP address
doesn't send more packets per second (_pps_) than the threshold.
```cython
 # Simple detection to see if pps are above a threshold
def threshold_dos_detect(self, threshold):
        # initialise dos suspicious addresses
        self.dos_suspicious_addresses = []
        # create an empty canvas to store data points
        canvas = EmbeddedCanvas()

        # get all unique source addresses
        sources_addresses = self.dataframe['SourceIP'].unique()

        # create a table with addresses and the packets per second
        pps_table = {'Address': [],
                     'PPS': []}

        # calculates packets per second sent for each address
        for address in sources_addresses:
            packets_ip = self.dataframe[self.dataframe['SourceIP'] == address]
            # if the address doesn't have enough source addresses to be suspicious, go to the next address
            if len(packets_ip) < 2:
                continue

            # get the difference in time between two packets
            difference = packets_ip['Time'].iloc[-1] - packets_ip['Time'].iloc[0]
            # if there is no difference in time, go to the next packet
            if difference == 0:
                continue
            # calculate this address' pps
            packet_per_sec = len(packets_ip) / difference

            # add the pps to the pps table
            pps_table['Address'].append(address)
            pps_table['PPS'].append(int(packet_per_sec))

        # create a dataframe from the pps table
        pps_dataframe = pd.DataFrame.from_dict(pps_table)
        
        # initialise a graph to represent pps
        dos_graph = pps_dataframe.plot(ax=canvas.axes, x="Address", kind='barh', legend=False)
        dos_graph.set(title="DOS Detection", xlabel="Packets Per Second")
        dos_graph.axvline(threshold, color='r', linestyle='--')

        # marks addresses as suspicious if the packets per second exceed the mean
        for index, address in pps_dataframe.iterrows():
            if address["PPS"] > threshold:
                # if the address isn't already marked as suspicious, add it to the suspicious lists
                if address["Address"] not in self.dos_suspicious_addresses:
                    self.dos_suspicious_addresses.append(address["Address"])
                if address["Address"] not in self.suspicious_addresses:
                    self.suspicious_addresses.append(address["Address"])

        # return the dataframe to be graphically represented
        return canvas
```
The method begins by creating a new canvas to contain a graphical representation of the DOS analysis. It then gets a 
list of all unique IP address.

After initialising axes and labels of the graph, the analysis loops through all ip addresses. If the address 
sends more packets per second than the threshold, it is marked as a suspicious address and is plotted on the graph.

After finishing analysis, the final state of the canvas is returned to graphically represent packets per second.

### ICMP Flood Detection
`icmp_flood_detect` uses the `calc_pps` function to mark ICMP echo packets that send more packets per second than the provided
threshold as suspicious.
```cython
def icmp_flood_detect(self, threshold):
        # initialise icmp suspicious addresses
        self.icmp_suspicious = []
        # create an empty canvas to store data points
        canvas = EmbeddedCanvas()

        # dataframe with only ICMP Echo packets
        icmp_packets = self.dataframe[(self.dataframe['Protocol'] == 'ICMP') & (self.dataframe['ICMP_Type'] == 8)]
        # if there are no ICMP packets, return nothing as there can be no icmp flood attacks
        if icmp_packets.empty:
            return None

        # removes any duplicated addresses
        icmp_addresses = icmp_packets['SourceIP'].unique()
        # create the packets per second table using the calc_pps function. This will also populate the suspicious list
        # with all icmp addresses that have a pps above the provided threshold
        pps_table = self.calc_pps(icmp_addresses, icmp_packets, self.icmp_suspicious, threshold)

        # creates dataframe from dictionary
        pps_dataframe = pd.DataFrame.from_dict(pps_table)

        # creates graph from dataframe
        pps_graph = pps_dataframe.plot(ax=canvas.axes, kind='barh', x="Address", legend=False)
        pps_graph.set(title="ICMP Flood Detection", xlabel="Packets Per Second")
        pps_graph.locator_params(axis="x", integer=True, tight=True)
        pps_graph.axvline(threshold, color='r', linestyle='--')

        # return the created graph to be represented on the GUI
        return canvas
```
The method begins by creating a new canvas to contain a graphical representation of the ICMP analysis. It then gets a 
list of all unique ICMP echo IP address.

After initialising axes and labels of the graph, the analysis calls `calc_pps` which loops through all ip addresses. If 
the address sends more packets per second than the threshold, it is marked as a suspicious address and is plotted on the 
graph. This function also removes any outlying packets that have a time more than 3 standard deviations from the mean time.

After finishing analysis, the final state of the canvas is returned to graphically represent packets per second.
