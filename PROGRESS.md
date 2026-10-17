# PROGRESS – QA Scenari AI

> Strumento **locale** e **generale**: legge un **requisito** di qualsiasi progetto, applica la **checklist** giusta (login, CRUD, form…) e con un modello AI piccolo (Ollama) genera:
> 1. **scenari di test in Gherkin**, ognuno con tipo, livello della piramide e codice della checklist;
> 2. **domande aperte** sui punti di cui il requisito non parla.
>
> Poi **misura** quale versione del prompt funziona meglio, usando come riferimento gli scenari scritti da me a mano.

Nato da: job-agent (ho riusato le idee che funzionavano: JSON con schema, lista chiusa, ciclo di correzione).
Repository: https://github.com/11292-stella/qa-scenari-ai
Ultimo aggiornamento: 17 ottobre 2026

---

## 1. Perché questo progetto

Voglio dimostrare che so **gestire un'AI**, e non solo usarla:
- scrivere prompt con regole ed esempi;
- obbligare l'AI a rispondere in un formato preciso (JSON con schema);
- controllare automaticamente le risposte e farle correggere;
- **misurare** se un prompt è migliore di un altro, con numeri.

Il tema è il QA, il mio lavoro: l'AI fa il primo lavoro della tester (legge il requisito e pensa a cosa testare), io controllo e misuro.
Lo strumento è **generale**: funziona con i requisiti di qualsiasi progetto, perché la mia esperienza da QA è nelle **checklist** riusabili.

---

## 2. Decisioni prese

| Tema | Decisione | Motivo |
|---|---|---|
| Modello AI | **Ollama** in locale con **`qwen2.5:3b`** | gratis, niente API key; il 3b sta nella GPU (RTX 2050, 4 GB) |
| Chat web di Claude | **Niente automazione** | non permessa dalle condizioni d'uso |
| Generalità | **Checklist** per tipo di funzione (`checklist/login.md`, `crud.md`…) | quasi tutti i gestionali hanno le stesse funzioni base; le checklist sono la mia esperienza da QA |
| Quale checklist | Riga `Checklist: login` in cima al requisito | Python sa quale file caricare |
| Punti della checklist | Codice univoco (`L1`, `L2`…) | il confronto con il riferimento è esatto, niente parole chiave |
| Tipi di test | **5**: positivo, negativo, limite, sicurezza, accessibilità | lista chiusa (`Literal`) |
| Livelli (piramide) | **3**: unit, api, e2e | ogni scenario ha UN solo livello; se un punto ne ha due → due scenari |
| Tag degli scenari | `@tipo @livello @codice` (es. `@negativo @api @L5`) | Python li legge per la valutazione |
| Punti non coperti dal requisito | **Domanda aperta**, mai comportamento inventato | è quello che fa una brava tester con un requisito incompleto |
| Domande attese | **Ricavate da Python**: i codici della checklist assenti nel riferimento | nessun file in più da scrivere |
| Tipo dello scenario | Lo copia **Python** dalla checklist | nella prova v0 l'AI sbagliava quasi sempre il tipo |
| Anti-invenzione | L'AI deve **citare la frase del requisito**; Python verifica che esista | trasforma "fidati" in "dimostramelo" |
| Gherkin | **In italiano** (`Funzionalità`, `Dato`, `Quando`, `Allora`), lo scrive **Python** dal JSON | sintassi sempre corretta; come la mia suite Selenium/Cucumber |
| Prompt | Un file per versione in `prompts/` (v1, v2, v3…) | così posso confrontarle |
| Contesto del modello | `num_ctx: 8192`, `num_predict` alto | con il default (2048) la checklist non entra e il modello taglia il prompt senza avvisare |
| Esecuzione | Gli scenari **non vengono eseguiti** | il progetto misura la qualità del prompt, non dell'app |
| Requisiti di prova | Da **progetti diversi** (gestionale, kiosk, requisiti inventati di altri settori) | dimostra con i numeri che lo strumento è generale |
| Codice di automazione | **Fase 8**, dopo il cuore: l'AI sceglie il metodo del page object da lista chiusa, Python scrive il codice con template | il 3b non conosce i miei progetti: inventerebbe metodi e selettori |

