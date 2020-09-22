from itertools import product

import ConvexHullMaxPairOfPoints as convHull
from Data_and_Dicts import dictOfTonnetz
from FirstNotePosition import TonnetzToString
from TrajectoryClass import TrajectoryClass
""" Import convex Hull Comparison on set of cartesian points """
""" Import function that turn a Tonnetz list to a string """
""" Import dictionary with Tonnetz Base positions """
""" Import trajectory Object class """

INVALID_POS = (104, 104)
""" The value of the invalid Position, feel free to change """


class PlacementError(RuntimeError):
    """Create an Error for Invalid Positioning."""

    def __init__(self, message="Could not place Chord with this strategy"):
        """Init function with ERROR message."""
        self.message = message


def isValidPos(pos):
    """Define a variable for Invalid Positions."""
    return pos != INVALID_POS


def applyFirstSuccessful(strategies):
    """Successively tries to apply different strategies.

    Successively tries to apply different strategies
    stopping at the first successful one.
    Strategies are functions which take no argument (typically lambdas
    wrapping a function with its arguments).
    """
    result = False
    for strategy in strategies:
        try:
            result = strategy()
        # Consume exceptions silently
        except PlacementError:
            pass
        if result:
            return result
    raise PlacementError()


def axesMovementsDict(T_axes, point):
    """A dictionary to compute movement in Tonnetz Space."""
    x, y = point
    # the point represents the poisition of the previous note
    # and T_axes represent the distance.
    movementsDict = {
        0: (x, y),
        T_axes[0]: (x, y + 1),
        T_axes[1]: (x + 1, y),
        T_axes[2]: (x - 1, y - 1),
        12 - T_axes[0]: (x, y - 1),
        12 - T_axes[1]: (x - 1, y),
        12 - T_axes[2]: (x + 1, y + 1)
    }
    return movementsDict


def axesMovementsDictDistancePlus(T_axes, point):
    """A dict to compute movement in Tonnetz for distances bigger than one."""
    x, y = point
    # the point represents the poisition of the previous note
    # and T_axes represent the distance.
    movementsDict = {
        (T_axes[0] * 2) % 12: (x, y + 2),
        ((12 - T_axes[2]) * 2) % 12: (x + 2, y + 2),
        (T_axes[1] - T_axes[0]) % 12: (x + 1, y - 1),
        (12 - T_axes[2]) + T_axes[1]: (x + 2, y + 1),
        (12 - T_axes[2]) + T_axes[1]: (x + 1, y + 2),
    }
    return movementsDict


def intervalToPoint(interval, point, T_axes):
    """Turn an interval to a Point.

    This adapts an interval to a Position in the Cartesian Plane note
    that Intervals who don't belong onto axes values are Invalid Positions.
    """
    movementDict = axesMovementsDict(T_axes, point)
    try:
        point = movementDict[interval]
    # here is the definition of Invalid Positions
    except KeyError:
        # If the point is not in the first dictionary create a second
        # with non connected fixed positions.
        try:
            movementDict2 = axesMovementsDictDistancePlus(T_axes, point)
            point = movementDict2[interval]
        except KeyError:
            point = INVALID_POS
    return point


def checkInvalidPosition(chord, point):
    """Check if a position is not valid."""
    if not isValidPos(point):
        print(chord, point)
        raise ValueError("Bad reference point")


def checkChordValidity(coordDict, chord, axes, Tonnetz):
    """If coordinates weren't found for all notes throw ERROR."""
    if(any(note not in coordDict for note in chord)):
        print(chord, coordDict.items(), axes, Tonnetz)
        raise BaseException("Lost chord")


