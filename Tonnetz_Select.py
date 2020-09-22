"""Calculations to automatically select Tonnetz.

This is a script to provide all functions in order to automatically select
Tonnetz System and modify chords.
"""
import ast
from itertools import product

from Data_and_Dicts import dictOfTonnetze
import music21 as ms

def parseMIDI(midifile):
	"""Take a MIDI file and return the list Of Chords.

	The file is first parsed, midi or xml. Then with chordify and
	PC-Set we compute a list of PC-chords.
	"""
	mfile = ms.converter.parse(midifile)
	mChords = mfile.chordify()
	chordList = []
	for c in mChords.recurse().getElementsByClass('Chord'):
		chordList.append(c.orderedPitchClasses)    
	return chordList


def parsedFile(file):
	"""Take a parsed file and return the list Of Chords and Interval Vectors.

	The file was already parsed possibly from corpus. Then with chordify and
	PC-Set we compute a list of PC-chords and Interval Vectors.
	"""
	mChords = file.chordify()
	chordList = []
	chordVectors = []
	for c in mChords.recurse().getElementsByClass('Chord'):
		chordList.append(c.orderedPitchClasses)
		chordVectors.append(c.intervalVector)
	# print('The number of chords found is : ',  len(chordList))
	return chordList, chordVectors


def parseMidi(midifile):
	"""Take a MIDI file and return the list Of Chords and Interval Vectors.

	The file is first parsed, midi or xml. Then with chordify and
	PC-Set we compute a list of PC-chords and Interval Vectors.
	"""
	mfile = ms.converter.parse(midifile)
	mChords = mfile.chordify()
	chordList = []
	chordVectors = []
	for c in mChords.recurse().getElementsByClass('Chord'):
		chordList.append(c.orderedPitchClasses)
		chordVectors.append(c.intervalVector)
	# print('The number of chords found is : ',  len(chordList))
	return chordList, chordVectors


def Connected(l1, x, y, z):
	"""The predicate that tests the representability chord based on IntVec.

	This is the decision predicate that chooses the appropriate Tonnetz for a
	piece. It matches the Tonnetz axes on every interval vector and checks
	how many chord are representable in every system.
	"""
	j = 0
	for i in l1:
		if (
		   sum(i) - 2 * (i[x] + i[y] + i[z]) < 0
		   ):
			j += 1
	return j


def TonnetzConnectivity(chordVectors):
	"""Taking the max of all representable chords."""
	TonnetzConnectivity = {
		'T129': Connected(chordVectors, 0, 1, 2),
		'T138': Connected(chordVectors, 0, 2, 3),
		'T147': Connected(chordVectors, 0, 3, 4),
		'T156': Connected(chordVectors, 0, 4, 5),
		'T237': Connected(chordVectors, 1, 2, 4),
		# 'T246' : Connected(chordVectors, 1, 3 ,5),
		'T345': Connected(chordVectors, 2, 3, 4)
	}
	# Just use 'min' instead of 'max' for minimum.
	GetTheBestTonnetz = max(TonnetzConnectivity, key=TonnetzConnectivity.get)
	# print('The Tonnetz Selected is :', GetTheBestTonnetz,
	# '\n' + 'The number of represented chords in this system is :'
	# , TonnetzConnectivity[GetTheBestTonnetz])
	return(GetTheBestTonnetz), TonnetzConnectivity


def TonnetzConfigDict(GetTheBestTonnetz):
	"""Finally choose the appropriate Tonnetz config."""
	Tonnetz = dictOfTonnetze[GetTheBestTonnetz]
	return Tonnetz


def axesDict(T_axes):
	"""Check connectivity based on Interval Vectors."""
	intervalList = [
		T_axes[0],
		T_axes[1],
		T_axes[2],
		(12 - T_axes[0]),
		(12 - T_axes[1]),
		(12 - T_axes[2])]
	return intervalList


def findIfConnected(interval, T_axes):
	"""Find if an interval is Connected."""
	intervalList = axesDict(T_axes)
	if interval in intervalList:
		return 1
	else:
		return 0


