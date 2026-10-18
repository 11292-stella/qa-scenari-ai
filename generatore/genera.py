"""Prima generazione: requisito + checklist + prompt → Ollama → JSON validato.

Uso:
    python -m generatore.genera requisiti/login.txt --prompt v1

Salva:
    risultati/v1/login.json          → la risposta valida
    risultati/v1/login_grezza.txt    → la risposta così com'è, se lo schema la rifiuta
"""

import argparse
import re
import time
from pathlib import Path

import ollama
from pydantic import BaseModel, ValidationError

from generatore import PROGETTO
from generatore.checklist import PuntoChecklist, leggi_checklist
from generatore.controlli import controlla_segnaposto
from generatore.schemas import schema_risposta

MODELLO = "qwen2.5:3b"
OPZIONI = {
    "temperature": 0,  # stessa domanda → stessa risposta: serve per confrontare i prompt
    "num_ctx": 8192,  # memoria: requisito + checklist devono entrarci tutti
    "num_predict": 4096,  # lunghezza massima della risposta
}


def nome_checklist(requisito: str) -> str:
    """Legge la riga 'Checklist: login' in cima al requisito."""
    trovata = re.search(r"^Checklist:\s*(\w+)", requisito, re.MULTILINE | re.IGNORECASE)
    if not trovata:
        raise ValueError("Nel requisito manca la riga 'Checklist: <nome>'")
    return trovata.group(1).lower()


def nomi_checklist(requisito: str) -> list[str]:
    """Legge 'Checklist: ordini, ordini_importi' in cima al requisito (una o più, separate da virgole)."""
    trovata = re.search(r"^Checklist:\s*(.+)$", requisito, re.MULTILINE | re.IGNORECASE)
    if not trovata:
        raise ValueError("Nel requisito manca la riga 'Checklist: <nome>'")
    return [n.strip().lower() for n in trovata.group(1).split(",") if n.strip()]


def testo_punti(punti: list[PuntoChecklist]) -> str:
    """I punti in forma breve per il prompt (senza il tipo: lo aggiunge Python)."""
    return "\n".join(
        f"- {p.codice}: {p.cosa} (livelli: {', '.join(p.livelli)})" for p in punti
    )


def prepara_prompt(versione: str, requisito: str, punti: list[PuntoChecklist]) -> str:
    """Legge prompts/<versione>.md e riempie i segnaposto."""
    file_prompt = PROGETTO / "prompts" / f"{versione}.md"
    modello_prompt = file_prompt.read_text(encoding="utf-8")
    controlla_segnaposto(modello_prompt, file_prompt.name, ["{REQUISITO}", "{PUNTI}"])
    return modello_prompt.replace("{REQUISITO}", requisito.strip()).replace(
        "{PUNTI}", testo_punti(punti)
    )


def chiedi_al_modello(
    prompt: str, schema: type[BaseModel], modello: str = MODELLO
) -> str:
    """Manda il prompt a Ollama obbligandolo a rispondere con la forma dello schema."""
    risposta = ollama.chat(
        model=modello,
        messages=[{"role": "user", "content": prompt}],
        format=schema.model_json_schema(),
        options=OPZIONI,
    )
    return risposta.message.content


def riepilogo(risultato, punti: list[PuntoChecklist]) -> None:
    in_scenari = [s.codice for s in risultato.scenari]
    in_domande = [d.codice for d in risultato.domande]
    saltati = [p.codice for p in punti if p.codice not in in_scenari + in_domande]

    print(f"\nScenari: {len(in_scenari)}  →  {', '.join(in_scenari) or '-'}")
    print(f"Domande: {len(in_domande)}  →  {', '.join(in_domande) or '-'}")
    print(f"Punti saltati: {len(saltati)}  →  {', '.join(saltati) or '-'}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Genera scenari di test da un requisito"
    )
    parser.add_argument("requisito", help="es. requisiti/login.txt")
    parser.add_argument(
        "--prompt", default="v1", help="versione del prompt (default: v1)"
    )
    args = parser.parse_args()

    percorso = Path(args.requisito)
    requisito = percorso.read_text(encoding="utf-8")
    punti = leggi_checklist(nome_checklist(requisito))
    Risposta = schema_risposta([p.codice for p in punti])
    prompt = prepara_prompt(args.prompt, requisito, punti)

    uscita = PROGETTO / "risultati" / args.prompt
    uscita.mkdir(parents=True, exist_ok=True)

    print(
        f"Requisito: {percorso.name} | checklist: {len(punti)} punti | prompt: {args.prompt}"
    )
    print("Invio al modello... (può volerci qualche minuto)")
    inizio = time.perf_counter()
    grezza = chiedi_al_modello(prompt, Risposta)
    print(f"Risposta in {time.perf_counter() - inizio:.1f} s")

    try:
        risultato = Risposta.model_validate_json(grezza)
    except ValidationError as errore:
        file_grezzo = uscita / f"{percorso.stem}_grezza.txt"
        file_grezzo.write_text(grezza, encoding="utf-8")
        print(
            f"❌ La risposta non rispetta lo schema ({errore.error_count()} errori). Salvata in {file_grezzo}"
        )
        for e in errore.errors()[:10]:
            print("  -", ".".join(str(p) for p in e["loc"]), "→", e["msg"])
        return

    file_json = uscita / f"{percorso.stem}.json"
    file_json.write_text(risultato.model_dump_json(indent=2), encoding="utf-8")
    print(f"✅ Risposta valida, salvata in {file_json}")
    riepilogo(risultato, punti)


if __name__ == "__main__":
    main()
