# Checklist – Prodotti e catalogo

Creazione e gestione dei prodotti, dati e validazioni.
Da usare insieme a prodotti_prezzi, prodotti_categorie, prodotti_varianti, prodotti_disponibilita, prodotti_ricerca, prodotti_immagini, prodotti_sicurezza quando il requisito ne parla.

Applica solo i punti che il requisito permette di verificare.
Per i punti di cui il requisito non parla, NON inventare il comportamento: scrivi una domanda aperta.
Ogni scenario ha UN solo livello: se un punto ne indica due, scrivi uno scenario per livello.

Tipi ammessi: positivo, negativo, limite, sicurezza, accessibilità
Livelli ammessi: unit, api, e2e

## 1. Creazione e gestione dei prodotti

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| P1 | Creazione di un prodotto con tutti i campi obbligatori validi | positivo | e2e |
| P2 | Creazione tramite API: il prodotto viene salvato e restituito con il suo ID | positivo | api |
| P3 | Il prodotto appena creato compare nel catalogo | positivo | e2e |
| P4 | Apertura del dettaglio di un prodotto esistente | positivo | e2e |
| P5 | Campo obbligatorio vuoto: il form segnala l'errore | negativo | unit |
| P6 | Campo obbligatorio mancante nella richiesta API | negativo | api |
| P7 | Campo obbligatorio contenente solo spazi | limite | unit |
| P8 | Modifica di un prodotto: i dati aggiornati vengono salvati e mostrati | positivo | e2e |
| P9 | Modifica tramite API: i campi aggiornati sono persistiti correttamente | positivo | api |
| P10 | Modifica di un singolo campo: gli altri campi non vengono alterati involontariamente | positivo | api |
| P11 | Annullamento della creazione: nessun prodotto viene salvato | negativo | e2e |
| P12 | Eliminazione di un prodotto con conferma | positivo | e2e |
| P13 | Eliminazione annullata: il prodotto resta presente | negativo | e2e |
| P14 | Recupero tramite API di un prodotto inesistente | negativo | api |
| P15 | ID malformato o inesistente nella richiesta di modifica | negativo | api |
| P16 | Doppio clic su Salva: non vengono creati prodotti duplicati indesiderati | limite | e2e |
| P17 | Errore del server durante il salvataggio: messaggio comprensibile e dati del form preservati, se previsto | negativo | e2e |

## 2. Dati, descrizioni e validazioni

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| P18 | Lunghezza minima e massima di nome e descrizione | limite | unit |
| P19 | Lunghezze non valide inviate direttamente all'API | limite | api |
| P20 | Caratteri accentati, apostrofi, simboli e caratteri Unicode salvati correttamente | limite | api |
| P21 | Spazi iniziali e finali nei campi testuali gestiti secondo le regole previste | limite | unit |
| P22 | Prezzo non numerico inserito nel form | negativo | unit |
| P23 | Prezzo negativo non ammesso | negativo | api |
| P24 | Prezzo pari a zero, se consentito o vietato dai requisiti | limite | api |
| P25 | Prezzo con più cifre decimali di quelle ammesse | limite | unit |
| P26 | Prezzo oltre il massimo consentito, se definito | limite | api |
| P27 | Codice prodotto o SKU con formato non valido | negativo | unit |
| P28 | Campo SKU obbligatorio mancante nella richiesta API | negativo | api |
| P29 | Codice prodotto duplicato, se deve essere univoco | negativo | api |
| P30 | Descrizione molto lunga o contenente caratteri speciali visualizzata correttamente | limite | e2e |

> Domande aperte tipiche: quali campi sono obbligatori? Quali limiti hanno prezzo, descrizione e SKU? Il prezzo zero è ammesso (omaggi, articoli non vendibili)?

## Esempio di scenario

PUNTO: P5: Campo obbligatorio vuoto: il form segnala l'errore
RIGA DEL REQUISITO: Nome, prezzo e categoria del prodotto sono obbligatori.
TIPO: negativo
LIVELLI AMMESSI: unit
Risposta:
{"livello": "unit",
 "titolo": "Prodotto senza nome non salvato",
 "dato": ["che sto compilando il form Nuovo prodotto"],
 "quando": ["lascio vuoto il campo Nome", "premo il bottone Salva"],
 "allora": ["vedo un messaggio di errore sotto il campo Nome"]}


## Esempio di scenario api

PUNTO: P6: Campo obbligatorio mancante nella richiesta API
RIGA DEL REQUISITO: Nome e prezzo del prodotto sono obbligatori.
TIPO: negativo
LIVELLI AMMESSI: api
Risposta:
{"livello": "api",
 "titolo": "Creazione via API senza nome rifiutata",
 "dato": ["che esiste la categoria 'Bevande'"],
 "quando": ["invio la richiesta di creazione di un prodotto con prezzo '2,50' e senza nome"],
 "allora": ["la richiesta viene rifiutata", "la risposta indica che manca il nome"]}
