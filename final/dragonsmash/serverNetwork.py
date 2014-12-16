from java.net import Socket, ServerSocket
from java.io import BufferedReader, InputStreamReader, PrintWriter

from threading import Thread

from playback import Speaker, Note

class Server(object):
    def __init__(self, port):
        self.port = port
        self._listener = ServerSocket(self.port)
        self.speaker = Speaker()

    def listen(self):
        while True:
            newConnection = ClientConnection(self,
                                             self._listener.accept(),
                                             self.speaker.newConnection())
            print 'New connection accepted!', newConnection
            Thread(target=newConnection.handle).start()

    def deleteConnection(self, connectionTrack):
        self.speaker.deleteConnection(connectionTrack)

class ClientConnection(object):
    def __init__(self, server, socket, connectionTrack):
        self.server = server
        self.connectionTrack = connectionTrack
        self.kill = False

        self.socket = socket
        self.in = BufferedReader(InputStreamReader(self.socket.getInputStream()))
        self.out = PrintWriter(self.socket.getOutputStream(), True)

    def handle(self):
        while not self.kill and not self.socket.isClosed():
            data = self.in.readLine()
            if data is None:
                self.kill = True
                break

            # TODO actually do things with data
            print data
            self.out.println('ACK')
        # clean up
        self.connectionTrack.deleteAllEvents()
        self.server.deleteConnection(self.connectionTrack)
        self.socket.close()

    def __str__(self):
        return str(self.socket.getInetAddress()).split('/')[-1]

if __name__ == '__main__':
    s = Server(1640)
    s.listen()