---

## 3. Architettura

```
requisiti/login.txt  (requisito + riga "Checklist: login")
   │
   ▼
[Python] carica checklist/login.md + prompts/vX.md
   │
   ▼
[AI qwen2.5:3b]  risponde in JSON (schema Pydantic):
                 - scenari: codice (lista chiusa), livello, citazione dal requisito, passi Dato/Quando/Allora
                 - domande aperte: codice + domanda
   │
   ▼
[Python] schemas.py   → formato valido? codici solo dalla checklist?
[Python] controlli.py → la citazione esiste nel requisito? livello ammesso per quel codice? doppioni? passi vuoti?
         ↺ se ci sono problemi: rimando gli errori all'AI (max 3 tentativi)
   │
   ▼
[Python] aggiunge il tipo (dalla checklist) → gherkin.py → risultati/vX/login.feature
   │
   ▼
[Python] valuta.py → confronta i codici con riferimenti/login.feature → report:
                     scenari attesi trovati, scenari inventati, domande aperte trovate
```

Due strategie da confrontare:
- **tutti insieme**: una sola chiamata con tutta la checklist;
- **un punto alla volta**: una chiamata breve per ogni punto della checklist.

---

## 4. Stack

| Parte | Tecnologia | La conoscevo già? |
|---|---|---|
| Linguaggio | Python 3.14 | ✅ |
| Modello AI | Ollama + qwen2.5:3b | ✅ (job-agent) |
| Validazione JSON | Pydantic (`BaseModel`, `Field`, `Literal`, `create_model`) | ✅ (job-agent) |
| Formato scenari | Gherkin in italiano | ✅ (Selenium + Cucumber sul gestionale) |
| Test | pytest | ✅ |
| CI | GitHub Actions | ✅ |

---

## 5. Struttura delle cartelle

```
qa-scenari-ai/
├── PROGRESS.md
├── requirements.txt        # ollama, pydantic, pytest
├── .gitignore
├── prova_v0.py             # prova a mano del prompt libero (usa e getta)
├── checklist/              # la mia esperienza da QA, valida per ogni progetto
│   └── login.md            # L1…L32
├── requisiti/              # INGRESSO: un file .txt per requisito
│   └── login.txt
├── riferimenti/            # i MIEI scenari scritti a mano, con tag @tipo @livello @codice
│   └── login.feature
├── prompts/                # v1.md, v2.md, v3.md...
├── risultati/              # uscite dell'AI, una cartella per versione di prompt
│   └── prova_v0.txt
├── generatore/             # il codice (scritto insieme, un file alla volta)
│   └── __init__.py
└── tests/                  # pytest
```

Comandi previsti:
```powershell
python -m generatore.genera requisiti/login.txt --prompt v1
python -m generatore.valuta --prompt v1
```

---

## 6. Piano di lavoro

### Fase 0 – Preparazione ✅
- [x] Cartella + ambiente virtuale + `pip install -r requirements.txt`
- [x] Git + repo GitHub
- [x] Ollama acceso e `qwen2.5:3b` presente

### Fase 1 – I dati (senza codice)
- [x] `checklist/login.md`: 32 punti (L1…L32) con tipo e livello
- [x] `requisiti/login.txt` + `riferimenti/login.feature` (gestionale)
- [ ] Verifica sul gestionale: stesso messaggio (L4), solo spazi (L6), endpoint e 401 (L2, L5)
- [x] Prova a mano del prompt v0 → `risultati/prova_v0.txt`
- [ ] Altri requisiti di login da progetti diversi (kiosk, requisiti inventati)

### Fase 2 – Lo schema
- [ ] `generatore/schemas.py`: tipi e livelli ammessi, scenario, domanda, schema con codici dalla checklist

### Fase 3 – Prima generazione
- [ ] `generatore/checklist.py`: legge la checklist (codice, cosa controllare, tipo, livelli)
- [ ] `prompts/v1.md`
- [ ] `generatore/gherkin.py`: da JSON a `.feature` in italiano con i tag
- [ ] `generatore/genera.py`: requisito + checklist + prompt → Ollama → `.feature` + domande

