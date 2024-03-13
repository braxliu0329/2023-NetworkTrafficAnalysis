package main

import (
	"bytes"
	"github.com/google/gopacket"
	"github.com/google/gopacket/layers"
	"github.com/google/gopacket/pcap"
	"math"
	"net"
	"sort"
	"time"
)

// Stage enum to store the status of tcp connections
const (
	syn       = iota
	synack    = iota
	connected = iota
)

// Report struct to contain slices of suspicious and attacked addresses
type Report struct {
	suspicious []string
	attacked   []string
}

// TCPAddressData struct to contain relevant counts of sent syn packets for tcp addresses
type TCPAddressData struct {
	Address     gopacket.Endpoint
	SendsSYN    int
	SendsAck    int
	ReceivesSyn int
	ReceivesACK int
}

// TCPPacketAddress struct to pair tcp packets with their source and Destination
type TCPPacketAddress struct {
	Source      gopacket.Endpoint
	Destination gopacket.Endpoint
	TcpPacket   *layers.TCP
	Packet      gopacket.Packet
}

// TCPConnection struct to store details and status of the stage of tcp addresses
type TCPConnection struct {
	Source      gopacket.Endpoint
	Destination gopacket.Endpoint
	TcpPacket   *layers.TCP
	Stage       int
}

// MACAddress struct to pair mac addresses and ip addresses as an endpoint and bytes
type MACAddress struct {
	MAC net.HardwareAddr
	IP  net.IP
}

// SourceTime struct to store a source IP with the packet's timestamp
type SourceTime struct {
	Source    net.IP
	TimeStamp time.Time
}

// DNSPacketAddress struct to pair dns packets with their Source and Destination, also stores if it is a response
type DNSPacketAddress struct {
	Source      gopacket.Endpoint
	Destination gopacket.Endpoint
	DnsPacket   *layers.DNS
	Packet      gopacket.Packet
	Response    bool
}

// getPackets retrieves packets from a file into a slice of packets
func getPackets(path string) []gopacket.Packet {
	// handle errors, such as incorrect file paths
	if handle, err := pcap.OpenOffline(path + ".pcap"); err != nil {
		panic(err)
	} else {
		// slice to store packets
		var packets []gopacket.Packet
		// set the packet source as the given pcap file
		packetSource := gopacket.NewPacketSource(handle, handle.LinkType())
		// loop through every packet in the pcap file
		for packet := range packetSource.Packets() {
			// add the packet to the packet slice
			packets = append(packets, packet)
		}
		return packets
	}
}

// getTCP extracts all TCP packet layers from a slice of packets
func getTCP(packets []gopacket.Packet) []TCPPacketAddress {
	// slice to return tcp packets
	var tcpPackets []TCPPacketAddress
	// *threaded* loop through all packets
	for _, packet := range packets {
		// assign a variable to the TCP layer if it exists. If it doesn't exist, move on.
		if tcpLayer := packet.Layer(layers.LayerTypeTCP); tcpLayer != nil {
			// get the actual tcp data from the layer, will not return an error as tcp status should have been checked
			tcp, _ := tcpLayer.(*layers.TCP)
			// get the source and destination of the packet
			source := packet.NetworkLayer().NetworkFlow().Src()
			dest := packet.NetworkLayer().NetworkFlow().Dst()
			// add the tcp layer and address to the slice
			tcpPackets = append(tcpPackets, TCPPacketAddress{source, dest, tcp, packet})
		}
	}

	// return found tcp layers
	return tcpPackets
}

// getMAC gets a slice of mac addresses and associated IPs from all Ethernet Packets
func getMAC(packets []gopacket.Packet) []MACAddress {
	// slice to return tcp packets
	var ethPackets []MACAddress
	// *threaded* loop through all packets
	for _, packet := range packets {
		// assign a variable to the TCP layer if it exists. If it doesn't exist, move on.
		if ethLayer := packet.Layer(layers.LayerTypeEthernet); ethLayer != nil {
			// get the actual tcp data from the layer, will not return an error as eth status should have been checked
			eth, _ := ethLayer.(*layers.Ethernet)

			// struct to store the mac address details
			mac := MACAddress{eth.SrcMAC, getIP(packet)}
			// add the tcp layer and address to the slice
			ethPackets = append(ethPackets, mac)
		}
	}
	// return found tcp layers
	return ethPackets
}

