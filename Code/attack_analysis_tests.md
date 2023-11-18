# Attack Analysis Tests
Attack analysis tests is a file that makes use of python unit tests to assert that the attack methods analysed within capture_analysis work as expected. Packets are provided to this file using .pcap files, as this file's main goal is to test the analysis of the packets works as expected, not to test the capturing of packets.

## Dependencies
```
import unittest
import matplotlib
matplotlib.use('Agg')
from pythonGUI.capture_analysis import attack_detection, GUI_actions
```
Attack analysis tests imports the following libraries and code:
 - unittest - The python framework for implementing unit tests
 - matplotlib - An object-oriented plotting library used to visualise the tests
   - .use('Agg') - Select the interactive backend implementation of matplotlib for GUI integration
 - from pythonGUI.capture_analysis import attack_detection, GUI_actions - Import dependencies from other parts of the program to execute the attack analyses

## My Test Case
MyTestCase is a class that wraps around all the tests within this file. Once this file is run, all tests within MyTestCase also run.
```
class MyTestCase(unittest.TestCase):
    # Define the actions for this to use as defined in GUI_actions
    def setUp(self):
        self.actions = GUI_actions.GUIActions()

```
The test to carry out is passed into MyTestCase as a test case. The class will then carry out the test specified. MyTestCase also starts by defining the actions to use when testing using the actions defined in GUI_actions.

### Test TCP Flood
test_tcp_flood is a test definition used to assert that the TCP flood analysis of packets is working as expected.

| Input Files | Method Executed      | Expected Suspicious | Expected Victim |
|-------------|----------------------|---------------------|-----------------|
| dns         | tcp_syn_flood_detect | None                | None            |
| dns, SYN    | tcp_syn_flood_detect | ["10.128.0.2"]      | ["10.0.0.2"]    |

       def test_tcp_flood(self):
        # set up an attack detection using a pcap file without tcp flood attacks
        attack_false_detect = self.setUpAttackDetection("dns")

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

It begins by retrieving the sniffed packets from the pcap files "dns.pcap" and "SYN.pcap".

It then executes the tcp flood detection method twice, once on packets only from dns.pcap, and once on packets from both files.

Lastly, the test asserts the detection run on only the dns packets returned no suspicious or attacked addresses (which is expected as the dns.pcap file should contain no tcp flood attacks).
The test then checks that the detection method found the expected suspicious and victim addresses in the SYN packets.

### Test TCP Scan Detect
test_tcp_scan_detect is a test definition used to assert that the TCP connect scanning detection method is working. The test behaves differently than test tcp flood as it does not return attacked addresses and requires a detection threshold as input.

| Input Files | Threshold | Method Executed             | Expected Suspicious |
|-------------|-----------|-----------------------------|---------------------|
| dns         | 100       | tcp_connect_scanning_detect | None                |
| dns, SYN    | 100       | tcp_connect_scanning_detect | ["10.128.0.2"]      |
| dns, SYN    | 10000     | tcp_connect_scanning_detect | None                |


    def test_tcp_scan_detect(self):
        # set up an attack detection using a pcap file without tcp flood attacks
        attack_false_detect = self.setUpAttackDetection("dns")

        # set up an attack detection adding a pcap file with a tcp flood attack
        attack_detect = self.setUpAttackDetection("SYN")

        # expected suspicious address
        known_sus = "10.128.0.2"

        # execute the tcp connection on a file that shouldn't flag any suspicion
        attack_false_detect.tcp_connect_scanning_detect(100)
        # obtain the suspicious addresses from the attack and store them in a list
        false_suspicious_addresses = attack_false_detect.tcp_scanning_suspicious

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

        # ensure that the method does not incur any false positives for clean packets
        self.assertFalse(false_suspicious_addresses,
                         "The TCP Connect Scanning Analysis has detected false suspicious addresses")

        # Tests whether the known suspicious addresses appeared in the correct lists
        self.assertIn(known_sus, suspicious_addresses,
                      "The TCP Connect Scanning Analysis has not detected an expected suspicious address")

        # Assert that the new suspicious address list is empty as expected
        self.assertNotIn(known_sus, suspicious_addresses_wthreshold,
                         "The TCP Connect Scanning Analysis has detected an unexpected suspicious address given a high "
                         "threshold")
It begins by retrieving the sniffed packets from the pcap files "dns.pcap" and "SYN.pcap".

