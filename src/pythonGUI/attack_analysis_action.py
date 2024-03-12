from PyQt5 import Qt
import json
<<<<<<< HEAD
=======
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
>>>>>>> dev

from PyQt5.QtWidgets import *


from pythonGUI.capture_analysis import attack_detection as attacking


<<<<<<< HEAD
class AttackAnalysis():
    def __init__(self, data, flagged_IPs):
=======
class AttackAnalysisWindow(attack_analysis_window.Ui_MainWindow, QMainWindow):
    def __init__(self, data, main_window, flagged_IPs):
        super(AttackAnalysisWindow, self).__init__()
        self.setupUi(self)
>>>>>>> dev
        self.data_use = data
        self.flagged_IPs = flagged_IPs
        self.attack_detect = attacking.AttackDetection(self.data_use, self.flagged_IPs)

<<<<<<< HEAD
=======
        # triggers methods if buttons are clicked
        self.actionTCPSYN.triggered.connect(self.tcp_syn_flood_detect)
        self.actionDOS.triggered.connect(self.dos_detect)
        self.actionTCPscan.triggered.connect(self.tcp_scanning_detect)
        self.actionARPPoi.triggered.connect(self.arp_poison_detect)
        self.actionICMP.triggered.connect(self.icmp_flood_detect)
        self.actionHTTP_Flood.triggered.connect(self.http_flood_detect)
        self.actionDNS.triggered.connect(self.dns_flood_detect)
        self.actionUDP_Flood.triggered.connect(self.udp_flood_detect)

        self.actionrunAll.triggered.connect(self.run_all_detect)
        self.actionFlagged.triggered.connect(self.display_flagged_addr)
>>>>>>> dev
        self.imported_IPs = []

    # when subwindow is closed save suspicious addresses to mainwindow and then close
    def closeEvent(self, event):
        for address in self.attack_detect.suspicious_addresses:
            if address not in self.parent.flaggedIPs:
                self.parent.flaggedIPs.append(address)
        event.accept()

    def tcp_syn_flood_detect(self):
        # gets graph canvas from calling attack detection method
        syn_addresses = self.attack_detect.tcp_syn_flood_detect()
        suspicious = self.attack_detect.tcp_suspicious_addresses
        attacked = self.attack_detect.attacked_addresses
        
        if not suspicious:
            suspicious_text = "No suspicious addresses detected"
        elif suspicious:
            suspicious_text = "Suspicious addresses: "
            suspicious_addresses = ', '.join(suspicious)
            suspicious_text = suspicious_text + suspicious_addresses


        # creates main widget and layout
        central = QWidget()
        layout = QVBoxLayout()

        suspicious_text = ""
        attacked_text = ""

        # if no graph is created then no packets were present
        if canvas is None:
            suspicious_text = "No TCP SYN or SYN-ACK packets present, no suspicious addresses detected"
        else:
            if not suspicious:
                suspicious_text = "No suspicious addresses detected"
            elif suspicious:
                suspicious_text = "Suspicious addresses: "
                suspicious_addresses = ', '.join(suspicious)
                suspicious_text = suspicious_text + suspicious_addresses

            if not attacked:
                attacked_text = "No attacked addresses detected"
            elif attacked:
                attacked_text = "Suspected Attacked addresses: "
                attacked_addresses = ', '.join(attacked)
                attacked_text = attacked_text + attacked_addresses

        explanation_text = "The suspicious addresses were marked because these addresses send a greater amount of " \
                           "SYN requests than it does receive SYN-ACK responses back, suggesting it is overloading a" \
                           "system. \n\nThe attacked addresses were marked because these addresses receive a greater " \
                           "amount of SYN requests than it sends SYN-ACK responses back, which is indicative that " \
                           "these addresses are being overwhelmed by SYN requests and cant response fast enough. "
