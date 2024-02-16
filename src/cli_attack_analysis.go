package main

import (
	"bytes"
	"github.com/google/gopacket"
	"github.com/google/gopacket/layers"
	"github.com/google/gopacket/pcap"
	"net"
	"sort"
	"time"
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

// MACAddress struct to pair mac addresses and ip addresses
type MACAddress struct {
	MAC     net.HardwareAddr
	Address []byte
}

func main() {

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

// getETH extracts all Ethernet packet layers from a slice of packets
func getETH(packets []gopacket.Packet) []MACAddress {
	// slice to return tcp packets
	var ethPackets []MACAddress
	// *threaded* loop through all packets
	for _, packet := range packets {
		// assign a variable to the TCP layer if it exists. If it doesn't exist, move on.
		if ethLayer := packet.Layer(layers.LayerTypeEthernet); ethLayer != nil {
			// if it has an ipv4 layer, get its ip
			if ipLayer := packet.Layer(layers.LayerTypeIPv4); ipLayer != nil {
				// get the ipv4 layer to obtain ip address
				ip, _ := ipLayer.(*layers.IPv4)
			} else {

			}

			// get the actual tcp data from the layer, will not return an error as tcp status should have been checked
			eth, _ := ethLayer.(*layers.Ethernet)
			// add the tcp layer and address to the slice
			ethPackets = append(ethPackets, MACAddress{eth.SrcMAC, ip.SrcIP})
		}
	}
	// return found tcp layers
	return ethPackets
}

// getTCPAddressData uses a slice of TCP packets to collate data for each address to be returned as a slice
func getTCPAddressData(tcpPackets []TCPPacketAddress) []TCPAddressData {
	// slice to store tcp address information
	var addresses []TCPAddressData
	// *threaded* obtain all tcp address information
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

	// *threaded* loop through obtained addresses
	for _, address := range addresses {
		// mark the address as attacked if it receives more SYN packets than SYN-ACK packets sent
		if address.ReceivesSyn > 3*address.SendsAck/2 {
			attackedAddresses = append(attackedAddresses, address.Address.String())
		}
		// mark the address as suspicious if it sends more SYN packets than SYN-ACK packets received
		if address.SendsSYN > 3*address.ReceivesACK/2 {
			suspiciousAddresses = append(suspiciousAddresses, address.Address.String())
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

// using the name of a pcap file and a given threshold, returns a slice containing any suspicious addresses
func tcpConnectScanDetect(file string, threshold int) []string {
	// constant time interval to determine how long a packet can send less SYN packets than the threshold
	interval := 5 * time.Second
	// get packets from a pcap file
	packets := getPackets(file)
	// extract all TCP layers
	tcpPackets := getTCP(packets)
	// collate address data
	// collate address data
	addresses := getTCPAddressData(tcpPackets)

	// slices to contain suspicious and attacked addresses
	var suspiciousAddresses []string

	// *threaded* loop through addresses
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
						if !contains(suspiciousAddresses, address.Address.String()) {
							suspiciousAddresses = append(suspiciousAddresses, address.Address.String())
						}
					} else { // if not, reset
						tcpConnectionCount = 0
					}
				}
				// add one to the packet number count
				tcpConnectionCount++
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
		if address.MAC.String() == addr.MAC.String() && !bytes.Equal(address.Address, addr.Address) {
			return true
		}
	}
	// mac not found
	return false
}

// using the name of a pcap file, returns a slice containing any suspicious addresses
func arpPoisonDetect(file string) []string {
	// get packets from a pcap file
	packets := getPackets(file)
	// get a list of mac addresses and their associated IPs
	macAddresses := getETH(packets)

	// slices to contain suspicious and attacked addresses
	var suspiciousAddresses []string

	// if the mac address appears more than once,it is associated to more than one IP and is therefore suspicious
	for _, address := range macAddresses {
		// check if the addresses without this address contains this mac address
		if containsMac(macAddresses, address) {
			suspiciousAddresses = append(suspiciousAddresses, address.MAC.String())
		}
	}

	// return the suspicious and attacked addresses as a pair
	return suspiciousAddresses
}

// using the name of a pcap file and a given threshold, returns a slice containing any suspicious addresses
func icmpFloodDetect(file string, threshold int) []string {
	// slices to contain suspicious and attacked addresses
	var suspiciousAddresses []string

	// return the suspicious and attacked addresses as a pair
	return suspiciousAddresses
}

// using the name of a pcap file and a given threshold, returns a slice containing any suspicious addresses
func httpFloodDetect(file string, threshold int) []string {
	// slices to contain suspicious and attacked addresses
	var suspiciousAddresses []string

	// return the suspicious and attacked addresses as a pair
	return suspiciousAddresses
}

// using the name of a pcap file and a given threshold, returns lists containing any suspicious and suspected attacked addresses
func dnsRequestResponse(file string, threshold int) Report {
	// slices to contain suspicious and attacked addresses
	var suspiciousAddresses []string
	var attackedAddresses []string

	// return the suspicious and attacked addresses as a pair
	return Report{suspicious: suspiciousAddresses, attacked: attackedAddresses}
}
