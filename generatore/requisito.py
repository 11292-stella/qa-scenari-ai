"""Aiuta a SCRIVERE il requisito prima dell'analisi: avvisi riga per riga, senza AI.

Le prove hanno mostrato che gli scenari sono buoni quanto il requisito:
- con il testo esatto ("Importo insufficiente") il modello lo usa, senza lo inventa o ripiega su "un messaggio";
- con "Solo gli amministratori possono..." il caso vietato finisce tra le domande aperte;
- una riga con due regole attira i punti di tutte e due e il passo A sceglie male.

Sono regole semplici in Python: immediate, sempre uguali, e non aggiungono niente al requisito.
Non bloccano l'analisi: sono consigli, la riga si può tenere com'è.

    from generatore.requisito import controlla_requisito
    for riga in controlla_requisito(testo):
        print(riga.numero, riga.testo, riga.avvisi)
"""

import re
from dataclasses import dataclass, field

from generatore.decidi import corpo_requisito, righe_requisito

# Il testo tra virgolette è il testo esatto di un messaggio o di uno stato: lì dentro non si controlla niente
TESTO_ESATTO = re.compile(r"\"[^\"]+\"|“[^”]+”|«[^»]+»")

# Parole che dicono COSA SUCCEDE: un esito che si può verificare in un test
ESITI = ("compare", "comparire", "mostra", "vede", "vedo", "viene", "vengono", "diventa", "resta", "restano",
         "riceve", "restituisce", "risponde", "passa", "torna", "rifiut", "accett", "blocc", "disattivat",
         "errore", "messaggio", "non può", "non possono", "non si può", "non viene", "non è", "salvat",
         "calcola", "contiene", "403", "401", "404", "400")
# Parole di un comportamento ammesso solo in certi casi: va detto anche cosa succede negli altri
SOLO = re.compile(r"\b(solo|soltanto|unicamente|esclusivamente)\b|\b(deve|devono) essere\b|\bammess[oiea]\b")
CONSEGUENZA = re.compile(r"\b(altriment\w*|se no|in caso contrario|senza \w+|riceve|ricevono|rifiut\w*|errore|messaggio|"
                         r"non può|non possono|non si può|non viene|viene|vengono|blocc\w*|disattivat\w*|"
                         r"disabilitat\w*|nascost\w*|riportat\w*|torna|40[0-9])\b")
# Parole che non si possono verificare: un test ha bisogno di un risultato preciso
# (radici: "gestit" prende gestito, gestita, gestiti...; nell'avviso si mostra la parola intera trovata)
VAGHE = re.compile(r"\b(corrett\w*|adeguat\w*|opportun\w*|appropriat\w*|gestit\w*|gestisce|veloce\w*|"
                   r"rapidamente|facilmente|intuitiv\w*|chiaramente|eventualmente|se necessario|ecc|e così via|"
                   r"in modo coerente|senza problemi)\b")
# Un limite deve avere il suo numero
# ("inferiore al totale" è un confronto, non un limite senza numero: non c'è)
LIMITE = re.compile(r"\b(troppo (lung|cort|grand|piccol)\w*|lunghezza|massim\w*|minim\w*|limite)\b")
NUMERO = re.compile(r"\d")
# Verbi che descrivono COME DEVE ESSERE una cosa (una regola, non un'azione): "è obbligatorio", "deve avere"...
STATO = re.compile(r"\b(è|sono|ha|hanno|può|possono|deve|devono|si può|si possono|nasconde|accede|arriva|"
                   r"appartiene|si apre|si aprono|si crea|si cerca|si cercano)\b")


@dataclass
class RigaControllata:
    numero: int
    testo: str
    avvisi: list[str] = field(default_factory=list)


def senza_testi(riga: str) -> str:
    """La riga senza i testi esatti tra virgolette, in minuscolo."""
    return TESTO_ESATTO.sub(" ", riga).lower()