<<<<<<< HEAD
        if syn_addresses is not None:
            data = {
                "suspicious": suspicious_text,
                "attacked": attacked_text,
                "explanation": explanation_text,
                "data": []
            }
            for i in range(syn_addresses.shape[0]):
                data["data"].append({
                    "address": syn_addresses.loc[i, "Address"],
                    "Sends SYN": int(syn_addresses.loc[i, "SendsSYN"]),
                    "Receives SYN": int(syn_addresses.loc[i, "ReceivesSYN"]),
                    "Sends SYN/ACK" : int(syn_addresses.loc[i, "SendsSYN-ACK"]),
                    "Receives SYN/ACK": int(syn_addresses.loc[i, "ReceivesSYN-ACK"])
                })
            with open("src/pythonGUI/plotData/tcpsyn.json", "w+") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
=======
        suspicious_label = QLabel(suspicious_text)
        suspicious_label.setFont(QFont('Arial', 25))
        suspicious_label.setAlignment(Qt.AlignCenter)
        suspicious_label.setWordWrap(True)

        explain_label = QLabel("\nExplanation:")
        explain_label.setFont(QFont('Arial', 25))

        explanation_label = QLabel(explanation_text)
        explanation_label.setFont(QFont('Arial', 20))
        explanation_label.setAlignment(Qt.AlignLeft)
        explanation_label.setWordWrap(True)

        layout.addWidget(canvas)
        layout.addWidget(suspicious_label)

        if canvas is not None:
            layout.addWidget(explain_label)
            layout.addWidget(explanation_label)
            layout.addStretch()

        self.setCentralWidget(central)
        central.setLayout(layout)

>>>>>>> dev

    def tcp_scanning_detect(self):
        syn_rate = self.attack_detect.tcp_connect_scanning_detect(100)
        suspicious = self.attack_detect.tcp_scanning_suspicious

        suspicious_text = ""

        if canvas is None:
            suspicious_text = "No TCP (SYN) packets present, no suspicious addresses detected"
        else:
            if not suspicious:
                suspicious_text = "No suspicious addresses detected"
            elif suspicious:
                suspicious_text = "Suspicious addresses: "
                suspicious_addresses = ', '.join(suspicious)
                suspicious_text = suspicious_text + suspicious_addresses

        explain_label = QLabel("\nExplanation:")


        explanation_text = "Addresses are marked as suspicious if the address sends SYN flags without receiving " \
                           "SYN-ACK packets and if the same address sends more SYN packets than the  within " \
                           "the time interval. "
<<<<<<< HEAD
        if syn_rate is not None:
=======

        explanation_label = QLabel(explanation_text)
        explanation_label.setFont(QFont('Arial', 20))
        explanation_label.setWordWrap(True)

        suspicious_label = QLabel(suspicious_text)
        suspicious_label.setFont(QFont('Arial', 25))
        suspicious_label.setAlignment(Qt.AlignCenter)
        suspicious_label.setWordWrap(True)

        if syn_rate:
>>>>>>> dev
            data = {
                "suspicious": suspicious_text,
                "explanation": explanation_text,
                "data": []
            }
            addresses = syn_rate["Address"]
            rates = syn_rate["SYN_rate"]
            for i in range(len(addresses)):
                data["data"].append({
                    "address": addresses[i],
                    "rate": rates[i]
                })
            with open("src/pythonGUI/plotData/tcpscan.json", "w+") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

    def dos_detect(self):

        pps_table = self.attack_detect.threshold_dos_detect(100)
        suspicious = self.attack_detect.dos_suspicious_addresses


        suspicious_text = ""


<<<<<<< HEAD
        if not suspicious:
            suspicious_text = "No suspicious addresses detected"
        elif suspicious:
            suspicious_text = "Suspicious addresses: "
            suspicious_addresses = ', '.join(suspicious)
            suspicious_text = suspicious_text + suspicious_addresses
            explanation_label = QLabel(
                    "These addresses are sending a greater amount of traffic then the  and therefore are marked as suspicious.")
        if pps_table is not None:
