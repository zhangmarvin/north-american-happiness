from javax.sound.midi import *

END_OF_TRACK = 47

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

    def addMidiEvents(self, *event):
        self.midi_events += event

class SingleEvent(Event):
    def __init__(self, offset, *args):
        Event.__init__(self, *args)
        self.offset = offset

class LoopedEvent(Event):
    def __init__(self, period, offset, *args):
        Event.__init__(self, *args)
        self.period = period
        self.offset = offset

class ConnectionTrack(MetaEventListener):
    def __init__(self, track):
        self.track = track

        # for one-time notes
        self.events = []

        #
        self.looped_events = []

        # for pending notes with offset > track length
        self.queue = []

    def addNote(self, note, offset):

        sm = ShortMessage(ShortMessage.PROGRAM_CHANGE, 1, note.instrument, 0)
        instrumentChange = MidiEvent(sm, offset)
        sm = ShortMessage(ShortMessage.NOTE_ON, 1, note.frequency, 127)
        noteOn = MidiEvent(sm, offset);
        sm = ShortMessage(ShortMessage.NOTE_OFF, 1, note.frequency, 127);
        noteOff = MidiEvent(sm, offset + note.duration)

        e = SingleEvent(offset, instrumentChange, noteOn, noteOff)
        self.addEvent(e)

        return e


    def addLoopedNote(self, note, offset, period):
        # create the events
        #self.addEvent(e)

        pass

    def addEvent(self, event):
        if event.offset > self.track.ticks():
            self.queue.append(event)
            return

        if isinstance(event, LoopedEvent):
            self.looped_events.append(event)
        else:
            self.events.append(event)
            for e in event.midi_events:
                self.track.add(e)

    def deleteNote(self, note):
        if note in self.events:
            del self.events[self.events.index(note)]
            for event in note.midi_events:
                self.track.remove(event)

    def deleteAllOneTimeEvents(self):
        for event in self.events:
            for e in event.midi_events:
                self.track.remove(e)
        self.events = []

    def meta(self, metaMessage):
        if metaMessage.getType() == END_OF_TRACK:
            self.deleteAllOneTimeEvents()

            for event in list(self.queue):
                event.offset -= self.track.ticks()
                if event.offset < self.track.ticks():
                    self.addEvent(event)
                    self.queue.remove(event)


class Speaker(MetaEventListener):

    def __init__(self):
        self.sequencer = MidiSystem.getSequencer()
        self.sequence = Sequence(Sequence.PPQ, 16)
        self.sequencer.setSequence(self.sequence)
        self.sequencer.addMetaEventListener(self)
        self.connections = []
        self.playing = False

    def meta(self, meta):
        if meta.getType() == END_OF_TRACK:
            if self.playing:
                self.sequencer.setTickPosition(0)
                self.sequencer.start()

    def newConnection(self):
        cTrack = ConnectionTrack(self.sequence.createTrack())
        self.sequencer.addMetaEventListener(cTrack)
        self.connections.append(cTrack)
        return cTrack

    def playAll(self):
        self.playing = True
        self.sequencer.open()
        self.sequencer.start()

    def stopAll(self):
        self.playing = False
        self.sequencer.stop()
        self.sequencer.close()
        self.sequencer.setSequence(self.sequence)

player = Speaker()
connect1 = player.newConnection()
connect2 = player.newConnection()

offset = 64
note = Note(60,0,16)
sm = ShortMessage(ShortMessage.PROGRAM_CHANGE, 1, note.instrument, 0)
instrumentChange = MidiEvent(sm, offset)
sm = ShortMessage(ShortMessage.NOTE_ON, 1, note.frequency, 127)
noteOn = MidiEvent(sm, offset);
sm = ShortMessage(ShortMessage.NOTE_OFF, 1, note.frequency, 127);
noteOff = MidiEvent(sm, offset + note.duration)

connect1.track.add(instrumentChange)
connect1.track.add(noteOn)
connect1.track.add(noteOff)

