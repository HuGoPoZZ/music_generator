# Générateur de musique par chaîne de Markov

Un petit projet Python pour s'initier aux **chaînes de Markov** en générant des mélodies à partir d'un fichier MIDI existant. Le programme lit un morceau, apprend quelles notes ont tendance à en suivre d'autres, puis compose une nouvelle mélodie qui respecte ces mêmes probabilités.

C'est un projet d'apprentissage : le code est volontairement simple et direct, pensé pour comprendre le concept plutôt que pour être exhaustif.

## Le principe : une chaîne de Markov d'ordre 2

Une chaîne de Markov prédit l'élément suivant en fonction des éléments précédents. Ici, la chaîne est **d'ordre 2** : pour choisir la prochaine note, le programme regarde les **deux dernières notes** jouées.

Le fonctionnement se déroule en trois temps :

1. **Apprentissage** : on parcourt le morceau source et, pour chaque paire de notes consécutives, on note quelle note vient ensuite. On obtient un dictionnaire qui associe chaque couple de notes à la liste de ses successeurs observés.
3. **Probabilités** : on transforme ces comptages en probabilités (une note qui suit souvent un couple donné aura plus de chances d'être choisie).
4. **Génération** : on part d'un couple de notes réel, et on tire au sort la suite en respectant les probabilités apprises, note après note, jusqu'à obtenir la longueur voulue.

Chaque note est représentée par un couple `(hauteur, durée)`, ce qui permet à la mélodie générée de conserver un rythme varié plutôt que d'enchaîner des notes toutes identiques.

## Prérequis

- Python 3
- La bibliothèque [music21](https://web.mit.edu/music21/) (développée par le MIT)
- Un logiciel de partition comme [MuseScore](https://musescore.org/) pour visualiser et écouter le résultat

Installation de music21 :

```bash
pip install music21
```

## Utilisation

1. Placez un fichier MIDI dans le dossier du projet et adaptez le chemin dans le code :

```python
chemin_fichier = Path("chemin/vers/votre_fichier.mid")
```

2. Lancez le programme :

```bash
python music_generator.py
```

3. Indiquez la longueur souhaitée quand elle vous est demandée. La partition générée s'ouvre automatiquement dans votre logiciel de notation.

## Comment ça marche, dans le détail

**Extraction des notes.** Le programme ne garde que la **voix mélodique** (la première voix de chaque mesure), afin d'éviter de mélanger la mélodie et l'accompagnement dans une même chaîne. Chaque note est stockée sous la forme d'un couple `(nom_avec_octave, durée)`.

**Construction du modèle.** Un dictionnaire associe chaque couple de notes consécutives à la liste des notes qui l'ont suivi. Un `Counter` compte les occurrences, puis ces comptages sont convertis en probabilités comprises entre 0 et 1.

**Génération et gestion des impasses.** La mélodie démarre sur un couple de notes réellement présent dans le morceau. À chaque étape, la note suivante est tirée au sort selon les probabilités (`random.choices` avec pondération). Si la chaîne tombe sur un couple qui n'a aucune suite connue (une impasse), elle **rebondit** en repartant d'un nouveau couple valide, ce qui évite que la génération s'arrête prématurément.

## Pistes d'amélioration

Ce projet est une base. Plusieurs directions permettraient d'aller plus loin :

- **Extraire les notes plus proprement** : l'isolation de la voix mélodique par « première voix de chaque mesure » fonctionne pour ce fichier, mais n'est pas garantie sur tous les MIDI (l'ordre des voix peut varier).
- **Mieux gérer les silences** : les silences (rests) ne sont pas pris en compte actuellement, ce qui appauvrit le rythme et le phrasé.
- **Ajouter une deuxième chaîne pour l'accompagnement** : générer la ligne de basse ou les accords avec une chaîne dédiée, en parallèle de la mélodie.
- **Entraîner sur plusieurs fichiers** : apprendre sur un dossier entier de morceaux du même style enrichirait les probabilités et réduirait fortement les impasses, tout en évitant que la mélodie recopie l'original.
- **Faire varier l'ordre de la chaîne** : un ordre plus élevé donne une mélodie plus cohérente mais plus proche de l'original ; un ordre plus bas laisse plus de liberté mais moins de structure.
