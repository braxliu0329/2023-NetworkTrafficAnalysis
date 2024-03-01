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
Initializes the AttackAnalysisWindow with necessary data and setups UI components.

```cython
class AttackAnalysisWindow(attack_analysis_window.Ui_MainWindow, QMainWindow):
    def __init__(self, data, main_window, flagged_IPs):
        super(AttackAnalysisWindow, self).__init__()
        self.setupUi(self)
        self.data_use = data
        self.parent = main_window
        self.flagged_IPs = flagged_IPs
        self.attack_detect = attacking.AttackDetection(self.data_use, self.flagged_IPs)
```

Binds UI actions to their corresponding methods for detecting various types of network attacks.
Each action, when triggered, calls a specific method to analyze the data for a particular type of attack.
```cython
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
Overrides the close event of the QMainWindow to perform custom operations when the AttackAnalysisWindow is being closed. 
It ensures that any new suspicious addresses identified during the current session are saved to the main window's list
of flagged IPs for persistent tracking across sessions.

```cython
def closeEvent(self, event):
    for address in self.attack_detect.suspicious_addresses:
        if address not in self.parent.flaggedIPs:
            self.parent.flaggedIPs.append(address)
    event.accept()
```

## TCP SYN Flood Detection
Retrieves the resulting canvas and address lists.
```cython
def tcp_syn_flood_detect(self):
    # gets graph canvas from calling attack detection method
    canvas = self.attack_detect.tcp_syn_flood_detect()
    suspicious = self.attack_detect.tcp_suspicious_addresses
    attacked = self.attack_detect.attacked_addresses
```

Sets up the central widget and layout for displaying detection results.
```cython
# creates main widget and layout
central = QWidget()
layout = QVBoxLayout()

suspicious_text = ""
attacked_text = ""
```

Checks weather graph was created and shows information for different situation
```cython
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
```

Compiles the information into a label for display.
```cython
suspicious_label = QLabel(suspicious_text + "\n" + attacked_text)
suspicious_label.setFont(QFont('Arial', 25))
suspicious_label.setAlignment(Qt.AlignCenter)
```

Describes the reason behind marking addresses as suspicious or attacked.
```cython
explanation_text = "The suspicious addresses were marked because these addresses send a greater amount of " \
                   "SYN requests than it does receive SYN-ACK responses back, suggesting it is overloading a" \
                   "system. \n\nThe attacked addresses were marked because these addresses receive a greater " \
                   "amount of SYN requests than it sends SYN-ACK responses back, which is indicative that " \
                   "these addresses are being overwhelmed by SYN requests and cant response fast enough. "
```

Sets up labels for the explanation text.
```cython
explain_label = QLabel("\nExplanation:")
explain_label.setFont(QFont('Arial', 25))

explanation_label = QLabel(explanation_text)
explanation_label.setFont(QFont('Arial', 20))
explanation_label.setAlignment(Qt.AlignLeft)
explanation_label.setWordWrap(True)

layout.addWidget(canvas)
layout.addWidget(suspicious_label)
```

Adds the canvas and labels to the layout.
```cython
if canvas is not None:
    layout.addWidget(explain_label)
    layout.addWidget(explanation_label)
    layout.addStretch()
```

Applies the layout to the central widget and sets it as the main content of the window.
```cython
self.setCentralWidget(central)
central.setLayout(layout)
```

## TCP Scanning Detection
Retrieves and sets threshold value for detection from the user input
```cython
def tcp_scanning_detect(self):
    threshold = self.threshold_input.text()
    if threshold == '':
        threshold = 100
    else:
        threshold = int(threshold)
```

obtain a canvas and suspicious list of address for visualization
```cython
canvas = self.attack_detect.tcp_connect_scanning_detect(threshold)
suspicious = self.attack_detect.tcp_scanning_suspicious
```

Sets up the central widget and layout for displaying detection results.
```cython
central = QWidget()
layout = QVBoxLayout()
```

Checks weather graph was created and shows information for different situation
```cython
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
```

Describes the reason behind marking addresses as suspicious or attacked.
```cython 
explain_label = QLabel("\nExplanation:")
explain_label.setFont(QFont('Arial', 25))

