import json

from PyQt5.QtWidgets import *


from pythonGUI.capture_analysis import attack_detection as attacking


class AttackAnalysis():
    def __init__(self, data, flagged_IPs):
        self.data_use = data
        self.flagged_IPs = flagged_IPs
        self.attack_detect = attacking.AttackDetection(self.data_use, self.flagged_IPs)

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

        if not attacked:
            attacked_text = "No attacked addresses detected"
        elif attacked:
            attacked_text = "Suspected Attacked addresses: "
            attacked_addresses = ', '.join(attacked)
            attacked_text = attacked_text + attacked_addresses
        explanation_text = "The suspicious addresses were marked because these addresses send a greater amount of " \
                           "SYN requests than it does receive SYN-ACK responses back, suggesting it is overloading a" \
                           "system. \nThe attacked addresses were marked because these addresses receive a greater " \
                           "amount of SYN requests than it sends SYN-ACK responses back, which is indicative that " \
                           "these addresses are being overwhelmed by SYN requests and cant response fast enough. "
        if not syn_addresses.empty:
            data = {
                "suspicious": suspicious_text,
                "attacked": attacked_text,
                "explanation": explanation_text,
                "data": []
            }
            for i in range(syn_addresses.shape[0]):
                data["data"].append({
                    "address": syn_addresses.loc[i, "Address"],
                    "sendsSYN": int(syn_addresses.loc[i, "SendsSYN"]),
                    "receivesSYN": int(syn_addresses.loc[i, "ReceivesSYN"]),
                    "sendSYNACK" : int(syn_addresses.loc[i, "SendsSYN-ACK"]),
                    "receivesSYNACK": int(syn_addresses.loc[i, "ReceivesSYN-ACK"])
                })
            with open("src/pythonGUI/plotData/tcpsyn.json", "w+") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

    def tcp_scanning_detect(self):
        syn_rate = self.attack_detect.tcp_connect_scanning_detect(100)
        suspicious = self.attack_detect.tcp_scanning_suspicious

        suspicious_text = ""
        if not suspicious:
            suspicious_text = "No suspicious addresses detected"
        elif suspicious:
            suspicious_text = "Suspicious addresses: "
            suspicious_addresses = ', '.join(suspicious)
            suspicious_text = suspicious_text + suspicious_addresses


        explanation_text = "Addresses are marked as suspicious if the address sends SYN flags without receiving " \
                           "SYN-ACK packets and if the same address sends more SYN packets than the  within " \
                           "the time interval. "
        if syn_rate:
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


        if not suspicious:
            suspicious_text = "No suspicious addresses detected"
        elif suspicious:
            suspicious_text = "Suspicious addresses: "
            suspicious_addresses = ', '.join(suspicious)
            suspicious_text = suspicious_text + suspicious_addresses
            explanation_label = QLabel(
                    "These addresses are sending a greater amount of traffic then the  and therefore are marked as suspicious.")
        if pps_table:
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
        if not suspicious:
            suspicious_text = "No suspicious addresses detected"
        elif suspicious:
            suspicious_text = "Suspicious addresses: "
            suspicious_addresses = ', '.join(suspicious)
            suspicious_text = suspicious_text + suspicious_addresses
        explanation_text = "These addresses were marked because the MAC addresses they originated from are associated " \
                           "with more than one IP address, which is erroneous and indicative of ARP Poisoning."
        if mac_addr_fre:
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
        if not suspicious:
            suspicious_text = "No suspicious addresses detected"
        elif suspicious:
            suspicious_text = "Suspicious addresses: "
            suspicious_addresses = ', '.join(suspicious)
            suspicious_text = suspicious_text + suspicious_addresses
        explanation_text = "These addresses were marked because the ICMP Echo packets sent from these addresses are " \
                           "over too high a frequency. "
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
            with open("src/pythonGUI/plotData/icmpflood.json", "w+") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

    def http_flood_detect(self):
        pps_dataframe = self.attack_detect.http_attack(100)
        suspicious = self.attack_detect.http_suspicious
        suspicious_text = ""
        if not suspicious:
            suspicious_text = "No suspicious addresses detected"
        elif suspicious:
            suspicious_text = "Suspicious addresses: "
            suspicious_addresses = ', '.join(suspicious)
            suspicious_text = suspicious_text + suspicious_addresses
        explanation_text = "These addresses were marked because the HTTP Request packets sent from these addresses " \
                           "after a tcp connection are established are " \
                           "over too high a frequency. "
        if not pps_dataframe.empty:
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

        
        if not response_suspicious:
            request_suspicious_text = "No DNS Response suspicious addresses detected"
        elif response_suspicious:
            response_suspicious_text = "DNS Response suspicious addresses: "
            suspicious_addresses = ', '.join(response_suspicious)
            response_suspicious_text = response_suspicious_text + suspicious_addresses

            suspicious_text = request_suspicious_text + "\n" + response_suspicious_text
        explanation_text = "These addresses were marked because the DNS packets sent from these addresses are " \
                           "over too high a frequency. "
        if pps_req or pps_res:
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

    def run_all_detect(self):
        self.tcp_syn_flood_detect()
        self.tcp_scanning_detect()
        self.dos_detect()
        self.arp_poison_detect()
        self.icmp_flood_detect()
        self.http_flood_detect()
        self.dns_flood_detect()


    

   