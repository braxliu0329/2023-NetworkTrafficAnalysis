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
	attackFalseDetect := tcpSynFloodDetect("dns")
	// detect an attack using a pcap file with a tcp flood attack
	attackDetect := tcpSynFloodDetect("SYN")

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
	attackFalseDetect := tcpConnectScanDetect("dns", 100)
	// detect an attack using a high threshold
	attackDetectThreshold := tcpConnectScanDetect("SYN", 10000)
	// detect an attack using a pcap file with a tcp flood attack
	attackDetect := tcpConnectScanDetect("SYN", 100)

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
