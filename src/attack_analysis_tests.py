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

    # set up an attack detection method by adding the packets in the provided file to sniffed packets, returning an
    # attack method using ALL sniffed packets
    def setUpAttackDetection(self, filename):
        # pcap file provided using filename
        self.actions.read_pcap("test_pcaps/" + filename + ".pcap", None)
        # define the method to get the packets
        read_packets = self.actions.get_sniffed_packets()
        # define the method to detect attacks using the sniffed packets
        return attack_detection.AttackDetection(read_packets, [])
 
    def test_ssl_stripping(self):
        attack_detect = self.setUpAttackDetection("ssl_stripping")
        known_source = "192.168.1.100"
        known_destination = "192.168.1.1"

        attack_detect.ssl_stripping()

        suspicious_source_address = attack_detect.ssl_stripping_suspicious_source_address
        suspicious_destination_address = attack_detect.ssl_stripping_suspicious_destination_address

        # Tests whether the known suspicious and victim addresses appeared in the correct lists
        self.assertIn(known_source, suspicious_source_address,
                      "The SSL_Stripping Attack Analysis has not detected an expected suspicious address")
        self.assertIn(known_destination, suspicious_destination_address,
                      "The SSL_Stripping Attack Analysis has not detected an expected victim address")
        self.assertNotIn(known_source, suspicious_destination_address,
                         "The SSL_Stripping Attack Analysis has identified a suspicious address as an attacked address")
        self.assertNotIn(known_destination, suspicious_source_address,
                         "The SSL_Stripping Attack Analysis has identified an attacked address as a suspicious address")

    def test_ssl_stripping_false(self):
        attack_false_detect = self.setUpAttackDetection("SYN")
        attack_false_detect.ssl_stripping()

        false_suspicious_source_address = attack_false_detect.ssl_stripping_suspicious_source_address
        false_suspicious_destination_address = attack_false_detect.ssl_stripping_suspicious_destination_address

        self.assertFalse(false_suspicious_source_address, "The SSL_Stripping Attack Analysis has detected false "
                                                          "suspicious source addresses ")
        self.assertFalse(false_suspicious_destination_address, "The SSL_Stripping Attack Analysis has detected "
                                                               "false destination addresses")

    def test_udp_flood(self):
        # set up an attack detection using a pcap file with udp flood attacks
        attack_detect = self.setUpAttackDetection("udp_flood")

        # expected suspicious address
        known_sus = '123.123.123.123'

        # execute the udp flood detection to test the method work correctly, providing a long enough threshold
        # detect the suspicious address
        attack_detect.udp_flood_detect(100)
        # obtain the suspicious addresses from the attack and store them in a new list
        suspicious_addresses = attack_detect.udp_suspicious

        # execute the udp flood detection to test the method works correctly, providing a threshold that should be too
        # high to detect the suspicious address
        attack_detect.udp_flood_detect(20000)
        # obtain the suspicious addresses from the attack and store them in a new list
        suspicious_addresses_wthreshold = attack_detect.udp_suspicious

        # Tests whether the known suspicious address appeared in the correct lists
        self.assertIn(known_sus, suspicious_addresses,
                      "The UDP Flood Analysis does not contain exactly all expected suspicious addresses")
        # Assert that the new suspicious address list is empty as expected
        self.assertNotIn(known_sus, suspicious_addresses_wthreshold,
                         "The UDP Flood Analysis has detected an unexpected suspicious address given a high threshold")

    def test_udp_flood_false(self):
        # set up an attack detection using a pcap file without udp flood attacks
        attack_false_detect = self.setUpAttackDetection("dns")

        # execute the udp detection on a file that shouldn't flag any suspicion
        attack_false_detect.udp_flood_detect(100)
        # obtain the suspicious addresses from the attack and store them in a list
        false_suspicious_addresses = attack_false_detect.udp_suspicious

        # ensure that the method does not incur any false positives for clean packets
        self.assertFalse(false_suspicious_addresses,
                         "the udp flood analysis has detected false suspicious addresses")

    def test_tcp_flood_false(self):
        # set up an attack detection using a pcap file without tcp flood attacks
        attack_false_detect = self.setUpAttackDetection("dns")

        # execute the tcp detection on a file without a tcp attack to ensure it doesn't flag  a false positive
        attack_false_detect.tcp_syn_flood_detect()
        # obtain the suspicious and victim addresses from the executed attack and store them in lists
        false_suspicious_addresses = attack_false_detect.tcp_suspicious_addresses
        false_attacked_addresses = attack_false_detect.attacked_addresses

        # ensure that the method does not incur any false positives
        self.assertFalse(false_suspicious_addresses, "The TCP Flood Attack Analysis has detected false suspicious "
                                                     "addresses ")
        self.assertFalse(false_attacked_addresses, "The TCP Flood Attack Analysis has detected false victim "
                                                   "addresses")

    def test_tcp_flood(self):
        # set up an attack detection adding a pcap file with a tcp flood attack
        attack_detect = self.setUpAttackDetection("SYN")

        # expected suspicious address
        known_sus = "10.128.0.2"
        # expected victim address
        known_vic = "10.0.0.2"

        # execute the tcp detection to test the method works correctly
        attack_detect.tcp_syn_flood_detect()
        # obtain the suspicious and victim addresses from the executed attack and store them in lists
        suspicious_addresses = attack_detect.tcp_suspicious_addresses
        attacked_addresses = attack_detect.attacked_addresses

        # Tests whether the known suspicious and victim addresses appeared in the correct lists
        self.assertIn(known_sus, suspicious_addresses,
                      "The TCP Flood Attack Analysis has not detected an expected suspicious address")
        self.assertIn(known_vic, attacked_addresses,
                      "The TCP Flood Attack Analysis has not detected an expected victim address")
        self.assertNotIn(known_sus, attacked_addresses,
                         "The TCP Flood Attack Analysis has identified a suspicious address as an attacked address")
        self.assertNotIn(known_vic, suspicious_addresses,
                         "The TCP Flood Attack Analysis has identified an attacked address as a suspicious address")

    def test_tcp_scan_detect_false(self):
        # set up an attack detection using a pcap file without tcp flood attacks
        attack_false_detect = self.setUpAttackDetection("dns")

        # execute the tcp connection on a file that shouldn't flag any suspicion
        attack_false_detect.tcp_connect_scanning_detect(100)
        # obtain the suspicious addresses from the attack and store them in a list
        false_suspicious_addresses = attack_false_detect.tcp_scanning_suspicious

        # ensure that the method does not incur any false positives for clean data packets
        self.assertFalse(false_suspicious_addresses,
                         "The TCP Connect Scanning Analysis has detected false suspicious addresses")

    def test_tcp_scan_detect(self):
        # set up an attack detection adding a pcap file with a tcp flood attack
        attack_detect = self.setUpAttackDetection("SYN")

        # expected suspicious address
        known_sus = "10.128.0.2"

        # execute the tcp connection scan to test the method works correctly, providing a low enough threshold to
        # detect the suspicious address
        attack_detect.tcp_connect_scanning_detect(100)
        # obtain the suspicious addresses from the attack and store them in a list
        suspicious_addresses = attack_detect.tcp_scanning_suspicious

        # execute the tcp connection scan to test the method works correctly, providing a threshold that should be too
        # high to detect the suspicious address
        attack_detect.tcp_connect_scanning_detect(10000)
        # obtain the suspicious addresses from the attack and store them in a new list
        suspicious_addresses_wthreshold = attack_detect.tcp_scanning_suspicious

        # Tests whether the known suspicious addresses appeared in the correct lists
        self.assertIn(known_sus, suspicious_addresses,
                      "The TCP Connect Scanning Analysis has not detected an expected suspicious address")

        # Assert that the new suspicious address list is empty as expected
        self.assertNotIn(known_sus, suspicious_addresses_wthreshold,
                         "The TCP Connect Scanning Analysis has detected an unexpected suspicious address given a high "
                         "threshold")

    def test_arp_poison_false(self):
        # set up an attack detection using a pcap file without arp poisoning attacks
        attack_false_detect = self.setUpAttackDetection("dns")

        # execute the arp poisoning on a file that shouldn't flag any suspicion
        attack_false_detect.arp_poison_detect()
        # obtain the suspicious addresses from the attack and store them in a list
        false_suspicious_addresses = attack_false_detect.arp_suspicious_addresses

        # ensure that the method does not incur any false positives for clean packets
        self.assertFalse(false_suspicious_addresses,
                         "The ARP Poisoning Analysis has detected false suspicious addresses")

    def test_arp_poison(self):
        # set up an attack detection adding a pcap file with arp poisoning attacks
        attack_detect = self.setUpAttackDetection("arp-poisoning")

        # expected suspicious addresses
        known_sus = ['192.168.1.1', '192.168.1.254']

        # execute the arp poison detection to test the method works correctly
        attack_detect.arp_poison_detect()
        # obtain the suspicious addresses from the attack and store them in a list
        suspicious_addresses = attack_detect.arp_suspicious_addresses

        # assert that every expected address appears in the suspicious addresses list
        self.assertCountEqual(suspicious_addresses, known_sus,
                              "The ARP Poisoning Analysis does not contain exactly all expected suspicious addresses")

    def test_icmp_flood_false(self):
        # set up an attack detection using a pcap file without arp poisoning attacks
        attack_false_detect = self.setUpAttackDetection("dns")

        # execute the icmp flood detection on a file that shouldn't flag any suspicion
        attack_false_detect.icmp_flood_detect(100)
        # obtain the suspicious addresses from the attack and store them in a list
        false_suspicious_addresses = attack_false_detect.tcp_scanning_suspicious

        # ensure that the method does not incur any false positives for clean packets
        self.assertFalse(false_suspicious_addresses,
                         "The ICMP Flood Analysis has detected false suspicious addresses")

    def test_icmp_flood(self):
        # set up an attack detection adding a pcap file with arp poisoning attacks
        attack_detect = self.setUpAttackDetection("icmp-ping")

        # expected suspicious address
        known_sus = '10.0.0.2'

        # execute the icmp flood detection to test the method works correctly, providing a low enough threshold to
        # detect the suspicious address
        attack_detect.icmp_flood_detect(100)
        # obtain the suspicious addresses from the attack and store them in a new list
        suspicious_addresses = attack_detect.icmp_suspicious

        # execute the icmp flood detection to test the method works correctly, providing a threshold that should be too
        # high to detect the suspicious address
        attack_detect.icmp_flood_detect(10000)
        # obtain the suspicious addresses from the attack and store them in a new list
        suspicious_addresses_wthreshold = attack_detect.icmp_suspicious

        # Tests whether the known suspicious address appeared in the correct lists
        self.assertIn(known_sus, suspicious_addresses,
                      "The ICMP Flood Analysis does not contain exactly all expected suspicious addresses")
        # Assert that the new suspicious address list is empty as expected
        self.assertNotIn(known_sus, suspicious_addresses_wthreshold,
                         "The ICMP Flood Analysis has detected an unexpected suspicious address given a high threshold")

    def test_http_flood_false(self):
        # set up an attack detection using a pcap file without http flood attacks
        attack_false_detect = self.setUpAttackDetection("dns")

        # execute the http flood detection on a file that shouldn't flag any suspicion
        attack_false_detect.http_attack(5)
        # obtain the suspicious addresses from the attack and store them in a list
        false_suspicious_addresses = attack_false_detect.http_suspicious

        # ensure that the method does not incur any false positives for clean packets
        self.assertFalse(false_suspicious_addresses,
                         "The HTTP Flood Analysis has detected false suspicious addresses")

    def test_http_flood(self):
        # set up an attack detection adding a pcap file with http flood attacks
        attack_detect = self.setUpAttackDetection("http-flood")

        # expected suspicious address
        known_sus = "10.0.0.2"

        # execute the http flood detection to test the method works correctly, providing a low enough threshold to
        # detect the suspicious address
        attack_detect.http_attack(5)
        # obtain the suspicious addresses from the attack and store them in a new list
        suspicious_addresses = attack_detect.http_suspicious

        # execute the http flood detection to test the method works correctly, providing a threshold that should be too
        # high to detect the suspicious address
        attack_detect.http_attack(500)
        # obtain the suspicious addresses from the attack and store them in a new list
        suspicious_addresses_wthreshold = attack_detect.http_suspicious

        # Tests whether the known suspicious address appeared in the correct lists
        self.assertIn(known_sus, suspicious_addresses,
                      "The HTTP Flood Analysis does not contain exactly all expected suspicious addresses")
        # Assert that the new suspicious address list is empty as expected
        self.assertNotIn(known_sus, suspicious_addresses_wthreshold,
                         "The HTTP Flood Analysis has detected an unexpected suspicious address given a high threshold")

    def test_dns_false(self):
        # set up an attack detection using a pcap file without dns attacks
        attack_false_detect = self.setUpAttackDetection("http-flood")

        # execute the http flood detection on a file that shouldn't flag any suspicion
        attack_false_detect.dns_request_response_detect(20)
        # obtain the suspicious addresses from the attack and store them in two lists
        false_request_sus_addresses = attack_false_detect.dns_request_suspicious
        false_response_sus_addresses = attack_false_detect.dns_response_suspicious

        # ensure that the method does not incur any false positives for clean packets
        self.assertFalse(false_request_sus_addresses,
                         "The DNS Analysis has detected false suspicious request addresses")
        self.assertFalse(false_response_sus_addresses,
                         "The DNS Analysis has detected false suspicious response addresses")

    def test_dns(self):
        # set up an attack detection adding a pcap file with dns attacks
        attack_detect = self.setUpAttackDetection("dns")

        # expected suspicious request and response addresses
        known_request_sus = "207.86.6.174"
        known_response_sus = "205.94.14.222"

        # execute the dns detection to test the method works correctly, providing a low enough threshold to
        # detect the suspicious address
        attack_detect.dns_request_response_detect(20)
        # obtain the suspicious request and response addresses from the attack and store them in new lists
        request_sus_addresses = attack_detect.dns_request_suspicious
        response_sus_addresses = attack_detect.dns_response_suspicious

        # execute the dns detection to test the method works correctly, providing a threshold that should be too
        # high to detect the suspicious address
        attack_detect.dns_request_response_detect(2000)
        # obtain the high-threshold suspicious request and response addresses from the attack and store them in new 
        # lists
        request_sus_addresses_wthreshold = attack_detect.dns_request_suspicious
        response_sus_addresses_wthreshold = attack_detect.dns_response_suspicious

        # Tests whether the known suspicious request and response addresses appeared in the correct lists
        self.assertIn(known_request_sus, request_sus_addresses,
                      "The DNS Analysis does not contain exactly all expected suspicious request addresses")
        self.assertIn(known_response_sus, response_sus_addresses,
                      "The DNS Analysis does not contain exactly all expected suspicious response addresses")
        # Assert that the new suspicious address list is empty as expected
        self.assertNotIn(known_request_sus, request_sus_addresses_wthreshold,
                         "The DNS Analysis has detected an unexpected suspicious request address given a high threshold")
        self.assertNotIn(known_response_sus, response_sus_addresses_wthreshold,
                         "The DNS Analysis has detected an unexpected suspicious request address given a high threshold")

    def test_run_all(self):
        # set up an attack detection using a pcap file with tcp flood attacks
        attack_syn_detect = self.setUpAttackDetection("SYN")
        # set up an attack detection using a pcap file with icmp attacks
        attack_icmp_detect = self.setUpAttackDetection("icmp-ping")

        # define the attacks to execute as all the implemented attack detection methods that shouldn't flag using tcp
        # packets
        attack_syn_lists = {"HTTP": attack_syn_detect.http_suspicious,
                            "ARP": attack_syn_detect.arp_suspicious_addresses,
                            "DNSreq": attack_syn_detect.dns_request_suspicious,
                            "DNS": attack_syn_detect.dns_response_suspicious,
                            "DOS": attack_syn_detect.dos_suspicious_addresses,
                            "ICMP": attack_syn_detect.icmp_suspicious}

        # define the attacks to execute as all the implemented attack detection methods on the icmp packets
        attack_icmp_lists = {"TCP Scanning": attack_icmp_detect.tcp_scanning_suspicious,
                             "TCP": attack_icmp_detect.tcp_suspicious_addresses,
                             "HTTP": attack_icmp_detect.http_suspicious,
                             "ARP": attack_icmp_detect.arp_suspicious_addresses,
                             "DNSreq": attack_icmp_detect.dns_request_suspicious,
                             "DNS": attack_icmp_detect.dns_response_suspicious}

        # the expected suspicious value that should be flagged for icmp and dos attacks
        known_sus = "10.0.0.2"
        known_tcp_sus = "10.128.0.2"

        # execute all detection methods to test the methods work correctly, providing a low enough threshold to
        # detect the suspicious address
        attack_syn_detect.run_all_detection(20)
        attack_icmp_detect.run_all_detection(20)
        # Checks that the address is not in all the lists it shouldn't be
        for attack_sus in attack_syn_lists:
            self.assertNotIn(known_tcp_sus, attack_sus,
                             "An attack detection method has unexpectedly flagged a suspicious address in the syn.pcap file")

        # check that the suspicious address is in the expected attack lists
        self.assertIn(known_tcp_sus, attack_syn_detect.tcp_scanning_suspicious,
                      "The TCP Scanning Analysis does not contain exactly all expected suspicious addresses")
        self.assertIn(known_tcp_sus, attack_syn_detect.tcp_suspicious_addresses,
                      "The TCP Flood Analysis does not contain exactly all expected suspicious addresses")

        # Checks that the address is not in all the lists it shouldn't be
        for attack_sus in attack_icmp_lists:
            self.assertNotIn(known_sus, attack_sus,
                             "An attack detection method has unexpectedly flagged a suspicious address in the icmp-ping.pcap file")

        # check that the suspicious address is in the expected attack lists
        self.assertIn(known_sus, attack_icmp_detect.icmp_suspicious,
                      "The ICMP Flood Analysis does not contain exactly all expected suspicious addresses")

        # Run with high threshold so should not be any list
        attack_syn_detect.run_all_detection(5000)
        attack_icmp_detect.run_all_detection(5000)

        # assert that the suspicious address isn't in any list
        for attack_sus in attack_syn_lists:
            self.assertNotIn(known_tcp_sus, attack_sus,
                             "An attack detection method has unexpectedly flagged a suspicious address in the syn.pcap file")

        self.assertNotIn(known_tcp_sus, attack_syn_detect.tcp_scanning_suspicious,
                         "The TCP Scanning Analysis has detected an unexpected suspicious address given a high threshold")

        # assert that the suspicious address isn't in any list
        for attack_sus in attack_icmp_lists:
            self.assertNotIn(known_sus, attack_sus,
                             "An attack detection method has unexpectedly flagged a suspicious address in the icmp-ping.pcap file")

        self.assertNotIn(known_sus, attack_icmp_detect.icmp_suspicious,
                         "The ICMP Flood Analysis has detected an unexpected suspicious address given a high threshold")
        self.assertNotIn(known_sus, attack_icmp_detect.dos_suspicious_addresses,
                         "The DOS Analysis has detected an unexpected suspicious address given a high threshold")


if __name__ == '__main__':
    unittest.main()
