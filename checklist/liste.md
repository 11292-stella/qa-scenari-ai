# Checklist – Liste e ricerca (modulo trasversale): caricamento e ricerca testuale

Modulo TRASVERSALE: pattern riutilizzabili per le aree che non hanno una checklist di liste propria (fornitori, fatture, utenti, report...).
NON spuntarlo insieme a ordini_liste o prodotti_ricerca: i punti si ripeterebbero.
Da usare con liste_filtri, liste_paginazione, liste_sicurezza quando il requisito ne parla.

Applica solo i punti che il requisito permette di verificare.
Per i punti di cui il requisito non parla, NON inventare il comportamento: scrivi una domanda aperta.
Ogni scenario ha UN solo livello: se un punto ne indica due, scrivi uno scenario per livello.

Tipi ammessi: positivo, negativo, limite, sicurezza, accessibilità
Livelli ammessi: unit, api, e2e

## 1. Caricamento e visualizzazione della lista

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| LS1 | Apertura della lista con dati presenti: vengono visualizzati i record previsti | positivo | e2e |
| LS2 | Recupero dei record tramite API | positivo | api |
| LS3 | Lista vuota: viene mostrato uno stato vuoto comprensibile | negativo | e2e |
| LS4 | API restituisce zero risultati senza generare un errore inatteso | positivo | api |
| LS5 | Errore server durante il caricamento: viene mostrato un feedback comprensibile | negativo | e2e |
| LS6 | Errore server: API restituisce una risposta di errore gestibile dal client | negativo | api |
| LS7 | Caricamento lento: l'interfaccia gestisce l'attesa senza mostrare dati ingannevoli | limite | e2e |
| LS8 | Richiesta di caricamento fallita: l'utente può riprovare, se previsto | negativo | e2e |
| LS9 | I dati visualizzati corrispondono ai record restituiti dall'API | positivo | e2e |
| LS10 | La lista non mostra record duplicati a seguito di un caricamento ripetuto | limite | e2e |
| LS11 | I campi principali di ogni record sono visualizzati correttamente | positivo | e2e |
| LS12 | Record con campi opzionali vuoti: la lista non presenta errori di visualizzazione | limite | e2e |

## 2. Ricerca testuale

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| LS13 | Ricerca tramite un valore esistente: vengono restituiti i record corrispondenti | positivo | api |
| LS14 | Ricerca tramite interfaccia: i risultati corrispondono al termine inserito | positivo | e2e |
| LS15 | Ricerca senza risultati: viene mostrato uno stato vuoto comprensibile | negativo | e2e |
| LS16 | Ricerca con campo vuoto: comportamento coerente con i requisiti | limite | unit |
| LS17 | Ricerca con soli spazi | limite | unit |
| LS18 | Ricerca con maiuscole e minuscole (non presumere che le ignori: segui il requisito) | limite | api |
| LS19 | Ricerca con caratteri accentati e Unicode (non presumere che ignori gli accenti: segui il requisito) | limite | api |
| LS20 | Ricerca con apostrofi, trattini e caratteri speciali | limite | api |
| LS21 | Ricerca con testo molto lungo, entro e oltre i limiti definiti | limite | unit |
| LS22 | Ricerca con input contenente tentativi di injection | sicurezza | api |
| LS23 | Modifica del termine di ricerca: i risultati precedenti non vengono mantenuti impropriamente | positivo | e2e |
| LS24 | Cancellazione del termine: la lista torna allo stato previsto | positivo | e2e |
| LS25 | Ricerca rapida con più termini consecutivi: una risposta precedente non sovrascrive impropriamente quella più recente | limite | e2e |
| LS26 | Invio della ricerca tramite Invio da tastiera | positivo | e2e |

> Per LS18 e LS19, non darei per scontato che tutte le ricerche debbano ignorare le maiuscole o gli accenti: il comportamento può dipendere dai requisiti e dal database.

## Esempio di scenario

PUNTO: LS15: Ricerca senza risultati: viene mostrato uno stato vuoto comprensibile
RIGA DEL REQUISITO: Se la ricerca non trova risultati compare il messaggio 'Nessun risultato'.
TIPO: negativo
LIVELLI AMMESSI: e2e
Risposta:
{"livello": "e2e",
 "titolo": "Ricerca senza risultati",
 "dato": ["che ho aperto la lista dei fornitori"],
 "quando": ["scrivo 'zzzz' nel campo di ricerca"],
 "allora": ["vedo il messaggio 'Nessun risultato'"]}

## Esempio di scenario api

PUNTO: LS13: Ricerca tramite un valore esistente: vengono restituiti i record corrispondenti
RIGA DEL REQUISITO: La ricerca trova i fornitori che contengono il testo cercato nel nome.
TIPO: positivo
LIVELLI AMMESSI: api
Risposta:
{"livello": "api",
 "titolo": "Ricerca via API per nome",
 "dato": ["che esistono i fornitori 'Rossi' e 'Bianchi'"],
 "quando": ["invio la richiesta di ricerca dei fornitori con testo 'Rossi'"],
 "allora": ["la richiesta viene accettata", "la risposta contiene solo il fornitore 'Rossi'"]}
