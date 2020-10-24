class InvalidStrtPacketReceived(Exception):
    """The packet received after AUTH was invalid."""
    pass

class InvalidUrlsPacketReceived(Exception):
    """The packet received after a URLS packet was invalid."""
    pass

class SocketClosed(Exception):
    """The connected socket was unexpectedly closed."""
    pass