explanation_text = "Addresses are marked as suspicious if the address sends SYN flags without receiving " \
                   "SYN-ACK packets and if the same address sends more SYN packets than the threshold within " \
                   "the time interval. "
```

Displays the suspicious addresses and explanation.
```cython
explanation_label = QLabel(explanation_text)
explanation_label.setFont(QFont('Arial', 20))
explanation_label.setWordWrap(True)

suspicious_label = QLabel(suspicious_text)
suspicious_label.setFont(QFont('Arial', 25))
suspicious_label.setAlignment(Qt.AlignCenter)
suspicious_label.setWordWrap(True)
```

Adds the canvas and labels to the layout, if applicable.
Applies the layout to the central widget and sets it as the main content of the window.
```cython
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
Retrieves and sets threshold value for detection from the user input
```cython
def dos_detect(self):
    threshold = self.threshold_input.text()
    if threshold == '':
        threshold = 200
    else:
        threshold = int(threshold)
```

obtain a canvas and suspicious list of address for visualization
```cython
canvas = self.attack_detect.threshold_dos_detect(threshold)
suspicious = self.attack_detect.dos_suspicious_addresses
```

Sets up the central widget and layout for displaying detection results.
```cython
central = QWidget()
layout = QVBoxLayout()
```

Checks weather graph was created and shows information for different situation
```cython
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
```

Displays the suspicious addresses and explanation.
```cython
suspicious_label = QLabel(suspicious_text)
suspicious_label.setFont(QFont('Arial', 25))
suspicious_label.setAlignment(Qt.AlignCenter)
suspicious_label.setWordWrap(True)

explain_label = QLabel("\nExplanation:")
explain_label.setFont(QFont('Arial', 25))

explanation_label.setFont(QFont('Arial', 20))
explanation_label.setWordWrap(True)
```

Adds the canvas and labels to the layout, if applicable.
Applies the layout to the central widget and sets it as the main content of the window.
```cython
layout.addWidget(canvas)
layout.addWidget(suspicious_label)
layout.addWidget(explain_label)
layout.addWidget(explanation_label)
layout.addStretch()

self.setCentralWidget(central)
central.setLayout(layout)
```

## ARP Poison Detection
Retrieves the resulting canvas and address lists.
```cython
def arp_poison_detect(self):
    canvas = self.attack_detect.arp_poison_detect()
    suspicious = self.attack_detect.arp_suspicious_addresses
```

Sets up the central widget and layout for displaying detection results.
```cython
central = QWidget()
layout = QVBoxLayout()

suspicious_text = ""
```

Checks weather graph was created and shows information for different situation
```cython
if canvas is None:
    suspicious_text = "No ARP packets present, no suspicious addresses detected"

else:
    if not suspicious:
        suspicious_text = "No suspicious addresses detected"
    elif suspicious:
        suspicious_text = "Suspicious addresses: "
        suspicious_addresses = ', '.join(suspicious)
        suspicious_text = suspicious_text + suspicious_addresses
```

Compiles the information into a label for display.
```cython
suspicious_label = QLabel(suspicious_text)
suspicious_label.setFont(QFont('Arial', 25))
suspicious_label.setAlignment(Qt.AlignCenter)
suspicious_label.setWordWrap(True)
```

Describes the reason behind marking addresses as suspicious or attacked.
```cython
explanation_text = "These addresses were marked because the MAC addresses they originated from are associated " \
                   "with more than one IP address, which is erroneous and indicative of ARP Poisoning."
```

Sets up labels for the explanation text.
```cython
explain_label = QLabel("\nExplanation:")
explain_label.setFont(QFont('Arial', 25))
explanation_label = QLabel(explanation_text)
explanation_label.setFont(QFont('Arial', 20))
explanation_label.setWordWrap(True)

layout.addWidget(canvas)
layout.addWidget(suspicious_label)
```

Adds the canvas and labels to the layout.
```cython
if canvas is not None:
    layout.addWidget(explain_label)
    layout.addWidget(explanation_label)
    layout.addStretch()
```

Applies the layout to the central widget and sets it as the main content of the window.
```cython
self.setCentralWidget(central)
central.setLayout(layout)
```

