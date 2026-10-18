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
# Dentro un valore tra apici è ammesso un apostrofo seguito da una lettera: 'L'ordine non può...' è UN valore
VALORI = re.compile(r"\"[^\"]*\"|“[^”]*”|‘[^’]*’|(?<!\w)'(?:[^']|'(?=\w))*'(?!\w)")
# "scrivo 'X' nel campo Y": per controllare che il valore non sia il nome del campo
NEL_CAMPO = re.compile(r"nel campo\s+(?:del\s+|della\s+|dello\s+|dei\s+|di\s+)?(.+)$", re.IGNORECASE)
# Parole dell'INTERFACCIA: in uno scenario @api non ci sono pagine, campi o bottoni, ci sono richieste e risposte
# ("pagina" da sola no: "la pagina '3' della lista" è un parametro dell'API, "ho aperto la pagina" è interfaccia)
INTERFACCIA = re.compile(r"\b(nel campo|sotto il campo|(?:aperto|apro|sulla|nella|sono sulla) (?:la )?pagina|form|bottone|pulsante|"
                         r"schermata|clicco|premo|vedo|non vedo)\b",
                         re.IGNORECASE)
# Frasi che in un "Allora" vogliono dire che lo scenario finisce con un errore o un rifiuto
ESITO_NEGATIVO = ("messaggio di errore", "viene rifiutat", "è rifiutat", "non riesco")
# ...e frasi che vogliono dire successo (per trovare un "allora" che dice tutte e due le cose)
ESITO_POSITIVO = ("viene accettat", "è accettat", "messaggio di conferma", "messaggio di successo", "con successo")
CODICE_ERRORE = re.compile(r"\b[45]\d\d\b|codice di errore")
# Un "dato" è una situazione di partenza, non un'azione: queste sono azioni, vanno nel "quando"
AZIONI = ("invio ", "premo ", "clicco ", "scrivo ", "seleziono ")


def valori_tra_apici(passo: str) -> list[str]:
    return [v.strip("'\"“”‘’") for v in VALORI.findall(passo)]


