from javax.sound.midi import *

END_OF_TRACK = 47

class Note(object):
    def __init__(self, frequency, instrument, duration, velocity):
        self.frequency = frequency
        self.instrument = instrument
        self.duration = duration
        self.velocity = velocity

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


class LoopedNoteEvent(object):
    def __init__(self, note, offset, period):
        self.note = note
        self.offset = offset
        self.period = period
        self.midiEvents = []

    def generateMidiEvents(self, trackLength):
        self.midiEvents = []

        for start in range(self.offset, trackLength, self.period):
            sm = ShortMessage(ShortMessage.PROGRAM_CHANGE, 1, self.note.instrument, 0)
            instrumentChange = MidiEvent(sm, start)
            sm = ShortMessage(ShortMessage.NOTE_ON, 1, self.note.frequency, self.note.velocity)
            noteOn = MidiEvent(sm, start);
            sm = ShortMessage(ShortMessage.NOTE_OFF, 1, self.note.frequency, self.note.velocity)
            noteOff = MidiEvent(sm, start + self.note.duration)

            self.midiEvents.extend([instrumentChange, noteOn, noteOff])

        self.offset = (start + self.period) - trackLength



class ConnectionTrack(MetaEventListener):
    dummyMessage = MetaMessage(42, None, 0)

    def __init__(self, track, measureLength):
        self.track = track
        self.measureLength = measureLength
        self.track.add(MidiEvent(self.dummyMessage, measureLength - 1))

        self.singleEvents = []
        self.loopedEvents = []

        # for pending notes with offset > track length
        self.queue = []
        self._deleteEOT()

    def addNote(self, note, offset):
        noteEvent = SingleNoteEvent(note, offset)
        self.addEvent(noteEvent)
        return noteEvent

    def addLoopedNote(self, note, offset, period):
        noteEvent = LoopedNoteEvent(note, offset, period)
        self.addEvent(noteEvent)
        return noteEvent

    def addEvent(self, event):
        if event.offset > self.track.ticks():
            self.queue.append(event)
            return

        # only called for current event
        if isinstance(event, LoopedNoteEvent):
            self.loopedEvents.append(event)
        else: # SingleNoteEvent
            self.singleEvents.append(event)

        for e in event.midiEvents:
            self.track.add(e)
        self._deleteEOT()

    def deleteNote(self, noteEvent):
        if noteEvent in self.singleEvents:
            self.singleEvents.remove(noteEvent)
            for event in noteEvent.midiEvents:
                self.track.remove(event)
        elif noteEvent in self.loopedEvents:
            self.loopedEvents.remove(noteEvent)
            for event in noteEvent.midiEvents:
                self.track.remove(event)


    def deleteAllEvents(self):
        for event in self.singleEvents:
            for e in event.midiEvents:
                self.track.remove(e)
        self.singleEvents = []

        for event in self.loopedEvents:
            for e in event.midiEvents:
                self.track.remove(e)
        self.loopedEvents = []

    def meta(self, metaMessage):
        if metaMessage.getType() == END_OF_TRACK:
            oldLoopedEvents = self.loopedEvents
            self.deleteAllEvents()

            for event in self.queue[:]:
                event.offset -= self.track.ticks()
                if event.offset < self.track.ticks():
                    self.addEvent(event)
                    self.queue.remove(event)

            for event in oldLoopedEvents:
                event.generateMidiEvents(self.measureLength)
                self.addEvent(event)

    def _deleteEOT(self):
        lastEvent = self.track.get(self.track.size()-1)
        while lastEvent.getTick() > self.measureLength - 1:
            self.track.remove(lastEvent)
            lastEvent = self.track.get(self.track.size()-1)


class Speaker(MetaEventListener):

    def __init__(self, ppq, measureLength):
        self.sequencer = MidiSystem.getSequencer()
        self.sequence = Sequence(Sequence.PPQ, ppq)
        self.sequencer.setSequence(self.sequence)
        self.sequencer.addMetaEventListener(self)
        self.connections = []
        self.measureLength = measureLength
        self.playing = False

    def meta(self, meta):
        if meta.getType() == END_OF_TRACK:
            if self.playing:
                self.sequencer.setTickPosition(0)
                self.sequencer.start()

    def newConnection(self):
        cTrack = ConnectionTrack(self.sequence.createTrack(), self.measureLength)
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

s = Speaker(16, 64)
c1 = s.newConnection()
c2 = s.newConnection()

