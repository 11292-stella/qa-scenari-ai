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

Strategia scelta: **un punto alla volta, in due passi** (prompt chaining).
La strategia "tutti i punti in una sola chiamata" è stata provata (v1) e scartata: risposta tagliata, 0 citazioni vere.

```
requisiti/login.txt  (requisito + riga "Checklist: login")
   │
   ▼
[Python] checklist.py → legge checklist/login.md (codici, tipo, livelli) e la controlla
[Python] decidi.py    → toglie "Titolo:"/"Checklist:" e NUMERA le righe del requisito
   │
   ▼  per ogni punto della checklist (32 chiamate brevi, ~0,3 s l'una)
[AI] PASSO A – prompts/v4_decidi.md
     "Quale riga del requisito parla di questo punto? (0 = nessuna)"
     risposta: {"riga": 5}   ← lista chiusa 0…N (schema_riga)
   │
   ├── riga 0  → DOMANDA APERTA
   └── riga N  → PASSO B (da fare): l'AI scrive lo scenario partendo dalla riga N
   │
   ▼
[Python] controlli.py → livello ammesso, doppioni, passi vuoti; ciclo di correzione
[Python] aggiunge il tipo (dalla checklist) → gherkin.py → risultati/vX/login.feature
   │
   ▼
[Python] valutazione → confronto con riferimenti/login.feature (tag @L.. e @rigaN):
         ✅ decisione e riga giuste · ⚠️ riga sbagliata · ❌ decisione sbagliata
         --ripetizioni N (ricaricando il modello) → media, min/max, punti instabili
```

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
- [x] `requisiti/login.txt` + `riferimenti/login.feature` (gestionale) con tag `@tipo @livello @codice @rigaN`
- [ ] Verifica sul gestionale: stesso messaggio (L4), solo spazi (L6), endpoint e 401 (L2, L5)
- [x] Prova a mano del prompt v0 → `risultati/prova_v0.txt`
- [ ] Altri requisiti di login da progetti diversi (kiosk, requisiti inventati)

### Fase 2 – Lo schema ✅
- [x] `generatore/schemas.py`: tipi e livelli ammessi, scenario, domanda, `schema_risposta`, `Decisione`, `schema_riga`

### Fase 3 – Passo A: il requisito parla del punto? ✅
- [x] `generatore/checklist.py`: legge e controlla la checklist
- [x] `generatore/genera.py` + `prompts/v1.md`: tutti i punti insieme → **scartato**
- [x] `generatore/controlli.py`: citazione presente nel requisito, segnaposto del prompt
- [x] `generatore/decidi.py`: un punto alla volta, modo citazione (v2) e modo riga (v3, v4)
- [x] Metrica con la riga attesa (✅ / ⚠️ / ❌) e `--ripetizioni` con punti instabili
- [x] **Prompt scelto: v4_decidi** (26/32 decisioni, 23/32 con la riga giusta, stabile)

### Fase 4 – Passo B: scrivere lo scenario
- [ ] Prompt e schema per lo scenario di UN punto, partendo dalla riga scelta
- [ ] Prompt per la domanda aperta
- [ ] `generatore/gherkin.py`: da JSON a `.feature` in italiano con i tag
- [ ] Controlli: livello ammesso per quel punto, passi non vuoti, ciclo di correzione (max 3 tentativi)

### Fase 5 – Prompt migliori
- [ ] Domanda di verifica solo sui "sì" ("la riga N dice cosa succede in questo caso?")
- [ ] Esempio nel prompt (few-shot)
- [ ] Errori stabili della v4 da attaccare: L2 → riga 2 invece di 8, L4 → 4 invece di 5, L5 → no, L13 → 1 invece di 2, falsi "sì" su L11, L14, L22, L26, L29