=======
        suspicious_label = QLabel(suspicious_text)
        suspicious_label.setFont(QFont('Arial', 25))
        suspicious_label.setAlignment(Qt.AlignCenter)
        suspicious_label.setWordWrap(True)

        explain_label = QLabel("\nExplanation:")
        explain_label.setFont(QFont('Arial', 25))

        explanation_label.setFont(QFont('Arial', 20))
        explanation_label.setWordWrap(True)

        layout.addWidget(canvas)
        layout.addWidget(suspicious_label)
        layout.addWidget(explain_label)
        layout.addWidget(explanation_label)
        layout.addStretch()

        self.setCentralWidget(central)
        central.setLayout(layout)
        if pps_table:
>>>>>>> dev
            data = {
                "suspicious": suspicious_text,
                "explanation": "These addresses are sending a greater amount of traffic then the  and therefore are marked as suspicious.",
                "data": []
            }
            addresses = pps_table["Address"]
            pps = pps_table["PPS"]
            for i in range(len(addresses)):
                data["data"].append({
                    "address": addresses[i],
                    "rate": pps[i]
                })
            with open("src/pythonGUI/plotData/dos.json", "w+") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

    def arp_poison_detect(self):
        mac_addr_fre = self.attack_detect.arp_poison_detect()
        suspicious = self.attack_detect.arp_suspicious_addresses        
        suspicious_text = ""
<<<<<<< HEAD
        if not suspicious:
            suspicious_text = "No suspicious addresses detected"
        elif suspicious:
            suspicious_text = "Suspicious addresses: "
            suspicious_addresses = ', '.join(suspicious)
            suspicious_text = suspicious_text + suspicious_addresses
        explanation_text = "These addresses were marked because the MAC addresses they originated from are associated " \
                           "with more than one IP address, which is erroneous and indicative of ARP Poisoning."
        if mac_addr_fre is not None:
=======
        if canvas is None:
            suspicious_text = "No ARP packets present, no suspicious addresses detected"

        else:
            if not suspicious:
                suspicious_text = "No suspicious addresses detected"
            elif suspicious:
                suspicious_text = "Suspicious addresses: "
                suspicious_addresses = ', '.join(suspicious)
                suspicious_text = suspicious_text + suspicious_addresses

        suspicious_label = QLabel(suspicious_text)
        suspicious_label.setFont(QFont('Arial', 25))
        suspicious_label.setAlignment(Qt.AlignCenter)
        suspicious_label.setWordWrap(True)

        explain_label = QLabel("\nExplanation:")

        explain_label.setFont(QFont('Arial', 25))

        explanation_text = "These addresses were marked because the MAC addresses they originated from are associated " \
                           "with more than one IP address, which is erroneous and indicative of ARP Poisoning."
        
        explanation_label = QLabel(explanation_text)
        explanation_label.setFont(QFont('Arial', 20))
        explanation_label.setWordWrap(True)

        layout.addWidget(canvas)
        layout.addWidget(suspicious_label)

        if canvas is not None:
            layout.addWidget(explain_label)
            layout.addWidget(explanation_label)
            layout.addStretch()

        self.setCentralWidget(central)
        central.setLayout(layout)
        if mac_addr_fre:
>>>>>>> dev
            mac_addr = mac_addr_fre['MAC_addresses']
            frequency = mac_addr_fre['Frequency']
            data = {
                "data": [],
                "suspicious": suspicious_text,
                "explanation": explanation_text
            }
            for i in range(len(mac_addr)):
                data["data"].append({
                    "mac": mac_addr[i],
                    "frequency": frequency[i]
                })
            with open ("src/pythonGUI/plotData/arp.json", "w+") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

    def icmp_flood_detect(self):
        pps_dataframe = self.attack_detect.icmp_flood_detect(100)
        suspicious = self.attack_detect.icmp_suspicious
        suspicious_text = ""
