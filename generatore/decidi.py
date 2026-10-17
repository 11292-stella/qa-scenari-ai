"""Passo A – un punto alla volta: il requisito parla di questo punto?

Due modi di chiederlo (si sceglie con il prompt):
  - CITAZIONE (prompt con {REQUISITO}, es. v2): l'AI copia la frase e dice sì/no,
    Python controlla che la frase esista davvero → se non esiste: INVENTA
  - RIGA (prompt con {RIGHE}, es. v3): Python numera le righe del requisito,
    l'AI sceglie solo un numero da lista chiusa (0 = nessuna riga ne parla)

Uso:
    python -m generatore.decidi requisiti/login.txt --prompt v2
    python -m generatore.decidi requisiti/login.txt --prompt v3
"""
import argparse
import json
import re
import time
from pathlib import Path

import ollama

from generatore.checklist import PuntoChecklist, leggi_checklist
from generatore.controlli import citazione_valida, controlla_segnaposto
from generatore.genera import nome_checklist
from generatore.schemas import Decisione, schema_riga

MODELLO = "qwen2.5:3b"
OPZIONI = {"temperature": 0, "num_ctx": 4096, "num_predict": 300}


def corpo_requisito(requisito: str) -> str:
    """Il requisito senza le righe 'Titolo:' e 'Checklist:', che non vanno citate."""
    righe = [r for r in requisito.splitlines() if not re.match(r"^(Titolo|Checklist):", r, re.IGNORECASE)]
    return "\n".join(righe).strip()


def righe_requisito(corpo: str) -> list[str]:
    """Le righe non vuote del requisito: la riga 1 è righe[0]."""
    return [r.strip() for r in corpo.splitlines() if r.strip()]


def codici_attesi(nome_requisito: str) -> set[str] | None:
    """I codici coperti secondo il MIO riferimento (tag @L.. in riferimenti/<nome>.feature)."""
    percorso = Path("riferimenti") / f"{nome_requisito}.feature"
    if not percorso.exists():
        return None
    return set(re.findall(r"@([A-Z]+\d+)\b", percorso.read_text(encoding="utf-8")))


def chiedi(prompt: str, schema) -> str:
    risposta = ollama.chat(
        model=MODELLO,
        messages=[{"role": "user", "content": prompt}],
        format=schema.model_json_schema(),
        options=OPZIONI,
    )
    return risposta.message.content


def decidi_con_citazione(modello_prompt: str, corpo: str, punto: PuntoChecklist) -> dict:
    prompt = modello_prompt.replace("{REQUISITO}", corpo).replace("{PUNTO}", f"{punto.codice}: {punto.cosa}")
    decisione = Decisione.model_validate_json(chiedi(prompt, Decisione))
    vera = citazione_valida(decisione.citazione, corpo)

    if decisione.ne_parla and vera:
        finale = "scenario"
    elif decisione.ne_parla:
        finale = "INVENTA"      # dice sì ma la frase non esiste nel requisito
    else:
        finale = "domanda"

    prova = "vera" if vera else ("falsa" if decisione.citazione else "-")
    return {"finale": finale, "ai": "sì" if decisione.ne_parla else "no", "prova": prova,
            "citazione": decisione.citazione}


def decidi_con_riga(modello_prompt: str, righe: list[str], punto: PuntoChecklist) -> dict:
    numerate = "\n".join(f"{n}. {riga}" for n, riga in enumerate(righe, start=1))
    prompt = modello_prompt.replace("{RIGHE}", numerate).replace("{PUNTO}", f"{punto.codice}: {punto.cosa}")
    Schema = schema_riga(len(righe))
    numero = Schema.model_validate_json(chiedi(prompt, Schema)).riga

    return {"finale": "scenario" if numero else "domanda", "ai": "sì" if numero else "no",
            "prova": f"riga {numero}" if numero else "-",
            "riga": numero, "testo_riga": righe[numero - 1] if numero else ""}


def main() -> None:
    parser = argparse.ArgumentParser(description="Passo A: il requisito parla di ogni punto?")
    parser.add_argument("requisito", help="es. requisiti/login.txt")
    parser.add_argument("--prompt", default="v3", help="versione del prompt (usa prompts/<versione>_decidi.md)")
    args = parser.parse_args()

    percorso = Path(args.requisito)
    testo = percorso.read_text(encoding="utf-8")
    corpo = corpo_requisito(testo)
    righe = righe_requisito(corpo)
    punti = leggi_checklist(nome_checklist(testo))
    attesi = codici_attesi(percorso.stem)

    file_prompt = Path(f"prompts/{args.prompt}_decidi.md")
    modello_prompt = file_prompt.read_text(encoding="utf-8")
    modo = "riga" if "{RIGHE}" in modello_prompt else "citazione"
    controlla_segnaposto(modello_prompt, file_prompt.name,
                         ["{RIGHE}" if modo == "riga" else "{REQUISITO}", "{PUNTO}"])

    print(f"Requisito: {percorso.name} | {len(punti)} punti | prompt: {file_prompt.stem} | modo: {modo}\n")
    print(f"{'punto':<6}{'AI':<8}{'prova':<11}{'finale':<10}{'atteso':<9}")

    risultati = []
    inizio = time.perf_counter()
    for punto in punti:
        if modo == "riga":
            esito = decidi_con_riga(modello_prompt, righe, punto)
        else:
            esito = decidi_con_citazione(modello_prompt, corpo, punto)

        atteso = "-" if attesi is None else ("scenario" if punto.codice in attesi else "domanda")
        # INVENTA è sempre un errore: l'AI ha detto "sì" senza una prova vera
        giusto = "" if atteso == "-" else (" ✅" if esito["finale"] == atteso else " ❌")
        print(f"{punto.codice:<6}{esito['ai']:<8}{esito['prova']:<11}{esito['finale']:<10}{atteso:<9}{giusto}")

        risultati.append({"codice": punto.codice, "atteso": atteso, **esito})

    durata = time.perf_counter() - inizio

    # Riepilogo
    print(f"\nTempo: {durata:.1f} s ({durata / len(punti):.1f} s a punto)")
    for nome in ("scenario", "domanda", "INVENTA"):
        print(f"{nome:<9}: {sum(r['finale'] == nome for r in risultati)}")
    if attesi is not None:
        giusti = sum(r["finale"] == r["atteso"] for r in risultati)
        print(f"Decisioni giuste: {giusti}/{len(punti)}")

    uscita = Path("risultati") / args.prompt
    uscita.mkdir(parents=True, exist_ok=True)
    file_json = uscita / f"{percorso.stem}_decisioni.json"
    file_json.write_text(json.dumps(risultati, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSalvato in {file_json}")


if __name__ == "__main__":
    main()