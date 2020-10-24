package protocol

import (
	"errors"
	"strings"
)

// Parse will parse a string into a message struct according to the CAP protocol.
func Parse(message string) (Message, error) {

	// Split the message
	p := strings.Split(message, " ")
	if len(p) < 2 {
		return Message{}, errors.New("packet has less than two parts")
	}

	// Initialize message struct
	m := Message{
		Proto: p[0],
	}

	// Set data based on type
	switch p[1] {
	case "AUTH":
		m.Type = AUTH
		if len(p) != 3 {
			return Message{}, errors.New("AUTH packet has no token")
		}
		m.Data = []string{p[2]}
		return m, nil
	case "URLS":
		m.Type = URLS
		return m, nil
	case "IMAG":
		m.Type = IMAG
		if len(p) != 3 {
			return Message{}, errors.New("IMAG packet has no URL")
		}
		m.Data = []string{p[2]}
		return m, nil
	default:
		return Message{}, errors.New("invalid packet type")
	}
}
