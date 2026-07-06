from music21 import *
import os
from pathlib import Path
from collections import Counter
import random

notes = []
dico_stats = {}
dico = {}
proba = 0
chemin_fichier = Path("Your path to you midi file")

s = converter.parse(chemin_fichier)
#s.show('text')
part = s.parts[0]
for n in part.getElementsByClass(stream.Measure):
    voix = n.getElementsByClass(stream.Voice)
    if len(voix) > 0:
        première_voix = voix[0]
        for i in première_voix.getElementsByClass(note.Note):
            notes.append((i.nameWithOctave, i.quarterLength))
    
#print(notes)

for i in range(len(notes)- 3):
    if (notes[i], notes[i+1]) in dico:
        dico[(notes[i], notes[i+1])].append(notes[i+2])
        
    else:
        dico[(notes[i], notes[i+1])] = [notes[i+2]]

#print(dico)

for cle, liste_notes in dico.items():
    dico_stats[cle] = Counter(liste_notes)

#print(dico_stats)
proba_dico = {}

for note_actuelle, compteur in dico_stats.items():
    total = round(sum(compteur.values()), 2)
    proba_dico[note_actuelle] = {}
    for note_suivante, count in compteur.items():
        proba_dico[note_actuelle][note_suivante] = count/total

print(proba_dico)
nouvelle_musique = []
debut = random.choice(list(dico.keys())) #première note
nouvelle_musique.extend(debut)
longueur = int(input("Quelle est la longueur de votre morceau : "))

for i in range(longueur):
    if tuple(nouvelle_musique[-2 : ]) in proba_dico:            
        notes_suivante = list(proba_dico[tuple(nouvelle_musique[-2 : ])].keys())
        pondération = list(proba_dico[tuple(nouvelle_musique[-2 : ])].values())
        suivante = random.choices(notes_suivante, pondération)
        nouvelle_musique.append(suivante[0])
        
    else:
        relance = random.choice(list(dico.keys()))
        nouvelle_musique.extend(relance)



stream1 = stream.Stream()

print(nouvelle_musique)
for i in range(len(nouvelle_musique)):
    a = note.Note(nouvelle_musique[i][0])
    a.quarterLength = nouvelle_musique[i][1]
    stream1.append(a)

#stream1.show('text')
stream1.show()

#print(nouvelle_musique)
