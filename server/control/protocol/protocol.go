package protocol

import (
	"net"
)

// Protover is the protocol version.
var Protover = "CAP/0.1.0"

// NewClient returns a new client from a net.Conn.
func NewClient(c net.Conn) Client {
	return Client{
		conn: c,
		addr: c.RemoteAddr().String(),
		Auth: false,
	}
}
