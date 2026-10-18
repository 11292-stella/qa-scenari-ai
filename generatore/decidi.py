"""Passo A – un punto alla volta: il requisito parla di questo punto?

Due modi di chiederlo (si sceglie con il prompt):
  - CITAZIONE (prompt con {REQUISITO}, es. v2): l'AI copia la frase e dice sì/no,
    Python controlla che la frase esista davvero → se non esiste: INVENTA
  - RIGA (prompt con {RIGHE}, es. v3): Python numera le righe del requisito,
    l'AI sceglie solo un numero da lista chiusa (0 = nessuna riga ne parla)

Uso:
    python -m generatore.decidi requisiti/login.txt --prompt v2
    python -m generatore.decidi requisiti/login.txt --prompt v3
    python -m generatore.decidi requisiti/login.txt --prompt v4 --ripetizioni 5
"""

import argparse
import json
import re
import time
from pathlib import Path

import ollama

from generatore import PROGETTO
from generatore.checklist import PuntoChecklist, leggi_checklist, leggi_checklist_multiple
from generatore.controlli import citazione_valida, controlla_segnaposto
from generatore.genera import nomi_checklist
from generatore.schemas import Decisione, schema_riga

MODELLO = "qwen2.5:3b"
OPZIONI = {"temperature": 0, "num_ctx": 4096, "num_predict": 300}


def corpo_requisito(requisito: str) -> str:
    """Il requisito senza le righe 'Titolo:' e 'Checklist:', che non vanno citate."""
    righe = [
        r
        for r in requisito.splitlines()
        if not re.match(r"^(Titolo|Checklist):", r, re.IGNORECASE)
    ]
    return "\n".join(righe).strip()


def righe_requisito(corpo: str) -> list[str]:
    """Le righe non vuote del requisito: la riga 1 è righe[0]."""
    return [r.strip() for r in corpo.splitlines() if r.strip()]


def leggi_riferimento(nome_requisito: str) -> dict[str, int | None] | None:
    """Dal MIO riferimento (riferimenti/<nome>.feature): {codice coperto: riga attesa}.

    Esempio di riga di tag:  @negativo @e2e @L3 @riga5  →  {"L3": 5}
    Se manca il tag @riga, la riga attesa è None (si controlla solo la decisione).
    """
    percorso = PROGETTO / "riferimenti" / f"{nome_requisito}.feature"
    if not percorso.exists():
        return None
    attesi: dict[str, int | None] = {}
    for riga in percorso.read_text(encoding="utf-8").splitlines():
        codici = re.findall(r"@([A-Z]+\d+)\b", riga)
        numero = re.search(r"@riga(\d+)\b", riga)
        for codice in codici:
            attesi[codice] = int(numero.group(1)) if numero else None
    return attesi


def chiedi(prompt: str, schema) -> str:
    risposta = ollama.chat(
        model=MODELLO,
        messages=[{"role": "user", "content": prompt}],
        format=schema.model_json_schema(),
        options=OPZIONI,
    )
    return risposta.message.content


def decidi_con_citazione(
    modello_prompt: str, corpo: str, punto: PuntoChecklist
) -> dict:
    prompt = modello_prompt.replace("{REQUISITO}", corpo).replace(
        "{PUNTO}", f"{punto.codice}: {punto.cosa}"
    )
    decisione = Decisione.model_validate_json(chiedi(prompt, Decisione))
    vera = citazione_valida(decisione.citazione, corpo)

    if decisione.ne_parla and vera:
        finale = "scenario"
    elif decisione.ne_parla:
        finale = "INVENTA"  # dice sì ma la frase non esiste nel requisito
    else:
        finale = "domanda"

    prova = "vera" if vera else ("falsa" if decisione.citazione else "-")
    return {
        "finale": finale,
        "ai": "sì" if decisione.ne_parla else "no",
        "prova": prova,
        "citazione": decisione.citazione,
    }


