package protocol

import (
	"net"
)

type Client struct {
	Auth bool
	conn net.Conn
	addr string
}

func (c Client) String() string {
	if c.Auth {
		return c.addr + "(auth)"
	}
	return c.addr
}

func (c Client) Close() {
	c.conn.Close()
}

func (c Client) Read() (Message, error) {

	// Read a packet
	recvData := make([]byte, 1024)
	n, err := c.conn.Read(recvData)
	if err != nil {
		return Message{}, err
	}

	// Parse the packet
	m, err := parse(string(recvData[:n]))
	if err != nil {
		return Message{}, err
	}

	return m, nil
}

func (c Client) Strt() error {
	_, err := c.conn.Write([]byte(Message{
		Proto: Protover,
		Type:  STRT,
	}.String()))

	return err
}

func (c Client) Urls() error {
	_, err := c.conn.Write([]byte(Message{
		Proto: Protover,
		Type:  URLS,
		Data:  []string{"https://www.reddit.com/r/cats"},
	}.String()))

	return err
}
