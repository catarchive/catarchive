package handler

import (
	"github.com/catarchive/catarchive/server/web/util"
	"net/http"
	"os"
)

// FileHandler handles static files.
func FileHandler(w http.ResponseWriter, r *http.Request) {

	util.Logger.Println("hit: " + util.GetRemoteAddr(r) + " " + r.RequestURI)

	var dir string
	if r.URL.Path[:8] == "/static/" {
		dir = "."
	} else {
		dir = "static"
	}

	if _, err := os.Stat(dir + r.URL.Path); err != nil {
		ErrorHandler(w, r, http.StatusNotFound)
		return
	}

	http.ServeFile(w, r, dir+r.URL.Path)
}
