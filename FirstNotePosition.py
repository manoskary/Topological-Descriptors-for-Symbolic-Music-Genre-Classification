from Data_and_Dicts import dictOfTonnetz, dictOfTonnetze, dictOfTonnetzeRearranged
from structural_functions import getKeyByValue


def TonnetzToString(Tonnetz):
    """TonnetzToString: List -> String."""
    TonnetzString = getKeyByValue(dictOfTonnetze, Tonnetz)
    return TonnetzString


# TODO just Take a Chord and Place the first Note.
def PlaceFirstNote(listOfChords, Tonnetz):
    """Take a Chord and Place the first Note."""
    try:
        firstNote = listOfChords[0][0]
        return dictOfTonnetz[TonnetzToString(Tonnetz)][firstNote]
    except KeyError():
        print("This Tonnetz's Initial position is not defined")
        return (0, 0)


def rerrangeTonnetz(Tonnetz):
    """Rearrenge the Tonnetz List to place points correctly."""
    TonnetzString = TonnetzToString(Tonnetz)
    return dictOfTonnetzeRearranged[TonnetzString]