It then executes the tcp connect scanning detection method three times, once on packets only from dns.pcap, once on packets with both files using a low threshold, and once on packets with both files using a high threshold.

Lastly, the test asserts the detection run on only the dns packets and the run with a high threshold returned no suspicious addresses.
The test then checks that the low threshold detection method found the expected suspicious addresses in the SYN packets.

### Test ARP Poison
test_arp_poison is a test definition used to assert that the ARP poison detection method is working. This method only returns suspicious addresses.

| Input Files        | Method Executed   | Expected Suspicious              |
|--------------------|-------------------|----------------------------------|
| dns                | arp_poison_detect | None                             |
| dns, arp-poisoning | arp_poison_detect | ['192.168.1.1', '192.168.1.254'] |

       def test_arp_poison(self):
        # set up an attack detection using a pcap file without arp poisoning attacks
        attack_false_detect = self.setUpAttackDetection("dns")

        # set up an attack detection adding a pcap file with arp poisoning attacks
        attack_detect = self.setUpAttackDetection("arp-poisoning")

        # expected suspicious addresses
        known_sus = ['192.168.1.1', '192.168.1.254']

        # execute the arp poison detection to test the method works correctly
        attack_detect.arp_poison_detect()
        # obtain the suspicious addresses from the attack and store them in a list
        suspicious_addresses = attack_detect.arp_suspicious_addresses

        # execute the arp poisoning on a file that shouldn't flag any suspicion
        attack_false_detect.arp_poison_detect()
        # obtain the suspicious addresses from the attack and store them in a list
        false_suspicious_addresses = attack_false_detect.arp_suspicious_addresses

        # ensure that the method does not incur any false positives for clean packets
        self.assertFalse(false_suspicious_addresses,
                         "The ARP Poisoning Analysis has detected false suspicious addresses")

        # assert that every expected address appears in the suspicious addresses list
        self.assertCountEqual(suspicious_addresses, known_sus,
                              "The ARP Poisoning Analysis does not contain exactly all expected suspicious addresses")

It begins by retrieving the sniffed packets from the pcap files "dns.pcap" and "arp-poisoning.pcap".

It then executes the arp poison detection method twice, once on packets only from dns.pcap and once on packets with both files.

Lastly, the test asserts the detection run on only the dns packets returned no suspicious addresses.
The test then checks that the detection method found the expected suspicious addresses in the arp-poisoning packets.

### Test ICMP Flood
test_icmp_flood is a test definition used to assert that the ICMP flood detection method is working. The test does not return attacked addresses and requires a detection threshold as input.

| Input Files    | Threshold | Method Executed             | Expected Suspicious |
|----------------|-----------|-----------------------------|---------------------|
| dns            | 100       | tcp_connect_scanning_detect | None                |
| dns, icmp-ping | 100       | tcp_connect_scanning_detect | ["10.0.0.2"]        |
| dns, icmp-ping | 10000     | tcp_connect_scanning_detect | None                |

        def test_icmp_flood(self):
        # set up an attack detection using a pcap file without arp poisoning attacks
        attack_false_detect = self.setUpAttackDetection("dns")

        # set up an attack detection adding a pcap file with arp poisoning attacks
        attack_detect = self.setUpAttackDetection("icmp-ping")

        # expected suspicious address
        known_sus = '10.0.0.2'

        # execute the icmp flood detection on a file that shouldn't flag any suspicion
        attack_false_detect.icmp_flood_detect(100)
        # obtain the suspicious addresses from the attack and store them in a list
        false_suspicious_addresses = attack_false_detect.tcp_scanning_suspicious

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

        # ensure that the method does not incur any false positives for clean packets
        self.assertFalse(false_suspicious_addresses,
                         "The ICMP Flood Analysis has detected false suspicious addresses")
        # Tests whether the known suspicious address appeared in the correct lists
        self.assertIn(known_sus, suspicious_addresses,
                      "The ICMP Flood Analysis does not contain exactly all expected suspicious addresses")
        # Assert that the new suspicious address list is empty as expected
        self.assertNotIn(known_sus, suspicious_addresses_wthreshold,
                         "The ICMP Flood Analysis has detected an unexpected suspicious address given a high threshold")
It begins by retrieving the sniffed packets from the pcap files "dns.pcap" and "icmp-ping.pcap".

It then executes the icmp flood detection method three times, once on packets only from dns.pcap, once on packets with both files using a low threshold, and once on packets with both files using a high threshold.

