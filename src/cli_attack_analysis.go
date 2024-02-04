package main

import (
	"github.com/google/gopacket"
	"github.com/google/gopacket/pcap"
)

// Report struct to contain slices of suspicious and attacked addresses
type Report struct {
	suspicious []string
	attacked   []string
}

func main() {

}

// get packets from a file into a slice of packets
func getPackets(path string) []gopacket.Packet {
	// handle errors, such as incorrect file paths
	if handle, err := pcap.OpenOffline(path); err != nil {
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

// using the name of a pcap file, returns lists containing any suspicious and suspected attacked addresses
func tcpSynFloodDetect(file string) Report {
	// slices to contain suspicious and attacked addresses
	var suspiciousAddresses []string
	var attackedAddresses []string

	// return the suspicious and attacked addresses as a pair
	return Report{suspicious: suspiciousAddresses, attacked: attackedAddresses}
}