<<<<<<< HEAD
        if not suspicious:
            suspicious_text = "No suspicious addresses detected"
        elif suspicious:
            suspicious_text = "Suspicious addresses: "
            suspicious_addresses = ', '.join(suspicious)
            suspicious_text = suspicious_text + suspicious_addresses
        explanation_text = "These addresses were marked because the ICMP Echo packets sent from these addresses are " \
                           "over too high a frequency. "
        if pps_dataframe is not None:
=======

        if canvas is None:
            suspicious_text = "No ICMP packets present, no suspicious addresses detected"
        else:
            if not suspicious:
                suspicious_text = "No suspicious addresses detected"
            elif suspicious:
                suspicious_text = "Suspicious addresses: "
                suspicious_addresses = ', '.join(suspicious)
                suspicious_text = suspicious_text + suspicious_addresses

        suspicious_label = QLabel(suspicious_text)
        suspicious_label.setFont(QFont('Arial', 25))
        suspicious_label.setAlignment(Qt.AlignCenter)
        suspicious_label.setWordWrap(True)

        explain_label = QLabel("\nExplanation:")
        explain_label.setFont(QFont('Arial', 25))

        explanation_text = "These addresses were marked because the ICMP Echo packets sent from these addresses are " \
                           "over too high a frequency. "

        explanation_label = QLabel(explanation_text)
        explanation_label.setFont(QFont('Arial', 20))
        explanation_label.setWordWrap(True)

        layout.addWidget(canvas)
        layout.addWidget(suspicious_label)

        if canvas is not None:
            layout.addWidget(explain_label)
            layout.addWidget(explanation_label)
            layout.addStretch()

        self.setCentralWidget(central)
        central.setLayout(layout)
        if not pps_dataframe.empty:
>>>>>>> dev
            data = {
                "suspicious": suspicious_text,
                "explanation": explanation_text,
                "data": []
            }
            for i in range(pps_dataframe.shape[0]):
                data["data"].append({
                    "address": pps_dataframe.loc[i, "Address"],
                    "rate": int(pps_dataframe.loc[i, "PPS"])
                })
            with open("src/pythonGUI/plotData/icmpflood.json", "w+") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

    def http_flood_detect(self):
        pps_dataframe = self.attack_detect.http_attack(100)
        suspicious = self.attack_detect.http_suspicious
        suspicious_text = ""
<<<<<<< HEAD
        if not suspicious:
            suspicious_text = "No suspicious addresses detected"
        elif suspicious:
            suspicious_text = "Suspicious addresses: "
            suspicious_addresses = ', '.join(suspicious)
            suspicious_text = suspicious_text + suspicious_addresses
        explanation_text = "These addresses were marked because the HTTP Request packets sent from these addresses " \
                           "after a tcp connection are established are " \
                           "over too high a frequency. "
        if pps_dataframe is not None:
=======

        if canvas is None:
            suspicious_text = "No HTTP packets/TCP handshake was present, no suspicious addresses detected"
        else:
            if not suspicious:
                suspicious_text = "No suspicious addresses detected"
            elif suspicious:
                suspicious_text = "Suspicious addresses: "
                suspicious_addresses = ', '.join(suspicious)
                suspicious_text = suspicious_text + suspicious_addresses

        suspicious_label = QLabel(suspicious_text)
        suspicious_label.setFont(QFont('Arial', 25))
        suspicious_label.setAlignment(Qt.AlignCenter)
        suspicious_label.setWordWrap(True)

        explain_label = QLabel("\nExplanation:")
        explain_label.setFont(QFont('Arial', 25))

        explanation_text = "These addresses were marked because the HTTP Request packets sent from these addresses " \
                           "after a tcp connection are established are " \
                           "over too high a frequency. "

        explanation_label = QLabel(explanation_text)
        explanation_label.setFont(QFont('Arial', 20))
        explanation_label.setWordWrap(True)

        layout.addWidget(canvas)
        layout.addWidget(suspicious_label)

        if canvas is not None:
            layout.addWidget(explain_label)
            layout.addWidget(explanation_label)
            layout.addStretch()

        self.setCentralWidget(central)
        central.setLayout(layout)
        if not pps_dataframe.empty:
