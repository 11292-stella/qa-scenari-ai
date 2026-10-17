"""Prova a mano del prompt v0: nessun controllo, solo per vedere cosa risponde il modello."""
from pathlib import Path

import ollama

ISTRUZIONI = """Sei una tester. Leggi il REQUISITO e la CHECKLIST.
Per ogni punto della checklist: se il requisito ne parla, scrivi uno scenario Gherkin in italiano
con i tag tipo, livello e codice (es. @negativo @api @L5).
Se il requisito non ne parla, scrivi una domanda aperta."""

requisito = Path("requisiti/login.txt").read_text(encoding="utf-8")
checklist = Path("checklist/login.md").read_text(encoding="utf-8")

prompt = f"{ISTRUZIONI}\n\nREQUISITO:\n{requisito}\n\nCHECKLIST:\n{checklist}"

print("Invio al modello... (può volerci qualche minuto)")
risposta = ollama.chat(
    model="qwen2.5:3b",
    messages=[{"role": "user", "content": prompt}],
    options={"num_ctx": 8192, "num_predict": 3000},
)

testo = risposta.message.content
Path("risultati/prova_v0.txt").write_text(testo, encoding="utf-8")
print(testo)
print("\nSalvato in risultati/prova_v0.txt")