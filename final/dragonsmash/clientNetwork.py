from java.net import Socket
from java.io import BufferedReader, InputStreamReader, PrintWriter

class Connection(object):
    def __init__(self, addr, port):
        self.socket = Socket(addr, port)
        self.in = BufferedReader(InputStreamReader(self.socket.getInputStream()))
        self.out = PrintWriter(self.socket.getOutputStream(), True)

    def sendMessage(self, msg):
        self.out.println(msg)
        return self.in.readLine()
