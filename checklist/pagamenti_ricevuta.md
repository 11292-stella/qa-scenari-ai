# Checklist – Pagamenti: ricevuta

Ricevuta generata dal gestionale. Lo scontrino FISCALE (registratore telematico, numerazione, corrispettivi) è un'altra cosa e non va considerato equivalente.

Applica solo i punti che il requisito permette di verificare.
Per i punti di cui il requisito non parla, NON inventare il comportamento: scrivi una domanda aperta.
Ogni scenario ha UN solo livello: se un punto ne indica due, scrivi uno scenario per livello.

Tipi ammessi: positivo, negativo, limite, sicurezza, accessibilità
Livelli ammessi: unit, api, e2e

## 5. Scontrino e ricevuta

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| PAY47 | Dopo un pagamento completato viene generata la ricevuta prevista | positivo | e2e |
| PAY48 | I dati della ricevuta corrispondono a ordine, importo e metodo di pagamento | positivo | api |
| PAY49 | Ricevuta con importo, data, identificativo e altri campi obbligatori mancanti | negativo | unit |
| PAY50 | La ricevuta non viene emessa come pagamento completato se la transazione è stata rifiutata | negativo | api |
| PAY51 | Apertura o visualizzazione della ricevuta dopo il pagamento | positivo | e2e |
| PAY52 | Stampa o esportazione della ricevuta, se prevista | positivo | e2e |
| PAY53 | Errore di stampa: la transazione non viene registrata nuovamente | negativo | e2e |
| PAY54 | Nuova richiesta di ricevuta: non genera un secondo pagamento | limite | api |
| PAY55 | Ricevuta associata all'ordine e al pagamento corretti | positivo | api |
| PAY56 | Utente non autorizzato tenta di leggere la ricevuta di un altro cliente | sicurezza | api |
| PAY57 | Dati sensibili della carta non vengono esposti nella ricevuta o nei log impropri | sicurezza | api |
| PAY58 | Ricevuta utilizzabile da tastiera e con etichette comprensibili, se visualizzata nell'interfaccia | accessibilità | e2e |

> Qui distinguerei la semplice ricevuta generata dal software dallo scontrino fiscale, che può richiedere integrazioni e vincoli specifici. Il tuo programma non dovrebbe considerarli equivalenti.

> La fiscalità, il registratore telematico, la numerazione fiscale e l'eventuale trasmissione dei corrispettivi devono diventare una sezione condizionale separata, perché non tutti i software gestiscono direttamente questi processi.

## Esempio di scenario

PUNTO: PAY47: Dopo un pagamento completato viene generata la ricevuta prevista
RIGA DEL REQUISITO: Dopo il pagamento la cassa genera la ricevuta dell'ordine.
TIPO: positivo
LIVELLI AMMESSI: e2e
Risposta:
{"livello": "e2e",
 "titolo": "Ricevuta dopo il pagamento",
 "dato": ["che ho pagato alla cassa l'ordine del tavolo '9'"],
 "quando": ["apro il dettaglio dell'ordine del tavolo '9'"],
 "allora": ["vedo la ricevuta dell'ordine"]}

## Esempio di scenario api

PUNTO: PAY50: La ricevuta non viene emessa come pagamento completato se la transazione è stata rifiutata
RIGA DEL REQUISITO: La ricevuta viene emessa solo per i pagamenti completati.
TIPO: negativo
LIVELLI AMMESSI: api
Risposta:
{"livello": "api",
 "titolo": "Nessuna ricevuta per un pagamento rifiutato",
 "dato": ["che il pagamento dell'ordine 'T9' è stato rifiutato"],
 "quando": ["invio la richiesta della ricevuta dell'ordine 'T9'"],
 "allora": ["la richiesta viene rifiutata", "la risposta non contiene una ricevuta"]}