def controlla_scenario(dato: list[str], quando: list[str], allora: list[str], riga: str = "",
                       tipo: str = "", livello: str = "") -> list[str]:
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

    for campo, passo in tutti:
        for valore in valori_tra_apici(passo):
            if not valore.strip(" .") or set(valore.strip()) <= {".", "…", " "}:
                problemi.append(f'"{campo}": il valore \'{valore}\' è un segnaposto: scrivi un valore concreto')

    # Un testo di più parole tra apici in un "Allora" è il testo di un messaggio: se la riga non lo dice, è inventato
    if riga:
        for passo in allora:
            for valore in valori_tra_apici(passo):
                if len(valore.split()) >= 2 and normalizza(valore) not in normalizza(riga):
                    problemi.append(f'"allora": il testo \'{valore}\' non è nel requisito: non inventarlo, '
                                    f'scrivi per esempio "vedo un messaggio di errore" o "vedo un messaggio di conferma"')

    # Il valore non deve essere il nome del campo: "scrivo 'Quantità' nel campo 'Quantità'"
    for campo, passo in tutti:
        trovato = NEL_CAMPO.search(VALORI.sub(lambda m: f" {m.group(0)} ", passo))
        if not trovato:
            continue
        nome_campo = normalizza(trovato.group(1).strip(" '\"“”‘’"))
        for valore in valori_tra_apici(passo.split("nel campo")[0]):
            v = normalizza(valore)
            if v and len(v) > 2 and (v in nome_campo or nome_campo in v):
                problemi.append(f'"{campo}": il valore \'{valore}\' è il nome del campo, non un dato di prova: '
                                f'scrivi un valore concreto (es. un nome, un numero, una data)')

    # Il tipo va rispettato: uno scenario positivo non finisce con un errore o un rifiuto
    if tipo == "positivo":
        negativi = [p for p in allora if any(e in normalizza(p) for e in ESITO_NEGATIVO)]
        if negativi:
            problemi.append(f'lo scenario è POSITIVO ma "allora" dice "{negativi[0]}": un positivo finisce con '
                            f'un successo (cosa succede quando l\'operazione è permessa)')

    # L'"allora" non può dire insieme successo ed errore ("accettata" + "codice di errore 401").
    # I passi negati ("non vedo un messaggio di errore") non contano
    affermati = [normalizza(p) for p in allora if not normalizza(p).startswith("non ")]
    successo = [p for p in affermati if any(e in p for e in ESITO_POSITIVO)]
    errore = [p for p in affermati if any(e in p for e in ESITO_NEGATIVO) or CODICE_ERRORE.search(p)]
    if successo and errore and set(successo) != set(errore):
        problemi.append(f'"allora" si contraddice: "{successo[0]}" è un successo, "{errore[0]}" è un errore. '
                        f'Lo scenario deve finire in un solo modo')
    elif successo and errore:   # stesso passo: "la richiesta viene accettata e la risposta contiene il codice 401"
        problemi.append(f'"allora" si contraddice: "{successo[0]}" dice insieme successo ed errore')

    # Il "dato" è la situazione di partenza: un'azione ("invio la richiesta...") va nel "quando"
    for passo in dato:
        testo = normalizza(passo).removeprefix("che ")
        if testo.startswith(AZIONI):
            problemi.append(f'"dato": "{passo}" è un\'azione, non una situazione di partenza: mettila nel "quando" '
                            f'e nel "dato" scrivi lo stato iniziale (es. "che esiste ...", "che ho aperto ...")')
            break

    # Il testo esatto del requisito va usato: se la riga dice il messaggio ("Importo insufficiente"),
    # uno scenario negativo non può ripiegare su "vedo un messaggio di errore"
    testi_riga = [t for t in valori_tra_apici(riga) if t.strip()] if riga else []
    if testi_riga and tipo in ("negativo", "limite"):
        scenario = normalizza(" ".join(dato + quando + allora))
        generico = any(re.search(r"\bmessaggio( di (errore|conferma|successo))?\b", normalizza(p)) for p in allora)
        if generico and not any(normalizza(t) in scenario for t in testi_riga):
            problemi.append(f'la riga del requisito dice il testo esatto ({", ".join(repr(t) for t in testi_riga)}): '
                            f'usalo nell\'"allora" invece di un messaggio generico (es. "vedo il messaggio \'{testi_riga[0]}\'")')

    # Uno scenario @e2e è fatto dall'utente nell'interfaccia: "invio la richiesta" è da API
    if livello == "e2e":
        for passo in quando:
            # solo se il passo COMINCIA così: "scrivo ... nel campo di ricerca e invio la richiesta" è un'azione da UI
            if normalizza(passo).startswith("invio la richiesta"):
                problemi.append(f'"quando": "{passo}" è una richiesta API, ma il livello è e2e: scrivi cosa fa '
                                f'l\'utente (es. "premo il bottone ...", "scrivo \'...\' nel campo ...")')
                break

    # Il livello va rispettato: uno scenario @api parla di richieste e risposte, non di pagine e campi
    if livello == "api":
        for campo, passo in tutti:
            trovata = INTERFACCIA.search(VALORI.sub(" ", passo))
            if trovata:
                problemi.append(f'"{campo}": il passo "{passo}" descrive l\'interfaccia ("{trovata.group(1)}"), ma il '
                                f'livello è api: scrivi la richiesta ("invio la richiesta di ... con ...") e la risposta '
                                f'("la richiesta viene accettata", "la richiesta viene rifiutata", "la risposta contiene ...")')
                break   # un avviso basta: il modello deve riscrivere tutto lo scenario

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


def parole_scenario(dato: list[str], quando: list[str], allora: list[str]) -> set[str]:
    return set(normalizza(" ".join(dato + quando + allora)).replace("'", " ").split())


def trova_simili(scenari: list, soglia: float = 0.8) -> dict[str, str]:
    """{codice: codice dello scenario a cui somiglia}. Due scenari sono "simili" se partono dalla
    stessa riga del requisito e hanno quasi le stesse parole nei passi (indice di Jaccard >= soglia)."""
    simili: dict[str, str] = {}
    for i, b in enumerate(scenari):
        parole_b = parole_scenario(b.dato, b.quando, b.allora)
        for a in scenari[:i]:
            if a.codice in simili or normalizza(a.citazione) != normalizza(b.citazione):
                continue
            parole_a = parole_scenario(a.dato, a.quando, a.allora)
            if parole_a and len(parole_a & parole_b) / len(parole_a | parole_b) >= soglia:
                simili[b.codice] = a.codice
                break
    return simili


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