>>>>>>> dev
            data = {
                "suspicious": suspicious_text,
                "explanation": explanation_text,
                "data": []
            }
            for i in range(pps_dataframe.shape[0]):
                data["data"].append({
                    "address": pps_dataframe.loc[i, "Address"],
                    "rate": int(pps_dataframe.loc[i, "PPS"]) 
                })
            with open("src/pythonGUI/plotData/httpflood.json", "w+") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        
    def dns_flood_detect(self):
        pps_res, pps_req = self.attack_detect.dns_request_response_detect(100)
        request_suspicious = self.attack_detect.dns_request_suspicious
        response_suspicious = self.attack_detect.dns_response_suspicious

        request_suspicious_text = ""
        if request_suspicious:
            request_suspicious_text = "DNS Request suspicious addresses: "
            suspicious_addresses = ', '.join(request_suspicious)
            request_suspicious_text = request_suspicious_text + suspicious_addresses

        response_suspicious_text = ""

<<<<<<< HEAD
        
        if not response_suspicious:
            request_suspicious_text = "No DNS Response suspicious addresses detected"
        elif response_suspicious:
            response_suspicious_text = "DNS Response suspicious addresses: "
            suspicious_addresses = ', '.join(response_suspicious)
            response_suspicious_text = response_suspicious_text + suspicious_addresses
=======
        if request_graph is None and response_graph is None:
            suspicious_text = "No DNS packets present, no suspicious addresses detected"
        else:
            request_suspicious = self.attack_detect.dns_request_suspicious
            response_suspicious = self.attack_detect.dns_response_suspicious

            request_suspicious_text = ""

            if request_graph is None:
                request_suspicious_text = "No DNS Request packets present, no suspicious addresses detected"
            else:
                if not request_suspicious:
                    request_suspicious_text = "No DNS Request suspicious addresses detected"
                elif request_suspicious:
                    request_suspicious_text = "DNS Request suspicious addresses: "
                    suspicious_addresses = ', '.join(request_suspicious)
                    request_suspicious_text = request_suspicious_text + suspicious_addresses

            response_suspicious_text = ""

            if response_graph is None:
                response_suspicious_text = "No DNS Response packets present, no suspicious addresses detected"
            else:
                if not response_suspicious:
                    request_suspicious_text = "No DNS Response suspicious addresses detected"
                elif response_suspicious:
                    response_suspicious_text = "DNS Response suspicious addresses: "
                    suspicious_addresses = ', '.join(response_suspicious)
                    response_suspicious_text = response_suspicious_text + suspicious_addresses

            suspicious_text = request_suspicious_text + "\n" + response_suspicious_text

            layout.addWidget(request_graph)
            layout.addWidget(response_graph)

        suspicious_label = QLabel(suspicious_text)
        suspicious_label.setFont(QFont('Arial', 25))
        suspicious_label.setAlignment(Qt.AlignCenter)
        suspicious_label.setWordWrap(True)

        explain_label = QLabel("\nExplanation:")
        explain_label.setFont(QFont('Arial', 25))
>>>>>>> dev

        suspicious_text = request_suspicious_text + "\n" + response_suspicious_text
        explanation_text = "These addresses were marked because the DNS packets sent from these addresses are " \
                           "over too high a frequency. "
<<<<<<< HEAD
        if pps_req is not None and pps_res is not None:
=======

        explanation_label = QLabel(explanation_text)
        explanation_label.setFont(QFont('Arial', 20))
        explanation_label.setWordWrap(True)

        layout.addWidget(suspicious_label)

        if request_graph is not None or response_graph is not None:
            layout.addWidget(explain_label)
            layout.addWidget(explanation_label)
            layout.addStretch()

        self.setCentralWidget(central)
        central.setLayout(layout)
        if pps_req or pps_res:
