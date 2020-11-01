package handler

import (
	"fmt"
	"github.com/catarchive/catarchive/server/web/util"
	"net/http"
)

// IndexHandler handles the / page.
func IndexHandler(w http.ResponseWriter, r *http.Request) {

	util.Logger.Println("hit: " + util.GetRemoteAddr(r) + " " + r.RequestURI)

	if r.URL.Path == "/" {
		fmt.Fprint(w, html["top"]+html["index"]+html["bottom"])
		return
	}

	h, ok := html[r.URL.Path[1:]]
	if !ok {
		ErrorHandler(w, r, http.StatusNotFound)
		return
	}

	fmt.Fprint(w, html["top"]+h+html["bottom"])
}