def decidi_con_riga(
    modello_prompt: str, righe: list[str], punto: PuntoChecklist
) -> dict:
    numerate = "\n".join(f"{n}. {riga}" for n, riga in enumerate(righe, start=1))
    prompt = modello_prompt.replace("{RIGHE}", numerate).replace(
        "{PUNTO}", f"{punto.codice}: {punto.cosa}"
    )
    Schema = schema_riga(len(righe))
    numero = Schema.model_validate_json(chiedi(prompt, Schema)).riga

    return {
        "finale": "scenario" if numero else "domanda",
        "ai": "sì" if numero else "no",
        "prova": f"riga {numero}" if numero else "-",
        "riga": numero,
        "testo_riga": righe[numero - 1] if numero else "",
    }


def valuta_esito(
    esito: dict, punto: PuntoChecklist, attesi: dict | None, modo: str
) -> dict:
    """Confronta un esito con il MIO riferimento: ✅, ⚠️ riga sbagliata, ❌ (o "" se non c'è riferimento)."""
    if attesi is None:
        return {"atteso": "-", "riga_attesa": None, "giusto": ""}
    atteso = "scenario" if punto.codice in attesi else "domanda"
    riga_attesa = attesi.get(punto.codice)
    # INVENTA è sempre un errore: l'AI ha detto "sì" senza una prova vera
    if esito["finale"] != atteso:
        giusto = "❌"
    elif (
        atteso == "scenario"
        and modo == "riga"
        and riga_attesa
        and esito["riga"] != riga_attesa
    ):
        giusto = "⚠️ riga sbagliata"  # decisione giusta, ma per il motivo sbagliato
    else:
        giusto = "✅"
    return {"atteso": atteso, "riga_attesa": riga_attesa, "giusto": giusto}


def esegui(
    punti, modo, modello_prompt, corpo, righe, attesi, stampa: bool
) -> list[dict]:
    """Un giro completo su tutti i punti della checklist."""
    risultati = []
    for punto in punti:
        if modo == "riga":
            esito = decidi_con_riga(modello_prompt, righe, punto)
        else:
            esito = decidi_con_citazione(modello_prompt, corpo, punto)
        esito = {
            "codice": punto.codice,
            **valuta_esito(esito, punto, attesi, modo),
            **esito,
        }

        if stampa:
            colonna_atteso = esito["atteso"] + (
                f" riga {esito['riga_attesa']}" if esito["riga_attesa"] else ""
            )
            print(
                f"{punto.codice:<6}{esito['ai']:<8}{esito['prova']:<11}{esito['finale']:<10}"
                f"{colonna_atteso:<18} {esito['giusto']}"
            )
        risultati.append(esito)
    return risultati


def scarica_modello() -> None:
    """Toglie il modello dalla memoria: al giro dopo Ollama lo ricarica da zero.

    Serve perché le risposte cambiano soprattutto tra un caricamento e l'altro
    (Ollama scarica il modello dopo 5 minuti di inattività): se lo lasciassimo
    caricato, tutti i giri sembrerebbero stabili anche quando non lo sono.
    """
    ollama.generate(model=MODELLO, keep_alive=0)


def conta(risultati: list[dict]) -> tuple[int, int]:
    """(decisioni giuste sì/no, giuste anche nella riga)"""
    decisioni = sum(r["finale"] == r["atteso"] for r in risultati)
    complete = sum(r["giusto"] == "✅" for r in risultati)
    return decisioni, complete


