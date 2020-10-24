package protocol

const (
	AUTH = iota
	IMAG = iota
	URLS = iota
	STRT = iota
)

// Message represents a CAP message.
type Message struct {
	Proto string
	Type  int
	Data  []string
}

// String converts a message struct into the corresponding string according to the CAP protocol.
func (m Message) String() string {
	out := m.Proto
	switch m.Type {
	case AUTH:
		out += " AUTH"
	case IMAG:
		out += " IMAG"
	case URLS:
		out += " URLS"
	case STRT:
		out += " STRT"
	}

	for _, i := range m.Data {
		out += " " + i
	}

	return out
}
