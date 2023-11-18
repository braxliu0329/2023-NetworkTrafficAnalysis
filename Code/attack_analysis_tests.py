import os
import sys
import unittest

import matplotlib

matplotlib.use('Agg')
from scapy.sendrecv import sniff

from pythonGUI.capture_analysis import attack_detection, GUI_actions, dataframe_create


# One test case to wrap around all the tests
class MyTestCase(unittest.TestCase):
    # Define the actions for this to use as defined in GUI_actions
    def setUp(self):
        self.actions = GUI_actions.GUIActions()

    def test_tcp_flood(self):
        # pcap file without a TCP SYN flood attack
        self.actions.read_pcap("test_pcaps/dns.pcap", None)
        # define the method to get the packets
        read_false_packets = self.actions.get_sniffed_packets()
        # define the method to detect attacks using the sniffed packets
        attack_false_detect = attack_detection.AttackDetection(read_false_packets, [])

        # pcap file of a TCP Syn Flood attack with 2 addresses
        self.actions.read_pcap("test_pcaps/SYN.pcap", None)
        # define the method to get the packets
        read_packets = self.actions.get_sniffed_packets()
        # define the method to detect attacks using the sniffed packets
        attack_detect = attack_detection.AttackDetection(read_packets, [])

        # expected suspicious address
        known_sus = "10.128.0.2"
        # expected victim address
        known_vic = "10.0.0.2"

        # execute the tcp detection to test the method works correctly
        attack_detect.tcp_syn_flood_detect()
        # obtain the suspicious and victim addresses from the executed attack and store them in lists
        suspicious_addresses = attack_detect.tcp_suspicious_addresses
        attacked_addresses = attack_detect.attacked_addresses

        # execute the tcp detection on a file without a tcp attack to ensure it doesn't flag  a false positive
        attack_false_detect.tcp_syn_flood_detect()
        # obtain the suspicious and victim addresses from the executed attack and store them in lists
        false_suspicious_addresses = attack_false_detect.tcp_suspicious_addresses
        false_attacked_addresses = attack_false_detect.attacked_addresses

        # ensure that the method does not incur any false positives
        self.assertFalse(false_suspicious_addresses, "The TCP Flood Attack Analysis has detected false suspicious "
                                                     "addresses")
        self.assertFalse(false_attacked_addresses, "The TCP Flood Attack Analysis has detected false victim "
                                                   "addresses")

        # Tests whether the known suspicious and victim addresses appeared in the correct lists
        self.assertIn(known_sus, suspicious_addresses,
                      "The TCP Flood Attack Analysis has not detected an expected suspicious address")
        self.assertIn(known_vic, attacked_addresses,
                      "The TCP Flood Attack Analysis has not detected an expected victim address")
        self.assertNotIn(known_sus, attacked_addresses,
                         "The TCP Flood Attack Analysis has identified a suspicious address as an attacked address")
        self.assertNotIn(known_vic, suspicious_addresses,
                         "The TCP Flood Attack Analysis has identified an attacked address as a suspicious address")

    def test_tcp_scan_detect(self):
        # pcap file of a TCP connection
        self.actions.read_pcap("test_pcaps/SYN.pcap", None)
        # define the method to get the packets
        read_packets = self.actions.get_sniffed_packets()
        # define the method to detect attacks using the sniffed packets
        attack_detect = attack_detection.AttackDetection(read_packets, [])

        # expected suspicious address
        known_sus = "10.128.0.2"

        # execute the tcp connection scan to test the method works correctly, providing a low enough threshold to
        # detect the suspicious address
        attack_detect.tcp_connect_scanning_detect(100)
        # obtain the suspicious addresses from the attack and store them in a list
        suspicious_addresses = attack_detect.tcp_scanning_suspicious

        # Tests whether any suspicious addresses were detected
        self.assertTrue(suspicious_addresses)

        # Tests whether the known suspicious addresses appeared in the correct lists
        self.assertTrue(known_sus in suspicious_addresses)

        # execute the tcp connection scan to test the method works correctly, providing a threshold that should be too
        # high to detect the suspicious address
        attack_detect.tcp_connect_scanning_detect(10000)
        # obtain the suspicious addresses from the attack and store them in a new list
        suspicious_addresses_wthreshold = attack_detect.tcp_scanning_suspicious

        # Assert that the new suspicious address list is empty as expected
        self.assertTrue(known_sus not in suspicious_addresses_wthreshold)

    def test_arp_poison(self):
        # pcap file of an ARP poison attack with 2 addresses
        self.actions.read_pcap("test_pcaps/arp-poisoning.pcap", None)
        # define the method to get the packets
        read_packets = self.actions.get_sniffed_packets()
        # define the method to detect attacks using the sniffed packets
        attack_detect = attack_detection.AttackDetection(read_packets, [])

        # expected suspicious addresses
        known_sus = ['192.168.1.1', '192.168.1.254']

        # execute the arp poison detection to test the method works correctly
        attack_detect.arp_poison_detect()
        # obtain the suspicious addresses from the attack and store them in a list
        suspicious_addresses = attack_detect.arp_suspicious_addresses

        # assert that every expected address appears in the suspicious addresses list
        self.assertCountEqual(suspicious_addresses, known_sus)

    def test_icmp_flood(self):
        # pcap file of an icmp flood attack
        self.actions.read_pcap("test_pcaps/icmp-ping.pcap", None)
        # define the method to get the packets
        read_packets = self.actions.get_sniffed_packets()
        # define the method to detect attacks using the sniffed packets
        attack_detect = attack_detection.AttackDetection(read_packets, [])

        # expected suspicious address
        known_sus = '10.0.0.2'

        # execute the icmp flood detection to test the method works correctly, providing a low enough threshold to
        # detect the suspicious address
        attack_detect.icmp_flood_detect(100)
        # obtain the suspicious addresses from the attack and store them in a new list
        suspicious_addresses = attack_detect.icmp_suspicious

        # Tests whether the known suspicious address appeared in the correct lists
        self.assertTrue(known_sus in suspicious_addresses)

        # execute the icmp flood detection to test the method works correctly, providing a threshold that should be too
        # high to detect the suspicious address
        attack_detect.icmp_flood_detect(10000)
        # obtain the suspicious addresses from the attack and store them in a new list
        suspicious_addresses_wthreshold = attack_detect.icmp_suspicious
        # Assert that the new suspicious address list is empty as expected
        self.assertTrue(known_sus not in suspicious_addresses_wthreshold)

    def test_http_flood(self):
        # pcap file of a http flood attack
        self.actions.read_pcap("test_pcaps/http-flood.pcap", None)
        # define the method to get the packets
        read_packets = self.actions.get_sniffed_packets()
        # define the method to detect attacks using the sniffed packets
        attack_detect = attack_detection.AttackDetection(read_packets, [])

        # expected suspicious address
        known_sus = "10.0.0.2"

        # execute the http flood detection to test the method works correctly, providing a low enough threshold to
        # detect the suspicious address
        attack_detect.http_attack(5)
        # obtain the suspicious addresses from the attack and store them in a new list
        suspicious_addresses = attack_detect.http_suspicious

        # Tests whether the known suspicious address appeared in the correct lists
        self.assertTrue(known_sus in suspicious_addresses)

        # execute the http flood detection to test the method works correctly, providing a threshold that should be too
        # high to detect the suspicious address
        attack_detect.http_attack(500)
        # obtain the suspicious addresses from the attack and store them in a new list
        suspicious_addresses_wthreshold = attack_detect.http_suspicious
        # Assert that the new suspicious address list is empty as expected
        self.assertTrue(known_sus not in suspicious_addresses_wthreshold)

    def test_dns(self):
        # pcap file of a dns attack
        self.actions.read_pcap("test_pcaps/dns.pcap", None)
        # define the method to get the packets
        read_packets = self.actions.get_sniffed_packets()
        # define the method to detect attacks using the sniffed packets
        attack_detect = attack_detection.AttackDetection(read_packets, [])

        # expected suspicious request and response addresses
        known_request_sus = "207.86.6.174"
        known_response_sus = "205.94.14.222"

        # execute the dns detection to test the method works correctly, providing a low enough threshold to
        # detect the suspicious address
        attack_detect.dns_request_response_detect(20)
        # obtain the suspicious request and response addresses from the attack and store them in new lists
        request_sus_addresses = attack_detect.dns_request_suspicious
        response_sus_addresses = attack_detect.dns_response_suspicious

        # Tests whether the known suspicious request and response addresses appeared in the correct lists
        self.assertTrue(known_request_sus in request_sus_addresses)
        self.assertTrue(known_response_sus in response_sus_addresses)

        # execute the dns detection to test the method works correctly, providing a threshold that should be too
        # high to detect the suspicious address
        attack_detect.dns_request_response_detect(2000)
        # obtain the high-threshold suspicious request and response addresses from the attack and store them in new 
        # lists
        request_sus_addresses_wthreshold = attack_detect.dns_request_suspicious
        response_sus_addresses_wthreshold = attack_detect.dns_response_suspicious

        # Assert that the new suspicious address list is empty as expected
        self.assertTrue(known_request_sus not in request_sus_addresses_wthreshold)
        self.assertTrue(known_response_sus not in response_sus_addresses_wthreshold)

    def test_run_all(self):
        # pcap file containing dos and icmp attacks
        self.actions.read_pcap("test_pcaps/icmp-ping.pcap", None)
        # define the method to get the packets
        read_packets = self.actions.get_sniffed_packets()
        # define the method to detect attacks using the sniffed packets
        attack_detect = attack_detection.AttackDetection(read_packets, [])

        # define the attacks to execute as all the implemented attack detection methods
        attack_lists = {"TCP Scanning": attack_detect.tcp_scanning_suspicious,
                        "TCP": attack_detect.tcp_suspicious_addresses,
                        "HTTP": attack_detect.http_suspicious,
                        "ARP": attack_detect.arp_suspicious_addresses,
                        "DNSreq": attack_detect.dns_request_suspicious,
                        "DNS": attack_detect.dns_response_suspicious}

        # the expected suspicious value that should be flagged for icmp and dos attacks
        known_sus = "10.0.0.2"

        # execute all detection methods to test the methods work correctly, providing a low enough threshold to
        # detect the suspicious address
        attack_detect.run_all_detection(500)

        # Checks that the address is not in all the lists it shouldn't be
        for attack_sus in attack_lists:
            self.assertTrue(known_sus not in attack_sus)

        # check that the suspicious address is in the expected attack lists
        self.assertTrue(known_sus in attack_detect.dos_suspicious_addresses)
        self.assertTrue(known_sus in attack_detect.icmp_suspicious)

        # Run with high threshold so should not be any list
        attack_detect.run_all_detection(5000)

        # assert that the suspicious address isn't in any list
        for attack_sus in attack_lists:
            self.assertTrue(known_sus not in attack_sus)

        self.assertTrue(known_sus not in attack_detect.dos_suspicious_addresses)
        self.assertTrue(known_sus not in attack_detect.icmp_suspicious)


if __name__ == '__main__':
    unittest.main()
