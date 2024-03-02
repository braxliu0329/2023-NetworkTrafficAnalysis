package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"path"
	"strings"
)

const FSPATH = "../App/dist/"

func main() {
	fs := http.FileServer(http.Dir(FSPATH))
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

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/" {
			fullPath := FSPATH + strings.TrimPrefix(path.Clean(r.URL.Path), "/")
			_, err := os.Stat(fullPath)
			if err != nil {
				if !os.IsNotExist(err) {
					panic(err)
				}
				r.URL.Path = "/"
			}
		}
		fs.ServeHTTP(w, r)
	})
	http.ListenAndServe(":8080", nil)
}