// getTCPAddressData uses a slice of TCP packets to collate data for each address to be returned as a slice
func getTCPAddressData(tcpPackets []TCPPacketAddress) []TCPAddressData {
	// slice to store tcp address information
	var addresses []TCPAddressData
	// obtain all tcp address information
	for _, packet := range tcpPackets {
		// go through existing addresses to see if this is a new source/destination
		newSource := true
		newDestination := true
		for _, address := range addresses {
			// see if this address is new
			if packet.Source == address.Address {
				newSource = false
				// variables to store whether the packet is a syn or ack
				syn := 0
				ack := 0
				// if it is a syn packet, set syn sent as 1
				if packet.TcpPacket.SYN {
					syn = 1
				}
				// if it is an ack packet, set ack as 1
				if packet.TcpPacket.ACK {
					ack = 1
				}
				address = TCPAddressData{packet.Source, address.SendsSYN, address.SendsAck, address.ReceivesSyn + syn, address.ReceivesACK + ack}
			}
			if packet.Destination == address.Address {
				newDestination = false
				// variables to store whether the packet is a syn or ack
				syn := 0
				ack := 0
				// if it is a syn packet, set syn sent as 1
				if packet.TcpPacket.SYN {
					syn = 1
				}
				// if it is an ack packet, set ack as 1
				if packet.TcpPacket.ACK {
					ack = 1
				}
				address = TCPAddressData{packet.Destination, address.SendsSYN + syn, address.SendsAck + ack, address.ReceivesSyn, address.ReceivesACK}
			}
		}
		// if the packet is from a new source, add it to the slice
		if newSource {
			// variables to store whether the packet is a syn or ack
			syn := 0
			ack := 0
			// if it is a syn packet, set syn sent as 1
			if packet.TcpPacket.SYN {
				syn = 1
			}
			// if it is an ack packet, set ack as 1
			if packet.TcpPacket.ACK {
				ack = 1
			}
			addresses = append(addresses, TCPAddressData{packet.Source, 0, 0, syn, ack})
		}
		// if the packet is from a new destination, add it to the slice
		if newDestination {
			// variables to store whether the packet is a syn or ack
			syn := 0
			ack := 0

			// if it is a syn packet, set syn sent as 1
			if packet.TcpPacket.SYN {
				syn = 1
			}
			// if it is an ack packet, set ack as 1
			if packet.TcpPacket.ACK {
				ack = 1
			}
			addresses = append(addresses, TCPAddressData{packet.Destination, syn, ack, 0, 0})
		}
	}
	// return found address data
	return addresses
}

// helper function to loop through addresses in parallel
func findSuspiciousTCP(addresses []TCPAddressData, suspicious chan<- string, attacked chan<- string, complete chan<- bool) {
	for _, address := range addresses {
		// mark the address as attacked if it receives more SYN packets than SYN-ACK packets sent
		if address.ReceivesSyn > 3*address.SendsAck/2 {
			attacked <- address.Address.String()
		}
		// mark the address as suspicious if it sends more SYN packets than SYN-ACK packets received
		if address.SendsSYN > 3*address.ReceivesACK/2 {
			suspicious <- address.Address.String()
		}
	}
	// signal this goroutine is complete
	complete <- true
}

