package main

import (
	"github.com/catarchive/catarchive/server/control/protocol"
	"github.com/catarchive/catarchive/server/control/util"
	"io"
	"net"
)

var protover = "CAP/0.1.0"

func handle(conn net.Conn) {

	for {
		// Read a packet
		recvData := make([]byte, 1024)
		n, err := conn.Read(recvData)
		if err == io.EOF {
			util.Logger.Println("EOF error reading from connection, closing", conn.RemoteAddr())
			conn.Close()
			return
		}
		if err != nil {
			util.Logger.Println("error reading from connection", conn.RemoteAddr(), err)
			continue
		}

		// Parse the packet
		m, err := protocol.Parse(string(recvData[:n]))
		if err != nil {
			util.Logger.Println("error parsing packet from", conn.RemoteAddr(), err)
			continue
		}

		switch m.Type {

		case protocol.AUTH:

			// Ensure the token is correct
			if m.Data[0] != *token {
				util.Logger.Println("attempted authentication with bad token", conn.RemoteAddr(), err)
				conn.Close()
				return
			}
			util.Logger.Println("client authenticated", conn.RemoteAddr())

			// Send the STRT packet
			_, err = conn.Write([]byte(protocol.Message{
				Proto: protover,
				Type:  protocol.STRT,
			}.String()))
			if err != nil {
				util.Logger.Println("error sending to client", conn.RemoteAddr(), err)
				continue
			}

		case protocol.URLS:

			// Send the response URLS packet
			util.Logger.Println("client requested for URLs", conn.RemoteAddr())
			_, err = conn.Write([]byte(protocol.Message{
				Proto: protover,
				Type:  protocol.URLS,
				Data:  []string{"https://www.reddit.com/r/cats"},
			}.String()))
			if err != nil {
				util.Logger.Println("error sending to client", conn.RemoteAddr(), err)
				continue
			}

		case protocol.IMAG:

			// Log cat images
			util.Logger.Println("image received", conn.RemoteAddr(), m.Data[0])
		}
	}
}
