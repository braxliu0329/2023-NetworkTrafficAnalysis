# Attack analysis action
PyQt5-based GUI application for analyzing network traffic to detect various types of network attacks.
script is structured into several sections, each responsible for initializing the main window, handling events, and implementing specific network attack detection functionalities.

## Dependencies
```cython
from PyQt5 import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import *
import sys

from pythonGUI.capture_analysis import attack_detection as attacking
from pythonGUI.capture_analysis import plotting
from pythonGUI import attack_analysis_window
```
## Initialization and UI Setup
```cython
class AttackAnalysisWindow(attack_analysis_window.Ui_MainWindow, QMainWindow):
    def __init__(self, data, main_window, flagged_IPs):
        super(AttackAnalysisWindow, self).__init__()
        self.setupUi(self)
        self.data_use = data

        self.parent = main_window
        self.flagged_IPs = flagged_IPs
        self.attack_detect = attacking.AttackDetection(self.data_use, self.flagged_IPs)

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
        self.imported_IPs = []
```

## Close Event Handling
```cython
    def closeEvent(self, event):
        for address in self.attack_detect.suspicious_addresses:
            if address not in self.parent.flaggedIPs:
                self.parent.flaggedIPs.append(address)
        event.accept()
```

## TCP SYN Flood Detection
```cython
    def tcp_syn_flood_detect(self):
        # gets graph canvas from calling attack detection method
        canvas = self.attack_detect.tcp_syn_flood_detect()
        suspicious = self.attack_detect.tcp_suspicious_addresses
        attacked = self.attack_detect.attacked_addresses

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

        suspicious_label = QLabel(suspicious_text + "\n" + attacked_text)
        suspicious_label.setFont(QFont('Arial', 25))
        suspicious_label.setAlignment(Qt.AlignCenter)

        explanation_text = "The suspicious addresses were marked because these addresses send a greater amount of " \
                           "SYN requests than it does receive SYN-ACK responses back, suggesting it is overloading a" \
                           "system. \n\nThe attacked addresses were marked because these addresses receive a greater " \
                           "amount of SYN requests than it sends SYN-ACK responses back, which is indicative that " \
                           "these addresses are being overwhelmed by SYN requests and cant response fast enough. "

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
```

## TCP Scanning Detection
```cython
    def tcp_scanning_detect(self):
        threshold = self.threshold_input.text()
        if threshold == '':
            threshold = 100
        else:
            threshold = int(threshold)

        canvas = self.attack_detect.tcp_connect_scanning_detect(threshold)
        suspicious = self.attack_detect.tcp_scanning_suspicious

        central = QWidget()
        layout = QVBoxLayout()

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
        explain_label.setFont(QFont('Arial', 25))

        explanation_text = "Addresses are marked as suspicious if the address sends SYN flags without receiving " \
                           "SYN-ACK packets and if the same address sends more SYN packets than the threshold within " \
                           "the time interval. "

        explanation_label = QLabel(explanation_text)
        explanation_label.setFont(QFont('Arial', 20))
        explanation_label.setWordWrap(True)

        suspicious_label = QLabel(suspicious_text)
        suspicious_label.setFont(QFont('Arial', 25))
        suspicious_label.setAlignment(Qt.AlignCenter)
        suspicious_label.setWordWrap(True)

        layout.addWidget(canvas)
        layout.addWidget(suspicious_label)

        if canvas is not None:
            layout.addWidget(explain_label)
            layout.addWidget(explanation_label)
            layout.addStretch()

        self.setCentralWidget(central)
        central.setLayout(layout)
```

## DoS Detection
```cython
    def dos_detect(self):
        threshold = self.threshold_input.text()
        if threshold == '':
            threshold = 200
        else:
            threshold = int(threshold)

        canvas = self.attack_detect.threshold_dos_detect(threshold)
        suspicious = self.attack_detect.dos_suspicious_addresses

        central = QWidget()
        layout = QVBoxLayout()

        suspicious_text = ""
        explanation_label = QLabel("")

        if canvas is None:
            suspicious_text = "No packets present"
        else:
            if not suspicious:
                suspicious_text = "No suspicious addresses detected"
            elif suspicious:
                suspicious_text = "Suspicious addresses: "
                suspicious_addresses = ', '.join(suspicious)
                suspicious_text = suspicious_text + suspicious_addresses
                explanation_label = QLabel(
                    "These addresses are sending a greater amount of traffic then the threshold and therefore are marked as suspicious.")

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
```

## ARP Poison Detection
```cython
    def arp_poison_detect(self):
        canvas = self.attack_detect.arp_poison_detect()
        suspicious = self.attack_detect.arp_suspicious_addresses

        central = QWidget()
        layout = QVBoxLayout()

        suspicious_text = ""
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

```