### Fase 6 – Valutazione (il cuore del progetto)
- [ ] `generatore/valuta.py`: tutte le versioni su tutti i requisiti → `risultati/report.md`
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
| 17/10/2026 | Passo A (`decidi.py`, prompt v2_decidi): prima prova | **Invalida**: prompt copiato dalla chat senza segnaposto → stessa frase inventata per 32 punti. Inoltre il conteggio dava 23/32 contando INVENTA come giusto (falso positivo della metrica) → aggiunto `controlla_segnaposto` e corretto il conteggio |
| 17/10/2026 | Passo A, prompt v2_decidi: prova valida (34 s, 1 s a punto) | **21/32** decisioni giuste. Scenari attesi trovati 6/9; domande giuste 15/23. Il controllo della citazione ha bloccato 4 invenzioni (L22, L24, ma anche L2 e L5: frase copiata dal PUNTO invece che dal requisito). Nuovo tipo di errore: **citazione vera ma che non c'entra** (6 casi: L12, L18, L25, L27, L31, L32) → prossima prova: righe numerate |
| 17/10/2026 | Passo A, prompt v3_decidi: righe numerate (lista chiusa 0–8) | **23/32**, 7,9 s (4 volte più veloce). Scenari attesi trovati **9/9** (L2, L5, L9 recuperati), ma 9 falsi "sì" (domande giuste 14/23): sceglie righe con parole simili (riga 2 "password" per L22, L23, L26, L29; riga 8 "token" per L11, L21). 2 decisioni giuste con la riga sbagliata (L3 → riga 3 invece di 5; L13 → riga 1 invece di 2). v2 era prudente, v3 generosa → v4: una regola contro le "parole simili", scritta in modo generico (niente "password"/"token", altrimenti il prompt si adatta solo al login) |
| 17/10/2026 | Passo A, prompt v4_decidi: v3 + regola contro le "parole simili" | **25/32**. Domande giuste 17/23 (L14, L18, L21, L23 sistemati), scenari attesi 8/9 (perso L5). Restano 6 falsi "sì" (L11, L12, L22, L26, L29, L31). Ma **3 decisioni giuste hanno la riga sbagliata** (L2 → riga 2 invece di 8, L4 → 4 invece di 5, L13 → 1 invece di 2): la metrica "decisioni giuste" è troppo generosa → serve controllare anche la riga |
| 17/10/2026 | Tag `@rigaN` nel riferimento + `decidi.py` con ✅ / ⚠️ riga sbagliata / ❌ | Rilanciata la v4: **26/32 decisioni, 23/32 anche con la riga giusta**. Ma il risultato **non è identico** alla prova prima (L12, L14, L31 cambiati) anche con `temperature: 0` → i punti "in bilico" possono cambiare tra un'esecuzione e l'altra: una misura sola non basta |
| 17/10/2026 | Rilanciata la v3 | 22/32 decisioni (prima 23), 21/32 con la riga giusta; anche qui risposte cambiate (L3 ora riga 5) → v3 e v4 non si possono confrontare con una prova sola → `decidi.py --ripetizioni N`: media, minimo, massimo e **punti instabili** (come i test flaky) |
| 17/10/2026 | v4 con 5 ripetizioni (modello sempre caricato) | 5 giri identici: 26/32 e 23/32, 0 instabili. Ipotesi: le risposte cambiano solo quando Ollama **ricarica** il modello (lo scarica dopo 5 min di inattività). Gli orari tornano: v2 rilanciata dopo 4 min → identica; v3 dopo 10 min e v4 dopo 5 min → cambiate → `decidi.py` ora scarica il modello tra un giro e l'altro (`keep_alive=0`) |
| 17/10/2026 | **Confronto finale passo A** – 5 ripetizioni, modello ricaricato a ogni giro | **v3**: 22/32 decisioni, 20,2/32 con la riga giusta (min 20, max 21), **4 punti instabili** (L3, L14, L23, L30). **v4**: **26/32 e 23/32 in tutti e 5 i giri, 0 instabili**. Gli intervalli non si sovrappongono → la v4 è davvero migliore, e la regola contro le "parole simili" l'ha resa anche più stabile. Ipotesi della ricarica confermata solo in parte: la v3 varia ricaricando, la v4 no (la differenza vista prima sulla v4 resta da capire) → **scelta la v4 per il passo B** |

---

## 8. Cosa racconterò ai colloqui

- Ho costruito uno strumento locale e **generale** che, partendo da un requisito e da una checklist, genera scenari Gherkin con tipo e livello della piramide.
- Con un prompt libero il modello **inventava** il comportamento dei punti non coperti dal requisito invece di fare domande: l'ho misurato (0 domande su 23).
- Ho fatto rispondere l'AI in **JSON con schema**, le ho fatto **citare il requisito** e ho verificato la citazione in Python.
- Ho **misurato** diverse versioni del prompt usando come riferimento i test scritti a mano da me.
