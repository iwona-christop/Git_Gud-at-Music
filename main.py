# Git_Gud@Music
# - Konwerter ścieżek audio na materiał MIDI
# - W programie mogę wczytać ścieżkę melodyczną i otrzymać na wyjściu plik MID lub SMF oddający wysokość i natężenie dźwięku
# - W programie mogę wczytać ścieżkę rytmiczną i otrzymać na wyjściu plik MID lub SMF oddający typ elementu zestawu perkusyjnego i natężenie
# - Bonus: wczytywania i wyboru mogę dokonać przez GUI

from appJar import gui


def getInput(btn):
    print(btn)

def getOutput(btn):
    if app.getRadioButton('type') == 'Ścieżka melodyczna':
        melodic()
    else:
        rhythmic()

def melodic():
    print('Melodic function')

def rhythmic():
    print('Rhythmic function')


# Tworzymy GUI i dostosowujemy wygląd okna
app = gui()
app.setTitle('Git_Gud@Music')
app.setSize('200x150')

app.addLabel('fileLabel', 'Wybierz plik z komputera:')
app.addOpenEntry('filename')
app.addButton('Wczytaj plik', getInput)

app.addRadioButton('type', 'Ścieżka melodyczna')
app.addRadioButton('type', 'Ścieżka rytmiczna')

app.addButton('Wygeneruj ścieżkę', getOutput)

# Start GUI
app.go()