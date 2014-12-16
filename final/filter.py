import ds
from ds.client import *

class FilteredPlayer(Player):
    def __init__(self, original, predicate):
        Player.__init__(self, original.connection)
        self.original = original
        self.predicate = predicate

    def _play(self, note):
        if self.predicate(note):
            return self.original._play(note)
        return 0

    def _loop(self, note, period):
        if self.predicate(note):
            return self.original._loop(note, period)
        return 0


isEvenNote = lambda n: n.offset % 16 == 0
isOddNote = lambda n: not isEvenNote(n)

def filterNote(player, func, predicate, *args, **kwargs):
    return FilteredPlayer(player, predicate).call(func, *args, **kwargs)

player = ds.connect()

root = Piano(60, 0.5, 127, 0)

def playEvens():
    return player.call(filterNote, Player.majorScale, isEvenNote, root)

def playOdds():
    return player.call(filterNote, Player.majorScale, isOddNote, root)

if __name__ == '__main__':
    e = playEvens()
    import time; time.sleep(5)
    o = playOdds()