def ChordConfiguration(chord, axes, Tonnetz):
    """Compute the coordinates of a chord.

    This function takes a chord (PC set) an origin point (usually the
    coordinates for one of the notes of the chord) and the Tonnetz System
    in which the trajectory is being build and returns (x, y) coordinates
    for all the notes of the chord. We take the Cartesian product of the chord
    and we iterate in order to find the coordinates.
    If the iteration exceed the length of the chord throw ERROR.
    """
    coordDict = {chord[0]: axes}
    n = 0
    while(len(chord) > len(coordDict)):
        for noteA, noteB in product(chord, chord):
            if(noteA in coordDict and noteB not in coordDict):
                newPoint = intervalToPoint(
                    (noteB - noteA) % 12, coordDict[noteA], Tonnetz)
                if isValidPos(newPoint):
                    coordDict[noteB] = newPoint
            if(n > len(chord)):
                print(
                    chord,
                    coordDict.items(),
                    axes,
                    n,
                    len(chord),
                    len(coordDict))
                raise RuntimeError("Infinite Loop")
        n += 1
    checkChordValidity(coordDict, chord, axes, Tonnetz)
    return coordDict


def distanceOne(T_axes):
    """Return A list of accepted distances(On Tonnetz axes)."""
    listofDist = [
        T_axes[0],
        T_axes[1],
        T_axes[2],
        (12 - T_axes[0]),
        (12 - T_axes[1]),
        (12 - T_axes[2])]
    return(listofDist)


def distanceInt(interval, T_axes):
    """Return a value that evaluates an interval.

    A single value in [0-2] estimation of note distance
    this is used to chose the origin point
    """
    listofDist = distanceOne(T_axes)
    if interval == 0:
        value = 0
    elif interval in listofDist:
        value = 1
    else:
        value = 2
    return value


def distNoteFromChord(chord, note, Tonnetz):
    """Search for distances mod12."""
    distanceValueList = [
        distanceInt((i - note) % 12, Tonnetz) for i in chord
    ]
    return distanceValueList


def IndexOfCloserNote(chord, note, Tonnetz):
    """Find the Index of the closest Note of a chord."""
    valueList = distNoteFromChord(chord, note, Tonnetz)
    minimumIndex = valueList.index(min(valueList))
    return minimumIndex


def positionFromMin(chord, note, coordDict, Tonnetz):
    """Find the note that fits the description and its coordinates."""
    keyIndex = IndexOfCloserNote(chord, note, Tonnetz)
    noteA = chord[keyIndex]
    number = (note - noteA) % 12
    position = coordDict[noteA]
    newPoint = intervalToPoint(number, position, Tonnetz)
    return newPoint


def chordMatrix(Chord1, Chord2, Tonnetz):
    """Just a chord Matrix."""
    m2 = [([(distanceInt((i - j) % 12, Tonnetz)) for i in Chord1])
          for j in Chord2]
    return m2


def distance_matrix(chord1, chord2, Tonnetz):
    """The distance matrix for every couple of notes between two chords."""
    matrix = chordMatrix(chord1, chord2, Tonnetz)
    # sum of rows
    l1 = [sum([row[i] for row in matrix]) for i in range(len(chord1))]
    # sum of collumns
    l2 = list(map(sum, matrix))
    return l1, l2


def IndexesOfMinimum(chord1, chord2, Tonnetz):
    """Take two chords and find the indexes of the pair with min distance.

    By searching the distance matrix collumn and row sums we find the closest
    pair of notes between two chords (usually distance 0 or 1).
    """
    l1, l2 = distance_matrix(chord1, chord2, Tonnetz)
    min1 = min(l1)
    min2 = min(l2)
    minimumIndex1 = l1.index(min1)
    minimumIndex2 = l2.index(min2)
    distValue = distanceInt(
        (chord1[minimumIndex1] - chord2[minimumIndex2]) %
        12, Tonnetz)
    if distValue >= 1:
        listOfMinIndices1 = [i for i, n in enumerate(l1) if n > min1 - 2]
        listOfMinIndices2 = [i for i, n in enumerate(l2) if n > min2 - 2]
        minCheck = 2
        for i in listOfMinIndices1:
            for j in listOfMinIndices2:
                distVal = distanceInt((chord1[i] - chord2[j]) % 12, Tonnetz)
                if distVal < minCheck:
                    minimumIndex1 = i
                    minimumIndex2 = j
                    minCheck = distVal
    return minimumIndex1, minimumIndex2


