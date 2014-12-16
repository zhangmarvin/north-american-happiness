from ds import *
from ds.instruments import AcousticGuitar, Piano, Saxophone

class FilteredPlayer(Player):
    def __init__(self, original, predicate):
        Player.__init__(self, original.connection)
        self.original = original
        self.predicate = predicate

    def play(self, note):
        if self.predicate(note):
            return self.original.play(note)
        return 0

    def loop(self, note, period):
        if self.predicate(note):
            return self.original.loop(note, period)
        return 0


isEvenNote = lambda n: n.offset % 16 == 0
isOddNote = lambda n: not isEvenNote(n)

def filterNote(player, func, predicate, *args, **kwargs):
    return FilteredPlayer(player, predicate).call(func, *args, **kwargs)

root = AcousticGuitar(60, 0.5, 127, 0)
third = Piano(64, 0.5, 127, 0)
fifth = Saxophone(67, 0.5, 127, 0)
beat = Note(60, 127, 0.5, 127, 0)

def playEvens():
    return player.call(filterNote, Player.majorScale, isEvenNote, root)

def playOdds():
    return player.call(filterNote, Player.majorScale, isOddNote, root)

def playThird():
    return player.majorScale(third)

def playFifth():
    return player.majorScale(fifth)

def playBeat():
    return player.majorScale(beat)

if __name__ == '__main__':
    player = connect()
