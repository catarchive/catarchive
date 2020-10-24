from socket import AF_INET, socket, SOCK_STREAM

from . import exceptions

PROTO = 'CAP/0.1.0'
BUFSIZ = 1024

def try_close(func):
    """Decorator to wrap function in a try/except for OSError.""" 

    def tc(*args, **kwarg):
        try:
            return func(*args, **kwarg)
        except (OSError, EOFError):
            raise exceptions.SocketClosed()

    return tc

class Server:
    """Represents a remote connection to a server."""

    def __init__(self, ip, port, token):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.token = token
        self.ip = ip
        self.port = port

    def connect(self):
        """Attempts to connect to the server."""

        self.socket.connect((self.ip, self.port))

    @try_close
    def auth(self):
        """Sends the authentication packet to the server.
        Blocks until a response packet is sent.
        Returns the server's protocol."""

        self.socket.send(bytes(PROTO + ' AUTH ' + self.token, 'utf8'))
        resp = self.socket.recv(BUFSIZ).decode('utf8').split(' ')

        if len(resp) != 2 or (len(resp) > 1 and (resp[1] != 'STRT')):
            raise exceptions.InvalidStrtPacketReceived()

        return resp[0]

    @try_close
    def imag(self, url):
        """Sends an image URL to the server."""

        self.socket.send(bytes(PROTO + ' IMAG ' + url, 'utf8'))

    @try_close
    def urls(self):
        """Request URLs to crawl from the server.
        Returns said URLs."""

        self.socket.send(bytes(PROTO + ' URLS', 'utf8'))
        resp = self.socket.recv(BUFSIZ).decode('utf8').split(' ')
        if len(resp) < 3 or (len(resp) > 1 and (resp[1] != 'URLS')):
            raise exceptions.InvalidUrlsPacketReceived()

        return resp[2:]

    def close(self):
        """Cleanly closes the socket."""

        self.socket.close()