def positionOfTheMinNote(chord1, chord2, coordDict1, Tonnetz):
    """Find the actual position of the pair of closest notes."""
    index1, index2 = IndexesOfMinimum(chord1, chord2, Tonnetz)
    noteA = chord1[index1]
    noteB = chord2[index2]
    chord2[0], chord2[index2] = chord2[index2], chord2[0]
    interval = (noteB - noteA) % 12
    position = coordDict1[noteA]
    newPoint = intervalToPoint(interval, position, Tonnetz)
    return newPoint, position


def concat3DictValues(Dict1, Dict2, Dict3):
    """Concat the positions of three consecutive chords."""
    l1 = list(Dict1.values())
    l2 = list(Dict2.values())
    l3 = list(Dict3.values())
    lconcat = l1 + l2 + l3
    return lconcat


def maximumDistanceOfConvexHull(graph1):
    """Compute maximum diameter of a Convex Hull.

    From a set of (x, y) points find the most distant and
    compute their cartesian distance.
    """
    point1, point2 = convHull.diameter(graph1)
    sumofsquares = (point1[0] - point2[0]) ^ 2 + (point1[1] - point2[1]) ^ 2
    maxdistance = format(sumofsquares**(0.5), '.2f')
    return maxdistance


def computeChordCoord(thisChord, someChordCoord, Tonnetz):
    """Compute a chord's coordinates in a dictionary format.

    Compute a chord's coordinates in a dictionary format with :
    -  keys : the name of the PC-notes
    -  values : (x, y) coordinates
    """
    origin, otherRefOrigin = positionOfTheMinNote(
        list(someChordCoord.keys()), thisChord, someChordCoord, Tonnetz)
    if not isValidPos(origin):
        raise PlacementError()
    thisChordCoord = ChordConfiguration(thisChord, origin, Tonnetz)
    edge = [(origin, otherRefOrigin)]
    return thisChordCoord, edge


def TrajectoryConvexHullComparison(
        placement1,
        placement2,
        lastChordCoord,
        secondLastChordCoord):
    """Convex Hull Comparison of two different chord sequences.

    From two different chordCoordinates choose the most compact
    That is done by choosing the minimum greatest convexHull diameter.
    """
    concatPoints1 = concat3DictValues(
        placement1[0],
        lastChordCoord,
        secondLastChordCoord)
    concatPoints2 = concat3DictValues(
        placement2[0],
        lastChordCoord,
        secondLastChordCoord)
    graph1 = list(set(concatPoints1))
    graph2 = list(set(concatPoints2))
    distance1 = maximumDistanceOfConvexHull(graph1)
    distance2 = maximumDistanceOfConvexHull(graph2)
    if distance1 > distance2:
        return placement2
    else:
        return placement1


def TrajectoryCheckSecond(placement1, trajectory):
    """Check if a second chord configuration based in future is valid."""
    try:
        secondLastChordCoord = trajectory.getLastPosition(2)
        lastChordCoord = trajectory.getLastPosition()
        nextChord = trajectory.getNextChord()
        placement2 = placeChordWithVirtualRef(
            trajectory.getThisChord(),
            lastChordCoord,
            nextChord,
            trajectory.Tonnetz)
        return TrajectoryConvexHullComparison(
            placement1, placement2, lastChordCoord, secondLastChordCoord)
    except PlacementError:
        return placement1


