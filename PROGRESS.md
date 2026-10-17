# PROGRESS – QA Scenari AI

> Strumento **locale** che legge un **requisito** scritto in italiano e genera **scenari di test in Gherkin** (Given/When/Then) con un modello AI piccolo (Ollama).
> Poi **misura** quale versione del prompt funziona meglio, usando come riferimento gli scenari che ho scritto io a mano.

Nato da: job-agent (ho riusato le idee che funzionavano: JSON con schema, lista chiusa, ciclo di correzione).
Ultimo aggiornamento: 17 ottobre 2026

---

## 1. Perché questo progetto

Voglio dimostrare che so **gestire un'AI**, e non solo usarla:
- scrivere prompt con regole ed esempi;
- obbligare l'AI a rispondere in un formato preciso (JSON);
- controllare automaticamente le risposte e farle correggere;
- **misurare** se un prompt è migliore di un altro, con numeri.

Il tema è il QA, che è il mio lavoro: l'AI fa il primo lavoro della tester (legge il requisito e pensa a cosa testare), io controllo e misuro.

---

## 2. Decisioni prese

| Tema | Decisione | Motivo |
|---|---|---|
| Modello AI | **Ollama** in locale con **`qwen2.5:3b`** | gratis, niente API key; il 3b sta nella GPU (RTX 2050, 4 GB) |
| Formato della risposta | **JSON con schema** (Pydantic), con `Literal` per il tipo di scenario | il 3b sbaglia meno se deve riempire campi precisi |
| Gherkin | Lo scrive **Python** partendo dal JSON | la sintassi è sempre corretta; l'AI pensa ai casi, Python impagina |
| Prompt | Un file per versione in `prompts/` (v1, v2, v3…) | così posso confrontarle e vedere cosa è cambiato |
| Riferimenti | Scenari scritti **a mano** da me in `riferimenti/` | sono la "risposta giusta" per misurare l'AI |
| Copertura | Per ogni requisito, una lista di **casi attesi** con parole chiave | confronto deterministico in Python, niente AI che giudica l'AI |
| Esecuzione | Gli scenari **non vengono eseguiti** | il progetto misura la qualità del prompt, non dell'app |
| Chat web di Claude | **Niente automazione** | non permessa dalle condizioni d'uso |

---

## 3. Architettura

```
requisiti/carrello.txt  (requisito in italiano)
   │
   ▼
[Python] genera.py  → legge il requisito + prompts/vX.md
   │
   ▼
[AI qwen2.5:3b]     → risponde in JSON: lista di scenari (titolo, tipo, given, when, then)
   │
   ▼
[Python] schemas.py → Pydantic controlla il formato
[Python] controlli.py → almeno 1 positivo, 1 negativo, 1 limite; passi non vuoti; niente doppioni
         ↺ se ci sono problemi: rimando gli errori all'AI (max 3 tentativi)
   │
   ▼
[Python] gherkin.py → scrive risultati/vX/carrello.feature
   │
   ▼
[Python] valuta.py  → confronta con riferimenti/ e scrive il report:
                      "v1: 40% casi negativi trovati — v3: 90%"
```

---

## 4. Stack

| Parte | Tecnologia | La conoscevo già? |
|---|---|---|
| Linguaggio | Python | ✅ |
| Modello AI | Ollama + qwen2.5:3b | ✅ (job-agent) |
| Validazione JSON | Pydantic | ✅ (job-agent) |
| Formato scenari | Gherkin | ✅ (Cucumber sul kiosk) |
| Test | pytest | ✅ |
| CI | GitHub Actions | ✅ |

---

## 5. Struttura delle cartelle

```
qa-scenari-ai/
├── PROGRESS.md
├── requirements.txt        # ollama, pydantic, pytest
├── .gitignore
├── requisiti/              # un file .txt per requisito (INGRESSO)
│   └── _modello.txt        # esempio di formato
├── riferimenti/            # i MIEI scenari scritti a mano, stesso nome del requisito
│   └── _modello.feature    # esempio di formato
├── prompts/                # v1.md, v2.md, v3.md...
├── risultati/              # scenari generati dall'AI, una cartella per versione di prompt
├── generatore/             # il codice (lo scriviamo insieme, un file alla volta)
│   └── __init__.py
└── tests/                  # pytest
```

---

## 6. Piano di lavoro

### Fase 0 – Preparazione
- [ ] Cartella + ambiente virtuale + `pip install -r requirements.txt`
- [ ] Git + repo GitHub
- [ ] Ollama acceso e `qwen2.5:3b` presente (`ollama list`)

### Fase 1 – I dati (senza codice)
- [ ] 3 requisiti del mio kiosk in `requisiti/`
- [ ] I relativi scenari scritti a mano in `riferimenti/`

### Fase 2 – Lo schema
- [ ] `generatore/schemas.py`: `Scenario` (titolo, tipo, given, when, then) e `Risposta` (lista di scenari)

### Fase 3 – Prima generazione
- [ ] `prompts/v1.md`: prompt semplice
- [ ] `generatore/gherkin.py`: da JSON a testo `.feature`
- [ ] `generatore/genera.py`: requisito + prompt → Ollama → `.feature`

### Fase 4 – Controlli
- [ ] `generatore/controlli.py`: tipi presenti, passi non vuoti, doppioni
- [ ] Ciclo di correzione (max 3 tentativi)

### Fase 5 – Prompt migliori
- [ ] `prompts/v2.md`: + regole
- [ ] `prompts/v3.md`: + esempio (few-shot)

### Fase 6 – Valutazione (il cuore del progetto)
- [ ] Casi attesi con parole chiave per ogni requisito
- [ ] `generatore/valuta.py`: tutte le versioni su tutti i requisiti → report in `risultati/report.md`
- [ ] Portare i requisiti di prova a ~10

### Fase 7 – Qualità e portfolio
- [ ] pytest su `schemas.py`, `controlli.py`, `gherkin.py` (senza Ollama)
- [ ] GitHub Actions
- [ ] README con il report e un video demo

---

## 7. Diario

| Data | Cosa ho fatto | Problemi / note |
|---|---|---|
| 17/10/2026 | Idea, decisioni, struttura del progetto | Scartata l'automazione della chat web di Claude: non permessa |

---

## 8. Cosa racconterò ai colloqui

- Ho costruito uno strumento locale che genera scenari Gherkin da un requisito.
- Ho fatto rispondere l'AI in JSON con schema, e ho lasciato a Python le parti che devono essere esatte.
- Ho **misurato** diverse versioni del prompt usando come riferimento i test scritti a mano da me.
