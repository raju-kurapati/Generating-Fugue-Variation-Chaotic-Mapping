from enum import Enum

import numpy
import numpy as np
from music21 import *
from scipy.integrate import solve_ivp
from copy import deepcopy
import lorenz
import rungekutta


class AttractorType(Enum):
    """Shepherd model choices"""

    LORENZ = '"lorrenz"'
    ROSSLER = '"pierson"'
    COUPLED_LORENZ = '"coupled_lorrenz"'


def convertmusictopitches(piece):
    pitches = []
    for element in piece.flat:
        if isinstance(element, note.Note):
            pitches.append(element)
    return pitches


def getRefCordinatesOfAttractor(attractorType: AttractorType, initialCondition):
    if attractorType == AttractorType.LORENZ:
        a = 16.0
        r = 45.0
        b = 4
        x0 = numpy.array(initialCondition, dtype=numpy.float64)
        lfunc = lorenz.lorenz(a, r, b)
        ts, xs = rungekutta.ark4(lfunc, 0.0, x0, 20, 0.01)
        return xs
    elif attractorType == AttractorType.COUPLED_LORENZ:
        a = 16.0
        r = 45.0
        b = 4
        x0 = numpy.array(initialCondition, dtype=numpy.float64)
        lfunc = lorenz.coupled_lorenz(a, r, b)
        ts, xs = rungekutta.ark4(lfunc, 0.0, x0, 20, 0.01)
        return xs


def getX_refCordinatesOfAttractor(attractorType: AttractorType, initialCondition, numPoints):
    if attractorType == AttractorType.LORENZ:
        xs = getRefCordinatesOfAttractor(AttractorType.LORENZ,initialCondition)
        res = xs[0][0:numPoints]
        print("Ref Traj: ", res)
        return res
        # solution = solve_ivp(lorenz1, (0, 20), x0 , args=(a, b, r))
        # print(solution.y[0])

def getY_refCordinatesOfAttractor(attractorType: AttractorType, initialCondition, numPoints):
    if attractorType == AttractorType.LORENZ:
        xs = getRefCordinatesOfAttractor(AttractorType.LORENZ,initialCondition)
        res = xs[1][0:numPoints]
        print("Ref Traj: ", res)
        return res
    elif attractorType == AttractorType.COUPLED_LORENZ:
        xs = getRefCordinatesOfAttractor(AttractorType.COUPLED_LORENZ,initialCondition)
        res = xs[1][0:numPoints]
        print("Ref Traj: ", res)
        return res

def getNewCordinatesOfAttractor(attractorType: AttractorType, initialCondition):
    if attractorType == AttractorType.LORENZ:
        a = 10.0
        r = 28.0
        b = 8 / 3.0
        x0 = numpy.array(initialCondition, dtype=numpy.float64)
        lfunc = lorenz.lorenz(a, r, b)
        ts, xxs = rungekutta.ark4(lfunc, 0.0, x0, 20, 0.01)
        xs = xxs.transpose()
        #res = xs[0:numPoints]
        #print("New Traj: ", res)
        return xs
    if attractorType == AttractorType.COUPLED_LORENZ:
        a = 10.0
        r = 28.0
        b = 8 / 3.0
        x0 = numpy.array(initialCondition, dtype=numpy.float64)
        lfunc = lorenz.coupled_lorenz(a, r, b)
        ts, xxs = rungekutta.ark4(lfunc, 0.0, x0, 20, 0.01)
        xs = xxs.transpose()
        #res = xs[:][0:numPoints]
        #print("New Traj: ", res)
        return xs

def getFirstNPoints(x, numPoints):
    return x[0:numPoints]


def sortedX(x):
    sorted_indices = np.argsort(x)
    x_sorted = x[sorted_indices]
    print("Sorted Index", sorted_indices)
    print("Sorted X", x_sorted)
    return sorted_indices, x_sorted


def findMappingIndex(A, c):
    index = numpy.searchsorted(A, c)
    if index == len(A):
        return len(A) - 1  # if c is greater than all elements in A, return -1
    elif A[index] == c:
        return index
    else:
        return index


def getNewPitches(x, pitches):
    newPitches = []
    xdash = getNewCordinatesOfAttractor(AttractorType.LORENZ, 100)
    si, sx = sortedX(x)
    for c in xdash:
        index = findMappingIndex(sx, c)
        newPitches.append(deepcopy(pitches[si[index]]))
    return newPitches


def getNotesStream(pitches, instrumentToBePlayed = None):
    s = stream.Stream()
    if instrumentToBePlayed:
        s.append(instrumentToBePlayed)
    for note in pitches:
         s.append(note)
    return s

def getNotesStreamWNI(pitches):
    s = stream.Stream()
    for note in pitches:
        s.append(note)
    return s




# piece = corpus.parse('bach/bwv108.6.xml')
# piece.show('midi')
# piece.write('midi', 'ref1.mid')
# pitches = convertmusictopitches(piece)
# x = getX_refCordinatesOfAttractor(AttractorType.LORENZ, 20)
# print(pitches)
# newPitches = getNewPitches(x, pitches)
# playNotesList(newPitches)

# bach = corpus.parse('bach/bwv244.10')
# soprano = bach.parts[0]
# pitches = convertmusictopitches(soprano)
# playNotesList(pitches)
#soprano.show('midi')


