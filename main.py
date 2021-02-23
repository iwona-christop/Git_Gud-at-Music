# Git_Gud@Music
# - Konwerter ścieżek audio na materiał MIDI
# - W programie mogę wczytać ścieżkę melodyczną i otrzymać na wyjściu plik MID
# lub SMF oddający wysokość i natężenie dźwięku
# - W programie mogę wczytać ścieżkę rytmiczną i otrzymać na wyjściu plik MID
# lub SMF oddający typ elementu zestawu perkusyjnego i natężenie
# - Bonus: wczytywania i wyboru mogę dokonać przez GUI

from appJar import gui
import scipy
from scipy.fft import fft
import numpy as np
from scipy.io import wavfile
import operator
import csv
from midiutil.MidiFile import MIDIFile


def getOutput(btn):
    # Pobieramy nazwę pliku wejściowego
    wavFilename = app.getEntry('filename')
    print(wavFilename)

    # W zależności od tego co wybraliśmy, uruchamia się albo funkcja dla ścieżki melodycznej albo perkusyjnej
    if app.getRadioButton('type') == 'Ścieżka melodyczna':
        melodic(wavFilename)
    else:
        rhythmic()

def frequency_sepectrum(x, sf):
    x = x - np.average(x)  # zero-centering
    n = len(x)
    k = np.arange(n)
    tarr = n / float(sf)
    frqarr = k / float(tarr)  # two sides frequency range
    frqarr = frqarr[range(n // 2)]  # one side frequency range
    x = fft(x) / n  # fft computing and normalization
    x = x[range(n // 2)]
    return frqarr, abs(x)

def generateMIDI(notes):
    # Tworzymy nasz obiekt MIDI z jedną ścieżką
    midifile = MIDIFile(1)
    track = 0
    time = 0
    midifile.addTrackName(track, time, "Track 0")
    midifile.addTempo(track, time, 120)

    # Dodajemy dźwięki
    for n in notes:
        midifile.addNote(track, 0, int(n), time, 1, 100)
        time += 1

    # Zapisujemy plik MIDI
    with open('output.mid', 'wb') as outf:
        midifile.writeFile(outf)

# Funkcja dla ścieżki melodycznej
def melodic(wavFilename):
    dic = []
    with open('MIDI.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            # print(row)
            dic.append(row)
    print('Melodic function', wavFilename)
    sr, signal = wavfile.read(wavFilename)
    tw = 2205
    notes = []
    time = []
    for i in range(0, len(signal), tw):
        tempSignal = signal[i:i + tw]
        frq, X = frequency_sepectrum(tempSignal, sr)
        index, value = max(enumerate(X), key=operator.itemgetter(1))
        our_freq = frq[index]
        # print(our_freq)
        for note in dic:
            if float(note[1]) <= float(our_freq):
                notes.append(note[0])
                time.append(i)
                break
    generateMIDI(notes)

# Funkcja dla ścieżki rytmicznej
def rhythmic():
    print('Rhythmic function')


# Tworzymy GUI
app = gui()

# Tytuł okna
app.setTitle('Git_Gud@Music')

# Rozmiar okna
app.setSize('200x150')

# Tekst przy wczytaniu pliku
app.addLabel('fileLabel', 'Wybierz plik z komputera:')

# Pole do wczytania pliku
app.addOpenEntry('filename')

# Przyciski do wyboru typu ścieżki
app.addRadioButton('type', 'Ścieżka melodyczna')
app.addRadioButton('type', 'Ścieżka rytmiczna')

# Przycisk generujący ścieżkę wyjściową
app.addButton('Wygeneruj ścieżkę', getOutput)

# Uruchomienie GUI
app.go()