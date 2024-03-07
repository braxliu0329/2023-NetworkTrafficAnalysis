package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"path"
	"strings"
	"sync"
	"syscall"

	"nta/backend/api"
)

const FSPATH = "../App/dist/"
const ENDPOINT = ":8080"

var ctxShutdown, cancel = context.WithCancel(context.Background())
var serverDone = &sync.WaitGroup{}
var srv = &http.Server{
	Addr: ENDPOINT,
}

func main() {
	// Create a channel which handels kill signals. Python program gets the name of the Go process
	// and sends a SIGINT to it
	c := make(chan os.Signal, 1)
	signal.Notify(c, syscall.SIGTERM, syscall.SIGINT)
	// deal with SIGTERM so that shutdown is graceful
	go func() {
		<-c
		log.Println("Shutting down server on localhost:8080...")
		cancel()
	}()
	serverDone.Add(1)
	start()
	serverDone.Wait()
}

// start file server on :8080
func start() {
	fs := http.FileServer(http.Dir(FSPATH))
	api.Run()
	// since we are doing client-side routing, server must acknowledge this
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
	shutdown()
	go func() {
		defer serverDone.Done()
		log.Println("Running server on http://localhost:8080")
		if err := srv.ListenAndServe(); err != http.ErrServerClosed {
			log.Fatalf("ListenAndServe(): %v", err)
		}
	}()
}

// shutdown will close server whenever a request is made to /shutdown
func shutdown() {
	http.HandleFunc("/shutdown", func(w http.ResponseWriter, r *http.Request) {
		select {
		case <-ctxShutdown.Done():
			fmt.Println("Sorry: Shuting down ...")
			return
		default:
		}
		cancel()
		log.Println("Shutting down server on localhost:8080...")
		err := srv.Shutdown(context.Background())
		if err != nil {
			log.Println("Server.Shutdown", err)
		}
	})
}
