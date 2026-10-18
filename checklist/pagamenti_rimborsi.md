# Checklist – Pagamenti: annullamento, interruzione e rimborso

Casi diversi tra loro: chiudere la finestra prima della conferma non è annullare una transazione autorizzata, e un rimborso non è cancellare un pagamento.
Se il gestionale non ha annullamenti o rimborsi, questi punti sono NON APPLICABILI (domande aperte), non test falliti.

Applica solo i punti che il requisito permette di verificare.
Per i punti di cui il requisito non parla, NON inventare il comportamento: scrivi una domanda aperta.
Ogni scenario ha UN solo livello: se un punto ne indica due, scrivi uno scenario per livello.

Tipi ammessi: positivo, negativo, limite, sicurezza, accessibilità
Livelli ammessi: unit, api, e2e

## 4. Annullamento, interruzione e rimborso

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| PAY35 | Annullamento prima della conferma: non viene registrato un pagamento completato | negativo | e2e |
| PAY36 | Chiusura o interruzione del flusso di pagamento prima dell'invio | limite | e2e |
| PAY37 | Annullamento di una transazione ancora annullabile tramite API | positivo | api |
| PAY38 | Tentativo di annullare un pagamento già completato, se non consentito | negativo | api |
| PAY39 | Doppio invio della richiesta di annullamento | limite | api |
| PAY40 | Pagamento già annullato: un secondo annullamento non crea effetti duplicati | limite | api |
| PAY41 | Pagamento rifiutato: non può essere annullato come se fosse completato | negativo | api |
| PAY42 | Rimborso di un pagamento completato, se previsto | positivo | api |
| PAY43 | Rimborso superiore all'importo rimborsabile | negativo | api |
| PAY44 | Richiesta di rimborso duplicata | limite | api |
| PAY45 | Annullamento o rimborso: stato e importi aggiornati correttamente nel dettaglio | positivo | e2e |
| PAY46 | Errore durante l'annullamento: lo stato non viene rappresentato in modo incoerente | negativo | api |

> Questi sono casi diversi: chiudere la finestra prima della conferma non equivale ad annullare una transazione già autorizzata, e un rimborso non equivale a cancellare un pagamento.

> Se il progetto non supporta annullamenti o rimborsi, questi casi devono essere contrassegnati come non applicabili, non come test falliti.

## Esempio di scenario

PUNTO: PAY43: Rimborso superiore all'importo rimborsabile
RIGA DEL REQUISITO: Il rimborso non può superare l'importo pagato.
TIPO: negativo
LIVELLI AMMESSI: api
Risposta:
{"livello": "api",
 "titolo": "Rimborso maggiore del pagato rifiutato",
 "dato": ["che l'ordine 'T3' è stato pagato '30,00'"],
 "quando": ["invio la richiesta di rimborso dell'ordine 'T3' di '35,00'"],
 "allora": ["la richiesta viene rifiutata", "l'importo rimborsato dell'ordine 'T3' resta '0,00'"]}

## Esempio di scenario e2e

PUNTO: PAY35: Annullamento prima della conferma: non viene registrato un pagamento completato
RIGA DEL REQUISITO: Se il cameriere annulla prima di confermare, il pagamento non viene registrato.
TIPO: negativo
LIVELLI AMMESSI: e2e
Risposta:
{"livello": "e2e",
 "titolo": "Annullamento prima della conferma",
 "dato": ["che ho aperto la schermata di pagamento dell'ordine del tavolo '3'"],
 "quando": ["premo il bottone Annulla"],
 "allora": ["l'ordine del tavolo '3' risulta ancora da pagare"]}
