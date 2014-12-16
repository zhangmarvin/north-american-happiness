from playback import Note

class Message(object):
    ADD_NOTE = 'AN'
    ADD_LOOPED_NOTE = 'ALN'
    DELETE_NOTE = 'DN'
    DELETE_ALL_NOTES = 'DAN'
    ACK = 'ACK'

    def __init__(self, msgType, msgData):
        self.msgType = msgType
        self.msgData = msgData

    def __str__(self):
        return self.msgType + ':' + str(self.msgData)

    def __eq__(self, other):
        if not isinstance(other, Message):
            return False
        return self.msgType == other.msgType and self.msgData == other.msgData

    @staticmethod
    def decode(message):
        msgType, msgData = message.split(':')
        args = msgData.split(',')

        if msgType == Message.ACK:
            return Ack(*args)
        elif msgType == Message.ADD_NOTE:
            args = map(int, args)
            return Message(msgType, (Note(*args[:-1]), args[-1]))
        elif msgType == Message.ADD_LOOPED_NOTE:
            args = map(int, args)
            return Message(msgType, (Note(*args[:-2]), args[-2], args[-1]))
        elif msgType == Message.DELETE_NOTE:
            return Message(msgType, args)
        elif msgType == Message.DELETE_ALL_NOTES:
            return Message(msgType, ())

class Ack(Message):
    def __init__(self, msgData=''):
        if msgData is None:
            msgData = ''
        Message.__init__(self, Message.ACK, msgData)

if __name__ == '__main__':
    from client import SingleNote, LoopedNote

    s = SingleNote(60, 0, 16, 127, 0)
    ls = LoopedNote(60, 0, 16, 127, 0, 64)

    anMessage = Message(Message.ADD_NOTE, s)
    alnMessage = Message(Message.ADD_LOOPED_NOTE, ls)