// tcpSynFloodDetect uses the name of a pcap file and returns lists containing any suspicious and suspected attacked addresses
func tcpSynFloodDetect(file string) Report {
	// get packets from a pcap file
	packets := getPackets(file)
	// extract all TCP layers
	tcpPackets := getTCP(packets)
	// collate address data
	addresses := getTCPAddressData(tcpPackets)

	// slices to contain suspicious and attacked addresses
	var suspiciousAddresses []string
	var attackedAddresses []string

	// channels to receive found suspicious and attacked addresses
	suspicious := make(chan string)
	attacked := make(chan string)
	// channel to keep track of which goroutines are done
	complete := make(chan bool)
	// number of addresses to give to each worker
	workload := len(addresses) / 2
	// make sure workload isn't 0
	if workload == 0 {
		workload = len(addresses)
	}
	// number of finished goroutines
	finished := 0

	// start workers
	for i := 0; i < 2; i++ {
		// if this is the last worker, give it the rest of the addresses
		if i == 1 {
			go findSuspiciousTCP(addresses[i*workload:], suspicious, attacked, complete)
		} else {
			go findSuspiciousTCP(addresses[i*workload:(i+1)*workload], suspicious, attacked, complete)
		}
	}

	// receive marked addresses from goroutines
Outer:
	for {
		select {
		// attacked address received
		case attackedAddress := <-attacked:
			attackedAddresses = append(attackedAddresses, attackedAddress)
		// suspicious address received
		case suspiciousAddress := <-suspicious:
			suspiciousAddresses = append(suspiciousAddresses, suspiciousAddress)
		// complete signal received
		case <-complete:
			// increment finished goroutines counter
			finished++
			// if all workers are finished, end
			if finished == 2 {
				break Outer
			}
		}
	}

	// return the suspicious and attacked addresses as a pair
	return Report{suspicious: suspiciousAddresses, attacked: attackedAddresses}
}

// getSentSYNPackets gets all SYN packets sent by a given address using a slice of TCP packets
func getSentSYNPackets(source gopacket.Endpoint, tcpPackets []TCPPacketAddress) []TCPPacketAddress {
	// list to store sent tcp packets
	var sentPackets []TCPPacketAddress

	// loop through all tcp packets
	for _, packet := range tcpPackets {
		// if the packet source address matches the given address and is a SYN packet, add it to the return list
		if packet.Source == source && packet.TcpPacket.SYN {
			sentPackets = append(sentPackets, packet)
		}
	}

	// sort the SYN packets by timestamp, ascending
	sort.Slice(sentPackets, func(i, j int) bool {
		return sentPackets[i].Packet.Metadata().Timestamp.Before(sentPackets[j].Packet.Metadata().Timestamp)
	})

	return sentPackets
}

// see if a string is in a slice of strings
func contains(strings []string, word string) bool {
	// loop through strings
	for _, s := range strings {
		// if the strings are equal, return true
		if s == word {
			return true
		}
	}
	// no strings found
	return false
}

// get the IP address of a packet
func getIP(packet gopacket.Packet) net.IP {
	// if it has an ipv4 layer, get its ip
	if ipLayer := packet.Layer(layers.LayerTypeIPv4); ipLayer != nil {
		// get the ipv4 layer to obtain ip address
		ip, _ := ipLayer.(*layers.IPv4)
		// update the running mac details with the IP as an IP and bytes
		return ip.SrcIP
	} else {
		// if it doesn't have an ipv4 layer, check for ARP
		if arpLayer := packet.Layer(layers.LayerTypeARP); arpLayer != nil {
			// get the arp layer
			arp, _ := arpLayer.(*layers.ARP)
			// add the IP only as bytes to the mac details
			return arp.SourceProtAddress
		}
	}
	// no IP found
	return nil
}

// helper function to be used in parallel by tcpConnectScanDetect
func findSuspiciousTcpScan(addresses []TCPAddressData, suspicious chan<- string, complete chan<- bool, tcpPackets []TCPPacketAddress, threshold int, interval time.Duration) {
	// loop through addresses
	for _, address := range addresses {
		// proceed with determining if the address is suspicious if it has sent SYN flags without receiving SYN-ACK packets
		if address.SendsSYN > 0 && address.ReceivesACK == 0 {
			// get the TCP Packets sent by the address
			sentSYNPackets := getSentSYNPackets(address.Address, tcpPackets)

			// initialise lists to contain the tcp connection count and time
			var tcpConnectionCount int
			var tcpConnectionTime time.Time

			// loop through sent packets
			for _, packet := range sentSYNPackets {
				// initialise the time
				tcpConnectionTime = packet.Packet.Metadata().Timestamp
				// If the number of SYN packet excels the threshold, check whether the time elapsed if less than interval.
				// If so, the packet is classified as suspicious
				if tcpConnectionCount >= threshold {
					if packet.Packet.Metadata().Timestamp.Sub(tcpConnectionTime) <= interval {
						// check if the address has been recorded already
						suspicious <- packet.Source.String()
					} else { // if not, reset
						tcpConnectionCount = 0
					}
				}
				// add one to the packet number count
				tcpConnectionCount++
			}
		}
	}
	complete <- true
}

