package util

import (
	"net/http"
)

// GetRemoteAddr will get the remote address taking Cloudflare into account.
func GetRemoteAddr(r *http.Request) string {
	ip := r.Header.Get("CF-Connecting-IP")
	if ip == "" {
		return r.RemoteAddr
	}
	return ip
}