def controlla_riga(riga: str) -> list[str]:
    avvisi: list[str] = []
    testo = senza_testi(riga)
    parole = testo.split()

    # 1. Una regola per riga
    frasi = [f for f in re.split(r";|(?<=[a-zà-ù0-9])\.\s+(?=[A-ZÀ-Ù])", riga) if f.strip()]
    if len(frasi) > 1:
        avvisi.append("Due regole nella stessa riga: dividile, una per riga. Il generatore sceglie UNA riga per ogni "
                      "punto della checklist, e una riga con due regole attira i punti di tutte e due.")
    elif len(parole) > 30:
        avvisi.append(f"Riga lunga ({len(parole)} parole): se dice più di una cosa, dividila.")
    if len(parole) < 4:
        avvisi.append("Riga troppo corta: scrivi una frase completa con chi fa cosa e cosa succede.")

    # 2. "Solo X può...": e gli altri?
    if SOLO.search(testo) and not CONSEGUENZA.search(testo):
        avvisi.append("Dice cosa è permesso, ma non cosa succede negli altri casi. Aggiungi l'esito del caso vietato "
                      "(es. \"un utente che non è amministratore riceve un errore 403\", "
                      "\"con un file di un altro formato compare il messaggio ...\"): senza, i test negativi finiscono tra le domande aperte.")

    # 3. Parole che non si possono verificare
    vaghe = sorted(set(VAGHE.findall(testo)))
    if vaghe:
        avvisi.append(f"Parole vaghe ({', '.join(vaghe)}): un test ha bisogno di un risultato preciso. "
                      "Scrivi cosa si vede o cosa risponde il sistema.")

    # 4. Un messaggio senza il suo testo
    if re.search(r"\bmessaggi[oi]\b", testo) and not TESTO_ESATTO.search(riga):
        avvisi.append("Parla di un messaggio senza dirne il testo. Se lo conosci, scrivilo tra virgolette "
                      "(es. compare il messaggio \"Importo insufficiente\"): il generatore lo userà invece di "
                      "\"vedo un messaggio di errore\".")

    # 5. Un limite senza numero
    if LIMITE.search(testo) and not NUMERO.search(testo):
        avvisi.append("Parla di un limite senza dire il numero: scrivilo (es. \"al massimo 80 caratteri\", "
                      "\"fino al 20%\"), così il generatore può scrivere i valori limite.")

    # 6. Manca il risultato: la riga non dice né cosa succede (ESITI) né come deve essere (STATO).
    # "Il cliente paga con carta" descrive un'azione: e poi? approvato? ricevuta? ordine pagato?
    if not any(e in testo for e in ESITI) and not STATO.search(testo):
        avvisi.append("Non dice cosa succede: aggiungi il risultato che il test deve verificare "
                      "(cosa compare, cosa viene salvato, cosa risponde il sistema, in che stato finisce).")
    return avvisi


def controlla_requisito(testo: str) -> tuple[list[RigaControllata], list[str]]:
    """(righe con i loro avvisi, avvisi sul requisito intero). Accetta anche le righe Titolo:/Checklist:."""
    righe = righe_requisito(corpo_requisito(testo))
    controllate = [RigaControllata(n, r, controlla_riga(r)) for n, r in enumerate(righe, start=1)]

    generali: list[str] = []
    if len(righe) < 3:
        generali.append("Il requisito ha meno di 3 righe: con poche regole quasi tutti i punti della checklist "
                        "finiranno tra le domande aperte.")
    negativi = ("non può", "non possono", "non si può", "non viene", "rifiut", "errore", "blocc", "non è ammess",
                "disattivat", "insufficient", "non valid", "40")
    if righe and not any(any(n in senza_testi(r) or n in r.lower() for n in negativi) for r in righe):
        generali.append("Nessuna riga dice cosa succede quando qualcosa va storto (un dato sbagliato, un utente "
                        "senza permessi, un errore): i test negativi saranno quasi tutti domande aperte.")
    return controllate, generali


# ---------- Prova veloce: python -m generatore.requisito requisiti/pagamenti.txt ----------

if __name__ == "__main__":
    import sys
    from pathlib import Path

    righe, generali = controlla_requisito(Path(sys.argv[1]).read_text(encoding="utf-8"))
    for riga in righe:
        print(f"{'⚠️ ' if riga.avvisi else '✅'} {riga.numero}. {riga.testo}")
        for avviso in riga.avvisi:
            print(f"     → {avviso}")
    for avviso in generali:
        print(f"\n⚠️  {avviso}")
