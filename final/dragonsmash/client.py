from util import *
from utilNetwork import *


class SingleNote(object):

    def __init__(self, note):
        self._attrs = [note.frequency, note.instrument, note.duration, note.velocity, note.offset]

    def __str__(self):
        return ','.join(map(str, self._attrs))

    def __eq__(self, other):
        return isinstance(other, SingleNote) and self._attrs == other._attrs


class LoopedNote(SingleNote):

    def __init__(self, note, period):
        SingleNote.__init__(self, note)
        self._attrs.append(period * 16)


class Note(object):

    def __init__(self, frequency, instrument, duration, velocity, offset):
        self.frequency = frequency if type(frequency) is int else note_to_num[frequency]
        self.instrument = instrument if type(instrument) is int else instrument_to_num[instrument]
        self.duration = int(duration * 16)
        self.velocity = velocity
        self.offset = int(offset * 16)


def noteFactoryFactory(instrument):
    def instrumentNoteFactory(frequency, duration, velocity, offset):
        return Note(frequency, instrument, duration, velocity, offset)
    return instrumentNoteFactory


Piano = noteFactoryFactory('Acoustic Grand')
Keyboard = noteFactoryFactory('Electric Piano 1')
AcousticGuitar = noteFactoryFactory('Steel String Guitar')
ElectricGuitar = noteFactoryFactory('Electric Clean Guitar')
Bass = noteFactoryFactory('Electric Bass(finger)')
Violin = noteFactoryFactory('Violin')
Trumpet = noteFactoryFactory('Trumpet')
Saxophone = noteFactoryFactory('Alto Sax')


class NoteEvent(object):

    def __init__(self, noteHashes, player):
        self.noteHashes = noteHashes
        self.player = player

    def kill(self):
        for noteHash in self.noteHashes:
            self.player.connection.sendMessage(Message(Message.DELETE_NOTE, noteHash))


class Player(object):
    """Main functionality for client-side playback."""

    def __init__(self, connection):
        self.connection = connection

    def _play(self, note):
        return self.connection.sendMessage(Message(Message.ADD_NOTE, SingleNote(note)))

    def _loop(self, note, period):
        return self.connection.sendMessage(Message(Message.ADD_LOOPED_NOTE, LoopedNote(note, period)))

    def play(self, note):
        noteHash = self._play(note)
        return NoteEvent([noteHash], self)

    def loop(self, note, period):
        noteHash = self._loop(note, period)
        return NoteEvent([noteHash], self)

    def call(self, func, *args):
        return func(self, *args)

    def stopAll(self):
        self.connection.sendMessage(Message(Message.DELETE_ALL_NOTES))

    def chord(self, root, differences, loop=True):
        noteHashes = []
        tonic = root.frequency
        period = (root.duration * 2) // 16
        if loop:
            noteHashes.append(self._loop(root, period))
        else:
            noteHashes.append(self._play(root))
        for diff in differences:
            root.frequency += diff
            if loop:
                noteHashes.append(self._loop(root, period))
            else:
                noteHashes.append(self._play(root))
        root.frequency = tonic
        return NoteEvent(noteHashes, self)

    def majorChord(self, root, loop=True):
        return self.chord(root, [4, 3], loop)

    def minorChord(self, root, loop=True):
        return self.chord(root, [3, 4], loop)

    def scale(self, root, differences, loop=True):
        noteHashes = []
        tonic, start = root.frequency, root.offset
        period = (root.duration * (len(differences) + 1)) // 16
        if loop:
            noteHashes.append(self._loop(root, period))
        else:
            noteHashes.append(self._play(root))
        for diff in differences:
            root.frequency += diff
            root.offset += root.duration
            if loop:
                noteHashes.append(self._loop(root, period))
            else:
                noteHashes.append(self._play(root))
        root.frequency, root.offset = tonic, start
        return NoteEvent(noteHashes, self)

    def majorScale(self, root, loop=True):
        return self.scale(root, [2, 2, 1, 2, 2, 2, 1], loop)

    def minorScale(self, root, loop=True):
        return self.scale(root, [2, 1, 2, 2, 1, 2, 2], loop)
