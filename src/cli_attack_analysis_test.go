package main

import (
	"sort"
	"testing"
)

// compare two slices of strings to check that they are equal (in any order)
func sliceEqual(s []string, t []string) bool {
	// check they have the same length
	if len(s) != len(t) {
		return false
	}

	// sort the slices to allow any ordering
	sort.Strings(s)
	sort.Strings(t)

	// go through each element in s, check that it is in t
	for i, str := range s {
		if str != t[i] {
			return false
		}
	}

	// return true as the slices are equal
	return true
}

// test the TCP Flood detection for the CLI tool is working as expected
func TestTcpFlood(t *testing.T) {
	// detect an attack using a pcap file without tcp flood attacks
	attackFalseDetect := tcpSynFloodDetect("test_pcaps/dns")
	// detect an attack using a pcap file with a tcp flood attack
	attackDetect := tcpSynFloodDetect("test_pcaps/SYN")

	// expected suspicious address
	knownSuspicious := []string{"10.128.0.2"}
	// expected attacked address
	knownAttacked := []string{"10.0.0.2"}

	// ensure that the method does not incur any false positives
	if len(attackFalseDetect.suspicious) > 0 {
		t.Fatalf("Expected no suspicious addresses, got %v instead", attackFalseDetect.suspicious)
	}
	if len(attackFalseDetect.attacked) > 0 {
		t.Fatalf("Expected no attacked addresses, got %v instead", attackFalseDetect.attacked)
	}

	// tests whether the known suspicious and attacked addresses appeared in the correct lists
	if !sliceEqual(attackDetect.suspicious, knownSuspicious) {
		t.Fatalf("Expected suspicious address %v, got %v instead", knownSuspicious, attackDetect.suspicious)
	}
	if !sliceEqual(attackDetect.attacked, knownAttacked) {
		t.Fatalf("Expected suspicious address %v, got %v instead", knownAttacked, attackDetect.attacked)
	}
}

// test the TCP Connect Scanning detection for the CLI tool is working as expected
func TestTcpConnectScanningFlood(t *testing.T) {
	// detect an attack using a pcap file without tcp flood attacks
	attackFalseDetect := tcpConnectScanDetect("test_pcaps/dns", 100)
	// detect an attack using a high threshold
	attackDetectThreshold := tcpConnectScanDetect("test_pcaps/SYN", 10000)
	// detect an attack using a pcap file with a tcp flood attack
	attackDetect := tcpConnectScanDetect("test_pcaps/SYN", 100)

	// expected suspicious address
	knownSuspicious := []string{"10.128.0.2"}

	// ensure that the method does not incur any false positives
	if len(attackFalseDetect) > 0 {
		t.Fatalf("Expected no suspicious addresses, got %v instead", attackFalseDetect)
	}
	// ensure that the method does not pick up any suspicious addresses if the threshold is high enough
	if len(attackDetectThreshold) > 0 {
		t.Fatalf("Expected no suspicious addresses, got %v instead", attackDetectThreshold)
	}

	// tests whether the known suspicious addresses appeared in the correct list
	if !sliceEqual(attackDetect, knownSuspicious) {
		t.Fatalf("Expected suspicious address %v, got %v instead", knownSuspicious, attackDetect)
	}
}

// test the ARP poison detection for the CLI tool is working as expected
func TestARPPoison(t *testing.T) {
	// detect an attack using a pcap file without arp poisoning attacks
	attackFalseDetect := arpPoisonDetect("test_pcaps/dns")
	// detect an attack using a pcap file with arp poisoning attacks
	attackDetect := arpPoisonDetect("test_pcaps/arp-poisoning")

	// expected suspicious address
	knownSuspicious := []string{"192.168.1.1", "192.168.1.254"}

	// ensure that the method does not incur any false positives
	if len(attackFalseDetect) > 0 {
		t.Fatalf("Expected no suspicious addresses, got %v instead", attackFalseDetect)
	}

	// tests whether the known suspicious addresses appeared in the correct list
	if !sliceEqual(attackDetect, knownSuspicious) {
		t.Fatalf("Expected suspicious addresses %v, got %v instead", knownSuspicious, attackDetect)
	}
}

