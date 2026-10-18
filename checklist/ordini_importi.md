# Checklist – Ordini: totali, sconti e importi

Calcoli di righe e totali, sconti, IVA, arrotondamenti. Riusabile anche per fatture e scontrini.

Applica solo i punti che il requisito permette di verificare.
Per i punti di cui il requisito non parla, NON inventare il comportamento: scrivi una domanda aperta.
Ogni scenario ha UN solo livello: se un punto ne indica due, scrivi uno scenario per livello.

Tipi ammessi: positivo, negativo, limite, sicurezza, accessibilità
Livelli ammessi: unit, api, e2e

## 3. Totali, sconti e importi

> Questi casi sono particolarmente importanti perché gli errori di calcolo possono propagarsi a fatture, pagamenti e report.

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| O31 | Il totale della riga corrisponde a quantità × prezzo unitario, secondo le regole di arrotondamento | positivo | unit |
| O32 | Il totale dell'ordine corrisponde alla somma delle righe e degli eventuali importi aggiuntivi previsti | positivo | unit |
| O33 | Applicazione di uno sconto percentuale valido | positivo | unit |
| O34 | Applicazione di uno sconto fisso valido | positivo | unit |
| O35 | Sconto superiore al limite consentito | limite | api |
| O36 | Sconto che rende il totale negativo, se non ammesso | negativo | api |
| O37 | Calcolo dell'IVA secondo aliquote e regole configurate | positivo | unit |
| O38 | Gestione degli importi con molte cifre decimali e arrotondamenti | limite | unit |
| O39 | Importo totale oltre il limite monetario consentito, se definito | limite | api |
| O40 | Il backend non accetta un totale manipolato inviato dal client senza ricalcolarlo o verificarlo | sicurezza | api |
| O41 | Modifica della quantità: i totali vengono aggiornati correttamente nell'interfaccia | positivo | e2e |
| O42 | Rimozione di una riga: il totale viene ricalcolato correttamente | positivo | e2e |

> Qui c'è una distinzione fondamentale: unit test per la matematica, API test per verificare i dati ricevuti e i calcoli lato server, E2E per controllare che l'utente veda il risultato corretto. Non serve verificare ogni combinazione matematica con un E2E lento.

## Esempio di scenario

PUNTO: O33: Applicazione di uno sconto percentuale valido
RIGA DEL REQUISITO: Sul totale dell'ordine si può applicare uno sconto percentuale.
TIPO: positivo
LIVELLI AMMESSI: unit
Risposta:
{"livello": "unit",
 "titolo": "Sconto del 10% su un ordine da 50",
 "dato": ["che il totale dell'ordine è '50,00'"],
 "quando": ["applico uno sconto del '10%'"],
 "allora": ["il totale dell'ordine diventa '45,00'"]}


## Esempio di scenario api

PUNTO: O40: Il backend non accetta un totale manipolato inviato dal client senza ricalcolarlo o verificarlo
RIGA DEL REQUISITO: Il totale dell'ordine è calcolato dal sistema in base alle righe.
TIPO: sicurezza
LIVELLI AMMESSI: api
Risposta:
{"livello": "api",
 "titolo": "Totale inviato dal client non usato",
 "dato": ["che l'ordine ha una riga da '2' pezzi a '5,00'"],
 "quando": ["invio la richiesta di salvataggio dell'ordine con totale '1,00'"],
 "allora": ["il totale salvato dell'ordine è '10,00'"]}
