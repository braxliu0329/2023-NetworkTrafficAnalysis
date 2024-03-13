package api

import (
	"fmt"
	"io"
	"net/http"
	"os"
)

func Ipv4() {
	http.HandleFunc("/api/ipv4data", func(w http.ResponseWriter, r *http.Request) {
		jsonFile, err := os.Open("../../pythonGUI/plotData/ipv4.json")
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

func Ipv6() {
	http.HandleFunc("/api/ipv6", func(w http.ResponseWriter, r *http.Request) {
		jsonFile, err := os.Open("../../pythonGUI/plotData/ipv6.json")
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

func Mac() {
	http.HandleFunc("/api/macdata", func(w http.ResponseWriter, r *http.Request) {
		jsonFile, err := os.Open("../../pythonGUI/plotData/mac.json")
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
