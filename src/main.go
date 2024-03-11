package main

import (
	"fmt"
	"os"
	"strconv"
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
	fmt.Printf("Usage:\ngo run . [tests] [\"filepath\"]\nUse All to run all tests, for a list of tests use:\ngo run . tests\nIf entering a threshold, 'd' can be used for default settings")
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

// get a default threshold using an ID for the threshold test and the `config.txt` file
func getDefaultThreshold(thresholdID int) int {
	// access the config.txt file
	f, err := os.ReadFile("config.txt")
	// handle config.txt not found
	if err != nil {
		print("config file not found, using a threshold of 20\n")
		return 20
	}
	// convert file into text
	data := string(f)

	// get relevant line
	line := strings.Split(data, ";")[thresholdID]
	// get threshold
	threshold, err := strconv.Atoi(strings.Split(line, ": ")[1])
	// handle bad config file
	if err != nil {
		print("config.txt not set up as expected, using a threshold of 20\n")
		return 20
	}

	return threshold
}

func inputThreshold(test string, thresholdID int) int {
	// ask user for a threshold
	fmt.Println("Enter threshold for " + test + ":")
	var input string

	// read a single line of input
	_, err := fmt.Scan(&input)
	if err != nil {
		fmt.Println("Error:", err)
		return -1
	}

	// convert input into an int
	threshold, err := strconv.Atoi(input)
	if err != nil {
		// if input is empty, use default input
		if input == "d" {
			getDefaultThreshold(thresholdID)
		} else {
			fmt.Println("Threshold must be an integer.")
			return -1
		}
	}

	return threshold
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

func runTcpConnect(filepath string) {
	// get the threshold
	threshold := inputThreshold("TCP Connection Scan", 1)
	// bad format
	if threshold == -1 {
		runTcpConnect(filepath)
		return
	}

	// notify start of TCP connection analysis
	print("Running TCP Connection Flood Scan on " + filepath + ".pcap...\n------------------------\n")

	// run attack analysis to get suspicious and attacked addresses
	suspicious := tcpConnectScanDetect(filepath, threshold)

	// if no addresses found, print accordingly
	if len(suspicious) == 0 {
		print("No suspicious addresses found.\n------------------------")
		return
	}

	// if addresses have been found, communicate
	print("Suspicious Addresses Found: " + strings.Join(suspicious, ", ") + "\n------------------------")

}
func runArp(filepath string) {
	// notify start of ARP analysis
	print("Running ARP Poison Detection on " + filepath + ".pcap...\n------------------------\n")

	// run attack analysis to get suspicious addresses
	suspicious := arpPoisonDetect(filepath)

	// if no addresses found, print accordingly
	if len(suspicious) == 0 {
		print("No signs of ARP Poisoning attack found.\n------------------------")
		return
	}

	// if addresses have been found, communicate
	print("ARP Poison attack detected:\nSuspicious Addresses: " + strings.Join(suspicious, ", ") + "\n------------------------")

}
func runIcmp(filepath string) {
	// get the threshold
	threshold := inputThreshold("ICMP Flood Detection", 2)
	// bad format
	if threshold == -1 {
		runIcmp(filepath)
		return
	}

	// notify start of ICMP Flood analysis
	print("Running ICMP Flood Detection on " + filepath + ".pcap...\n------------------------\n")

	// run attack analysis to get suspicious addresses
	suspicious := icmpFloodDetect(filepath, float64(threshold))

	// if no addresses found, print accordingly
	if len(suspicious) == 0 {
		print("No suspicious addresses found.\n------------------------")
		return
	}

	// if addresses have been found, communicate
	print("Suspicious Addresses Found: " + strings.Join(suspicious, ", ") + "\n------------------------")
}
func runHttp(filepath string) {
	// get the threshold
	threshold := inputThreshold("HTTP Flood Detection", 3)
	// bad format
	if threshold == -1 {
		runHttp(filepath)
		return
	}

	// notify start of HTTP connection analysis
	print("Running HTTP Flood Detection on " + filepath + ".pcap...\n------------------------\n")

	// run attack analysis to get suspicious and attacked addresses
	suspicious := httpFloodDetect(filepath, float64(threshold))

	// if no addresses found, print accordingly
	if len(suspicious) == 0 {
		print("No suspicious addresses found.\n------------------------")
		return
	}

	// if addresses have been found, communicate
	print("Suspicious Addresses Found: " + strings.Join(suspicious, ", ") + "\n------------------------")
}
func runDns(filepath string) {
	// get the threshold
	threshold := inputThreshold("DNS Attack Detection", 4)
	// bad format
	if threshold == -1 {
		runDns(filepath)
		return
	}

	// notify start of DNS analysis
	print("Running DNS Attack Detection on " + filepath + ".pcap...\n------------------------\n")

	// run attack analysis to get request and attacked response
	report := dnsRequestResponse(filepath, float64(threshold))

	// if no addresses found, print accordingly
	if len(report.suspicious) == 0 {
		print("No signs of a DNS attack found.\n------------------------")
		return
	}

	// if addresses have been found, communicate
	print("TCP Flood attack detected:\nSuspicious Request Addresses: " + strings.Join(report.suspicious, ", ") + "\nSuspicious Response Addresses: " + strings.Join(report.attacked, ", ") + "\n------------------------")

}
func runAll(filepath string) {
	// run all other attack analyses
	runTcp(filepath)
	print("\n")
	runTcpConnect(filepath)
	print("\n")
	runArp(filepath)
	print("\n")
	runIcmp(filepath)
	print("\n")
	runHttp(filepath)
	print("\n")
	runDns(filepath)
	// finished confirmation
	print("\nAll Tests Finished.")
}
