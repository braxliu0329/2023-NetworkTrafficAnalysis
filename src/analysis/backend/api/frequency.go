package api

import (
	"fmt"
	"io"
	"net/http"
	"os"
)

func Protocol() {
	http.HandleFunc("/api/protocoldata", func(w http.ResponseWriter, r *http.Request) {
		jsonFile, err := os.Open("../../pythonGUI/plotData/Protocol.json")
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

func Source() {
	http.HandleFunc("/api/sourcedata", func(w http.ResponseWriter, r *http.Request) {
		jsonFile, err := os.Open("../../pythonGUI/plotData/SourceIP.json")
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

func Dest() {
	http.HandleFunc("/api/destdata", func(w http.ResponseWriter, r *http.Request) {
		jsonFile, err := os.Open("../../pythonGUI/plotData/DestIP.json")
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
