# Checklist – Prodotti: ricerca, filtri, ordinamento e paginazione

Applica solo i punti che il requisito permette di verificare.
Per i punti di cui il requisito non parla, NON inventare il comportamento: scrivi una domanda aperta.
Ogni scenario ha UN solo livello: se un punto ne indica due, scrivi uno scenario per livello.

Tipi ammessi: positivo, negativo, limite, sicurezza, accessibilità
Livelli ammessi: unit, api, e2e

## 7. Ricerca, filtri, ordinamento e paginazione

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| P78 | Ricerca di un prodotto tramite nome | positivo | e2e |
| P79 | Ricerca di un prodotto tramite SKU o codice identificativo | positivo | api |
| P80 | Ricerca senza risultati: messaggio o stato vuoto comprensibile | negativo | e2e |
| P81 | Ricerca con maiuscole/minuscole gestite secondo le regole previste | limite | api |
| P82 | Ricerca con accenti, spazi e caratteri speciali | limite | api |
| P83 | Combinazione di filtri per categoria, prezzo e disponibilità, se supportati | positivo | api |
| P84 | Ordinamento per nome o prezzo secondo il criterio selezionato | positivo | api |
| P85 | Ordinamento con prezzi uguali, valori vuoti o nomi accentati | limite | api |
| P86 | Paginazione: nessun prodotto perso o duplicato tra pagine, a dati invariati | limite | api |
| P87 | Filtri e paginazione combinati restituiscono risultati coerenti | limite | api |
| P88 | Catalogo vuoto: la pagina non mostra errori o contenuti incoerenti | negativo | e2e |
| P89 | Modifica di un prodotto: i risultati della ricerca riflettono i nuovi dati | positivo | e2e |

## Esempio di scenario

PUNTO: P80: Ricerca senza risultati: messaggio o stato vuoto comprensibile
RIGA DEL REQUISITO: Se la ricerca non trova prodotti compare il messaggio 'Nessun prodotto trovato'.
TIPO: negativo
LIVELLI AMMESSI: e2e
Risposta:
{"livello": "e2e",
 "titolo": "Ricerca senza risultati",
 "dato": ["che ho aperto la pagina del catalogo"],
 "quando": ["scrivo 'zzzz' nel campo di ricerca"],
 "allora": ["vedo il messaggio 'Nessun prodotto trovato'"]}


## Esempio di scenario api

PUNTO: P79: Ricerca di un prodotto tramite SKU o codice identificativo
RIGA DEL REQUISITO: Un prodotto si può cercare anche con il suo codice SKU.
TIPO: positivo
LIVELLI AMMESSI: api
Risposta:
{"livello": "api",
 "titolo": "Ricerca via API per SKU",
 "dato": ["che esiste il prodotto 'Tiramisù' con SKU 'DOL-001'"],
 "quando": ["invio la richiesta di ricerca con SKU 'DOL-001'"],
 "allora": ["la richiesta viene accettata", "la risposta contiene il prodotto 'Tiramisù'"]}
