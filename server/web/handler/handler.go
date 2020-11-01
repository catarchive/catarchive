package handler

import (
	"github.com/catarchive/catarchive/server/web/util"
	"io/ioutil"
)

var html = map[string]string{}

// readHTML reads an html file and returns the contents as a string.
func readHTML(name string) string {

	file := "./template/" + name + ".html"

	b, err := ioutil.ReadFile(file)

	if err != nil {
		util.Logger.Fatalln("fatal:", err)
	}

	util.Logger.Println("read html file: " + file)

	return string(b)
}

func init() {

	// Read HTML into memory for faster requests
	html["top"] = readHTML("top")
	html["bottom"] = readHTML("bottom")

	html["index"] = readHTML("index")
	html["error"] = readHTML("error")
}
