"""Passo B – per ogni punto a cui il passo A ha dato una riga, l'AI scrive lo scenario
partendo SOLO da quella riga.

Uso:
    python -m generatore.scrivi requisiti/login.txt --decisioni v4 --prompt s1

Legge:  risultati/v4/login_decisioni.json        (le decisioni del passo A)
        prompts/s1_scenario.md                   (il prompt dello scenario)
Salva:  risultati/v4/login_scenari_s1.json       (i dati)
        risultati/v4/login_scenari_s1.feature    (il Gherkin, scritto da Python)
"""
import argparse
import json
import re
import time
from pathlib import Path

import ollama

from generatore import PROGETTO
from generatore.checklist import PuntoChecklist, leggi_checklist
from generatore.controlli import controlla_segnaposto
from generatore.genera import nome_checklist
from generatore.gherkin import feature, scenario_gherkin
from generatore.schemas import Scenario, schema_scenario

MODELLO = "qwen2.5:3b"
OPZIONI = {"temperature": 0, "num_ctx": 4096, "num_predict": 500}


def scrivi_scenario(modello_prompt: str, punto: PuntoChecklist, testo_riga: str) -> Scenario:
    """L'AI scrive lo scenario di UN punto partendo dalla riga; Python aggiunge codice, tipo e citazione."""
    Schema = schema_scenario(punto.livelli)
    prompt = (modello_prompt
              .replace("{PUNTO}", f"{punto.codice}: {punto.cosa}")
              .replace("{RIGA}", testo_riga)
              .replace("{LIVELLI}", ", ".join(punto.livelli)))
    risposta = ollama.chat(
        model=MODELLO,
        messages=[{"role": "user", "content": prompt}],
        format=Schema.model_json_schema(),
        options=OPZIONI,
    )
    scritto = Schema.model_validate_json(risposta.message.content)
    return Scenario(codice=punto.codice, tipo=punto.tipo, citazione=testo_riga, **scritto.model_dump())


def livelli_attesi(nome_requisito: str) -> dict[str, str]:
    """Dal MIO riferimento: {codice: livello}, es. @negativo @e2e @L3 → {"L3": "e2e"}."""
    percorso = PROGETTO / "riferimenti" / f"{nome_requisito}.feature"
    if not percorso.exists():
        return {}
    attesi = {}
    for riga in percorso.read_text(encoding="utf-8").splitlines():
        codice = re.search(r"@([A-Z]+\d+)\b", riga)
        livello = re.search(r"@(unit|api|e2e)\b", riga)
        if codice and livello:
            attesi[codice.group(1)] = livello.group(1)
    return attesi


def main() -> None:
    parser = argparse.ArgumentParser(description="Passo B: scrive gli scenari dei punti coperti")
    parser.add_argument("requisito", help="es. requisiti/login.txt")
    parser.add_argument("--decisioni", default="v4", help="versione del passo A da cui partire (default: v4)")
    parser.add_argument("--prompt", default="s1", help="versione del prompt dello scenario (default: s1)")
    args = parser.parse_args()

    percorso = Path(args.requisito)
    testo = percorso.read_text(encoding="utf-8")
    titolo = re.search(r"^Titolo:\s*(.+)$", testo, re.MULTILINE)
    titolo = titolo.group(1).strip() if titolo else percorso.stem
    punti = {p.codice: p for p in leggi_checklist(nome_checklist(testo))}

    file_decisioni = PROGETTO / "risultati" / args.decisioni / f"{percorso.stem}_decisioni.json"
    if not file_decisioni.exists():
        raise FileNotFoundError(f"Manca {file_decisioni}: lancia prima il passo A "
                                f"(python -m generatore.decidi {args.requisito} --prompt {args.decisioni})")
    decisioni = json.loads(file_decisioni.read_text(encoding="utf-8"))
    da_scrivere = [d for d in decisioni if d["finale"] == "scenario" and d.get("riga")]

    file_prompt = PROGETTO / "prompts" / f"{args.prompt}_scenario.md"
    modello_prompt = file_prompt.read_text(encoding="utf-8")
    controlla_segnaposto(modello_prompt, file_prompt.name, ["{PUNTO}", "{RIGA}", "{LIVELLI}"])

    attesi = livelli_attesi(percorso.stem)
    print(f"Requisito: {percorso.name} | decisioni: {args.decisioni} | prompt: {file_prompt.stem} "
          f"| scenari da scrivere: {len(da_scrivere)}\n")

    scenari: list[Scenario] = []
    inizio = time.perf_counter()
    for decisione in da_scrivere:
        punto = punti[decisione["codice"]]
        scenario = scrivi_scenario(modello_prompt, punto, decisione["testo_riga"])
        scenari.append(scenario)

        livello_atteso = attesi.get(punto.codice)
        nota = "" if not livello_atteso else (
            "   livello ✅" if scenario.livello == livello_atteso else f"   livello ❌ (atteso {livello_atteso})")
        print(f"# riga {decisione['riga']}: {decisione['testo_riga']}{nota}")
        print(scenario_gherkin(scenario) + "\n")

    durata = time.perf_counter() - inizio
    domande = [f"{d['codice']}: {punti[d['codice']].cosa}" for d in decisioni if d["finale"] != "scenario"]

    uscita = PROGETTO / "risultati" / args.decisioni
    base = uscita / f"{percorso.stem}_scenari_{args.prompt}"
    base.with_suffix(".json").write_text(
        json.dumps([s.model_dump() for s in scenari], ensure_ascii=False, indent=2), encoding="utf-8")
    base.with_suffix(".feature").write_text(feature(titolo, scenari, domande), encoding="utf-8")

    print(f"Tempo: {durata:.1f} s ({durata / max(len(scenari), 1):.1f} s a scenario)")
    print(f"Salvati {len(scenari)} scenari in {base}.json e {base}.feature")


if __name__ == "__main__":
    main()
