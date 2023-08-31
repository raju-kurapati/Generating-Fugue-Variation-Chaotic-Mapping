import numpy as np
from music21.stream import Score, Part, Opus
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from music21 import *


piece = corpus.parse('bach/bwv108.6.xml')

print(piece)
piece.show('midi')

piece.notes

littleMelody = converter.parse("tinynotation: 3/4 c4 d8 f g16 a g f#")

#littleMelody.show('midi')

print(dir(note))