// using the name of a pcap file and a given threshold, returns a slice containing any suspicious addresses
func tcpConnectScanDetect(file string, threshold int) []string {
	// constant time interval to determine how long a packet can send less SYN packets than the threshold
	const interval = 5 * time.Second
	// get packets from a pcap file
	packets := getPackets(file)
	// extract all TCP layers
	tcpPackets := getTCP(packets)
	// collate address data
	addresses := getTCPAddressData(tcpPackets)

	// slices to contain suspicious and attacked addresses
	var suspiciousAddresses []string

	// channels to receive found suspicious and attacked addresses
	suspicious := make(chan string)
	// channel to keep track of which goroutines are done
	complete := make(chan bool)
	// number of addresses to give to each worker
	workload := len(addresses) / 2
	// make sure workload isn't 0
	if workload == 0 {
		workload = len(addresses)
	}
	// number of finished goroutines
	finished := 0

	// start workers
	for i := 0; i < 2; i++ {
		// if this is the last worker, give it the rest of the addresses
		if i == 1 {
			go findSuspiciousTcpScan(addresses[i*workload:], suspicious, complete, tcpPackets, threshold, interval)
		} else {
			go findSuspiciousTcpScan(addresses[i*workload:(i+1)*workload], suspicious, complete, tcpPackets, threshold, interval)
		}
	}

	// receive marked addresses from goroutines
Outer:
	for {
		select {
		// suspicious address received
		case address := <-suspicious:
			if !contains(suspiciousAddresses, address) {
				suspiciousAddresses = append(suspiciousAddresses, address)
			}
		// complete signal received
		case <-complete:
			// increment finished goroutines counter
			finished++
			// if all workers are finished, end
			if finished == 2 {
				break Outer
			}
		}
	}

	// return the suspicious and attacked addresses as a pair
	return suspiciousAddresses
}

// see if a MACAddress appears in a slice related to more than one IP
func containsMac(macAddresses []MACAddress, addr MACAddress) bool {
	// loop through all structs
	for _, address := range macAddresses {
		// mac found
		if address.MAC.String() == addr.MAC.String() && !bytes.Equal(address.IP, addr.IP) {
			return true
		}
	}
	// mac not found
	return false
}

func arpWorker(macAddresses []MACAddress, suspicious chan<- string, complete chan<- bool) {
	// if the mac address appears more than once, it is associated to more than one IP and is therefore suspicious
	for i, address := range macAddresses {
		// check if the addresses without this address contains this mac address
		if containsMac(append(macAddresses[:i], macAddresses[i+1:]...), address) {
			// send address through channel
			suspicious <- address.IP.String()
		}
	}
	complete <- true
}

// using the name of a pcap file, returns a slice containing any suspicious addresses
func arpPoisonDetect(file string) []string {
	// get packets from a pcap file
	packets := getPackets(file)
	// get a list of mac addresses and their associated IPs
	macAddresses := getMAC(packets)

	// slices to contain suspicious and attacked addresses
	var suspiciousAddresses []string

	// number of threads
	threads := 6
	// channels to receive found suspicious and attacked addresses
	suspicious := make(chan string)
	// channel to keep track of which goroutines are done
	complete := make(chan bool)
	// number of addresses to give to each worker
	workload := len(macAddresses) / threads
	// make sure workload isn't 0
	if threads > len(macAddresses) {
		threads = len(macAddresses)
		workload = 1
	}
	// number of finished goroutines
	finished := 0

	// start workers
	for i := 0; i < threads; i++ {
		// if this is the last worker, give it the rest of the addresses
		if i == threads-1 {
			go arpWorker(macAddresses[i*workload:], suspicious, complete)
		} else {
			go arpWorker(macAddresses[i*workload:(i+1)*workload], suspicious, complete)
		}
	}

	// receive marked addresses from goroutines
Outer:
	for {
		select {
		// suspicious address received
		case address := <-suspicious:
			if !contains(suspiciousAddresses, address) {
				suspiciousAddresses = append(suspiciousAddresses, address)
			}
		// complete signal received
		case <-complete:
			// increment finished goroutines counter
			finished++
			// if all workers are finished, end
			if finished == threads {
				break Outer
			}
		}
	}

	// return the suspicious and attacked addresses as a pair
	return suspiciousAddresses
}

