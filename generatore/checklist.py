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
    area: str = ""          # la checklist da cui viene il punto (es. "ordini_importi")


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

        punti.append(PuntoChecklist(codice, cosa, tipo, livelli, area=nome))

    if not punti:
        errori.append("nessun punto trovato: la tabella è scritta bene?")
    if errori:
        raise ValueError(f"Checklist {percorso} non valida:\n- " + "\n- ".join(errori))
    return punti


def leggi_checklist_multiple(nomi: list[str]) -> list[PuntoChecklist]:
    """Più checklist insieme (es. ["ordini", "ordini_importi"]). Un codice ripetuto tra due file è un errore."""
    punti: list[PuntoChecklist] = []
    for nome in nomi:
        for punto in leggi_checklist(nome):
            gia = next((p for p in punti if p.codice == punto.codice), None)
            if gia:
                raise ValueError(f"Il codice {punto.codice} è sia in '{gia.area}' sia in '{nome}': i codici devono essere unici")
            punti.append(punto)
    return punti


def leggi_esempio(nome: str, livello: str = "") -> str:
    """Lo scenario di esempio della checklist: la sezione "## Esempio di scenario" (vuoto se non c'è).
    Con un livello ("api") cerca prima "## Esempio di scenario api"; se non c'è, usa quello normale.

    L'esempio sta nella checklist e non nel prompt: così ogni area ha il SUO esempio,
    e un modello piccolo che copia il contenuto copia almeno parole dell'area giusta.
    """
    testo = (CARTELLA / f"{nome}.md").read_text(encoding="utf-8")
    for titolo in ([f"Esempio di scenario {livello}"] if livello else []) + ["Esempio di scenario"]:
        trovato = re.search(rf"^##\s*{titolo}\s*$(.*?)(?=^##\s|\Z)", testo, re.MULTILINE | re.DOTALL)
        if trovato:
            return trovato.group(1).strip()
    return ""


def esempio_per(punto: PuntoChecklist) -> str:
    """L'esempio giusto per un punto: della SUA checklist e del SUO livello, se la checklist ce l'ha
    ("## Esempio di scenario api", "## Esempio di scenario e2e"...), altrimenti quello normale.
    Un modello piccolo scrive come l'esempio: con un esempio di form scrive anche gli scenari API come un form,
    e con un esempio API scrive anche gli e2e come richieste."""
    if not punto.area:
        return ""
    livello = punto.livelli[0] if len(set(punto.livelli)) == 1 else ""
    return leggi_esempio(punto.area, livello)


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
    esempio = leggi_esempio(nome)
    print("Esempio di scenario:", "✅ presente" if esempio else "❌ manca (sezione '## Esempio di scenario')")