### Fase 4 – Controlli
- [ ] `generatore/controlli.py`: citazione presente nel requisito, livello ammesso, doppioni, passi vuoti
- [ ] Ciclo di correzione (max 3 tentativi)

### Fase 5 – Prompt migliori
- [ ] `prompts/v2.md`: + regole (non ribaltare il significato, niente invenzioni)
- [ ] `prompts/v3.md`: + esempio (few-shot)
- [ ] Strategia "un punto alla volta" contro "tutti insieme"

### Fase 6 – Valutazione (il cuore del progetto)
- [ ] `generatore/valuta.py`: scenari attesi trovati, scenari inventati, domande trovate → `risultati/report.md`
- [ ] Altre checklist: `crud.md`, `form.md`, `liste.md`, `permessi.md`
- [ ] Portare i requisiti di prova a ~10, da progetti diversi

### Fase 7 – Qualità e portfolio
- [ ] pytest su `schemas.py`, `checklist.py`, `controlli.py`, `gherkin.py`, `valuta.py` (senza Ollama)
- [ ] GitHub Actions
- [ ] README con il report e un video demo

### Fase 8 – Estensione: scheletri di automazione
- [ ] Elenco dei metodi dei miei page object (es. `LoginPage.login`, `DashboardPage.isVisible`)
- [ ] L'AI sceglie per ogni passo il metodo da **lista chiusa**; se non esiste → `TODO: metodo mancante`
- [ ] Python scrive il codice con **template**, scelto in base al livello:
  - `@e2e` → prima **Selenium + Cucumber Java**, poi Playwright, Cypress, Robot Framework
  - `@api` → REST Assured / `requests`
  - `@unit` → nessun codice UI (va nel progetto Angular)

---

## 7. Diario

| Data | Cosa ho fatto | Problemi / note |
|---|---|---|
| 17/10/2026 | Idea, decisioni, struttura del progetto | Scartata l'automazione della chat web di Claude: non permessa |
| 17/10/2026 | Setup: venv, librerie, Git, GitHub | Lo zip estratto aveva creato una cartella dentro l'altra → file spostati con `Get-ChildItem -Force \| Move-Item` |
| 17/10/2026 | Strumento generale: checklist del login (32 punti) | Aggiunti da me L14–L32 (rete, doppio clic, account disabilitato, accessibilità…); "security test" non è un livello → `api` |
| 17/10/2026 | Requisito e riferimento del login con tag `@tipo @livello @codice` | I codici assenti dal riferimento diventano le domande attese |
| 17/10/2026 | Prova a mano del prompt v0 (testo libero) | Passare il prompt come argomento da PowerShell non funziona (a capo e virgolette) → `prova_v0.py` con la libreria `ollama` |
| 17/10/2026 | Risultato del prompt v0 | 7/9 punti trovati, **0 domande aperte su 23**, ~20 scenari inventati, tipi sbagliati, tag inventato `@limit`, doppioni, 2 significati ribaltati, risposta tagliata → servono schema, citazione obbligatoria e controlli |
| 17/10/2026 | Prompt v1 con schema JSON, tutti i punti insieme | Formato e livelli ok, ma risposta tagliata a L27 (91 s), 0 domande, **0/27 citazioni vere** (copiava una frase della checklist), ripetizioni, passi con "@utente" → strategia "un punto alla volta" (prompt chaining) |

---

## 8. Cosa racconterò ai colloqui

- Ho costruito uno strumento locale e **generale** che, partendo da un requisito e da una checklist, genera scenari Gherkin con tipo e livello della piramide.
- Con un prompt libero il modello **inventava** il comportamento dei punti non coperti dal requisito invece di fare domande: l'ho misurato (0 domande su 23).
- Ho fatto rispondere l'AI in **JSON con schema**, le ho fatto **citare il requisito** e ho verificato la citazione in Python.
- Ho **misurato** diverse versioni del prompt usando come riferimento i test scritti a mano da me.