// gets all icmp echo packets from a slice of packets
func getICMP(packets []gopacket.Packet) []SourceTime {
	// slice to store found icmp echo packets
	var icmpPackets []SourceTime
	// loop through all provided packets
	for _, packet := range packets {
		// check if it has an icmp echo layer
		if icmpLayer := packet.Layer(layers.LayerTypeICMPv4); icmpLayer != nil {
			// add the icmp echo layer to return slice
			icmpPackets = append(icmpPackets, SourceTime{getIP(packet), packet.Metadata().Timestamp})
		}
	}
	return icmpPackets
}

// return all addresses with pps greater than the given threshold
func testPPS(packets []SourceTime, threshold float64) []string {
	// slice to store suspicious addresses
	var suspiciousAddresses []string

	// collate addresses and their packets
	for i, packet := range packets {
		// check the address for the packet exists
		if packet.Source != nil {
			// IP to search
			ip := packet.Source.String()
			// set this packet to seen
			packets[i].Source = nil

			// minimum and maximum time, and count to calculate packets per second
			start := packet.TimeStamp
			end := packet.TimeStamp
			var count float64 = 1

			// slice of timestamps with this address
			var times []time.Time
			times = append(times, packet.TimeStamp)

			// loop through all other packets
			for j, icmpPacket := range packets {
				// if the address matches, update time and count
				if icmpPacket.Source.String() == ip {
					// remove the packet if it is an outlier
					// update start or end time
					if icmpPacket.TimeStamp.Before(start) {
						start = icmpPacket.TimeStamp
					} else if icmpPacket.TimeStamp.After(end) {
						end = icmpPacket.TimeStamp
					}
					// increment count
					count++
					// mark ip as counted
					packets[j].Source = nil
					// addd this time to times
					times = append(times, icmpPacket.TimeStamp)
				}
			}

			// get the mean
			var sum float64 = 0
			for _, t := range times {
				sum += t.Sub(start).Seconds()
			}
			mean := sum / count

			// get the sum of square differences to the mean
			var squareDifference float64 = 0
			for _, t := range times {
				squareDifference += (t.Sub(start).Seconds() - mean) * (t.Sub(start).Seconds() - mean)
			}
			std := math.Sqrt(squareDifference / (count - 1))

			var timesNoOutliers []time.Time

			// remove outliers
			for _, t := range times {
				if t.Sub(start).Seconds() <= mean+(3*std) {
					timesNoOutliers = append(timesNoOutliers, t)
				}
			}

			// get the difference between the first and last packets in no outliers
			outCount := len(times)
			sort.Slice(times, func(i, j int) bool {
				return times[i].Before(times[j])
			})
			difference := times[outCount-1].Sub(times[0]).Seconds()

			// get the pps
			pps := float64(outCount) / difference

			// if pps is above the threshold, mark the address as suspicious
			if pps > threshold {
				suspiciousAddresses = append(suspiciousAddresses, ip)
			}
		}
	}
	return suspiciousAddresses
}

// using the name of a pcap file and a given threshold, returns a slice containing any suspicious addresses
func icmpFloodDetect(file string, threshold float64) []string {
	// get packets from a pcap file
	packets := getPackets(file)
	// get all ICMP echo packets
	icmpPackets := getICMP(packets)

	// return the suspicious addresses as a pair
	return testPPS(icmpPackets, threshold)
}

