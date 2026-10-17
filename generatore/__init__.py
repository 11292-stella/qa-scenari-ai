"""Pacchetto del generatore di scenari.

PROGETTO è la cartella principale (quella con checklist/, prompts/, risultati/...).
Tutti i percorsi partono da qui, così il codice funziona anche quando viene
lanciato da un'altra cartella (per esempio dal server Django).
"""
from pathlib import Path

PROGETTO = Path(__file__).resolve().parent.parent
