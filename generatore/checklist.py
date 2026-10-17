"""Legge una checklist in markdown (checklist/login.md) e la trasforma in dati.

Ogni riga della tabella diventa un PuntoChecklist:
| L15 | Spazi prima o dopo username/email | limite | unit, api |
  → PuntoChecklist(codice="L15", cosa="Spazi prima...", tipo="limite", livelli=("unit", "api"))

La checklist la scrivo io a mano, quindi anche lei va controllata:
tipi e livelli solo dalle liste chiuse di schemas.py, nessun codice ripetuto.
"""

import re
from dataclasses import dataclass
from pathlib import Path

from generatore import PROGETTO
from generatore.schemas import LIVELLI, TIPI

CARTELLA = PROGETTO / "checklist"

# | L15 | Spazi prima o dopo username/email | limite | unit, api |
RIGA = re.compile(r"^\|\s*([A-Z]+\d+)\s*\|(.+?)\|(.+?)\|(.+?)\|\s*$")
INIZIO_PUNTO = re.compile(r"^\|\s*[A-Z]+\d+\s*\|")   # una riga che "vuole" essere un punto


@dataclass(frozen=True)
class PuntoChecklist:
    codice: str
    cosa: str
    tipo: str
    livelli: tuple[str, ...]


def leggi_checklist(nome: str) -> list[PuntoChecklist]:
    """Legge checklist/<nome>.md e restituisce i punti. Se la checklist ha errori, si ferma e li elenca."""
    percorso = CARTELLA / f"{nome}.md"
    punti: list[PuntoChecklist] = []
    errori: list[str] = []

    for numero, riga in enumerate(
        percorso.read_text(encoding="utf-8").splitlines(), start=1
    ):
        trovata = RIGA.match(riga.strip())
        if not trovata:
            if INIZIO_PUNTO.match(riga.strip()):
                # inizia con un codice ma non ha le 4 colonne: errore, non la salto in silenzio
                errori.append(f"riga {numero}: servono 4 colonne (codice | cosa | tipo | livello): {riga.strip()}")
            continue  # titolo, regole, intestazione della tabella...

        codice, cosa, tipo, livelli = (parte.strip() for parte in trovata.groups())
        livelli = tuple(l.strip() for l in livelli.split(","))

        if tipo not in TIPI:
            errori.append(f"riga {numero} ({codice}): tipo '{tipo}' non ammesso")
        for livello in livelli:
            if livello not in LIVELLI:
                errori.append(
                    f"riga {numero} ({codice}): livello '{livello}' non ammesso"
                )
        if any(p.codice == codice for p in punti):
            errori.append(f"riga {numero}: codice '{codice}' ripetuto")

        punti.append(PuntoChecklist(codice, cosa, tipo, livelli))

    if not punti:
        errori.append("nessun punto trovato: la tabella è scritta bene?")
    if errori:
        raise ValueError(f"Checklist {percorso} non valida:\n- " + "\n- ".join(errori))
    return punti


# ---------- Prova veloce: python -m generatore.checklist login ----------

if __name__ == "__main__":
    import sys

    nome = sys.argv[1] if len(sys.argv) > 1 else "login"
    punti = leggi_checklist(nome)

    print(f"✅ Checklist '{nome}': {len(punti)} punti")
    for p in punti[:3]:
        print(f"  {p.codice:<4} {p.tipo:<13} {', '.join(p.livelli):<10} {p.cosa}")
    print("  ...")
    print("Codici:", [p.codice for p in punti])