## ICMP flood detection
Retrieves and sets threshold value for detection from the user input
```cython
def icmp_flood_detect(self):
    threshold = self.threshold_input.text()
    if threshold == '':
        threshold = 100
    else:
        threshold = int(threshold)
```

obtain a canvas and suspicious list of address for visualization
```cython
canvas = self.attack_detect.icmp_flood_detect(threshold)
suspicious = self.attack_detect.icmp_suspicious
```

Sets up the central widget and layout for displaying detection results.
```cython
central = QWidget()
layout = QVBoxLayout()
```

Checks weather graph was created and shows information for different situation
```cython
suspicious_text = ""

if canvas is None:
    suspicious_text = "No ICMP packets present, no suspicious addresses detected"
else:
    if not suspicious:
        suspicious_text = "No suspicious addresses detected"
    elif suspicious:
        suspicious_text = "Suspicious addresses: "
        suspicious_addresses = ', '.join(suspicious)
        suspicious_text = suspicious_text + suspicious_addresses
```

Describes the reason behind marking addresses as suspicious or attacked.
```cython
suspicious_label = QLabel(suspicious_text)
suspicious_label.setFont(QFont('Arial', 25))
suspicious_label.setAlignment(Qt.AlignCenter)
suspicious_label.setWordWrap(True)

explain_label = QLabel("\nExplanation:")
explain_label.setFont(QFont('Arial', 25))
explanation_text = "These addresses were marked because the ICMP Echo packets sent from these addresses are " \
                   "over too high a frequency. "
```

Adds the canvas and labels to the layout, if applicable.
Applies the layout to the central widget and sets it as the main content of the window.
```cython
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

## http flood detection
Retrieves and sets threshold value for detection from the user input
```cython
def http_flood_detect(self):
    threshold = self.threshold_input.text()
    if threshold == '':
        threshold = 5
    else:
        threshold = int(threshold)
```

obtain a canvas and suspicious list of address for visualization
```cython
canvas = self.attack_detect.http_attack(threshold)
suspicious = self.attack_detect.http_suspicious
```

Sets up the central widget and layout for displaying detection results.
```cython
central = QWidget()
layout = QVBoxLayout()
```

Checks weather graph was created and shows information for different situation
```cython
suspicious_text = ""

if canvas is None:
    suspicious_text = "No HTTP packets present or no TCP handshake was established, no suspicious addresses detected"
else:
    if not suspicious:
        suspicious_text = "No suspicious addresses detected"
    elif suspicious:
        suspicious_text = "Suspicious addresses: "
        suspicious_addresses = ', '.join(suspicious)
        suspicious_text = suspicious_text + suspicious_addresses
```

Displays the suspicious addresses and explanation.
```cython
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
```

Adds the canvas and labels to the layout, if applicable.
Applies the layout to the central widget and sets it as the main content of the window.
```cython
    layout.addWidget(canvas)
    layout.addWidget(suspicious_label)

    if canvas is not None:
        layout.addWidget(explain_label)
        layout.addWidget(explanation_label)
        layout.addStretch()

    self.setCentralWidget(central)
    central.setLayout(layout)
```

## DNS flood detection 
Retrieves and sets the threshold value for detection from user input.
```cython
def dns_flood_detect(self):
    threshold = self.threshold_input.text()
    if threshold == '':
        threshold = 20
    else:
        threshold = int(threshold)
```

Obtains canvases for visualization of request and response packets.
```cython
canvases = self.attack_detect.dns_request_response_detect(threshold)
```

Sets up the central widget and layout for displaying detection results.
```cython
central = QWidget()
layout = QVBoxLayout()
```

Separates the canvases for request and response graphs.
```cython
request_graph = canvases[0]
response_graph = canvases[1]
```

Determines the message to display based on detection outcome.
```cython
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
```

creating a user interface layout to display the results of a DNS flood detection process
```cython
suspicious_text = request_suspicious_text + "\n" + response_suspicious_text

layout.addWidget(request_graph)
layout.addWidget(response_graph)

