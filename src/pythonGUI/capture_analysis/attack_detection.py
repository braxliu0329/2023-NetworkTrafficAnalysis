import numpy as np
import pandas as pd

from pythonGUI.capture_analysis import dataframe_create

class AttackDetection:
    # initialise attack detection variables
    def __init__(self, data, flagged_IPs):
        # initialise all flagged ip addresses as empty
        self.ssl_stripping_suspicious_address = None
        self.udp_suspicious = None
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

    def tcp_syn_flood_detect(self):
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
        return syn_addresses

    def tcp_connect_scanning_detect(self, threshold):
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
        return syn_rate

    def arp_poison_detect(self):
        # initialise arp suspicious addresses
        self.arp_suspicious_addresses = []

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

        # removes any repeated addresses
        self.arp_suspicious_addresses = list(dict.fromkeys(suspicious_addresses))

        # adds suspicious addresses to main suspicious address list
        for address in self.arp_suspicious_addresses:
            if address not in self.suspicious_addresses:
                self.suspicious_addresses.append(address)

        # return the canvas to graphically display the suspicious addresses
        return mac_freq_table

    # Simple detection to see if pps are above a threshold
    def threshold_dos_detect(self, threshold):
        # initialise dos suspicious addresses
        self.dos_suspicious_addresses = []
        
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

        # marks addresses as suspicious if the packets per second exceed the mean
        for index, address in pps_dataframe.iterrows():
            if address["PPS"] > threshold:
                # if the address isn't already marked as suspicious, add it to the suspicious lists
                if address["Address"] not in self.dos_suspicious_addresses:
                    self.dos_suspicious_addresses.append(address["Address"])
                if address["Address"] not in self.suspicious_addresses:
                    self.suspicious_addresses.append(address["Address"])

        # return the dataframe to be graphically represented
        return pps_table

    def icmp_flood_detect(self, threshold):
        # initialise icmp suspicious addresses
        self.icmp_suspicious = []

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

        # return the created graph to be represented on the GUI
        return pps_dataframe

    def http_attack(self, threshold):
        self.http_suspicious = []

        tcp_packets = pd.DataFrame(
            self.dataframe[(self.dataframe['Protocol'] == 'TCP') & (self.dataframe["IP_Version"] == "IPv4")])

        # Returns None if no tcp packets
        if tcp_packets.empty:
            return None

        # Loop to establish if a tcp handshake has been established
        synlist = []
        source_ips = []
        for index, packet in tcp_packets.iterrows():
            # adds addresses to dictionary if syn packet is found
            if packet["TCP_Flags"] == "S":
                synlist.append({"SourceIP": packet["SourceIP"],
                                "DestIP": packet["DestIP"],
                                "Stage": "syn"})
            # if syn-ack is found, checks if packet addresses link up
            if packet["TCP_Flags"] == "SA":
                for syn_packet in synlist:
                    if syn_packet["SourceIP"] == packet["DestIP"] and syn_packet["DestIP"] == packet["SourceIP"]:
                        syn_packet["Stage"] = "synack"
            # if ack is found, check if syn_ack was previously found and adds addresses and sets tcp_connection to true
            if packet["TCP_Flags"] == "A":
                for syn_packet in synlist:
                    if syn_packet["SourceIP"] == packet["SourceIP"] and syn_packet["DestIP"] == packet["DestIP"] and \
                            syn_packet["Stage"] == "synack":
                        syn_packet["Stage"] = "connected"
                        if syn_packet["SourceIP"] not in source_ips:
                            source_ips.append(syn_packet["SourceIP"])

        # if no tcp connection was established return None
        if not source_ips:
            return None

        request_packets = []
        # for each address in which a tcp connection was established, check if packets sent are GET or POST requests
        for sourceIP in source_ips:
            tcp_requests = tcp_packets[(tcp_packets["SourceIP"] == sourceIP) & tcp_packets["raw"].notna()]
            for index, packet in tcp_requests.iterrows():
                request = packet["raw"]

                request_utf = ""
                request_latin = ""
                try:
                    request_utf = request.decode("utf-8")
                except:
                    request_latin = request.decode("latin-1")

                if ("GET" in request_utf or "POST" in request_utf) or (
                        "GET" in request_latin or "POST" in request_latin):
                    request_packets.append(packet["Number"])

        # dataframe of request packets
        requests = tcp_packets[tcp_packets["Number"].isin(request_packets)]

        if requests.empty:
            return None

        # calculates packets per second for http request packets
        pps_table = self.calc_pps(source_ips, requests, self.http_suspicious, threshold)

        # creates dataframe from dictionary
        pps_dataframe = pd.DataFrame.from_dict(pps_table)
        return pps_dataframe

    def dns_request_response_detect(self, threshold):
        self.dns_request_suspicious = []
        self.dns_response_suspicious = []

        # Filters to DNS protocols only
        dns_packets = pd.DataFrame(self.dataframe[self.dataframe['Protocol'] == 'UDP/DNS'])

        # Returns empty canvas if no packets are present
        if dns_packets.empty:
            return [None, None]

        # Requests have a qr flag of 0 and responses have a qr flag of 1
        dns_requests = pd.DataFrame(dns_packets[dns_packets['DNS_Type'] == 0])
        dns_responses = pd.DataFrame(dns_packets[dns_packets['DNS_Type'] == 1])

        # Obtains unique addresses
        dns_request_addresses = dns_requests['SourceIP'].unique()
        dns_response_addresses = dns_responses['SourceIP'].unique()

        # Calculates packets per second for dns requests
        pps_table_req = self.calc_pps(dns_request_addresses, dns_requests, self.dns_request_suspicious, threshold)

        # Calculates packets per second for dns_responses
        pps_table_res = self.calc_pps(dns_response_addresses, dns_responses, self.dns_response_suspicious, threshold)

        # Returns both graphs
        return pps_table_res, pps_table_req


        # -------------Below are new attack methods----------------
    def ssl_stripping(self):
        # initialises suspicious addresses address lists
        self.ssl_stripping_suspicious_source_address = []
        self.ssl_stripping_suspicious_destination_address = []

        # check for HTTP traffic on port 443, suppose to be HTTPS rather than HTTP
        for index, row in self.dataframe.iterrows():
            if row['Protocol'] == 'TCP' and row['DestinationPort'] == 443:
                source_ip = row['SourceIP']
                dest_ip = row['DestIP']
                if source_ip not in self.ssl_stripping_suspicious_source_address:
                    self.ssl_stripping_suspicious_source_address.append(source_ip)
                if dest_ip not in self.ssl_stripping_suspicious_destination_address:
                    self.ssl_stripping_suspicious_destination_address.append(dest_ip)
        
        http_packets = self.dataframe[(self.dataframe['Protocol'] == 'TCP') & (self.dataframe['DestinationPort'] == 443)]
        if http_packets.empty:
            return None

        # Create dataframes from the lists of suspicious addresses
        source_addresses_df = pd.DataFrame(self.ssl_stripping_suspicious_source_address, columns=["Suspicious Source IPs"])
        destination_addresses_df = pd.DataFrame(self.ssl_stripping_suspicious_destination_address,
                                                columns=["Suspicious Destination IPs"])

        # Count the number of occurrences for each IP
        source_counts = source_addresses_df["Suspicious Source IPs"].value_counts().rename_axis('Source IP').reset_index(
            name="Counts")
        destination_counts = destination_addresses_df["Suspicious Destination IPs"].value_counts().rename_axis(
            'Destination IP').reset_index(name="Counts")
        return (source_counts, destination_counts)

    def udp_flood_detect(self, threshold):
        # initialise udp suspicious addresses
        self.udp_suspicious = []

        # dataframe with only UDP packets
        udp_packets = self.dataframe[self.dataframe['Protocol'] == 'UDP']
        # if there are no UDP packets, return nothing as there can be no udp flood attacks
        if udp_packets.empty:
            return None
        
        # removes any duplicated addresses
        udp_addresses = udp_packets['SourceIP'].unique()

        # create the packets per second table using the calc_pps function. This will also populate the suspicious list
        # with all udp addresses that have a pps above the provided threshold
        pps_table = self.calc_pps(udp_addresses, udp_packets, self.udp_suspicious, threshold)
        # creates dataframe from dictionary
        pps_dataframe = pd.DataFrame.from_dict(pps_table)
        return pps_dataframe

    def calc_pps(self, suspicious_addresses, packets, attack_sus_list, threshold):
        # dictionary of the addresses and their packets per second
        pps_table = {'Address': [],
                     'PPS': []}

        # For each address:
        #    - calculate mean and standard deviation
        #    - remove any outliers using these
        #    - calculate the packets per second sent by each address
        #    - adds to suspicious addresses if above the threshold
        for address in suspicious_addresses:
            packets_ip = packets[packets['SourceIP'] == address]

            # calculates mean and standard deviation
            mean = packets_ip['Time'].mean()
            std = packets_ip['Time'].std()

            # removes any outliers (timestamps that are more than 3 standard deviations away from the mean)
            packets_no_outliers = packets_ip[packets_ip['Time'] <= mean + (3 * std)]
            packet_per_sec = 0
            if len(packets_no_outliers.index) != 0:
                # calculates average packets per second
                difference = packets_no_outliers['Time'].iloc[-1] - packets_no_outliers['Time'].iloc[0]
                packet_per_sec = len(packets_no_outliers) / difference

            pps_table['Address'].append(address)
            pps_table['PPS'].append(int(packet_per_sec))

            # adds to suspicious addresses if above threshold
            if packet_per_sec > threshold:
                if address not in self.suspicious_addresses:
                    self.suspicious_addresses.append(address)
                if address not in attack_sus_list:
                    attack_sus_list.append(address)


        return pps_table

