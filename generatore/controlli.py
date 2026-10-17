"""Controlli di qualità sulle risposte dell'AI: la mia parte da QA nel progetto."""
import re


def normalizza(testo: str) -> str:
    """Rende confrontabili due testi: minuscole, stesse virgolette, spazi singoli, niente punto finale."""
    testo = testo.lower()
    testo = re.sub(r"[\"“”‘’`]", "'", testo)   # tutte le virgolette diventano '
    testo = re.sub(r"\s+", " ", testo)         # a capo e spazi multipli → uno spazio
    return testo.strip(" .;:")


def citazione_valida(citazione: str, requisito: str, min_caratteri: int = 15) -> bool:
    """La citazione esiste davvero nel requisito? (anche solo un pezzo di frase, ma non troppo corto)"""
    citazione = normalizza(citazione)
    return len(citazione) >= min_caratteri and citazione in normalizza(requisito)


def controlla_segnaposto(modello_prompt: str, nome_file: str, segnaposto: list[str]) -> None:
    """Si ferma se nel file del prompt manca un segnaposto: senza, il modello non vedrebbe i dati."""
    mancanti = [s for s in segnaposto if s not in modello_prompt]
    if mancanti:
        raise ValueError(f"Nel prompt {nome_file} mancano i segnaposto: {', '.join(mancanti)}")


# ---------- Prova veloce: python -m generatore.controlli ----------

if __name__ == "__main__":
    requisito = 'Il bottone "Accedi" è disabilitato finché username o password sono vuoti.\nCon credenziali valide l\'utente arriva alla dashboard.'
    prove = [
        ("Con credenziali valide l'utente arriva alla dashboard.", True,  "frase identica"),
        ("Il bottone 'Accedi' è disabilitato",                      True,  "pezzo di frase, virgolette diverse"),
        ("Con credenziali valide l'API restituisce token",          False, "frase della checklist, non del requisito"),
        ("dashboard",                                               False, "troppo corta"),
        ("",                                                        False, "vuota"),
    ]
    for citazione, atteso, descrizione in prove:
        ottenuto = citazione_valida(citazione, requisito)
        print("✅" if ottenuto == atteso else "❌", f"{descrizione}: {ottenuto}")
