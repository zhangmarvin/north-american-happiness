from util import *
from dragonsmash import *

def tdfw(c):
    c.addLoopedNote(Note(note_to_num['E6'], 13, 8, 127), 0, 64)
    c.addLoopedNote(Note(note_to_num['E6'], 13, 4, 127), 8, 64)
    c.addLoopedNote(Note(note_to_num['C6'], 13, 8, 127), 12, 64)
    c.addLoopedNote(Note(note_to_num['B5'], 13, 12, 127), 24, 64)
    c.addLoopedNote(Note(note_to_num['B5'], 13, 4, 127), 40, 64)
    c.addLoopedNote(Note(note_to_num['C6'], 13, 8, 127), 44, 64)
    c.addLoopedNote(Note(note_to_num['E5'], 13, 8, 127), 56, 64)

s = Speaker(16, 64)
tdfw(s.newConnection())
s.playAll()
