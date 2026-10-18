"""Controlli di qualità sulle risposte dell'AI: la mia parte da QA nel progetto."""

import re


def normalizza(testo: str) -> str:
    """Rende confrontabili due testi: minuscole, stesse virgolette, spazi singoli, niente punto finale."""
    testo = testo.lower()
    testo = re.sub(r"[\"“”‘’`]", "'", testo)  # tutte le virgolette diventano '
    testo = re.sub(r"\s+", " ", testo)  # a capo e spazi multipli → uno spazio
    return testo.strip(" .;:")


def citazione_valida(citazione: str, requisito: str, min_caratteri: int = 15) -> bool:
    """La citazione esiste davvero nel requisito? (anche solo un pezzo di frase, ma non troppo corto)"""
    citazione = normalizza(citazione)
    return len(citazione) >= min_caratteri and citazione in normalizza(requisito)


# Simboli che in un passo Gherkin vogliono dire "il modello ha scritto codice"
SIMBOLI_CODICE = re.compile(r"[=&{}<>|;]|@\w|\w+\.\w+\.\w+|\w+_\w+")
# I valori tra apici o virgolette possono contenere di tutto ('mario.rossi@test.it'): non si controllano.
# L'apice conta solo se non è attaccato a una lettera prima (l'apostrofo di "l'email" non è una virgoletta)
VALORI = re.compile(r"\"[^\"]*\"|“[^”]*”|‘[^’]*’|(?<!\w)'[^']*'(?!\w)")


def controlla_scenario(dato: list[str], quando: list[str], allora: list[str]) -> list[str]:
    """Errori di FORMA di uno scenario scritto dall'AI. Lista vuota = scenario OK.

    Controlla la forma, non il contenuto: se il passo è sensato lo decide la tester.
    """
    problemi: list[str] = []
    tutti = [("dato", p) for p in dato] + [("quando", p) for p in quando] + [("allora", p) for p in allora]

    for campo, passo in tutti:
        parole = passo.split()
        if SIMBOLI_CODICE.search(VALORI.sub(" ", passo)):
            problemi.append(f'"{campo}": il passo "{passo}" contiene codice o simboli: scrivilo in italiano normale')
        if len(parole) < 3:
            problemi.append(f'"{campo}": il passo "{passo}" è troppo corto: scrivi una frase completa con un verbo')
        if len(parole) > 25:
            problemi.append(f'"{campo}": il passo "{passo[:40]}..." è troppo lungo: dividilo in più passi')

    for passo in allora:
        if normalizza(passo).startswith(("verifica", "controlla", "il sistema verifica")):
            problemi.append(f'"allora": "{passo}" non deve dire "verifica": scrivi cosa si vede o cosa risponde il sistema')

    visti = set()
    for campo, passo in tutti:
        chiave = normalizza(passo)
        if chiave in visti:
            problemi.append(f'il passo "{passo}" è ripetuto: ogni passo deve dire una cosa diversa')
        visti.add(chiave)
    return problemi


def controlla_segnaposto(
    modello_prompt: str, nome_file: str, segnaposto: list[str]
) -> None:
    """Si ferma se nel file del prompt manca un segnaposto: senza, il modello non vedrebbe i dati."""
    mancanti = [s for s in segnaposto if s not in modello_prompt]
    if mancanti:
        raise ValueError(
            f"Nel prompt {nome_file} mancano i segnaposto: {', '.join(mancanti)}"
        )


# ---------- Prova veloce: python -m generatore.controlli ----------

if __name__ == "__main__":
    print("Scenario dell'A21 (codice nel Gherkin):")
    for problema in controlla_scenario(
            dato=[".azienda.ragione_sociale = 'Compagnia Srl' && @api.azienda.partita_iva = '123'"],
            quando=["nome"], allora=["verifica che la partita IVA sia valida"]):
        print("  ❌", problema)
    print("Scenario buono:", controlla_scenario(
        dato=["che sono nella pagina Nuovo cliente"],
        quando=["scrivo 'mario.rossi@test.it' nel campo Email", "clicco su \"Salva\" nell'anagrafica"],
        allora=["vedo un messaggio di errore sotto il campo Email"]) or "✅ nessun problema")
    print()

    requisito = 'Il bottone "Accedi" è disabilitato finché username o password sono vuoti.\nCon credenziali valide l\'utente arriva alla dashboard.'
    prove = [
        (
            "Con credenziali valide l'utente arriva alla dashboard.",
            True,
            "frase identica",
        ),
        (
            "Il bottone 'Accedi' è disabilitato",
            True,
            "pezzo di frase, virgolette diverse",
        ),
        (
            "Con credenziali valide l'API restituisce token",
            False,
            "frase della checklist, non del requisito",
        ),
        ("dashboard", False, "troppo corta"),
        ("", False, "vuota"),
    ]
    for citazione, atteso, descrizione in prove:
        ottenuto = citazione_valida(citazione, requisito)
        print("✅" if ottenuto == atteso else "❌", f"{descrizione}: {ottenuto}")