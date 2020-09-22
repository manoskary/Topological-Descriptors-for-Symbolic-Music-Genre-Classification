from Tonnetz_Select import fromMidiToPCS, analysisFromCorpus
from structural_functions import testInput, getKeyByValue
from Data_and_Dicts import dictOfTonnetze
import numpy as np
from scipy.ndimage.measurements import label
from TrajectoryCalculationsWithClass import NewTrajectory

def createList(r1, r2):
    """Create a list from a range."""
    return list(range(r1, r2 + 1))

def addCouples(v, u):
    x, y = v
    z, r = u 
    return x+z, y+r

def squarematrixcreate(maxWidth, minWidth, maxHeight, minHeight, points):
    """Create a square matrix of zeros."""
    width = maxWidth - minWidth + 1 
    height = maxHeight - minHeight + 1
    matrix = np.zeros((width, height))
    nlist = list(map(lambda x: addCouples(x, (abs(minWidth), abs(minHeight))), points))
    for el in nlist:
        x, y = el
        matrix[x, y] = 1
    return matrix

def ccl(matrix):
    structure = np.array([[1, 1, 0], [1, 1, 1], [0, 1, 1]])
    labeled, ncomponents = label(matrix, structure)
    return ncomponents


def dimensionsOfTrajectory(TrajectoryPoints):
    totalPoints = []
    for dicts in TrajectoryPoints:
        totalPoints = totalPoints + list(dicts.values())
    totalPoints = list(set(totalPoints))
    x, y = zip(*totalPoints)
    maxW = max(x)
    minW = min(x)
    maxH = max(y)
    minH = min(y)
    numberOfComponents = ccl(squarematrixcreate(maxW, minW, maxH, minH, totalPoints))
    width = maxW - minW
    height = maxH - minH
    return numberOfComponents, width*height

def addConnectivity(TonnetzList, connectivity):
    for el in TonnetzList:
        el[3] = connectivity[getKeyByValue(dictOfTonnetze, el[0])]
    return TonnetzList





def applyingCoefficients(maxChords, maxComponents, maxDimensions, TonnetzDetails):
    coef1 = 1 - TonnetzDetails[3]/maxChords
    coef2 = TonnetzDetails[1]/maxComponents
    coef3 = TonnetzDetails[2]/maxDimensions
    coefGen = (coef1*2 + coef2 + coef3)/4
    return coefGen

def finalCompliance(TonnetzList):
    Tonnetze, components, dimensions, chords = zip(*TonnetzList)
    maxChords = max(chords)
    maxComponents = max(components)
    maxDimensions = max(dimensions)
    newlist = []
    for el in TonnetzList:
        coefGen = applyingCoefficients(maxChords, maxComponents, maxDimensions, el)
        newlist.append((el[0], coefGen))
    sortedList = sorted(newlist, key = lambda x: x[1]) 
    return sortedList[0][0], sortedList[1][0]


def complianceFunction(midiFile, type):
	if type == "Corpus":
		chordListConnectNoDoubles, Tonnetz, connectivity = analysisFromCorpus(midiFile)
	else:
		chordListConnectNoDoubles, Tonnetz, connectivity = fromMidiToPCS(midiFile)
	trajectory345 = NewTrajectory(chordListConnectNoDoubles, [3,4,5])
	trajectory147 = NewTrajectory(chordListConnectNoDoubles, [1,4,7])
	trajectory138 = NewTrajectory(chordListConnectNoDoubles, [1,3,8])
	trajectory237 = NewTrajectory(chordListConnectNoDoubles, [2,3,7])
	trajectory129 = NewTrajectory(chordListConnectNoDoubles, [1,2,9])

	D345 = dimensionsOfTrajectory(trajectory345.chordPositions)
	D147 = dimensionsOfTrajectory(trajectory147.chordPositions)
	D237 = dimensionsOfTrajectory(trajectory237.chordPositions)
	D129 = dimensionsOfTrajectory(trajectory129.chordPositions)
	D138 = dimensionsOfTrajectory(trajectory138.chordPositions)

	D345 = [sorted(trajectory345.Tonnetz), D345[0], D345[1], 0]
	D147 = [sorted(trajectory147.Tonnetz), D147[0], D147[1], 0]
	D237 = [sorted(trajectory237.Tonnetz), D237[0], D237[1], 0]
	D129 = [sorted(trajectory129.Tonnetz), D129[0], D129[1], 0]
	D138 = [sorted(trajectory138.Tonnetz), D138[0], D138[1], 0]

	TonnetzList = [D345, D147, D237, D129, D138]
	TonnetzList = addConnectivity(TonnetzList, connectivity)

	return chordListConnectNoDoubles, finalCompliance(TonnetzList)
