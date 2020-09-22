from itertools import groupby, islice
from operator import itemgetter
import os
import pickle

from FirstNotePosition import PlaceFirstNote
from graph_creation import CreateGraph
import music21 as ms
import pretty_midi as ptm
from structural_functions import testInput
from Tonnetz_Select import analysisFromCorpus
from Tonnetz_Select import fromMidiToPCS as fmpc
from TrajectoryCalculationsWithClass import NewTrajectory, TrajectoryLookBefore


def pickleSave(dictOfGraphs, Composer_Name):
    """Save a python object(list or dictionary) as a pickle object."""
    print("Enter the directory Location")
    directory = testInput(os.path.isdir)
    file_name = input("The Name of the File")
    completeName = directory + "/" + file_name + ".p"
    with open(completeName, 'wb') as config_dictionary_file:
        # Step 3
        pickle.dump(dictOfGraphs, config_dictionary_file)


def findInstruments(file):
    """Find the Instruments from a midi file."""
    instruments = []
    time_signatures = []
    s = ms.converter.parse(file)
    for element in s.recurse():
        if 'TimeSignature' in element.classes:
            time_signatures.append(element.ratioString)
        if 'Instrument' in element.classes:
            x = str(element)
            if x != '':
                if ': ' in x:
                    newstring = x.split(': ', -1)[1]
                    instruments.append(newstring)
                else:
                    instruments.append(x)
    time_signatures = list(map(itemgetter(0), groupby(time_signatures)))
    return instruments, time_signatures


def TempoAdd(directory):
    """Extract tempo from Midi file via PrettyMidi."""
    s = ptm.PrettyMIDI(directory)
    tempo = s.estimate_tempo()
    return int(tempo)


def GraphOfNewPiece(newPiece, directory):
    """Create a graph object from a midi file."""
    # extract the directory and the file extension from the piece
    shortfilename = os.path.splitext(os.path.basename(newPiece))[0]
    # Choose from where to parse (directory, corpus)
    if directory == 'corpus':
        file = ms.corpus.parse(newPiece)
        chordList, Tonnetz = analysisFromCorpus(file)
    # add the instruments
        instruments, time_signatures = findInstruments(newPiece)
        tempo = []
    else:
        if newPiece.endswith(".mid") or newPiece.endswith(".MID"):
            complete_name = directory + '/' + newPiece
            chordList, Tonnetz = fmpc(complete_name)
        # add the instruments
            instruments, time_signatures = findInstruments(complete_name)
            tempo = TempoAdd(complete_name)
    firstPoint = PlaceFirstNote(chordList, Tonnetz)
    # build trajectory with future
    trajectoryFut = NewTrajectory(chordList, Tonnetz, firstPoint)
    trajectoryFut.addType('Trajectory With Future')
    trajectoryFut.addInstruments(instruments)
    trajectoryFut.addTime_signature_changes(time_signatures)
    trajectoryFut.addTempo(tempo)
    graphFut = CreateGraph(trajectoryFut)
    graphFut.addName(shortfilename)
    # build recursive trajectory
    trajectoryRec = TrajectoryLookBefore(chordList, Tonnetz, firstPoint)
    trajectoryRec.addType('Recursive Trajectory')
    trajectoryRec.addInstruments(instruments)
    trajectoryRec.addTime_signature_changes(time_signatures)
    trajectoryRec.addTempo(tempo)
    graphRec = CreateGraph(trajectoryRec)
    graphRec.addName(shortfilename)
    # return both methods
    return graphFut, graphRec


def GetWorksByDirectory(directory, composer, style):
    """Create graphs of trajectories from a local file."""
    listOfGraphs = []
#     composer, style, harmony = inputQuestions()
    for file in os.listdir(directory):
        if file.endswith(".mid") or file.endswith(
                ".MID") or file.endswith(".mxl") or file.endswith(".xml"):
            try:
                print("Building Trajectory for ", file)
                graphFut, graphRec = GraphOfNewPiece(file, directory)
#                 addingLabels(composer, style, harmony, graph)
                graphFut.addStyle(style)
                graphFut.addComposer(composer)
                graphRec.addStyle(style)
                graphRec.addComposer(composer)
                listOfGraphs.append([graphFut, graphRec])
            except BaseException:
                print("--> Cannot build Trajectory for ", file)
    return listOfGraphs


def GetWorksByComposer(composerName, composer, style):
    """Create graphs of trajectories from corpus."""
    listOfGraphs = []
#     composer, style, harmony = inputQuestions()
    listofWorks = ms.corpus.getComposer(composerName)
    if len(listofWorks) > 60:
        listofWorks = list(islice(listofWorks, 60))
    if len(listofWorks) > 0:
        for piece in listofWorks:
            try:
                print("Building Trajectory for ", piece)
                graphFut, graphRec = GraphOfNewPiece(piece, 'corpus')
#                 addingLabels(composer, style, harmony, graph)
                graphFut.addStyle(style)
                graphFut.addComposer(composer)
                graphRec.addStyle(style)
                graphRec.addComposer(composer)
                listOfGraphs.append([graphFut, graphRec])
            except BaseException:
                print("--> Cannot build Trajectory for ", piece)
    return listOfGraphs
