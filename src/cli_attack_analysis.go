package main

import (
	"github.com/google/gopacket"
	"github.com/google/gopacket/layers"
	"github.com/google/gopacket/pcap"
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

// TCPAddress struct to pair tcp packets with their source and Destination
type TCPAddress struct {
	Source      gopacket.Endpoint
	Destination gopacket.Endpoint
	TcpPacket   *layers.TCP
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
func getTCP(packets []gopacket.Packet) []TCPAddress {
	// slice to return tcp packets
	var tcpPackets []TCPAddress
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
			tcpPackets = append(tcpPackets, TCPAddress{source, dest, tcp})
		}
	}

	// return found tcp layers
	return tcpPackets
}

// maskAddress turns an endpoint into a string address by taking the first and last 3 sections
func maskAddress(source gopacket.Endpoint) string {
	//// get the full address chunks as a string
	//addressBytes := strings.Split(source.String(), ".")
	//// return the wanted masked address
	//return addressBytes[0] + addressBytes[4] + addressBytes[5] + addressBytes[6]
	return source.String()
}

// tcpSynFloodDetect uses the name of a pcap file and returns lists containing any suspicious and suspected attacked addresses
func tcpSynFloodDetect(file string) Report {
	// get packets from a pcap file
	packets := getPackets(file)
	// extract all TCP layers
	tcpPackets := getTCP(packets)

	// slices to contain suspicious and attacked addresses
	var suspiciousAddresses []string
	var attackedAddresses []string

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
				address = TCPAddressData{packet.Source, address.SendsSYN + syn, address.SendsAck + ack, address.ReceivesSyn, address.ReceivesACK}
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
				address = TCPAddressData{packet.Destination, address.SendsSYN, address.SendsAck, address.ReceivesSyn + syn, address.ReceivesACK + ack}
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
			addresses = append(addresses, TCPAddressData{packet.Source, syn, ack, 0, 0})
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
			addresses = append(addresses, TCPAddressData{packet.Destination, 0, 0, syn, ack})
		}
	}

	// *threaded* loop through obtained addresses
	for _, address := range addresses {
		// mark the address as suspicious if it receives more SYN packets than SYN-ACK packets sent
		if address.ReceivesSyn > 3*address.SendsAck/2 {
			suspiciousAddresses = append(suspiciousAddresses, maskAddress(address.Address))
		}
		// mark the address as suspicious if it sends more SYN packets than SYN-ACK packets received
		if address.SendsSYN > 3*address.ReceivesACK/2 {
			attackedAddresses = append(attackedAddresses, maskAddress(address.Address))
		}
	}

	// return the suspicious and attacked addresses as a pair
	return Report{suspicious: suspiciousAddresses, attacked: attackedAddresses}
}

// using the name of a pcap file and a given threshold, returns a slice containing any suspicious addresses
func tcpConnectScanDetect(file string, threshold int) []string {
	// slices to contain suspicious and attacked addresses
	var suspiciousAddresses []string

	// return the suspicious and attacked addresses as a pair
	return suspiciousAddresses
}

// using the name of a pcap file, returns a slice containing any suspicious addresses
func arpPoisonDetect(file string) []string {
	// slices to contain suspicious and attacked addresses
	var suspiciousAddresses []string

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
