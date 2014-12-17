from clientNetwork import Connection
from serverNetwork import Server
from client import Note, Player
import instruments

def listen(addr='localhost', port=1640):
    """Starts up a dragonsmash server, which listens at port PORT."""
    print 'Now listening on port %d...' % port
    s = Server(port)
    s.listen()

def connect(addr='localhost', port=1640):
    """Connects to an existing dragonsmash server at (addr, port)."""
    print 'Connecting to', (addr, port)
    return Player(Connection(addr, port))

__all__ = [
    'listen', # server-side
    'connect', # client-side
    'Note',
    'Player',
    'instruments',
]