def TrajectoryLookConnected(trajectory):
    """A test to check conditions."""
    thisChord = trajectory.getThisChord()
    thisChordPoints1, edge1 = computeChordCoord(
        thisChord, trajectory.getLastPosition(), trajectory.Tonnetz)
    if edge1[0][1] != edge1[0][0]:
        try:
            thisChordPoints2, edge2 = computeChordCoord(
                thisChord, trajectory.getLastPosition(2), trajectory.Tonnetz)
            if edge2[0][1] == edge2[0][0]:
                return TrajectoryCheckSecond(
                    (thisChordPoints2, edge2), trajectory)
        except PlacementError:
            pass
    return TrajectoryCheckSecond((thisChordPoints1, edge1), trajectory)


def TrajectoryCheckPosition(trajectory):
    """Apply tactics on trajectory calculations."""
    return applyFirstSuccessful([
        lambda: TrajectoryLookConnected(trajectory),
        lambda: computeChordCoord(
                trajectory.getThisChord(),
                trajectory.getLastPosition(2),
                trajectory.Tonnetz),
        *(
            lambda: placeChordWithVirtualRef(
                    trajectory.getThisChord(),
                    trajectory.getLastPosition(),
                    trajectory.getNextChord(lookahead),
                    trajectory.Tonnetz)
            for lookahead in range(1, min(5, trajectory.chordsRemaining()))
        )
    ])


def TrajectoryWithFuture(trajectory):
    """Start Normal Calculations."""
    if trajectory.index > 1 and trajectory.chordsRemaining() > 1:
        return TrajectoryCheckPosition(trajectory)
    elif trajectory.index == 0:
        raise PlacementError("Strategy not valid for this position")
    else:
        return computeChordCoord(
            trajectory.getThisChord(),
            trajectory.getLastPosition(),
            trajectory.Tonnetz)


def placeChordWithVirtualRef(thisPCS, placedChordCoord, tempPCS, Tonnetz):
    """Find a chords coordinates based on a reference chord."""
    virtualChordCoord, _ = computeChordCoord(
        tempPCS, placedChordCoord, Tonnetz)
    return computeChordCoord(thisPCS, virtualChordCoord, Tonnetz)


def NewTrajectory(listOfChords, Tonnetz, origin=(0, 0)):
    """The Call function for trajectory with future Calculations."""
    trajectory = TrajectoryClass(
        ChordConfiguration(
            listOfChords[0],
            origin,
            Tonnetz),
        listOfChords,
        Tonnetz)
    for index, chord in enumerate(listOfChords):
        if index == 0:
            continue
        elif index == 1:
            thisChordCoord, connectingEdge = applyFirstSuccessful([
                lambda: computeChordCoord(
                    trajectory.getThisChord(),
                    trajectory.getLastPosition(),
                    trajectory.Tonnetz),
                lambda: placeChordWithVirtualRef(
                    trajectory.getThisChord(),
                    trajectory.getLastPosition(),
                    trajectory.getNextChord(),
                    trajectory.Tonnetz)
            ])
        else:
            thisChordCoord, connectingEdge = TrajectoryWithFuture(trajectory)
        trajectory.addChord(thisChordCoord, connectingEdge)
    return trajectory

# ----------------------------------------------OTHER TRAJECTORY----------


def trajectoryRecursive(trajectory):
    """A simpler definition of trajectory."""
    alpha = 1
    while trajectory.index - alpha >= 0:
        try:
            return computeChordCoord(
                trajectory.getThisChord(),
                trajectory.getLastPosition(alpha),
                trajectory.Tonnetz)
        except PlacementError:
            pass
        alpha += 1
    raise PlacementError()


def TrajectoryLookBefore(listOfChords, Tonnetz, origin=(0, 0)):
    """The call for recursive trajectory."""
    trajectory = TrajectoryClass(
        ChordConfiguration(
            listOfChords[0],
            origin,
            Tonnetz),
        listOfChords,
        Tonnetz)
    for index, chord in enumerate(listOfChords):
        if index == 0:
            continue
        elif index == 1:
            thisChordCoord, connectingEdge = applyFirstSuccessful([
                lambda: computeChordCoord(trajectory.getThisChord(),
                                          trajectory.getLastPosition(),
                                          trajectory.Tonnetz),
                lambda: placeChordWithVirtualRef(trajectory.getThisChord(),
                                                 trajectory.getLastPosition(),
                                                 trajectory.getNextChord(),
                                                 trajectory.Tonnetz)
            ])
        else:
            thisChordCoord, connectingEdge = trajectoryRecursive(trajectory)
        trajectory.addChord(thisChordCoord, connectingEdge)
    return trajectory

