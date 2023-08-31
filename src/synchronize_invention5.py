from copy import deepcopy

import music21
import numpy
from music21 import *


import plot
import lorenz
import rungekutta
import music_utils
#import pandas as pd

''' 
# Testing Synchronization
a = 10.0
r = 28.0
b = 8 / 3.0
x0 = numpy.array([1, 1, 1, 1, 1], dtype=numpy.float64)

master_slave = lorenz.coupled_lorenz(a,r,b)
ts,xs = rungekutta.rk4(master_slave, 0.0, x0, 0.01, 1000)
print(xs.shape)


ys1 = xs[1]
print(max(ys1), min(ys1))
ys2 = xs[3]
print(max(ys1), min(ys1))
'''

name = "pirates"

piece = converter.parse('Fugues/pirates.mid')
#piece.show('midi')
piece.write('midi', 'fugue_' + name + '.mid')


a = piece.parts[0]
b = piece.parts[1]
on1 = music_utils.getNotesStream(a,music21.instrument.Piano())
#s1.append(music21.instrument.Soprano())
on2 = music_utils.getNotesStream(b, music21.instrument.Piano())
#s2.append(music21.instrument.Soprano())

score = stream.Score()
score.insert(0,on1)
score.insert(0,on2)
score.write('midi', 'sync_' + name + '_ref.mid')
#fugue.show('midi')


refPitches1 = music_utils.convertmusictopitches(a)
refPitches2 = music_utils.convertmusictopitches(b)

N = 60
reftraj = music_utils.getRefCordinatesOfAttractor(music_utils.AttractorType.COUPLED_LORENZ, [-13 ,-12, 52, 1, 1])
y1ref = reftraj[1]
y2ref = reftraj[3]

for i in range(N):
    print(i, y1ref[i], y2ref[i])


si, sx = music_utils.sortedX(y1ref[0:N])
si2, sx2 = music_utils.sortedX(y2ref[0:N])

y1dash = reftraj[1][0:N]
y2dash = reftraj[3][0:N]
#print(pitches)
sp1 = []
sp2 = []

for c in range(N):
    index = music_utils.findMappingIndex(sx, y1dash[c])
    sp1.append(deepcopy(refPitches1[si[index]]))
    index = music_utils.findMappingIndex(sx2, y2dash[c])
    sp2.append(deepcopy(refPitches2[si2[index]]))
for i in range(N):
    print(y1dash[i], y2dash[i])
for i in range(N):
    print(sp1[i], sp2[i])
s1 = music_utils.getNotesStream(sp1, music21.instrument.Piano())
#s1.append(music21.instrument.Soprano())
s2 = music_utils.getNotesStream(sp2, music21.instrument.Piano())
#s2.append(music21.instrument.Soprano())

score = stream.Score()
score.insert(0,s1)
score.insert(0,s2)

#score.show('midi')
score.write('midi', 'sync_' + name + '_synchronized.mid')



# Perturbation
perturbPoint = reftraj[:,N-1]
newPoint = numpy.sum([perturbPoint,[0,0,0,1,-1]], axis = 0)
asp1 = []
asp2 = []

N2 = 100
xd = music_utils.getNewCordinatesOfAttractor(music_utils.AttractorType.COUPLED_LORENZ, newPoint)

xdash = music_utils.getFirstNPoints(xd,N2)
for c in range(40):
    print(c, xdash[c][1], xdash[c][3], xdash[c][2], xdash[c][4])
#
# si, sx = music_utils.sortedX(y1ref)
# si2, sx2 = music_utils.sortedX(y2ref)

for c in range(N2):
    index = music_utils.findMappingIndex(sx, xdash[c][1])
    asp1.append(deepcopy(refPitches1[si[index]]))
    index = music_utils.findMappingIndex(sx2, xdash[c][3])
    asp2.append(deepcopy(refPitches2[si2[index]]))
for i in range(N2):
    print(xdash[i][1], xdash[i][3])
for i in range(N2):
    print(asp1[i], asp2[i])
as1 = music_utils.getNotesStream(asp1,music21.instrument.Piano())
#s1.append(music21.instrument.Soprano())
as2 = music_utils.getNotesStream(asp2, music21.instrument.Piano())
#s2.append(music21.instrument.Soprano())

score = stream.Score()
score.insert(0,as1)
score.insert(0,as2)

#score.show('midi')
score.write('midi', 'sync_' + name + '_Async.mid')

assp1 = deepcopy(sp1)
assp2 = deepcopy(sp2)

assp1.append(asp1)
assp2.append(asp2)

as1 = music_utils.getNotesStream(assp1,music21.instrument.Piano())
#s1.append(music21.instrument.Soprano())
as2 = music_utils.getNotesStream(assp2, music21.instrument.Piano())
#s2.append(music21.instrument.Soprano())


score = stream.Score()
score.insert(0,as1)
score.insert(0,as2)

#score.show('midi')
score.write('midi', 'sync+async_' + name + '.mid')










# newPitches = []
# xdash = ys1[0::6]
# si, sx = music_utils.sortedX(yref)
# for c in xdash:
#     index = music_utils.findMappingIndex(sx, c)
#     newPitches.append(deepcopy(pitches[si[index]]))
# music_utils.playNotesList(newPitches, "syncTest1")
# playNotesList(newPitches)











