class SingleNote(object):
    def __init__(self, frequency, instrument, duration, velocity, offset):
        self.frequency = frequency
        self.instrument = instrument
        self.duration = duration
        self.velocity = velocity
        self.offset = offset

        self._attrs = [frequency, instrument, duration, velocity, offset]

    def __str__(self):
        return ','.join(map(str, self._attrs))

class LoopedNote(SingleNote):
    def __init__(self, frequency, instrument, duration, velocity, offset, period):
        SingleNote.__init__(self, frequency, instrument, duration, velocity, offset)
        self.period = period

        self._attrs.append(period)
