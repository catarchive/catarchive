package main

import (
	"flag"
	"github.com/catarchive/catarchive/server/control/protocol"
	"github.com/catarchive/catarchive/server/control/util"
	"net"
	"strconv"
)

var token = flag.String("t", "token", "the authentication token")
var port = flag.Int("p", 9908, "the port to listen on")

func main() {

	// Parse command-line args
	flag.Parse()

	// Set addr to the address to listen on
	addr := ":" + strconv.Itoa(*port)

	// Start a tcp listener
	ln, err := net.Listen("tcp", addr)
	if err != nil {
		util.Logger.Fatalln("could not listen:", err)
	}
	util.Logger.Println("listening on", addr)

	for {
		// Accept a connection
		conn, err := ln.Accept()
		if err != nil {
			util.Logger.Println("warning: error accepting connection")
			continue
		}
		util.Logger.Println("accepted new connection from", conn.RemoteAddr())

		// Handle it in another goroutine
		go handle(protocol.NewClient(conn))
	}
}
