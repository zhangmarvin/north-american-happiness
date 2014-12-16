from client import *

def tdfw(volume=127):
    notes = [
        Note('E6', 13, 0.5,  volume, 0),
        Note('E6', 13, 0.25, volume, 0.5),
        Note('C6', 13, 0.5,  volume, 0.75),
        Note('B5', 13, 0.75, volume, 1.5),
        Note('B5', 13, 0.25, volume, 2.5),
        Note('C6', 13, 0.5,  volume, 2.75),
        Note('E5', 13, 0.5,  volume, 3.5),
    ]

    for note in notes:
        player.loop(note, 4)

if __name__ == '__main__':
    tdfw(volume=32)
