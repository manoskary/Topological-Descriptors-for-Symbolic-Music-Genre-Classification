class TrajectoryClass:
    """A class containing Trajectory Information."""

    def __init__(self, initialChordPosition, listOfChords, Tonnetz):
        """Initialize function of Trajectory."""
        self.chordPositions = [initialChordPosition]
        self.connectingEdges = []
        self.index = 1  # Redundant: should always be len(chordPositions)
        self.listOfChords = listOfChords
        self.Tonnetz = Tonnetz

    def addChord(self, chordPosition, connectingEdge):
        """Add a new chord in Trajectory."""
        self.chordPositions.append(chordPosition)
        self.connectingEdges.append(connectingEdge)
        self.index += 1

    def getLastPosition(self, offset=1):
        """Get the last chord coordinates, or change offset."""
        if offset > self.index:
            raise IndexError()
        return self.chordPositions[-offset]

    def getThisChord(self):
        """Get the PC values of the currect chord."""
        return self.listOfChords[self.index]

    def getNextChord(self, offset=1):
        """Get the PC values of the next chord, or change offest."""
        return self.listOfChords[self.index + offset]

    def addType(self, trajType):
        """Precise the type of the Trajectory, recursive, with future, etc."""
        self.type = trajType

    def chordsRemaining(self):
        """Return the number of remaining chords to place."""
        return len(self.listOfChords) - len(self.chordPositions)

# ADD MIDI FILE PROPERTIES

    def addNumberOfInstruments(self, numberOfInstruments):
        """How many instruments in midi file.

        The number of instruments typically is provides by program changes.
        """
        self.numOfInstr = numberOfInstruments

    def addInstruments(self, listOfInstruments):
        """A list with all the instruments, no duplicates."""
        self.instruments = list(set(listOfInstruments))
        self.addNumberOfInstruments(len(set(listOfInstruments)))

    def addTempo(self, tempo):
        """Tempo Estimation."""
        self.tempo = tempo

    def addNumber_of_signature_changes(self, number):
        """Number of time signature changes."""
        self.number_of_signature_changes = number

    def addTime_signatures(self, signature_changes):
        """Add the time signatures of the piece.

        The default value if the time signature is not precised is 4/4
        """
        self.time_signatures = list(set(signature_changes))
        self.addNumber_of_signature_changes(len(signature_changes))
