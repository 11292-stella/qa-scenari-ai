# Checklist – Ordini: ricerca, filtri, ordinamento e liste

Lista degli ordini, ricerca, filtri, paginazione.

Applica solo i punti che il requisito permette di verificare.
Per i punti di cui il requisito non parla, NON inventare il comportamento: scrivi una domanda aperta.
Ogni scenario ha UN solo livello: se un punto ne indica due, scrivi uno scenario per livello.

Tipi ammessi: positivo, negativo, limite, sicurezza, accessibilità
Livelli ammessi: unit, api, e2e

## 7. Ricerca, filtri, ordinamento e liste

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| O71 | Ricerca di un ordine tramite identificativo | positivo | api |
| O72 | Ricerca di un ordine tramite identificativo dall'interfaccia | positivo | e2e |
| O73 | Ricerca senza risultati: viene mostrato uno stato vuoto comprensibile | negativo | e2e |
| O74 | Filtraggio degli ordini per stato | positivo | api |
| O75 | Filtri combinati, per esempio cliente e stato, restituiscono i risultati attesi | positivo | api |
| O76 | Ordinamento per data, importo o identificativo secondo il criterio selezionato | positivo | api |
| O77 | Paginazione: nessun ordine duplicato o perso tra pagine, a dati invariati | limite | api |
| O78 | Filtri e paginazione combinati mantengono i risultati coerenti | limite | api |
| O79 | Ricerca con input vuoto, spazi o caratteri speciali gestita correttamente | limite | unit |
| O80 | La lista mostra lo stato e il totale corretti per ogni ordine | positivo | e2e |

## Esempio di scenario

PUNTO: O73: Ricerca senza risultati: viene mostrato uno stato vuoto comprensibile
RIGA DEL REQUISITO: Dalla lista degli ordini si può cercare un ordine per numero.
TIPO: negativo
LIVELLI AMMESSI: e2e
Risposta:
{"livello": "e2e",
 "titolo": "Ricerca di un numero d'ordine inesistente",
 "dato": ["che ho aperto la lista degli ordini"],
 "quando": ["cerco il numero d'ordine '999999'"],
 "allora": ["la lista non mostra nessun ordine", "vedo un messaggio che dice che non ci sono risultati"]}


## Esempio di scenario api

PUNTO: O74: Filtraggio degli ordini per stato
RIGA DEL REQUISITO: Gli ordini si possono filtrare per stato.
TIPO: positivo
LIVELLI AMMESSI: api
Risposta:
{"livello": "api",
 "titolo": "Filtro degli ordini per stato Pagato",
 "dato": ["che esistono ordini in stato 'Pagato' e in stato 'Annullato'"],
 "quando": ["invio la richiesta della lista degli ordini con filtro stato 'Pagato'"],
 "allora": ["la richiesta viene accettata", "la risposta contiene solo ordini in stato 'Pagato'"]}