Lastly, the test asserts the detection run on only the dns packets and the run with a high threshold returned no suspicious addresses.
The test then checks that the low threshold detection method found the expected suspicious addresses in the icmp-ping packets.

### Test HTTP Flood
test_http_flood is a test definition used to assert that the HTTP flood detection method is working. The test does not return attacked addresses and requires a detection threshold as input.

| Input Files     | Threshold | Method Executed | Expected Suspicious |
|-----------------|-----------|-----------------|---------------------|
| dns             | 5         | http_attack     | None                |
| dns, http-flood | 5         | http_attack     | ["10.0.0.2"]        |
| dns, http-flood | 500       | http_attack     | None                |


            def test_http_flood(self):
        # set up an attack detection using a pcap file without http flood attacks
        attack_false_detect = self.setUpAttackDetection("dns")

        # set up an attack detection adding a pcap file with http flood attacks
        attack_detect = self.setUpAttackDetection("http-flood")

        # expected suspicious address
        known_sus = "10.0.0.2"

        # execute the http flood detection on a file that shouldn't flag any suspicion
        attack_false_detect.http_attack(5)
        # obtain the suspicious addresses from the attack and store them in a list
        false_suspicious_addresses = attack_false_detect.http_suspicious

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

        # ensure that the method does not incur any false positives for clean packets
        self.assertFalse(false_suspicious_addresses,
                         "The HTTP Flood Analysis has detected false suspicious addresses")
        # Tests whether the known suspicious address appeared in the correct lists
        self.assertIn(known_sus, suspicious_addresses,
                      "The HTTP Flood Analysis does not contain exactly all expected suspicious addresses")
        # Assert that the new suspicious address list is empty as expected
        self.assertNotIn(known_sus, suspicious_addresses_wthreshold,
                         "The HTTP Flood Analysis has detected an unexpected suspicious address given a high threshold")
It begins by retrieving the sniffed packets from the pcap files "dns.pcap" and "http-flood.pcap".

It then executes the http flood detection method three times, once on packets only from dns.pcap, once on packets with both files using a low threshold, and once on packets with both files using a high threshold.

Lastly, the test asserts the detection run on only the dns packets and the run with a high threshold returned no suspicious addresses.
The test then checks that the low threshold detection method found the expected suspicious addresses in the http-flood packets.

### Test DNS
test_dns is a test definition used to assert that the dns detection method is working as expected. The test returns both suspicious request and suspicious response addresses and requires a detection threshold as input.

**Expected Output:** request_sus_addresses{"207.86.6.174"}, response_sus_addresses{"205.94.14.222"}, request_sus_addresses_wthreshold{}, response_sus_addresses_wthreshold{}

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
It begins by retrieving the sniffed packets from the pcap file "dns.pcap" and pointing the method to detect attacks to this file. The expected suspicious request and response addresses are predefined. These addresses should only be flagged if the threshold is low enough.

It then executes the dns detection method defined in actions, using a low enough threshold to allow detection of the expected addresses and retrieving the results of the suspicious addresses to two lists. It also calls this method with a higher threshold of 2000, which should be too high to pick up the attack. The result of this scan is stored in separate lists.

Lastly, the test checks that the expected return values match the actual executed return values by first checking that
the low-threshold lists are not empty and the high-threshold lists are empty, and then checking that the low-threshold lists only contains the expected suspicious request and response addresses.

### Test Run All
test_run_all is a test definition used to assert that all detection methods are working as expected. The test returns suspicious addresses for all tests and requires a detection threshold as input.

**Expected Output:** attack_detect.dos_suspicious_addresses{"10.0.0.2"}, attack_detect.icmp_suspicious{"10.0.0.2"}  

```
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
```
It begins by retrieving the sniffed packets from the pcap file "icmp-ping.pcap" and pointing the method to detect attacks to this file. The expected suspicious address is predefined. These addresses should only be flagged if the threshold is low enough, and should only be flagged by the dos and icmp detection methods.

It then executes all the detection methods defined in actions, using a low enough threshold to allow detection of the expected address and retrieving the results of the suspicious address to a list for each method. It also calls this method with a higher threshold of 5000, which should be too high to pick up the attack. The result of these scans are stored in separate lists.

Lastly, the test checks that the expected return values match the actual executed return values by first checking that
the icmp and dos low-threshold lists are not empty and the high-threshold lists are empty, and then checking that the low-threshold icmp and dos lists only contain the expected suspicious addresses.