# ------------------------TRAJECTORY NO FUTURE------------------------------


"""Here we build a version of the trajectory which is recursive and doesn't
fail. We do this by taking the definition of the recursive trajectory and add
a tactic that searches base positions for notes and adds them
to the current coordinates
"""


def getDictFromTonnetz(Tonnetz):
    """Get base positions on Tonnetz grid."""
    notePoints = dictOfTonnetz[TonnetzToString(Tonnetz)]
    return notePoints


def lastResort(trajectory):
    """The last Resort Tactic that possibly never fails."""
    baseNoteDict = getDictFromTonnetz(trajectory.Tonnetz)
    thisChordRandomNote = trajectory.getThisChord()[0]
    lastChordRandomNote = trajectory.listOfChords[trajectory.index - 1][0]
    lastChordCoord = trajectory.getLastPosition()
    x1, y1 = baseNoteDict[lastChordRandomNote]
    x2, y2 = baseNoteDict[thisChordRandomNote]
    relation = (x2 - x1, y2 - y1)
    thisChordNoteCoord = (lastChordCoord[lastChordRandomNote][0] + relation[0],
                          lastChordCoord[lastChordRandomNote][1] + relation[1]
                          )
    coordinates = ChordConfiguration(
        trajectory.getThisChord(), thisChordNoteCoord, trajectory.Tonnetz)
    return coordinates, []


def TrajectoryNoFuture(listOfChords, Tonnetz, origin=(0, 0)):
    """The Call Function of this version of the trajectory."""
    trajectory = TrajectoryClass(
        ChordConfiguration(
            listOfChords[0],
            origin,
            Tonnetz),
        listOfChords,
        Tonnetz)
    for index, chord in enumerate(listOfChords):
        if index == 0:
            continue
        else:
            thisChordCoord, connectingEdge = applyFirstSuccessful([
                lambda: trajectoryRecursive(trajectory),
                lambda: lastResort(trajectory)
            ])
        trajectory.addChord(thisChordCoord, connectingEdge)
    return trajectory


# ------------------------TRAJECTORY EDGES----------------------------------


def TrajectoryNoteEdges(trajectory):
    """Compute the edges of every chord in the trajectory."""
    TotalEdges = []
    dist = [-1, 0, 1]
    for dicts in trajectory.chordPositions:
        chordEdges = []
        cartl = list(product(dicts.values(), dicts.values()))
        for couple in cartl:
            (x1, y1), (x2, y2) = couple
            if (x1 - x2) in dist and (y1 - y2) in dist:
                if not (((x1 - x2) == 1 and (y1 - y2) == -1) or
                        ((x1 - x2) == -1 and (y1 - y2) == 1)):
                    chordEdges.append(couple)
        TotalEdges.append(chordEdges)
    return TotalEdges


def SetOfPoints(trajectory):
    """Remove duplicate points."""
    AllPoints = []
    for dicts in trajectory.chordPositions:
        AllPoints = AllPoints + list(dicts.values())
    PointSet = list(set(AllPoints))
    return PointSet, AllPoints


def weightsOfTrajPoints(setOfPoints, multiSetOfPoints):
    """Calculate the multiplicity of Points and normalize."""
    dictOfPointWeight = dict()
    for point in setOfPoints:
        dictOfPointWeight[point] = multiSetOfPoints.count(point)
    # Ideas about Using Normalized weights :
    # Maximum = max(list(dictOfPointWeight.values()))
    # Minimum = min(list(dictOfPointWeight.values()))
    return dictOfPointWeight
