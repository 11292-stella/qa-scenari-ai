"""Il generatore come SERVIZIO: una funzione che riceve un requisito e restituisce tutto come dati.

Non stampa niente e non legge argomenti da terminale: così la può usare chiunque,
per esempio una pagina Django.

    from generatore.servizio import analizza
    analisi = analizza("Login del negozio", testo_requisito, checklist="login")
    analisi.scenari, analisi.domande, analisi.feature ...
"""

import io
import time
import zipfile
from dataclasses import dataclass, field
from typing import Callable

from generatore import PROGETTO
from generatore.checklist import leggi_checklist_multiple, esempio_per
from generatore.controlli import controlla_segnaposto, trova_simili
from generatore.decidi import corpo_requisito, decidi_con_riga, righe_requisito
from generatore.gherkin import feature, scenario_gherkin
from generatore.scheletri import file_completi, per_scenario
from generatore.schemas import Scenario
from generatore.scrivi import scrivi_scenario

CARTELLA_PROMPT = PROGETTO / "prompts"

# Le versioni MIGLIORI, scelte misurando (vedi il diario in PROGRESS.md). Le altre restano in prompts/
# come storia degli esperimenti: si possono ancora scegliere dal form, sotto "Opzioni avanzate".
PROMPT_DECIDI = "v4"      # v5 provata il 18/10: dice "sì" a quasi tutto (10/32 contro 26/32)
PROMPT_SCENARIO = "s3"


@dataclass
class Decisione:
    codice: str
    cosa: str
    tipo: str
    livelli: tuple[str, ...]
    riga: int  # 0 = il requisito non ne parla
    testo_riga: str

    @property
    def coperto(self) -> bool:
        return self.riga > 0


