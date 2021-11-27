# Mondlandung mithilfe von Fuzzy-Logik

Dieses Projekt dient zur Demonstration eines Fuzzy-Systems basierend auf einer Übungsaufgabe der Vorlesung "Künstliche Intelligenz" an der Hochschule Bochum. 

Eine Übersicht über die Funktionweise des Fuzzy-Systems findet sich im Verzeichnis `docs`.

## Verwendung

Das Projekt besteht aus zwei Programmen:
- Mondlandung (`mondlandung.py`)
- Plotting (`plotting.py`)

### Mondlandung

```
python mondlandung.py -h 
```

```
usage: mondlandung.py [-h] [--variant {3 sets,5 sets,5 sets smooth}] [--live-plot] [--debug]

optional arguments:
  -h, --help            show this help message and exit
  --variant {3 sets,5 sets,5 sets smooth}
                        Verwendet die gewählte Konfiguration an Fuzzy-Mengen.
  --live-plot           Zeigt eine Visualisierung während die Rakete landet. (Sehr unperformant!)
  --debug
``` 

### Plotting

```
python plotting.py -h  
```

```
usage: plotting.py [-h] [--value VALUE] [--variant {3 sets,5 sets,5 sets smooth}]

Visualisiert die Fuzzy-Mengen, deren Aggregation und Ausgabe während der Landung.

optional arguments:
  -h, --help            show this help message and exit
  --value VALUE         Plottet einen einzigen X-Wert (hier Höhe) und spielt keine Animation ab.
  --variant {3 sets,5 sets,5 sets smooth}
                        Verwendet die gewählte Konfiguration an Fuzzy-Mengen.
```

## Module

__fuzzy__: Enthält das Fuzzy-Sytem (Mengen, Aggregator & Defuzzy).

__library__: Beinhaltet Konfigurationen von Fuzzy-Mengen, mit denen die Rakete erfolgreich gelandet werden kann.

__mondlandung__: Das Hauptprogramm

__plotting__: Modul für verschiedene Visualisierungen.

__landing_game__: Das vorgegebene Spiel aus der Vorlesung – ausgelagert in ein eigenständiges Modul.