suspicious_label = QLabel(suspicious_text)
suspicious_label.setFont(QFont('Arial', 25))
suspicious_label.setAlignment(Qt.AlignCenter)
suspicious_label.setWordWrap(True)

explain_label = QLabel("\nExplanation:")
explain_label.setFont(QFont('Arial', 25))

explanation_text = "These addresses were marked because the DNS packets sent from these addresses are " \
               "over too high a frequency. "

explanation_label = QLabel(explanation_text)
explanation_label.setFont(QFont('Arial', 20))
explanation_label.setWordWrap(True)

layout.addWidget(suspicious_label)
```

Only displays explanation if there are suspicious addresses.
```cython
if request_graph is not None or response_graph is not None:
    layout.addWidget(explain_label)
    layout.addWidget(explanation_label)
    layout.addStretch()

self.setCentralWidget(central)
central.setLayout(layout)
```

## UDP flood detection
Retrieves and sets threshold value for detection from the user input
```cython
def udp_flood_detect(self):
    # Retrieve the threshold value from the input field. If it's empty, use a default value of 500.
    threshold = self.threshold_input.text()
    if threshold == '':
        threshold = 500
    else:
        threshold = int(threshold)
```

obtain a canvas and suspicious list of address for visualization
```cython
canvas = self.attack_detect.udp_flood_detect(threshold)
suspicious = self.attack_detect.udp_suspicious
```

Sets up the central widget and layout for displaying detection results.
```cython
central = QWidget()
layout = QVBoxLayout()
```

Checks weather graph was created and shows information for different situation
```cython
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
```

Displays the suspicious addresses
```cython
    # Create a label to display the suspicious addresses or the status message.
    suspicious_label = QLabel(suspicious_text)
    suspicious_label.setFont(QFont('Arial', 25))
    suspicious_label.setAlignment(Qt.AlignCenter)
    suspicious_label.setWordWrap(True)
```

Adds the canvas and labels to the layout, if applicable.
Applies the layout to the central widget and sets it as the main content of the window.
```cython
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
```
## display flagged address

Setting Up the Main Widget and Layout
```cython
def display_flagged_addr(self):
    central = QWidget()
    layout = QVBoxLayout()
```

Displaying Suspicious Addresses
```cython
suspicious = self.attack_detect.suspicious_addresses
if not suspicious:
    suspicious_text = "No suspicious addresses detected"
elif suspicious:
    suspicious_text = "Suspicious addresses: "
    suspicious_addresses = ', '.join(suspicious)
    suspicious_text = suspicious_text + suspicious_addresses
suspicious_label = QLabel(suspicious_text)
suspicious_label.setFont(QFont('Arial', 15))
suspicious_label.setWordWrap(True)

layout.addWidget(suspicious_label)
```

creates save button, connect and add save button to the layout
```cython
save_button = QPushButton(central)
save_button.setText("Save flagged IP addresses")
save_button.clicked.connect(self.saveIPList)
```

creates, connect and add import button to the layout
```cython
import_button = QPushButton(central)
import_button.setText("Import flagged IP addresses")
import_button.clicked.connect(self.importIPList)
layout.addWidget(save_button)
```

Finalizing the Window
```cython
layout.addWidget(import_button)
self.setCentralWidget(central)
central.setLayout(layout)
```

## Save IP address list 
save the list of suspicious IP addresses to a text file. 
```cython
def saveIPList(self):
    file_name = QFileDialog.getSaveFileName(self, 'Save File')
    addresses = self.attack_detect.suspicious_addresses

    if file_name[0] != "":
        file_name_txt = file_name[0] + ".txt"
        file = open(file_name[0], 'w')
        for ip in addresses:
            file.write(ip + '\n')
        file.close()
```

## Import IP address list
import a list of IP addresses from a file and update the list of flagged IP addresses
```cython
def importIPList(self):
    imported_ips = []
    file_name = QFileDialog.getOpenFileName(self, 'Open file', "", 'All files (*);; txt (*.txt)')

    file = open(file_name[0], 'r')

    lines = file.read().splitlines()

    for line in lines:
        imported_ips.append(str(line))
    file.close()

    self.attack_detect.update_flagged_ips(imported_ips)
    self.display_flagged_addr()
```
