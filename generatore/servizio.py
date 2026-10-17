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
from generatore.checklist import leggi_checklist
from generatore.controlli import controlla_segnaposto
from generatore.decidi import corpo_requisito, decidi_con_riga, righe_requisito
from generatore.gherkin import feature, scenario_gherkin
from generatore.scheletri import file_completi, per_scenario
from generatore.schemas import Scenario
from generatore.scrivi import scrivi_scenario

CARTELLA_PROMPT = PROGETTO / "prompts"


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
    checklist: str
    prompt_decidi: str
    prompt_scenario: str
    righe: list[str]
    decisioni: list[Decisione] = field(default_factory=list)
    scenari: list[Scenario] = field(default_factory=list)
    secondi: float = 0.0

    @property
    def domande(self) -> list[str]:
        """Per ora le domande aperte sono i punti non coperti (le domande vere arriveranno dopo)."""
        return [f"{d.codice}: {d.cosa}" for d in self.decisioni if not d.coperto]

    @property
    def feature(self) -> str:
        return feature(self.titolo, self.scenari, self.domande)

    def schede(self) -> list[dict]:
        """Per ogni scenario: il Gherkin e lo scheletro nei tre framework (per i bottoni della pagina)."""
        return [{"scenario": s, "gherkin": scenario_gherkin(s), "codice": per_scenario(s, self.checklist)}
                for s in self.scenari]

    def zip_scheletri(self) -> bytes:
        """Uno zip con il .feature e gli scheletri completi: playwright/, robot/, appium/."""
        memoria = io.BytesIO()
        with zipfile.ZipFile(memoria, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("scenari.feature", self.feature)
            z.writestr("LEGGIMI.txt", LEGGIMI)
            for nome, testo in file_completi(self.titolo, self.scenari, self.checklist).items():
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
    checklist: str,
    prompt_decidi: str = "v4",
    prompt_scenario: str = "s1",
    avanzamento: Callable[[str], None] | None = None,
) -> Analisi:
    """Passo A + passo B su un requisito. `avanzamento` (facoltativo) riceve messaggi tipo "L3 (5/32)"."""
    avvisa = avanzamento or (lambda messaggio: None)

    righe = righe_requisito(corpo_requisito(requisito))
    if not righe:
        raise ValueError("Il requisito è vuoto")
    punti = leggi_checklist(checklist)
    testo_decidi = leggi_prompt(prompt_decidi, "decidi", ["{RIGHE}", "{PUNTO}"])
    testo_scenario = leggi_prompt(
        prompt_scenario, "scenario", ["{PUNTO}", "{RIGA}", "{LIVELLI}"]
    )

    analisi = Analisi(
        titolo=titolo.strip() or "Senza titolo",
        checklist=checklist,
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
        analisi.scenari.append(
            scrivi_scenario(testo_scenario, punto, decisione.testo_riga)
        )

    analisi.secondi = time.perf_counter() - inizio
    return analisi


# ---------- Prova veloce: python -m generatore.servizio requisiti/login.txt ----------

if __name__ == "__main__":
    import sys
    from pathlib import Path

    from generatore.genera import nome_checklist

    testo = Path(sys.argv[1]).read_text(encoding="utf-8")
    risultato = analizza(
        "Prova dal terminale", testo, nome_checklist(testo), avanzamento=print
    )
    print(
        f"\n{len(risultato.scenari)} scenari, {len(risultato.domande)} domande, {risultato.secondi:.1f} s\n"
    )
    print(risultato.feature)