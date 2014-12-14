from javax.sound.midi import *

class Note():
    def __init__(self, frequency, instrument, duration):
        self.frequency = frequency
        self.instrument = instrument
        self.duration = duration

class InstrumentNote(Note):
    def __init__(self, frequency, duration):
        pass

class ConnectionTrack():
    def __init__(self, track):
        self.track = track
        self.instrument = None

class Player():
    def __init__(self):
        self.sequencer = MidiSystem.getSequencer()
        self.sequence = Sequence(Sequence.PPQ, 16)

    def _addNote(self, track, freq, instrument, start, duration):
        if instrument != track.instrument:
            track.instrument = instrument
            sm = ShortMessage(ShortMessage.PROGRAM_CHANGE, 1, instrument, 0)
            noteChange = MidiEvent(sm, start)
            track.track.add(noteChange)

        sm = ShortMessage(ShortMessage.NOTE_ON, 1, freq, 127)
        noteOn = MidiEvent(sm, start);
        track.track.add(noteOn);

        sm = ShortMessage(ShortMessage.NOTE_OFF, 1, freq, 127);
        noteOff = MidiEvent(sm, start + duration - 1)
        track.track.add(noteOff);

    def addNote(self, track, note, start):
        self._addNote(track, note.frequency, note.instrument, start, note.duration)

    def newConnection(self):
        return ConnectionTrack(self.sequence.createTrack())

    def playAll(self):
        self.sequencer.setSequence(self.sequence)
        self.sequencer.setLoopCount(Sequencer.LOOP_CONTINUOUSLY)
        self.sequencer.open()
        self.sequencer.start()
    
    def stopAll(self):
        self.sequencer.stop()
        self.sequencer.close()

player = Player()
connect1 = player.newConnection()
connect2 = player.newConnection()

