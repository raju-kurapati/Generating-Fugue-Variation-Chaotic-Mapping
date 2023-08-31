from copy import deepcopy

import music21
import numpy
from music21 import *


import plot
import lorenz
import rungekutta
import music_utils
#import pandas as pd


name = "bach-invention-12"

piece = converter.parse('Fugues/IMSLP220156-WIMA.02f4-i2v12.mid')
#piece.show('midi')
piece.write('midi', 'fugue_' + name + '.mid')


a = piece.parts[0]
b = piece.parts[1]
on1 = music_utils.getNotesStream(a, music21.instrument.Piano())
on1.write('midi', name + '_a.mid')

on2 = music_utils.getNotesStream(b, music21.instrument.Piano())
on2.write('midi', name + '_b.mid')

score = stream.Score()
score.insert(0,on1)
score.insert(0,on2)
score.write('midi', name + '_ref.mid')
#fugue.show('midi')


refPitches1 = music_utils.convertmusictopitches(a)[20:]
refPitches2 = music_utils.convertmusictopitches(b)[20:]

N = 80
reftraj = music_utils.getRefCordinatesOfAttractor(music_utils.AttractorType.COUPLED_LORENZ, [-13 ,-12, 52, 1, 1])
reftraj = numpy.around(reftraj, 7)
y1ref = reftraj[1]
y2ref = reftraj[3]

for i in range(N):
    print(i, y1ref[i], y2ref[i])


si, sx = music_utils.sortedX(y1ref[0:N])
si2, sx2 = music_utils.sortedX(y2ref[0:N])

reftraj1 = music_utils.getRefCordinatesOfAttractor(music_utils.AttractorType.COUPLED_LORENZ, [-13.5 ,-12.5, 50, 1.3, 1.3])
reftraj1 = numpy.around(reftraj1, 7)
y1dash = reftraj1[1][0:N]
y2dash = reftraj1[3][0:N]
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
s1 = music_utils.getNotesStream(sp1)
#s1.append(music21.instrument.Soprano())
s2 = music_utils.getNotesStream(sp2)
#s2.append(music21.instrument.Soprano())

score = stream.Score()
score.insert(0,s1)
score.insert(0,s2)

#score.show('midi')
score.write('midi', name + '_sync.mid')



# Perturbation
perturbPoint = reftraj[:,N-1]
print("Perturbation Point : ", perturbPoint)
#[1 ,1, 1, -1, -1]
newPoint = numpy.sum([perturbPoint,[-1,0, 0 , +3, -50]], axis = 0)
print(newPoint)
asp1 = []
asp2 = []

N2 = 40
xd = music_utils.getNewCordinatesOfAttractor(music_utils.AttractorType.COUPLED_LORENZ, newPoint)
xd = numpy.around(xd,7)

xdash = music_utils.getFirstNPoints(xd,N2)
for c in range(N2):
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
as1 = music_utils.getNotesStream(asp1)
#s1.append(music21.instrument.Violin())
as2 = music_utils.getNotesStream(asp2)
#s2.append(music21.instrument.Violin())

score = stream.Score()
score.insert(0,as1)
score.insert(0,as2)

#score.show('midi')
score.write('midi', name + '_Async.mid')

assp1 = deepcopy(sp1)
assp2 = deepcopy(sp2)

assp1.append(asp1)
assp2.append(asp2)

as1 = music_utils.getNotesStream(assp1)
#s1.append(music21.instrument.Soprano())
as2 = music_utils.getNotesStream(assp2)
#s2.append(music21.instrument.Soprano())


score = stream.Score()
score.insert(0,as1)
score.insert(0,as2)

#score.show('midi')
score.write('midi',  name + '_sync_async.mid')


# Perturbation 2
perturbPoint = reftraj[:,N-1]
print("Perturbation Point : ", perturbPoint)
newPoint = numpy.array([13 ,-12, 52, 1, 1])
aasp1 = []
aasp2 = []

#N2 = 100
xd = music_utils.getNewCordinatesOfAttractor(music_utils.AttractorType.COUPLED_LORENZ, newPoint)
xd = numpy.around(xd,7)

xdash = music_utils.getFirstNPoints(xd,N)
for c in range(30):
    print(c, xdash[c][1], xdash[c][3], xdash[c][2], xdash[c][4])
#
# si, sx = music_utils.sortedX(y1ref)
# si2, sx2 = music_utils.sortedX(y2ref)

for c in range(N):
    index = music_utils.findMappingIndex(sx, xdash[c][1])
    aasp1.append(deepcopy(refPitches1[si[index]]))
    index = music_utils.findMappingIndex(sx2, xdash[c][3])
    aasp2.append(deepcopy(refPitches2[si2[index]]))
for i in range(N):
    print(xdash[i][1], xdash[i][3])
# for i in range(N):
#     print(asp1[i], asp2[i])
as1 = music_utils.getNotesStream(aasp1)
#s1.append(music21.instrument.Violin())
as2 = music_utils.getNotesStream(aasp2)
#s2.append(music21.instrument.Violin())

score = stream.Score()
score.insert(0,as1)
score.insert(0,as2)

#score.show('midi')
score.write('midi', 'sync_' + name + '_Async.mid')

assap1 = deepcopy(assp1)
assap2 = deepcopy(assp2)

assp1.append(aasp1)
assp2.append(aasp2)

as1 = music_utils.getNotesStream(assp1, instrumentToBePlayed= music21.instrument.Harpsichord())
#s1.append(music21.instrument.Soprano())
as2 = music_utils.getNotesStream(assp2, instrumentToBePlayed = music21.instrument.Harpsichord())
#s2.append(music21.instrument.Soprano())


score = stream.Score()
score1 = stream.Score()
score2 = stream.Score()
score.insert(0,as1)
score.write('midi', name + 'sync_async_sync_1.mid')
score.insert(0,as2)

score1.insert(0,as1)
score2.insert(0,as2)

score1.write('midi', name + 'sync_async_sync_1.mid')
score2.write('midi', name + 'sync_async_sync_2.mid')
#score.show('midi')
score.write('midi', name + 'sync_async_sync_.mid')








# newPitches = []
# xdash = ys1[0::6]
# si, sx = music_utils.sortedX(yref)
# for c in xdash:
#     index = music_utils.findMappingIndex(sx, c)
#     newPitches.append(deepcopy(pitches[si[index]]))
# music_utils.playNotesList(newPitches, "syncTest1")
# playNotesList(newPitches)











