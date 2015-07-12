from java.net import Socket, ServerSocket
from java.io import BufferedReader, InputStreamReader, PrintWriter

from threading import Thread

from utilNetwork import Message, Ack
from playback import Speaker, Note

class Server(object):
    def __init__(self, port):
        self.port = port
        self._listener = ServerSocket(self.port)
        self.speaker = Speaker()
        self.speaker.playAll()
        self.connections = []

    def listen(self):
        while True:
            newConnection = ClientConnection(self,
                                             self._listener.accept(),
                                             self.speaker.newConnection())
            print 'New connection accepted!', newConnection
            self.connections.append(newConnection)
            Thread(target=newConnection.handle).start()

    def deleteConnection(self, connectionTrack):
        self.speaker.deleteConnection(connectionTrack)


class ClientConnection(object):
    def __init__(self, server, socket, connectionTrack):
        self.server = server
        self.connectionTrack = connectionTrack
        self.kill = False
        self.notes = {}

        self.socket = socket
        self.in = BufferedReader(InputStreamReader(self.socket.getInputStream()))
        self.out = PrintWriter(self.socket.getOutputStream(), True)

        self.handlers = {
            Message.ADD_NOTE: self._addNote,
            Message.ADD_LOOPED_NOTE: self._addLoopedNote,
            Message.DELETE_NOTE: self._deleteNote,
            Message.DELETE_ALL_NOTES: self._deleteAllNotes
        }

    def _addNote(self, args):
        result = self.connectionTrack.addNote(*args)
        key = hash(result)
        self.notes[key] = result
        return key

    def _addLoopedNote(self, args):
        result = self.connectionTrack.addLoopedNote(*args)
        key = hash(result)
        self.notes[key] = result
        return key

    def _deleteNote(self, args):
        note = self.notes.get(args[0])
        if note is not None:
            self.connectionTrack.deleteNote(note)
        else:
            print 'Unknown note hash:', args[0]

    def _deleteAllNotes(self, args):
        self.connectionTrack.deleteAllNotes()

    def handle(self):
        while not self.kill and not self.socket.isClosed():
            data = self.in.readLine()
            if data is None:
                self.kill = True
                break

            msg = Message.decode(data)
            msgType = msg.msgType
            msgData = msg.msgData
            handle = self.handlers[msgType](msgData)

            print data, '->', msg
            ack = Ack(handle)
            self.out.println(str(ack))

        # clean up
        self.connectionTrack.deleteAllEvents()
        self.server.deleteConnection(self.connectionTrack)
        self.socket.close()

    def __str__(self):
        return str(self.socket.getInetAddress()).split('/')[-1]


if __name__ == '__main__':
    s = Server(1640)
    Thread(target=s.listen).start()