@dataclass
class Analisi:
    titolo: str
    checklist: str          # per mostrarla: "ordini + ordini_importi"
    area: str               # la prima checklist: dà il nome agli scheletri (OrdiniPage, ordini_page.resource)
    prompt_decidi: str
    prompt_scenario: str
    righe: list[str]
    decisioni: list[Decisione] = field(default_factory=list)
    scenari: list[Scenario] = field(default_factory=list)
    avvisi: dict[str, list[str]] = field(default_factory=dict)
    non_scritti: list[str] = field(default_factory=list)
    simili: dict[str, str] = field(default_factory=dict)   # codice → codice dello scenario quasi uguale
    secondi: float = 0.0

    @property
    def domande(self) -> list[str]:
        """Per ora le domande aperte sono i punti non coperti (le domande vere arriveranno dopo)."""
        domande = [f"{d.codice}: {d.cosa}" for d in self.decisioni if not d.coperto]
        domande += [f"{d.codice}: {d.cosa} (riga {d.riga}, ma il modello non ha scritto uno scenario valido: "
                    f"scrivilo a mano)" for d in self.decisioni if d.codice in self.non_scritti]
        return domande

    @property
    def feature(self) -> str:
        return feature(self.titolo, self.scenari, self.domande)

    def schede(self) -> list[dict]:
        """Per ogni scenario: il Gherkin e lo scheletro nei tre framework (per i bottoni della pagina)."""
        return [{"scenario": s, "gherkin": scenario_gherkin(s), "codice": per_scenario(s, self.area),
                 "avvisi": self.avvisi.get(s.codice, []), "simile_a": self.simili.get(s.codice),
                 # quanti tentativi sono stati corretti, e se alla fine lo scenario è a posto o va controllato
                 "correzioni": sum(a.startswith("Tentativo") for a in self.avvisi.get(s.codice, [])),
                 "non_risolto": any(a.startswith("Problemi non risolti") for a in self.avvisi.get(s.codice, []))}
                for s in self.scenari]

    def zip_scheletri(self) -> bytes:
        """Uno zip con il .feature e gli scheletri completi: playwright/, robot/, appium/."""
        memoria = io.BytesIO()
        with zipfile.ZipFile(memoria, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("scenari.feature", self.feature)
            z.writestr("LEGGIMI.txt", LEGGIMI)
            for nome, testo in file_completi(self.titolo, self.scenari, self.area).items():
                z.writestr(nome, testo)
        return memoria.getvalue()


LEGGIMI = """Scheletri generati da QA Scenari AI

playwright/  pages/<Area>Page.py + tests/test_<area>.py     (pytest + pytest-playwright)
robot/       resources/<area>_page.resource + tests/<area>.robot   (Browser Library)
appium/      pages/<Area>Page.java + tests/<Area>Test.java  (TestNG, senza Cucumber)

Ogni metodo / keyword e' un TODO che FALLISCE apposta: uno scheletro che passa senza
fare niente sarebbe un falso verde. Completa locator e corpi, poi il test diventa vero.
Gli scenari @unit non sono generati: vanno testati nel progetto frontend.
"""


# ---------- Cosa si può scegliere ----------


def checklist_disponibili() -> list[str]:
    """I nomi delle checklist in checklist/ (es. ["login"])."""
    return sorted(p.stem for p in (PROGETTO / "checklist").glob("*.md"))


def prompt_disponibili(tipo: str) -> list[str]:
    """Le versioni dei prompt: tipo "decidi" (solo modo riga) o "scenario". Es. ["v3", "v4"]."""
    versioni = []
    for p in sorted(CARTELLA_PROMPT.glob(f"*_{tipo}.md")):
        if tipo == "decidi" and "{RIGHE}" not in p.read_text(encoding="utf-8"):
            continue  # il servizio usa solo il modo riga (v3, v4...), non la citazione (v2)
        versioni.append(p.stem.removesuffix(f"_{tipo}"))
    return versioni


def leggi_prompt(versione: str, tipo: str, segnaposto: list[str]) -> str:
    file_prompt = CARTELLA_PROMPT / f"{versione}_{tipo}.md"
    testo = file_prompt.read_text(encoding="utf-8")
    controlla_segnaposto(testo, file_prompt.name, segnaposto)
    return testo


# ---------- L'analisi completa ----------


def analizza(
    titolo: str,
    requisito: str,
    checklist: str | list[str],
    prompt_decidi: str = PROMPT_DECIDI,
    prompt_scenario: str = PROMPT_SCENARIO,
    avanzamento: Callable[[str], None] | None = None,
) -> Analisi:
    """Passo A + passo B su un requisito. `avanzamento` (facoltativo) riceve messaggi tipo "L3 (5/32)"."""
    avvisa = avanzamento or (lambda messaggio: None)

    righe = righe_requisito(corpo_requisito(requisito))
    if not righe:
        raise ValueError("Il requisito è vuoto")
    nomi = [checklist] if isinstance(checklist, str) else list(checklist)
    if not nomi:
        raise ValueError("Scegli almeno una checklist")
    punti = leggi_checklist_multiple(nomi)
    testo_decidi = leggi_prompt(prompt_decidi, "decidi", ["{RIGHE}", "{PUNTO}"])
    testo_scenario = leggi_prompt(
        prompt_scenario, "scenario", ["{PUNTO}", "{RIGA}", "{LIVELLI}"]
    )

    analisi = Analisi(
        titolo=titolo.strip() or "Senza titolo",
        checklist=" + ".join(nomi),
        area=nomi[0],
        prompt_decidi=prompt_decidi,
        prompt_scenario=prompt_scenario,
        righe=righe,
    )
    inizio = time.perf_counter()

    # Passo A: per ogni punto, quale riga ne parla?
    for i, punto in enumerate(punti, start=1):
        avvisa(f"Passo A: {punto.codice} ({i}/{len(punti)})")
        esito = decidi_con_riga(testo_decidi, righe, punto)
        analisi.decisioni.append(
            Decisione(
                punto.codice,
                punto.cosa,
                punto.tipo,
                punto.livelli,
                esito.get("riga", 0),
                esito.get("testo_riga", ""),
            )
        )

    # Passo B: uno scenario per ogni punto coperto
    coperti = [(d, p) for d, p in zip(analisi.decisioni, punti) if d.coperto]
    for i, (decisione, punto) in enumerate(coperti, start=1):
        avvisa(f"Passo B: {punto.codice} ({i}/{len(coperti)})")
        scenario, avvisi = scrivi_scenario(testo_scenario, punto, decisione.testo_riga, esempio_per(punto))
        if avvisi:
            analisi.avvisi[punto.codice] = avvisi
        if scenario is None:
            analisi.non_scritti.append(punto.codice)   # il punto finisce tra le domande, con un avviso
        else:
            analisi.scenari.append(scenario)

    analisi.simili = trova_simili(analisi.scenari)
    analisi.secondi = time.perf_counter() - inizio
    return analisi


# ---------- Prova veloce: python -m generatore.servizio requisiti/login.txt ----------

if __name__ == "__main__":
    import sys
    from pathlib import Path

    from generatore.genera import nomi_checklist

    testo = Path(sys.argv[1]).read_text(encoding="utf-8")
    risultato = analizza(
        "Prova dal terminale", testo, nomi_checklist(testo), avanzamento=print
    )
    print(
        f"\n{len(risultato.scenari)} scenari, {len(risultato.domande)} domande, {risultato.secondi:.1f} s\n"
    )
    print(risultato.feature)
