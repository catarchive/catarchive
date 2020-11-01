from socket import AF_INET, socket, SOCK_STREAM

from . import exceptions

PROTO = 'CAP/0.1.0'
BUFSIZ = 1024

local_urls = []

def try_close(func):
    """Decorator to wrap function in a try/except for OSError.""" 

    def tc(*args, **kwarg):
        try:
            return func(*args, **kwarg)
        except (OSError, EOFError):
            raise exceptions.SocketClosed()

    return tc

def local(func):
    """Decorator cancel network if local_urls != []""" 

    def nop():
        pass

    def ll(*args, **kwarg):
        if local_urls == []:
            return func(*args, **kwarg)
        else:
            return nop()

    return ll

class Server:
    """Represents a remote connection to a server."""

    def __init__(self, ip, port, token):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.token = token
        self.ip = ip
        self.port = port

    @local
    def connect(self):
        """Attempts to connect to the server."""

        self.socket.connect((self.ip, self.port))

    @local
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

    @local
    @try_close
    def imag(self, url):
        """Sends an image URL to the server."""

        self.socket.send(bytes(PROTO + ' IMAG ' + url, 'utf8'))

    @try_close
    def urls(self):
        """Request URLs to crawl from the server.
        Returns said URLs."""

        if local_urls != []:
            return local_urls

        self.socket.send(bytes(PROTO + ' URLS', 'utf8'))
        resp = self.socket.recv(BUFSIZ).decode('utf8').split(' ')
        if len(resp) < 3 or (len(resp) > 1 and (resp[1] != 'URLS')):
            raise exceptions.InvalidUrlsPacketReceived()

        return resp[2:]

    @local
    def close(self):
        """Cleanly closes the socket."""

        self.socket.close()