def risposta_breve(esito: dict) -> str:
    """Come ha risposto l'AI, in breve: 'riga 2', 'no', 'INVENTA'..."""
    if esito["finale"] == "domanda":
        return "no"
    return esito["prova"] if esito["prova"].startswith("riga") else esito["finale"]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Passo A: il requisito parla di ogni punto?"
    )
    parser.add_argument("requisito", help="es. requisiti/login.txt")
    parser.add_argument(
        "--prompt",
        default="v3",
        help="versione del prompt (usa prompts/<versione>_decidi.md)",
    )
    parser.add_argument(
        "--ripetizioni",
        type=int,
        default=1,
        help="quante volte ripetere tutto (ricaricando il modello ogni volta): "
        "con più di 1 mostra media e punti instabili",
    )
    args = parser.parse_args()

    percorso = Path(args.requisito)
    testo = percorso.read_text(encoding="utf-8")
    corpo = corpo_requisito(testo)
    righe = righe_requisito(corpo)
    punti = leggi_checklist_multiple(nomi_checklist(testo))
    attesi = leggi_riferimento(percorso.stem)

    file_prompt = PROGETTO / "prompts" / f"{args.prompt}_decidi.md"
    modello_prompt = file_prompt.read_text(encoding="utf-8")
    modo = "riga" if "{RIGHE}" in modello_prompt else "citazione"
    controlla_segnaposto(
        modello_prompt,
        file_prompt.name,
        ["{RIGHE}" if modo == "riga" else "{REQUISITO}", "{PUNTO}"],
    )

    n = args.ripetizioni
    print(
        f"Requisito: {percorso.name} | {len(punti)} punti | prompt: {file_prompt.stem} "
        f"| modo: {modo} | ripetizioni: {n}\n"
    )
    if n == 1:
        print(f"{'punto':<6}{'AI':<8}{'prova':<11}{'finale':<10}{'atteso':<18}")

    giri = []
    inizio = time.perf_counter()
    for giro in range(1, n + 1):
        if n > 1:
            if giro > 1:
                scarica_modello()
            print(f"Giro {giro}/{n}...", end=" ", flush=True)
        risultati = esegui(
            punti, modo, modello_prompt, corpo, righe, attesi, stampa=(n == 1)
        )
        giri.append(risultati)
        if n > 1 and attesi is not None:
            decisioni, complete = conta(risultati)
            print(
                f"decisioni {decisioni}/{len(punti)}, con la riga giusta {complete}/{len(punti)}"
            )
    durata = time.perf_counter() - inizio

    # Con più giri: tabella dei punti, con quante volte sono giusti e le risposte diverse
    instabili = []
    if n > 1:
        print(f"\n{'punto':<6}{'atteso':<18}{'giusto':<9}risposte dell'AI")
        for i, punto in enumerate(punti):
            esiti = [g[i] for g in giri]
            risposte = [risposta_breve(e) for e in esiti]
            diverse = {r: risposte.count(r) for r in dict.fromkeys(risposte)}
            giusti = sum(e["giusto"] == "✅" for e in esiti)
            atteso = esiti[0]["atteso"] + (
                f" riga {esiti[0]['riga_attesa']}" if esiti[0]["riga_attesa"] else ""
            )
            segno = "  ← instabile" if len(diverse) > 1 else ""
            if len(diverse) > 1:
                instabili.append(punto.codice)
            print(
                f"{punto.codice:<6}{atteso:<18}{giusti}/{n:<7}"
                f"{', '.join(f'{r} ×{c}' for r, c in diverse.items())}{segno}"
            )

    # Riepilogo
    print(f"\nTempo: {durata:.1f} s ({durata / (len(punti) * n):.1f} s a punto)")
    if n == 1:
        for nome in ("scenario", "domanda", "INVENTA"):
            print(f"{nome:<9}: {sum(r['finale'] == nome for r in giri[0])}")
    if attesi is not None:
        conteggi = [conta(g) for g in giri]
        for indice, nome in (
            (0, "Decisioni giuste (sì/no)"),
            (1, "Giuste anche nella riga (vere)"),
        ):
            if indice == 1 and modo != "riga":
                continue
            valori = [c[indice] for c in conteggi]
            if n == 1:
                print(f"{nome + ':':<33}{valori[0]}/{len(punti)}")
            else:
                print(
                    f"{nome + ':':<33}media {sum(valori) / n:.1f}/{len(punti)}  (min {min(valori)}, max {max(valori)})"
                )
    if n > 1:
        print(f"Punti instabili: {len(instabili)}  →  {', '.join(instabili) or '-'}")

    uscita = PROGETTO / "risultati" / args.prompt
    uscita.mkdir(parents=True, exist_ok=True)
    nome_file = (
        f"{percorso.stem}_decisioni.json"
        if n == 1
        else f"{percorso.stem}_decisioni_x{n}.json"
    )
    file_json = uscita / nome_file
    dati = (
        giri[0] if n == 1 else {"ripetizioni": n, "instabili": instabili, "giri": giri}
    )
    file_json.write_text(
        json.dumps(dati, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nSalvato in {file_json}")


if __name__ == "__main__":
    main()
