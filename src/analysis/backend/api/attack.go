package api

import (
	"fmt"
	"io"
	"net/http"
	"os"
)

func ARPPoison() {
	http.HandleFunc("/api/arpdata", func(w http.ResponseWriter, r *http.Request) {
		jsonFile, err := os.Open("../../pythonGUI/plotData/arp.json")
		if err != nil {
			fmt.Println("Error opening JSON...")
		}
		defer jsonFile.Close()
		jsonData, err := io.ReadAll(jsonFile)
		if err != nil {
			http.Error(w, "Unable to read JSON file", http.StatusInternalServerError)
		}
		w.Header().Set("Content-Type", "application/json")
		w.Write(jsonData)
	})
}

func DNSRequest() {
	http.HandleFunc("/api/dnsreqdata", func(w http.ResponseWriter, r *http.Request) {
		jsonFile, err := os.Open("../../pythonGUI/plotData/dnsrequest.json")
		if err != nil {
			fmt.Println("Error opening JSON...")
		}
		defer jsonFile.Close()
		jsonData, err := io.ReadAll(jsonFile)
		if err != nil {
			http.Error(w, "Unable to read JSON file", http.StatusInternalServerError)
		}
		w.Header().Set("Content-Type", "application/json")
		w.Write(jsonData)
	})
}

func DNSResponse() {
	http.HandleFunc("/api/dnsresdata", func(w http.ResponseWriter, r *http.Request) {
		jsonFile, err := os.Open("../../pythonGUI/plotData/dnsresponse.json")
		if err != nil {
			fmt.Println("Error opening JSON...")
		}
		defer jsonFile.Close()
		jsonData, err := io.ReadAll(jsonFile)
		if err != nil {
			http.Error(w, "Unable to read JSON file", http.StatusInternalServerError)
		}
		w.Header().Set("Content-Type", "application/json")
		w.Write(jsonData)
	})
}

func DoS() {
	http.HandleFunc("/api/dosdata", func(w http.ResponseWriter, r *http.Request) {
		jsonFile, err := os.Open("../../pythonGUI/plotData/dos.json")
		if err != nil {
			fmt.Println("Error opening JSON...")
		}
		defer jsonFile.Close()
		jsonData, err := io.ReadAll(jsonFile)
		if err != nil {
			http.Error(w, "Unable to read JSON file", http.StatusInternalServerError)
		}
		w.Header().Set("Content-Type", "application/json")
		w.Write(jsonData)
	})
}

func Httpflood() {
	http.HandleFunc("/api/httpflooddata", func(w http.ResponseWriter, r *http.Request) {
		jsonFile, err := os.Open("../../pythonGUI/plotData/httpflood.json")
		if err != nil {
			fmt.Println("Error opening JSON...")
		}
		defer jsonFile.Close()
		jsonData, err := io.ReadAll(jsonFile)
		if err != nil {
			http.Error(w, "Unable to read JSON file", http.StatusInternalServerError)
		}
		w.Header().Set("Content-Type", "application/json")
		w.Write(jsonData)
	})
}

func Icmpflood() {
	http.HandleFunc("/api/icmpflooddata", func(w http.ResponseWriter, r *http.Request) {
		jsonFile, err := os.Open("../../pythonGUI/plotData/icmpflood.json")
		if err != nil {
			fmt.Println("Error opening JSON...")
		}
		defer jsonFile.Close()
		jsonData, err := io.ReadAll(jsonFile)
		if err != nil {
			http.Error(w, "Unable to read JSON file", http.StatusInternalServerError)
		}
		w.Header().Set("Content-Type", "application/json")
		w.Write(jsonData)
	})
}

func Tcpscan() {
	http.HandleFunc("/api/tcpscandata", func(w http.ResponseWriter, r *http.Request) {
		jsonFile, err := os.Open("../../pythonGUI/plotData/tcpscan.json")
		if err != nil {
			fmt.Println("Error opening JSON...")
		}
		defer jsonFile.Close()
		jsonData, err := io.ReadAll(jsonFile)
		if err != nil {
			http.Error(w, "Unable to read JSON file", http.StatusInternalServerError)
		}
		w.Header().Set("Content-Type", "application/json")
		w.Write(jsonData)
	})
}

func Tcpsyn() {
	http.HandleFunc("/api/tcpsyndata", func(w http.ResponseWriter, r *http.Request) {
		jsonFile, err := os.Open("../../pythonGUI/plotData/tcpsyn.json")
		if err != nil {
			fmt.Println("Error opening JSON...")
		}
		defer jsonFile.Close()
		jsonData, err := io.ReadAll(jsonFile)
		if err != nil {
			http.Error(w, "Unable to read JSON file", http.StatusInternalServerError)
		}
		w.Header().Set("Content-Type", "application/json")
		w.Write(jsonData)
	})
}

func SSLStrippingSource() {
	http.HandleFunc("/api/sslsourcedata", func(w http.ResponseWriter, r *http.Request) {
		jsonFile, err := os.Open("../../pythonGUI/plotData/sslsource.json")
		if err != nil {
			fmt.Println("Error opening JSON...")
		}
		defer jsonFile.Close()
		jsonData, err := io.ReadAll(jsonFile)
		if err != nil {
			http.Error(w, "Unable to read JSON file", http.StatusInternalServerError)
		}
		w.Header().Set("Content-Type", "application/json")
		w.Write(jsonData)
	})
}

func SSLStrippingDest() {
	http.HandleFunc("/api/ssldestdata", func(w http.ResponseWriter, r *http.Request) {
		jsonFile, err := os.Open("../../pythonGUI/plotData/ssldest.json")
		if err != nil {
			fmt.Println("Error opening JSON...")
		}
		defer jsonFile.Close()
		jsonData, err := io.ReadAll(jsonFile)
		if err != nil {
			http.Error(w, "Unable to read JSON file", http.StatusInternalServerError)
		}
		w.Header().Set("Content-Type", "application/json")
		w.Write(jsonData)
	})
}

func UDPFlood() {
	http.HandleFunc("/api/udpflooddata", func(w http.ResponseWriter, r *http.Request) {
		jsonFile, err := os.Open("../../pythonGUI/plotData/udpflood.json")
		if err != nil {
			fmt.Println("Error opening JSON...")
		}
		defer jsonFile.Close()
		jsonData, err := io.ReadAll(jsonFile)
		if err != nil {
			http.Error(w, "Unable to read JSON file", http.StatusInternalServerError)
		}
		w.Header().Set("Content-Type", "application/json")
		w.Write(jsonData)
	})
}
