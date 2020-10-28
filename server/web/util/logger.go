package util

import (
	"io"
	"log"
	"net/http"
	"os"
	"strconv"
	"time"
)

var Logger *log.Logger
var LogFile os.File

func init() {

	// Log to stdout and a file
	LogFile, err := os.Create("./log/go-website-" + strconv.Itoa(int(time.Now().Unix())) + ".log")
	if err != nil {
		log.Fatal("fatal:", err)
	}

	LogFile.Sync()
	Logger = log.New(io.MultiWriter(LogFile, os.Stdout), "", log.Ldate|log.Ltime)
}

// LoggerMiddleware logs all hits to a handler.
func LoggerMiddleware(handle func(w http.ResponseWriter, r *http.Request)) func(w http.ResponseWriter, r *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		handle(w, r)
	}
}
