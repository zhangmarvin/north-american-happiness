from java.net import Socket
from java.io import BufferedReader, InputStreamReader, PrintWriter

from utilNetwork import Message, Ack

class Connection(object):
    def __init__(self, addr, port):
        self.socket = Socket(addr, port)
        self.in = BufferedReader(InputStreamReader(self.socket.getInputStream()))
        self.out = PrintWriter(self.socket.getOutputStream(), True)

    def sendMessage(self, msg):
        self.out.println(str(msg))
        response = self.in.readLine()
        if response is None: # abort abort abort
            exit(1)
        decoded = Message.decode(response)
        return decoded.msgData # empty string or hash

if __name__ == '__main__':
    from client import *
    me = Connection('192.168.1.3', 1640)

    def t(tone=60, offset=0, period=64):
        me.sendMessage(Message(Message.ADD_LOOPED_NOTE, LoopedNote(tone, 0, 16, 127, offset, period)))