>>>>>>> dev
            res_data = {
                "suspicious": suspicious_text,
                "explanation": explanation_text,
                "data": []
            }
            req_data = {
                "data": []
            }
            res_addr = pps_res["Address"]
            res_pps = pps_res["PPS"]
            for i in range(len(res_addr)):
                res_data["data"].append({
                    "address": res_addr[i],
                    "rate": res_pps[i]
                })
            req_addr = pps_req["Address"]
            req_pps = pps_req["PPS"]
            for i in range(len(req_addr)):
                req_data["data"].append({
                    "address": req_addr[i],
                    "rate": req_pps[i]
                })
            with open("src/pythonGUI/plotData/dnsresponse.json", "w+") as f:
                json.dump(res_data, f, ensure_ascii=False, indent=4)
            with open("src/pythonGUI/plotData/dnsrequest.json", "w+") as f:
                json.dump(req_data, f, ensure_ascii=False, indent=4)

    def udp_flood_detect(self):
<<<<<<< HEAD
        pps_dataframe = self.attack_detect.udp_flood_detect(100)
        suspicious = self.attack_detect.udp_suspicious
        # Initialize the central widget and layout for displaying the results.
        suspicious_text = ""
        explanation_text = ""
=======
        # Retrieve the threshold value from the input field. If it's empty, use a default value of 500.
        threshold = self.threshold_input.text()
        if threshold == '':
            threshold = 500
        else:
            threshold = int(threshold)

        canvas = self.attack_detect.udp_flood_detect(threshold)
        suspicious = self.attack_detect.udp_suspicious

        # Initialize the central widget and layout for displaying the results.
        central = QWidget()
        layout = QVBoxLayout()

        suspicious_text = ""

        # If no canvas is returned, it implies no UDP packets were detected.
        if canvas is None:
            suspicious_text = "No UDP packets present, no suspicious addresses detected"
        else:
            # Always add the canvas to the layout if it exists.
            layout.addWidget(canvas)  # This ensures canvas is displayed regardless of suspicious addresses detection.

            # If there are no suspicious addresses, update the text accordingly.
            if not suspicious:
                suspicious_text = "No suspicious addresses detected"
            else:
                # If there are suspicious addresses, compile them into a string for display.
                suspicious_text = "Suspicious addresses: " + ', '.join(suspicious)

        # Create a label to display the suspicious addresses or the status message.
        suspicious_label = QLabel(suspicious_text)
        suspicious_label.setFont(QFont('Arial', 25))
        suspicious_label.setAlignment(Qt.AlignCenter)
        suspicious_label.setWordWrap(True)

        layout.addWidget(suspicious_label)

        # Only add explanation if suspicious addresses were detected.
        if suspicious:
            explain_label = QLabel("Explanation:")
            explain_label.setFont(QFont('Arial', 25))

            explanation_text = ("These addresses were marked because the UDP packets sent from these addresses are "
                                "over a too high frequency")
            explanation_label = QLabel(explanation_text)
            explanation_label.setFont(QFont('Arial', 20))
            explanation_label.setWordWrap(True)

            layout.addWidget(suspicious_label)
            layout.addWidget(explain_label)
            layout.addWidget(explanation_label)

        self.setCentralWidget(central)
        central.setLayout(layout)

    def run_all_detect(self):
        threshold = self.threshold_input.text()
        if threshold == '':
            threshold = None
        else:
            threshold = int(threshold)

        self.attack_detect.run_all_detection(threshold)

        central = QWidget()
        layout = QVBoxLayout()

        dns_suspicious = self.attack_detect.dns_request_suspicious + self.attack_detect.dns_response_suspicious

        # Dictionary of attack detection methods in order to enumerate through them
        attack_list = {"DOS": self.attack_detect.dos_suspicious_addresses,
                       "TCP Scanning": self.attack_detect.tcp_scanning_suspicious,
                       "TCP": self.attack_detect.tcp_suspicious_addresses,
                       "ICMP": self.attack_detect.icmp_suspicious,
                       "HTTP": self.attack_detect.http_suspicious,
                       "ARP": self.attack_detect.arp_suspicious_addresses,
                       "DNS": dns_suspicious}

        # creates gui labels for each attack
        for attack in attack_list:
            suspicious_text = ""
            if not attack_list[attack]:
                suspicious_text = attack + ": no suspicious addresses detected"
            elif attack:
                suspicious_text = attack + " suspicious addresses: "
                suspicious_addresses = ', '.join(attack_list[attack])
                suspicious_text = suspicious_text + suspicious_addresses

            suspicious_label = QLabel(suspicious_text)
            suspicious_label.setFont(QFont('Arial', 15))
            suspicious_label.setWordWrap(True)

            layout.addWidget(suspicious_label)

        layout.addStretch()
        self.setCentralWidget(central)
        central.setLayout(layout)

    def display_flagged_addr(self):
        central = QWidget()
        layout = QVBoxLayout()

        suspicious = self.attack_detect.suspicious_addresses
