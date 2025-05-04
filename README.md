# Conway's Game of Life simulation
Dies ist ein "Null-Spieler-Spiel", welches anhand einer vorgegebenen
Anfangskonfiguration den Lebenszyklus von Zellen (Pixeln), anhand von bestimmten
Regeln, im Verlauf der Zeit simuliert.

## Spielregeln
- Nachbarschaft von Zellen ist definiert als 8er Nachbarschaft (Moore)
1. Unterbevölkerung - Eine lebende Zelle mit weniger als zwei lebenden Nachbarn stirbt in der nächsten Generation.
2. Überleben - Eine lebende Zelle mit genau zwei oder drei lebenden Nachbarn bleibt in der nächsten Generation lebendig.
3. Überbevölkerung - Eine lebende Zelle mit mehr als drei lebenden Nachbarn stirbt in der nächsten Generation.
4. Reproduktion - Eine tote Zelle mit genau drei lebenden Nachbarn wird in der nächsten Generation lebendig.

## Muster zum Ausprobieren. Was lässt sich beobachten?
[Game of life - Konfigurationenbibliothek](https://conwaylife.appspot.com/library/)

```
001110  01110
010000  00010
010000  00100
010000  00000
```