def removeDoubles(l, lvec):
	"""Remove duplicate consecutive chords."""
	N = len(l)
	nlpc = []
	nlVec = []
	sl = [str(i) for i in l]
	nlpc.append(l[0])
	nlVec.append(lvec[0])
	for i in range(1, N):
		if sl[i] != sl[i - 1]:
			nlpc.append(ast.literal_eval(sl[i]))
			nlVec.append(lvec[i])
	return nlpc, nlVec


def checkEdges(chord, T_axes):
	"""Thouragly check if a chord is connected."""
	if len(chord) == 1:
		return False
	elif len(chord) == 2:
		interval = (chord[0] - chord[1]) % 12
		if findIfConnected(interval, T_axes) == 1:
			return True
		else:
			return False
	else:
		constrain = True
		pdct = product(chord, chord)
		edges = []
		# from a chord take the cartesian product and keep those couples that
		# form an interval on the axes
		for (a, b) in pdct:
			if findIfConnected((a - b) % 12, T_axes) == 1:
				edges.append((a, b))
		if edges != []:
			proj1, proj2 = zip(*edges)
		else:
			proj1 = []
		# If a note is not contained in the edges return false
		for note in chord:
			if note not in proj1:
				constrain = False
		# If all the above is satisfied check if an edge is isolated
		if constrain:
			for (a, b) in edges:
				if proj1.count(a) == 1 and proj1.count(b) == 1:
					constrain = False
		return constrain


def checkConnectivityBack(listofchords, currentindex, chord, T_axes, alpha=1):
	"""Check if there are enough elements for recursive call.

	Check if there are enough elements for recursive call
	and limit the loop of the recursive call.
	"""
	if (currentindex - alpha >= 0 and alpha < 6):
		conexCondition = checkEdges(chord, T_axes)
		if not conexCondition:
			my_set = set(listofchords[currentindex] +
						 listofchords[currentindex - alpha])
			NewChord = list(my_set)
			alpha += 1
			# Recursive call
			return checkConnectivityBack(
				listofchords, currentindex, NewChord, T_axes, alpha)
		else:
			return chord
	else:
		return 'Error recursive call'


def checkConnectivityForth(listofchords, currentindex, chord, T_axes, alpha=1):
	"""Check if there are enough elements for recursive call.

	Check if there are enough elements for recursive call
	and limit the loop of the recursive call.
	"""
	if (currentindex + alpha < len(listofchords) and alpha < 6):
		conexCondition = checkEdges(chord, T_axes)
		if not conexCondition:
			my_set = set(listofchords[currentindex] +
						 listofchords[currentindex + alpha])
			NewChord = list(my_set)
			alpha += 1
			# Recursive call
			return checkConnectivityForth(
				listofchords, currentindex, NewChord, T_axes, alpha)
		else:
			return chord
	else:
		return 'Error recursive call'


def checkConnectivityBackForth(
		listofchords,
		currentindex,
		chord,
		T_axes,
		alpha=1):
	"""Check if there are enough elements for recursive call.

	Check if there are enough elements for recursive call
	and limit the loop of the recursive call.
	"""
	if listofchords[currentindex - alpha]:
		return []
	else:
		# Check if there are enough elements recursive call and limit the loop
		# of the recursive call
		if (currentindex - alpha >= 0 and alpha < 15):
			conexCondition = checkEdges(chord, T_axes)
			if not conexCondition:
				my_set = set(listofchords[currentindex] +
							 listofchords[currentindex - alpha])
				NewChord = list(my_set)
				alpha += 1
				# Recursive call
				return checkConnectivityForthBack(
					listofchords, currentindex, NewChord, T_axes, alpha)
			else:
				return chord
		else:
			raise RecursionError('Too many recursions')


