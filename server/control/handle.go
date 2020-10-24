package main

import (
	"github.com/catarchive/catarchive/server/control/protocol"
	"github.com/catarchive/catarchive/server/control/util"
	"io"
)

func handle(c protocol.Client) {

	for {
		// Read a packet
		m, err := c.Read()
		if err == io.EOF {
			util.Logger.Println("EOF error reading from connection, closing", c)
			c.Close()
			return
		} else if err != nil {
			util.Logger.Println("error reading from packet from", c, err)
			continue
		}

		// Ensure authentication (unless its an AUTH packet)
		if !c.Auth && (m.Type != protocol.AUTH) {
			util.Logger.Println("attempted to send packet without authentication, disconnecting", c, err)
			c.Close()
			return
		}

		// Handle each packet type
		switch m.Type {

		case protocol.AUTH:

			// Ensure the token is correct
			if m.Data[0] != *token {
				util.Logger.Println("attempted authentication with bad token, disconnecting", c, err)
				c.Close()
				return
			}
			c.Auth = true
			util.Logger.Println("client authenticated", c)
			if m.Proto != protocol.Protover {
				util.Logger.Println("warning: client using differnt protocol", c, m.Proto)
			}

			// Send the STRT packet
			c.Strt()
			if err != nil {
				util.Logger.Println("error sending STRT packet to client", c, err)
				continue
			}

		case protocol.URLS:

			// Send the response URLS packet
			util.Logger.Println("client requested for URLs", c)
			c.Urls()
			if err != nil {
				util.Logger.Println("error sending URLS packet to client", c, err)
				continue
			}

		case protocol.IMAG:

			// Log cat images
			util.Logger.Println("image received from", c, m.Data[0])
		}
	}
}
