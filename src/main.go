package main

import (
	"fmt"
	"os"
	"strings"
)

// enum to store the kind of test
const (
	tcp        = iota
	tcpConnect = iota
	arp        = iota
	icmp       = iota
	http       = iota
	dns        = iota
	all        = iota
)

// provide help on how to use the program on the CLI
func help() {
	// print help
	fmt.Printf("Usage:\ngo run . [tests] [\"filepath\"]\nUse All to run all tests, for a list of tests use:\ngo run . tests")
}

// provide a list of tests usable
func tests() {
	// print tests
	fmt.Printf("Tests:\n0 - TCPFlood\n1 - TCPConnectScan\n2 - ARPPoison\n3 - ICMPFlood\n4 - HTTPFlood\n5 - DNS")
}

// decodes a string argument to figure out the test as an integer
func getTest(testArg string) int {
	// check if it fits a format
	switch strings.ToLower(testArg) {
	case "0", "tcp", "tcpflood":
		return tcp
	case "1", "tcpconnect", "tcpconnectscan", "tcpconnectscanning":
		return tcpConnect
	case "2", "arp", "arppoison":
		return arp
	case "3", "icmp", "icmpflood":
		return icmp
	case "4", "http", "httpflood":
		return http
	case "5", "dns":
		return dns
	case "a", "all", "*":
		return all
	default:
		return -1
	}
}

func runTcpConnect(filepath string) {
	print("tcp connect")
}
func runArp(filepath string) {
	print("arp")
}
func runIcmp(filepath string) {
	print("icmp")
}
func runHttp(filepath string) {
	print("http")
}
func runDns(filepath string) {
	print("dns")
}
func runAll(filepath string) {
	print("all")
}

func main() {
	// check the number of arguments, if there aren't enough, give help
	args := os.Args
	if len(args) == 1 {
		help()
	} else if len(args) == 2 {
		// if there is one argument provided, check that it is asking for a list of tests
		if strings.ToLower(args[1]) == "tests" {
			tests()
		} else {
			// wrong format, provide help
			help()
		}
	} else {
		// get the filepath and test
		var testArg string
		var filepath string
		// if the first argument is the filepath, switch around arguments
		if strings.ContainsAny(args[1], "./") {
			filepath = args[1]
			testArg = args[2]
		} else {
			filepath = args[2]
			testArg = args[1]
		}
		// trim filepath, ignore src/ and .pcap
		filepath = strings.ReplaceAll(filepath, "\"", "")
		filepath = strings.Split(filepath, ".")[0]
		filepath = strings.ReplaceAll(filepath, "src/", "")

		// check the filepath
		_, err := os.ReadFile(filepath + ".pcap")
		if err == nil {
			// get the test
			test := getTest(testArg)
			// check and run the tests
			switch test {
			case tcp:
				runTcp(filepath)
			case tcpConnect:
				runTcpConnect(filepath)
			case arp:
				runArp(filepath)
			case icmp:
				runIcmp(filepath)
			case http:
				runHttp(filepath)
			case dns:
				runDns(filepath)
			case all:
				runAll(filepath)
			default:
				print("unrecognised test, for a list of all tests use:\ngo run . tests")
			}
		} else {
			// file path not found
			print("filepath \"" + filepath + ".pcap\" not found")
		}
	}
}

// logic for running checks
func runTcp(filepath string) {
	// notify start of TCP analysis
	print("Running TCP Flood Detection on " + filepath + ".pcap...\n------------------------\n")

	// run attack analysis to get suspicious and attacked addresses
	report := tcpSynFloodDetect(filepath)

	// if no addresses found, print accordingly
	if len(report.suspicious) == 0 {
		print("No signs of a TCP Flood attack found.\n------------------------")
		return
	}

	// if addresses have been found, communicate
	print("TCP Flood attack detected:\nSuspicious Addresses: " + strings.Join(report.suspicious, ", ") + "\nAttacked Addresses: " + strings.Join(report.attacked, ", ") + "\n------------------------")
}