>>>>>>> dev
        if not suspicious:
            suspicious_text = "No suspicious addresses detected"
        else:
            # If there are suspicious addresses, compile them into a string for display.
            suspicious_text = "Suspicious addresses: " + ', '.join(suspicious)

        # Only add explanation if suspicious addresses were detected.
        if suspicious:
            explanation_text = ("These addresses were marked because the UDP packets sent from these addresses are "
                                "over a too high frequency")
        if pps_dataframe is not None:
            data = {
                "suspicious": suspicious_text,
                "explanation": explanation_text,
                "data": []
            }
            for i in range(pps_dataframe.shape[0]):
                data["data"].append({
                    "address": pps_dataframe.loc[i, "Address"],
                    "rate": int(pps_dataframe.loc[i, "PPS"])
                })
            with open("src/pythonGUI/plotData/udpflood.json", "w+") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

    def ssl_stripping_detect(self):
        source_df, dest_df = self.attack_detect.ssl_stripping()
        suspicious_source = self.attack_detect.ssl_stripping_suspicious_source_address
        suspicious_dest = self.attack_detect.ssl_stripping_suspicious_destination_address
        suspicious_source_text = ""
        suspicious_dest_text = ""
        explanation_text = ""
        if not suspicious_source:
            suspicious_source_text = "No suspicious addresses detected"
            explanation_text = ("These addresses were marked suspicious because the packets from these addresses were "
                                "meant to use HTTPS but use HTTP instead.")
        else:
            suspicious_source_text = "Suspicious source addresses: " + ','.join(suspicious_source)
        if suspicious_dest:
            suspicious_dest_text = "Suspicious destination addresses: " + ','.join(suspicious_dest)
        if source_df is not None and dest_df is not None:
            source_data = {
                "suspicious": suspicious_source_text + '\n' + suspicious_dest_text,
                "explanation": explanation_text,
                "data": []
            }
            dest_data = {
                "data": []
            }
            for i in range(source_df.shape[0]):
                source_data["data"].append({
                    "address": source_df.loc[i, "Source IP"],
                    "frequency": int(source_df.loc[i, "Counts"])
                })
            for i in range(dest_df.shape[0]):
                dest_data["data"].append({
                    "address": dest_df.loc[i, "Destination IP"],
                    "frequency": int(dest_df.loc[i, "Counts"])
                })
            with open("src/pythonGUI/plotData/sslsource.json", "w+") as f:
                json.dump(source_data, f, ensure_ascii=False, indent=4)
            with open("src/pythonGUI/plotData/ssldest.json", "w+") as f:
                json.dump(dest_data, f, ensure_ascii=False, indent=4)

    def run_all_detect(self):
        self.tcp_syn_flood_detect()
        self.tcp_scanning_detect()
        self.dos_detect()
        self.arp_poison_detect()
        self.icmp_flood_detect()
        self.http_flood_detect()
        self.dns_flood_detect()
        self.udp_flood_detect()
        self.ssl_stripping_detect()

<<<<<<< HEAD

    
=======
        for line in lines:
            imported_ips.append(str(line))
        file.close()
>>>>>>> dev

   