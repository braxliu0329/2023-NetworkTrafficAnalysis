package api

import (
	"context"
	"fmt"
	"log"
	"net/http"
)

func Run() {
	Ipv4()
	Ipv6()
	Mac()
	Protocol()
	Source()
	Dest()
	DNSRequest()
	DNSResponse()
	Httpflood()
	Icmpflood()
	DoS()
	Tcpscan()
	Tcpsyn()
}

func Shutdown(srv *http.Server, ctxShutdown context.Context, cancel context.CancelFunc) {
	http.HandleFunc("/callback", func(w http.ResponseWriter, r *http.Request) {
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
