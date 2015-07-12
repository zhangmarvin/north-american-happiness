from ds import *
from ds.instruments import Marimba, Piano, Trumpet

def tdfw_mel(player, volume=127):
    melody = [
        Marimba('E6', 0.5,  volume, 0),
        Marimba('E6', 0.25, volume, 0.5),
        Marimba('C6', 0.5,  volume, 0.75),
        Marimba('B5', 0.75, volume, 1.5),
        Marimba('B5', 0.25, volume, 2.5),
        Marimba('C6', 0.5,  volume, 2.75),
        Marimba('E5', 0.5,  volume, 3.5),
    ]
    notes = []
    for note in melody:
        notes.append(player.loop(note, 4))
    return notes

def tdfw_bass(player, volume=127):
    bassline = [
        Piano('E2', 1, volume, 0),
        Piano('E2', 2, volume, 1.5)
    ]
    notes = []
    for note in bassline:
        notes.append(player.loop(note, 4))
    return notes

def tdfw_alt(player, volume=127):
    alt_mel = [
        Trumpet('E4', 0.5, volume, 0),
        Trumpet('E4', 0.5, volume, 0.75),
        Trumpet('F4', 0.25, volume, 1.5),
        Trumpet('E4', 0.25, volume, 2),
        Trumpet('E4', 0.25, volume, 2.5),
        Trumpet('E4', 0.25, volume, 3),
        Trumpet('F4', 0.25, volume, 3.5),
    ]
    notes = []
    for note in alt_mel:
        notes.append(player.loop(note, 4))
    return notes

if __name__ == '__main__':
    player = connect()
