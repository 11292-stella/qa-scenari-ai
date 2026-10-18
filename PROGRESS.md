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

### Fase 4b – Interfaccia web (Django)
- [x] `generatore/servizio.py`: `analizza()` restituisce tutto come dati (niente stampe); percorsi da `PROGETTO`
- [ ] Progetto Django `sito` + app `analisi` (manage.py nella cartella principale)
- [ ] Form: titolo, requisito, checklist, prompt passo A e passo B (menu letti dalle cartelle)
- [ ] Pagina risultati: righe numerate, scenari Gherkin, domande aperte, tabella decisioni, scarica `.feature`
- [ ] Errori gestiti nella pagina (Ollama spento, requisito troppo corto)
- [ ] Dopo: storico delle analisi nel database

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

### Fase 8 – Passo C: codice di automazione (specifica in `automazione/SPECIFICA.md`)
- [x] Letti i miei repository: Robot (Browser Library), Selenium + Cucumber Java, Playwright + pytest (Impronto), Appium + Cucumber (kiosk). Robot e Selenium testano **lo stesso gestionale con gli stessi selettori**
- [x] **Scheletri senza AI** (`generatore/scheletri.py`): ogni passo → metodo/keyword del page object (nome dal testo), `Allora` → verifica, valori tra virgolette → parametri, corpi TODO che **falliscono** (niente falso verde), `@unit` esclusi. Playwright (pytest, classi), Robot (Browser Library), Appium Java (TestNG, senza Cucumber). Controllati con `py_compile`, parser di Robot e `javac`
- [x] Django: per ogni scenario linguette **Gherkin · Playwright · Robot · Appium** + Copia, e **zip** con tutti gli scheletri
- [ ] (dopo) `automazione/catalogo_login.md` per riempire i corpi con i miei metodi e keyword veri
- [ ] `generatore/automatizza.py`: l'AI sceglie l'azione per ogni passo (lista chiusa), `MANCANTE` → TODO
- [ ] Template Robot (`.robot` con le mie risorse) → prova sul gestionale vero
- [ ] Template Selenium/Cucumber (classe di step Java)
- [ ] Suite modello Playwright sul gestionale nel mio stile + template
- [ ] Django: bottoni di download per ogni framework
- [ ] Dopo: Appium (kiosk) con checklist e catalogo del carrello

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
| 17/10/2026 | Passo B (`scrivi.py`, prompt s1_scenario): 13 scenari dalle decisioni v4, 21 s | Livelli tutti giusti (lista chiusa). **5/13 scenari usabili** (L1, L3, L6, L9, L10), tutti con la riga giusta. Gli errori del passo A **si propagano**: con la riga sbagliata il modello inventa per accontentare il punto (L4 messaggio 'Password errata' inventato; L26 "la password viene mostrata in modo non cifrato" → **contraddice** il requisito). L11 ha scritto in realtà lo scenario di L5 (401). Bug mio in `pulisci_passo`: "API" → "aPI" → corretto (le sigle non si toccano) |
| 17/10/2026 | `servizio.py`: passo A + B in una funzione che restituisce dati | 13 scenari + 19 domande in 36 s con un comando. Percorsi resi indipendenti dalla cartella di lancio (`PROGETTO`), serve per Django. Il test ha trovato un caso limite: riga del requisito più corta di 10 caratteri → errore sulla citazione dello scenario finale → tolto il minimo solo lì |
| 17/10/2026 | Interfaccia Django (`sito` + app `analisi`): form, risultati, download `.feature`, errori nella pagina | Funziona. Requisito di un'altra app (login e-commerce): L1, L12, L14 giusti; stessi difetti noti (la riga con "email" attira L4, L26, L29; L9 perso) → i difetti non dipendono dal login del gestionale |
| 17/10/2026 | Specifica del passo C (automazione) scritta leggendo i miei 4 repository | Ordine: Robot → Selenium/Cucumber → Playwright → Appium. Il codice generato userà i miei metodi e keyword veri |
| 17/10/2026 | Scelto di partire dagli **scheletri** (struttura + TODO) invece del catalogo: è quello che mi serve davvero, una base di codice da completare | Nessuna AI: sempre corretto. Bug trovato dal test: l'apostrofo di "l'email" veniva preso come virgoletta → un apice conta solo se non è attaccato a una lettera |
| 17/10/2026 | Checklist `anagrafica` (55 punti, 20 aggiunti da me: valori limite, idempotenza, IDOR, mass assignment, XSS memorizzato…) | A55 era senza tipo e livello e `checklist.py` l'avrebbe **saltata in silenzio** → ora una riga con codice ma senza 4 colonne ferma il programma. Divisi 3 punti che si sovrapponevano (A15/A39, A31/A52, A35/A53) |
| 17/10/2026 | Prima prova anagrafica (requisito cliente persona fisica/azienda) | Passo A: A13, A16, A17, A20, A21 giusti; la riga "cliente con ordini" finita su A8/A9 invece di A26; A23 e A40 inventati. **Passo B debole**: "Dato nome", codice dentro il Gherkin (A21), "Allora verifica che…" → gli scheletri sono buoni quanto gli scenari |
| 17/10/2026 | **s2**: prompt con 7 regole di scrittura + esempio (il mio L3) + `{TIPO}`; `controlla_scenario` (simboli di codice, passi troppo corti/lunghi, "verifica", doppioni) con **ciclo di correzione** (max 3) | Falsi positivi evitati: i valori tra apici ('mario.rossi@test.it') non si controllano; si controlla il passo già pulito da `pulisci_passo`, così gli errori che corregge Python non sprecano tentativi. La pagina mostra "🔁 corretto N×" |
| 18/10/2026 | Confronto s1 / s2 sul requisito del cliente (stesso passo A) | Forma molto migliore con s2: niente "Dato nome", niente codice, niente "verifica che"; scenari usabili ~2/11 → ~5/11. **Problema nuovo: il modello copia l'esempio** (few-shot del login): A13, A20, A21 parlano di "pagina di login" e "mrossi". A8 coerente col suo tipo ma **contraddice il requisito** (colpa della riga sbagliata del passo A) |
| 18/10/2026 | **s3**: l'esempio sta nella **checklist** (sezione `## Esempio di scenario`, una per area) + regola "non copiare l'esempio"; esempi delle regole resi neutri ("che ho aperto la pagina ...") | Anche gli esempi dentro le regole venivano copiati. Scheletri: tolte le parole vuote in fondo ai nomi ("..._codice_fiscale_con" → "..._codice_fiscale") |
| 18/10/2026 | Prima prova della s3: **l'analisi si blocca** con "Invalid JSON: EOF while parsing a string" | Il modello si è ripetuto ("dichiaro che…") e `num_predict` ha tagliato il JSON: **uno scenario rotto faceva fallire tutta l'analisi**. Sistemato con: lunghezze massime nello schema (titolo 120, passo 200, max 6 passi: Ollama le usa per guidare la risposta), JSON rotto dentro il ciclo di correzione, scenario **saltato** dopo 3 tentativi (il punto va tra le domande con "scrivilo a mano") e `num_predict` 500 → 1200 |
| 18/10/2026 | Confronto s2 / s3 (11 scenari ciascuno) | s3: **0 contaminazioni dal login** e passi con valori concreti (metodi riusabili: `scrivo_nel_campo_nome(valore)`), ma copia l'esempio dell'area ("il bottone Salva resta disabilitato" in 6 scenari), copia il segnaposto `'...'` della regola (2), inventa testi di messaggi (3), ribalta A17 ("11 cifre non accettata"). **Errore mio: l'esempio stesso aggiungeva un comportamento non scritto nella sua riga** → corretto l'esempio; nuovi controlli generici: valore segnaposto e testo tra apici nell'"Allora" che non è nella riga (inventato) |
| 18/10/2026 | Checklist `ordini` (91 punti scritti da me, 8 sezioni con note) | Note "per il generatore" portate dentro il testo dei punti (O26, O49, O67), perché il modello vede solo il testo del punto. Prima prova fatta per sbaglio con la checklist **anagrafica** (preselezionata, prima in ordine alfabetico): 54 domande su 55, nessun errore segnalato → **la checklist ora va scelta per forza** ("— scegli —"). Caso limite: testo inventato con apostrofo ('L'ordine non può...') non riconosciuto dal controllo |
| 18/10/2026 | Prova ordini (91 punti, 108 s): 32 scenari | Buoni O18, O19, O31 (2×10=20), O51, O57, O58. Problemi: la riga "Pagato non modificabile" attira **12 punti** (quasi doppioni), 6 positivi che finiscono con un errore, valori uguali al nome del campo ('Quantità' nel campo 'Quantità'), **O32 con un calcolo sbagliato** (2×10+3×20+1×5 = 85, non 50: lo trova solo una revisione umana) |
| 18/10/2026 | Checklist ordini **divisa in 5** (`ordini` 50, `ordini_importi` 12, `ordini_magazzino` 8, `ordini_liste` 10, `ordini_sicurezza` 11), codici O invariati; form con **più checklist insieme** (caselle) | Ogni punto usa l'esempio della **sua** checklist; un codice ripetuto tra due file ferma il programma; la prima checklist della lista dà il nome agli scheletri. Requisito da terminale: `Checklist: ordini, ordini_importi` |
| 18/10/2026 | Prova ordini + ordini_importi + ordini_magazzino (37 scenari) → **4 controlli generici nuovi**: valore uguale al nome del campo, positivo che finisce con un errore, apostrofo dentro un testo tra apici, **doppioni** (stessa riga + passi quasi uguali, indice di Jaccard ≥ 0,8 → "≈ simile a Oxx" nella pagina) | Provati sui miei 37 scenari veri: **ne avrebbero bloccati 7** (O1, O3, O9, O16, O48 valore = nome del campo; O56 positivo con errore; O70 testo inventato con apostrofo) e segnato O34 simile a O33. Restano fuori dai controlli, e li trova solo il tester: **calcoli sbagliati** e stati presi da un'altra riga ('In preparazione' invece di 'Pagato') |
| 18/10/2026 | Checklist **prodotti** (107 punti in 8 file, tolti P72 e P77 perché uguali a O64/O69 e O67/O68) e prima prova (4 checklist, 63 punti): 35 scenari | Circa 10/35 buoni (P24 prezzo zero, P25, P37 sconto 31% rifiutato). Il passo A copre troppi punti ("se previsto" → sì); P36 positivo con 31% accettato e calcolo sbagliato; "Esaurito" del requisito ignorato. **7 scenari @api scritti come interfaccia** → nuovo controllo sul **livello**: in un @api niente pagina, campo, bottone, "vedo". Sui due .feature veri avrebbe preso 9 scenari prodotti e 6 ordini, 0 esempi delle checklist bloccati |
| 18/10/2026 | **Esempio per livello**: sezione `## Esempio di scenario api` nella checklist, `esempio_per(punto)` la usa per i punti solo api. Aggiunto a `prodotti.md` (esempio P6) | Stessa analisi, stesso passo A: i **7 scenari @api di prodotti.md** che il controllo segnalava ma il modello non sapeva correggere (P2, P10, P19, P23, P24, P26, P29) ora sono tutti scritti come richiesta/risposta; P29 parla finalmente dello SKU duplicato e P19 usa il limite di 80 caratteri. Gli scenari delle altre checklist sono **identici** a prima (temperatura 0): l'unica variabile cambiata è l'esempio → esperimento pulito. Lezione: il controllo trova il problema, ma la causa era l'esempio sbagliato |
| 18/10/2026 | **v5_decidi**: v4 + regola "una riga che dice cosa è permesso (solo…, deve essere…, al massimo…) parla anche del caso vietato", per recuperare P91/P92, P101/P102, O82/O83 persi dal passo A | **Bocciata**: login 10/32 decisioni e 8/32 con la riga giusta (v4: 26 e 23), stabile ×3 → dice "sì" a 31 punti su 32. La regola nuova ha cancellato quella contro le "parole simili": un modello da 3B non tiene in equilibrio due regole opposte. **Resta la v4**, che diventa la versione unica del form (i menu dei prompt vanno sotto "Opzioni avanzate"). Riflessione: "Solo gli amministratori possono creare prodotti" non dice COSA succede a chi non lo è (403? bottone nascosto? messaggio?) → metterlo tra le domande aperte è il comportamento giusto: la domanda va al product owner |
| 18/10/2026 | Checklist **pagamenti** (68 punti in 5 file: avvio e coerenza, contanti, carta simulata, rimborsi, ricevuta) e **liste** (78 punti in 4 file, modulo trasversale da NON spuntare con ordini_liste o prodotti_ricerca). Esempi per **ogni livello** (`## Esempio di scenario e2e/unit/api`): `esempio_per` ora sceglie l'esempio del livello del punto, non solo api | Le note importanti (timeout che non vuol dire fallito, concorrenza dei pagamenti, maiuscole/accenti, ordinamento 2-10-100) portate dentro il testo dei punti; LS78 era troncato → completato. Il controllo sul livello api segnalava 'pagina '3'' della paginazione: "pagina" da sola non è più interfaccia, solo "ho aperto la pagina", "sulla pagina"… Rifatto il controllo sui vecchi .feature: stessi 15 scenari presi, nessun falso positivo. 24 checklist in tutto, nessun codice ripetuto |
| 18/10/2026 | Prova **pagamenti** (35 scenari, ~12 buoni: PAY27 timeout 'In verifica' giusto, PAY59, PAY60, PAY68) + **ultimi 4 controlli di forma**: "allora" che dice successo ed errore insieme; "dato" con un'azione (invio, premo, clicco, scrivo); testo esatto della riga ignorato in un negativo/limite ("Importo insufficiente" → "vedo un messaggio di errore"); @e2e che comincia con "invio la richiesta" | Provati sugli 8 .feature veri: presi A3, A38, A42, P63 (contraddizione), A21, A26, P19, P23, P24, P26, P29 (dato con azione), PAY16, P69 (testo ignorato), A2, P90, P94, P96 (e2e come API). Un falso positivo trovato e tolto: "scrivo 'pizza' nel campo di ricerca **e invio la richiesta**" è un'azione da interfaccia → il controllo e2e guarda solo i passi che COMINCIANO con "invio la richiesta". **Fine dei controlli**: quello che resta (calcoli, righe sbagliate, copie dell'esempio) lo trova la revisione |

---

## 8. Cosa racconterò ai colloqui

- Ho costruito uno strumento locale e **generale** che, partendo da un requisito e da una checklist, genera scenari Gherkin con tipo e livello della piramide.
- Con un prompt libero il modello **inventava** il comportamento dei punti non coperti dal requisito invece di fare domande: l'ho misurato (0 domande su 23).
- Ho fatto rispondere l'AI in **JSON con schema**, le ho fatto **citare il requisito** e ho verificato la citazione in Python.
- Ho **misurato** diverse versioni del prompt usando come riferimento i test scritti a mano da me.
