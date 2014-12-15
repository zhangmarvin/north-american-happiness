from javax.sound.midi import *

class Note(object):
    def __init__(self, frequency, instrument, duration):
        self.frequency = frequency
        self.instrument = instrument
        self.duration = duration

class Event(object):
    def __init__(self, *args):
        if args:
            self.midi_events = args
        else:
            self.midi_events = ()

    def addMidiEvent(self, *event):
        self.midi_events += event


class ConnectionTrack(MetaEventListener):
    def __init__(self, track):
        self.track = track
        self.events = []

    def addNote(self, note, offset):

        sm = ShortMessage(ShortMessage.PROGRAM_CHANGE, 1, note.instrument, 0)
        noteChange = MidiEvent(sm, offset)
        self.track.add(noteChange)

        sm = ShortMessage(ShortMessage.NOTE_ON, 1, note.frequency, 127)
        noteOn = MidiEvent(sm, offset);
        self.track.add(noteOn)

        sm = ShortMessage(ShortMessage.NOTE_OFF, 1, note.frequency, 127);
        noteOff = MidiEvent(sm, offset + note.duration)
        self.track.add(noteOff)

        e = Event(noteChange, noteOn, noteOff)
        self.events.append(e)
        return e

    def deleteNote(self, note):
        if note in self.events:
            del self.events[self.events.index(note)]
            for event in note.midi_events:
                self.track.remove(event)

    def deleteAll(self):
        for event in self.events:
            for e in event.midi_events:
                self.track.remove(e)
        self.events = []

    def meta(self, metaMessage):
        pass

class Player(MetaEventListener):
    END_OF_TRACK = 47

    def __init__(self):
        self.sequencer = MidiSystem.getSequencer()
        self.sequence = Sequence(Sequence.PPQ, 16)
        self.sequencer.setSequence(self.sequence)
        self.sequencer.addMetaEventListener(self)
        self.connections = []
        self.stop = True

    def meta(self, meta):
        if meta.getType() == Player.END_OF_TRACK:
            if not self.stop and self.sequencer.isOpen():
                self.sequencer.setTickPosition(0)
                self.sequencer.start()

    def newConnection(self):
        cTrack = ConnectionTrack(self.sequence.createTrack())
        self.sequencer.addMetaEventListener(cTrack)
        self.connections.append(cTrack)
        return cTrack

    def playAll(self):
        self.stop = False
        self.sequencer.open()
        self.sequencer.start()

    def stopAll(self):
        self.stop = True
        self.sequencer.stop()
        self.sequencer.close()
        self.sequencer.setSequence(self.sequence)

player = Player()
connect1 = player.newConnection()
connect2 = player.newConnection()

