from javax.sound.midi import *

END_OF_TRACK = 47

class Note(object):
    def __init__(self, frequency, instrument, duration, velocity):
        self.frequency = frequency
        self.instrument = instrument
        self.duration = duration
        self.velocity = velocity

class Event(object):
    def __init__(self, *args):
        if args:
            self.midiEvents = args
        else:
            self.midiEvents = ()

    def addMidiEvents(self, *event):
        self.midiEvents += event

class SingleNoteEvent(object):
    def __init__(self, note, offset):
        self.note = note
        self.offset = offset
        self._midiEvents = []

    @property
    def midiEvents(self):
        if not self._midiEvents:
            sm = ShortMessage(ShortMessage.PROGRAM_CHANGE, 1, self.note.instrument, 0)
            instrumentChange = MidiEvent(sm, self.offset)
            sm = ShortMessage(ShortMessage.NOTE_ON, 1, self.note.frequency, self.note.velocity)
            noteOn = MidiEvent(sm, self.offset)
            sm = ShortMessage(ShortMessage.NOTE_OFF, 1, self.note.frequency, self.note.velocity)
            noteOff = MidiEvent(sm, self.offset + self.note.duration)

            self._midiEvents = [instrumentChange, noteOn, noteOff]

        return self._midiEvents


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
        self.loopedEvents = []

        # for pending notes with offset > track length
        self.queue = []

    def addNote(self, note, offset):
        noteEvent = SingleNoteEvent(note, offset)

        if offset > self.track.ticks():
            self.queue.append(noteEvent)
        else:
            self.addEvent(noteEvent)
        return noteEvent

    def addLoopedNote(self, note, offset, period):
        # create the events
        #self.addEvent(e)

        pass

    def addEvent(self, event):
        # only called for current event
        if isinstance(event, LoopedEvent):
            self.loopedEvents.append(event)
        else: # SingleNoteEvent
            self.events.append(event)
            for e in event.midiEvents:
                self.track.add(e)

    def deleteNote(self, noteEvent):
        if noteEvent in self.events:
            self.events.remove(noteEvent)
            for event in noteEvent.midiEvents:
                self.track.remove(event)

    def deleteAllOneTimeEvents(self):
        for event in self.events:
            for e in event.midiEvents:
                self.track.remove(e)
        self.events = []

    def meta(self, metaMessage):
        if metaMessage.getType() == END_OF_TRACK:
            self.deleteAllOneTimeEvents()

            for event in self.queue[:]:
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
#connect2 = player.newConnection()

offset = 48
note = Note(60,0,16,127)
sm = ShortMessage(ShortMessage.PROGRAM_CHANGE, 1, note.instrument, 0)
instrumentChange = MidiEvent(sm, offset)
sm = ShortMessage(ShortMessage.NOTE_ON, 1, note.frequency, note.velocity)
noteOn = MidiEvent(sm, offset)
sm = ShortMessage(ShortMessage.NOTE_OFF, 1, note.frequency, note.velocity)
noteOff = MidiEvent(sm, offset + note.duration)

connect1.track.add(instrumentChange)
connect1.track.add(noteOn)
connect1.track.add(noteOff)