// getTCPConnected uses a slice of TCPPacketAddress and returns all addresses with an established tcp connection
func getTCPConnected(packets []TCPPacketAddress) []TCPPacketAddress {
	// connected addresses
	var connectedPackets []TCPPacketAddress
	// slice to contain syn addresses
	var synPackets []TCPConnection

	// loop through addresses
	for _, packet := range packets {
		// adds packets to synPackets
		if packet.TcpPacket.SYN && !packet.TcpPacket.ACK {
			synPackets = append(synPackets, TCPConnection{packet.Source, packet.Destination, packet.TcpPacket, syn})
			// if syn-ack is found, check if the packet addresses link up
		} else if packet.TcpPacket.SYN && packet.TcpPacket.ACK {
			// loop through found syn packets
			for i, synPacket := range synPackets {
				// if they match up, progress the stage of the connection
				if synPacket.Source.String() == packet.Destination.String() && synPacket.Destination.String() == packet.Source.String() {
					synPackets[i].Stage = synack
				}
			}
			// if ack is found, check if the syn-ack was previously found
		} else if packet.TcpPacket.ACK {
			// loop through found syn packets
			for i, synPacket := range synPackets {
				// if the ack is found and the addresses match up, progress to connected
				if synPacket.Source.String() == packet.Destination.String() && synPacket.Destination.String() == packet.Source.String() && synPacket.Stage == synack {
					synPackets[i].Stage = connected
					// add the packet to connected packets
					connectedPackets = append(connectedPackets, packet)
				}
			}
		}
	}

	return connectedPackets
}

// using the name of a pcap file and a given threshold, returns a slice containing any suspicious addresses
func httpFloodDetect(file string, threshold float64) []string {
	// get packets from a pcap file
	packets := getPackets(file)
	// extract all TCP layers
	tcpPackets := getTCP(packets)
	// return nil if no packets found
	if tcpPackets == nil {
		return nil
	}

	// get all tcp connected packets
	connectedPackets := getTCPConnected(tcpPackets)
	// if no connections found, return nil
	if connectedPackets == nil {
		return nil
	}

	// convert between packet address and time source
	var packetTimes []SourceTime
	for _, packet := range connectedPackets {
		packetTimes = append(packetTimes, SourceTime{getIP(packet.Packet), packet.Packet.Metadata().Timestamp})
	}
	// get the pps
	suspiciousAddresses := testPPS(packetTimes, threshold)

	// return the suspicious and attacked addresses as a pair
	return suspiciousAddresses
}

// getDNS extracts all DNS packet layers from a slice of packets
func getDNS(packets []gopacket.Packet) []DNSPacketAddress {
	// slice to return tcp packets
	var dnsPackets []DNSPacketAddress
	// *threaded* loop through all packets
	for _, packet := range packets {
		// assign a variable to the TCP layer if it exists. If it doesn't exist, move on.
		if dnsLayer := packet.Layer(layers.LayerTypeDNS); dnsLayer != nil {
			// get the actual tcp data from the layer, will not return an error as tcp status should have been checked
			dns, _ := dnsLayer.(*layers.DNS)
			// get the source and destination of the packet
			source := packet.NetworkLayer().NetworkFlow().Src()
			dest := packet.NetworkLayer().NetworkFlow().Dst()
			// add the tcp layer and address to the slice
			dnsPackets = append(dnsPackets, DNSPacketAddress{source, dest, dns, packet, dns.QR})
		}
	}

	// return found tcp layers
	return dnsPackets
}

// using the name of a pcap file and a given threshold, returns lists containing any suspicious and suspected attacked addresses
func dnsRequestResponse(file string, threshold float64) Report {
	// get packets from a pcap file
	packets := getPackets(file)
	// extract all TCP layers
	dnsPackets := getDNS(packets)
	// return nil if no packets found
	if dnsPackets == nil {
		return Report{nil, nil}
	}

	// slices to contain request and response times
	var requestTimes []SourceTime
	var responseTimes []SourceTime

	// populate request and response times
	for _, packet := range dnsPackets {
		// if the packet is a response, add it to the response slice
		if packet.Response {
			responseTimes = append(responseTimes, SourceTime{getIP(packet.Packet), packet.Packet.Metadata().Timestamp})
			// the packet is a request
		} else {
			requestTimes = append(requestTimes, SourceTime{getIP(packet.Packet), packet.Packet.Metadata().Timestamp})
		}
	}

	// get all suspicious request and response addresses using testPPS
	requestAddresses := testPPS(requestTimes, threshold)
	responseAddresses := testPPS(responseTimes, threshold)

	// return the suspicious and attacked addresses as a pair
	return Report{suspicious: requestAddresses, attacked: responseAddresses}
}
