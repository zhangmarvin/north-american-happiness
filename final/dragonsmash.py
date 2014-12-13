from javax.sound.midi import *

class ConnectionTrack():
    def __init__(self, track):
        self.track = track
        self.instrument = None

class Player():

    def __init__(self):
        self.sequencer = MidiSystem.getSequencer()
        self.sequencer.setLoopCount(Sequencer.LOOP_CONTINUOUSLY)
        self.sequence = Sequence(Sequence.PPQ, 16)
        self.sequencer.setSequence(self.sequence)
        self.sequencer.open()

    def addNote(self, track, note, instrument, start, duration):
        if instrument != track.instrument:
            track.instrument = instrument
            sm = ShortMessage(ShortMessage.PROGRAM_CHANGE, 1, instrument, 0)
            noteChange = MidiEvent(sm, start)
            track.track.add(noteChange)

        sm = ShortMessage(ShortMessage.NOTE_ON, 1, note, 127)
        noteOn = MidiEvent(sm, start);
        track.track.add(noteOn);

        sm = ShortMessage(ShortMessage.NOTE_OFF, 1, note, 100);
        noteOff = MidiEvent(sm, start + duration - 1)
        track.track.add(noteOff);

    def newConnection(self):
        return ConnectionTrack(self.sequence.createTrack())

    def playAll(self):
        self.sequencer.start()
    
    def stopAll(self):
        self.sequencer.stop()


player = Player()
connect = player.newConnection()



