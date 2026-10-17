"""Da scenari (dati) a testo Gherkin in italiano: lo scrive Python, quindi la sintassi è sempre giusta.

  @negativo @e2e @L3
  Scenario: Login con password errata
    Dato che sono sulla pagina di login
    Quando eseguo il login con una password errata
    Allora vedo il messaggio di errore
    E resto sulla pagina di login
"""
import re

from generatore.schemas import Scenario

PAROLE = ("Dato", "Quando", "Allora", "E", "Ma")


def pulisci_passo(passo: str) -> str:
    """Toglie gli errori di forma che il modello fa spesso: 'Quando ...' ripetuto, tag '@utente', punto finale."""
    passo = passo.strip()
    passo = re.sub(r"^@\w+\s*", "", passo)                                  # "@utente accede..." → "accede..."
    passo = re.sub(rf"^({'|'.join(PAROLE)})\b\s*", "", passo, flags=re.I)   # "Quando clicco" → "clicco"
    passo = passo.rstrip(" .")
    prima_parola = passo.split()[0] if passo else ""
    if len(prima_parola) > 1 and prima_parola[1].isupper():
        return passo                       # sigla (API, POST, URL): non la tocco
    return passo[:1].lower() + passo[1:]   # "Vedo il messaggio" → "vedo il messaggio"


def scenario_gherkin(scenario: Scenario) -> str:
    righe = [f"  @{scenario.tipo} @{scenario.livello} @{scenario.codice}",
             f"  Scenario: {scenario.titolo.strip().rstrip('.')}"]
    for parola, passi in (("Dato", scenario.dato), ("Quando", scenario.quando), ("Allora", scenario.allora)):
        for i, passo in enumerate(passi):
            righe.append(f"    {parola if i == 0 else 'E'} {pulisci_passo(passo)}")
    return "\n".join(righe)


def feature(titolo: str, scenari: list[Scenario], domande: list[str] | None = None) -> str:
    """Il file .feature completo. Le domande aperte vanno in fondo come commenti."""
    parti = ["# language: it", f"Funzionalità: {titolo}", ""]
    parti += [scenario_gherkin(s) + "\n" for s in scenari]
    if domande:
        parti += ["  # ---------- DOMANDE APERTE ----------"] + [f"  # {d}" for d in domande]
    return "\n".join(parti) + "\n"


# ---------- Prova veloce: python -m generatore.gherkin ----------

if __name__ == "__main__":
    prova = Scenario(
        codice="L3", tipo="negativo", livello="e2e",
        citazione="Con username o password errati compare lo stesso messaggio di errore...",
        titolo="Login con password errata.",
        dato=["@utente Dato che sono sulla pagina di login"],
        quando=["Quando eseguo il login con una password errata."],
        allora=["Vedo il messaggio di errore", "resto sulla pagina di login"],
    )
    print(feature("Login al gestionale", [prova], ["L12: Cosa succede dopo troppi tentativi errati?"]))
