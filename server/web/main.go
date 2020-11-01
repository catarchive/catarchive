package main

import (
	"flag"
	"github.com/catarchive/catarchive/server/web/handler"
	"github.com/catarchive/catarchive/server/web/util"
	"net/http"
	"os"
	"strconv"
)

var port = flag.Int("p", 8000, "the port to listen on, overriden by CA_WEB_PORT")

func main() {

	flag.Parse()

	// Get port
	if p := os.Getenv("CA_WEB_PORT"); p != "" {
		np, err := strconv.Atoi(p)
		if err != nil {
			util.Logger.Fatalln("fatal: invalid port:", p)
		}
		port = &np
	}
	addr := ":" + strconv.Itoa(*port)

	// Setup logger
	defer util.LogFile.Close()

	// Handle routes
	http.HandleFunc("/", handler.IndexHandler)
	http.HandleFunc("/favicon.ico", handler.FileHandler)
	http.HandleFunc("/static/", handler.FileHandler)

	// Start the server
	util.Logger.Println("attempting to listen on port", *port)
	util.Logger.Fatalln("fatal:", http.ListenAndServe(addr, nil))
}