// test the ICMP Flood detection for the CLI tool is working as expected
func TestIcmpFlood(t *testing.T) {
	// detect an attack using a pcap file without icmp flood attacks
	attackFalseDetect := icmpFloodDetect("dns", 100)
	// detect an attack using a high threshold
	attackDetectThreshold := icmpFloodDetect("icmp-ping", 10000)
	// detect an attack using a pcap file with an icmp flood attack
	attackDetect := icmpFloodDetect("icmp-ping", 100)

	// expected suspicious address
	knownSuspicious := []string{"10.0.0.2"}

	// ensure that the method does not incur any false positives
	if len(attackFalseDetect) > 0 {
		t.Fatalf("Expected no suspicious addresses, got %v instead", attackFalseDetect)
	}
	// ensure that the method does not pick up any suspicious addresses if the threshold is high enough
	if len(attackDetectThreshold) > 0 {
		t.Fatalf("Expected no suspicious addresses, got %v instead", attackDetectThreshold)
	}

	// tests whether the known suspicious addresses appeared in the correct list
	if !sliceEqual(attackDetect, knownSuspicious) {
		t.Fatalf("Expected suspicious address %v, got %v instead", knownSuspicious, attackDetect)
	}
}

// test the HTTP Flood detection for the CLI tool is working as expected
func TestHttpFlood(t *testing.T) {
	// detect an attack using a pcap file without http flood attacks
	attackFalseDetect := httpFloodDetect("dns", 5)
	// detect an attack using a high threshold
	attackDetectThreshold := httpFloodDetect("http-flood", 500)
	// detect an attack using a pcap file with an icmp flood attack
	attackDetect := httpFloodDetect("http-flood", 5)

	// expected suspicious address
	knownSuspicious := []string{"10.0.0.2"}

	// ensure that the method does not incur any false positives
	if len(attackFalseDetect) > 0 {
		t.Fatalf("Expected no suspicious addresses, got %v instead", attackFalseDetect)
	}
	// ensure that the method does not pick up any suspicious addresses if the threshold is high enough
	if len(attackDetectThreshold) > 0 {
		t.Fatalf("Expected no suspicious addresses, got %v instead", attackDetectThreshold)
	}

	// tests whether the known suspicious addresses appeared in the correct list
	if !sliceEqual(attackDetect, knownSuspicious) {
		t.Fatalf("Expected suspicious address %v, got %v instead", knownSuspicious, attackDetect)
	}
}

// test the DNS Request Response detection for the CLI tool is working as expected
func TestDns(t *testing.T) {
	// detect an attack using a pcap file without http flood attacks
	attackFalseDetect := dnsRequestResponse("http-flood", 20)
	// detect an attack using a high threshold
	attackDetectThreshold := dnsRequestResponse("dns", 500)
	// detect an attack using a pcap file with an icmp flood attack
	attackDetect := dnsRequestResponse("dns", 20)

	// expected suspicious addresses
	knownRequestSuspicious := []string{"207.86.6.174"}
	knownResponseSuspicious := []string{"205.94.14.222"}

	// ensure that the method does not incur any false positives
	if len(attackFalseDetect.attacked)+len(attackFalseDetect.suspicious) > 0 {
		t.Fatalf("Expected no suspicious addresses, got %v instead", attackFalseDetect)
	}
	// ensure that the method does not pick up any suspicious addresses if the threshold is high enough
	if len(attackDetectThreshold.attacked)+len(attackDetectThreshold.suspicious) > 0 {
		t.Fatalf("Expected no suspicious addresses, got %v instead", attackDetectThreshold)
	}

	// tests whether the known suspicious addresses appeared in the correct list
	if !(sliceEqual(attackDetect.attacked, knownResponseSuspicious) && sliceEqual(attackDetect.suspicious, knownResponseSuspicious)) {
		t.Fatalf("Expected suspicious addresses %v, got %v instead", Report{knownRequestSuspicious, knownResponseSuspicious}, attackDetect)
	}
}