def checkConnectivityForthBack(
		listofchords,
		currentindex,
		chord,
		T_axes,
		alpha=1):
	"""Check if there are enough elements for recursive call.

	Check if there are enough elements for recursive call
	and limit the loop of the recursive call.
	"""
	if listofchords[currentindex - alpha]:
		return []
	else:
		# Check if there are enough elements recursive call and limit the loop
		# of the recursive call
		if (currentindex + alpha <= len(listofchords) and alpha < 15):
			conexCondition = checkEdges(chord, T_axes)
			if not conexCondition:
				my_set = set(listofchords[currentindex] +
							 listofchords[currentindex + alpha])
				NewChord = list(my_set)
				alpha += 1
				# Recursive call
				return checkConnectivityBackForth(
					listofchords, currentindex, NewChord, T_axes, alpha)
			else:
				return chord
		else:
			raise RecursionError('Too many recursions')


def removeNonConnected(listOfChords, listOfVectors, T_axes):
	"""Modify non connected chords."""
	axe1 = T_axes[0] - 1
	axe2 = T_axes[1] - 1
	if T_axes[2] > 6:
		axe3 = (12 - T_axes[2]) - 1
	else:
		axe3 = T_axes[2] - 1
	newListOfChords = listOfChords
	newListOfVectors = []
	for index, vector in enumerate(listOfVectors):
		axesCondition = sum(vector) - 2 * \
			(vector[axe1] + vector[axe2] + vector[axe3])
		if axesCondition < 0:
			newListOfVectors.append(vector)
		else:
			chord = listOfChords[index]
			enlargeChord = checkConnectivityBack(
				listOfChords, index, chord, T_axes)
			if enlargeChord == 'Error recursive call':
				enlargeChord = checkConnectivityForth(
					listOfChords, index, chord, T_axes)
				if enlargeChord == 'Error recursive call':
					enlargeChord = checkConnectivityBackForth(
						listOfChords, index, chord, T_axes)
			if enlargeChord == []:
				enlargeChord = newListOfChords[index - 1]
			del newListOfChords[index]
			newListOfChords.insert(index, enlargeChord)
	return newListOfChords, newListOfVectors


def fromMidiToPCS(midifile):
	"""Take a Midi file and return a list of chords and the Tonnetz."""
	chordList, chordVectors = parseMidi(midifile)
	bestconnected, connectivity = TonnetzConnectivity(chordVectors)
	Tonnetz = TonnetzConfigDict(bestconnected)
	chordListNoDoubles, chordListNoDoublesVec = removeDoubles(
		chordList, chordVectors)
	# print('After duplicate reduction the number of chords is :',
	# len(chordListNoDoubles))
	# chordListConnect, vectorsListConnect = removeNonConnected(
	#     chordListNoDoubles, chordListNoDoublesVec, Tonnetz)
	print(len(chordListNoDoubles))
	return chordListNoDoubles, Tonnetz, connectivity


def analysisFromCorpus(file):
	"""Take a file from corpus and return a list of chords and the Tonnetz."""
	chordList, chordVectors = parsedFile(file)
	bestconnected, connectivity = TonnetzConnectivity(chordVectors)
	Tonnetz = TonnetzConfigDict(bestconnected)
	chordListNoDoubles, chordListNoDoublesVec = removeDoubles(
		chordList, chordVectors)
	# print('After duplicate reduction the number of chords is :',
	# len(chordListNoDoubles))
	# chordListConnect, vectorsListConnect = removeNonConnected(
	#     chordListNoDoubles, chordListNoDoublesVec, Tonnetz)
	print(len(chordListNoDoubles))
	return chordListNoDoubles, Tonnetz, connectivity

def extract_chords(midifile):
	"""Take a MIDI file and return the list of chords without duplicates."""
	chordList = parseMIDI(midifile)
	N = len(chordList)
	chordListNoDoubles = []
	sl = [str(i) for i in chordList]
	chordListNoDoubles.append(chordList[0])
	for i in range(1, N):
		if sl[i] != sl[i - 1]:
			chordListNoDoubles.append(ast.literal_eval(sl[i]))
	return chordListNoDoubles