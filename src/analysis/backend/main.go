package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"path"
	"src/analysis/backend/api"
	"strings"
	"sync"
)

const FSPATH = "../App/dist/"
const ENDPOINT = ":8080"

var ctxShutdown, cancel = context.WithCancel(context.Background())

func main() {
	serverDone := &sync.WaitGroup{}
	serverDone.Add(1)
	Start(serverDone)
	serverDone.Wait()
}

func Start(wg *sync.WaitGroup) {
	fs := http.FileServer(http.Dir(FSPATH))
	api.Run()

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
	srv := &http.Server{
		Addr: ENDPOINT,
	}
	api.Shutdown(srv, ctxShutdown, cancel)
	go func() {
		defer wg.Done()
		log.Println("Running server on http://localhost:8080")
		if err := srv.ListenAndServe(); err != http.ErrServerClosed {
			log.Fatalf("ListenAndServe(): %v", err)
		}
	}()
}
