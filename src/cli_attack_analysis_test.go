package main

import (
	"github.com/google/gopacket"
	"github.com/google/gopacket/pcap"
	"testing"
)

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

// test the TCP Flood detection for the CLI tool is working as expected
func TestTcpFlood(t *testing.T) {
	t.Fatal("test")
}
