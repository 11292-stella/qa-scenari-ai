# Checklist – Pagamenti: carta simulata (autorizzazione, rifiuto, timeout)

Ambiente di test con un SIMULATORE di pagamento, non una carta reale: i casi dipendono dalle risposte che il simulatore permette di configurare.

Applica solo i punti che il requisito permette di verificare.
Per i punti di cui il requisito non parla, NON inventare il comportamento: scrivi una domanda aperta.
Ogni scenario ha UN solo livello: se un punto ne indica due, scrivi uno scenario per livello.

Tipi ammessi: positivo, negativo, limite, sicurezza, accessibilità
Livelli ammessi: unit, api, e2e

## 3. Carta simulata: autorizzazione, rifiuto e timeout

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| PAY21 | Pagamento con carta simulata approvato: l'operazione risulta completata | positivo | e2e |
| PAY22 | API di pagamento: risposta di approvazione gestita correttamente | positivo | api |
| PAY23 | Carta simulata rifiutata: il pagamento non risulta completato | negativo | api |
| PAY24 | Carta rifiutata: messaggio comprensibile e possibilità di riprovare, se prevista | negativo | e2e |
| PAY25 | Simulazione di fondi insufficienti | negativo | api |
| PAY26 | Simulazione di carta scaduta o non valida | negativo | api |
| PAY27 | Timeout del servizio di pagamento: stato gestito senza presumere che la transazione sia fallita (il provider potrebbe averla già approvata: niente doppio addebito) | limite | api |
| PAY28 | Servizio di pagamento non raggiungibile | negativo | api |
| PAY29 | Risposta del simulatore malformata o incompleta | negativo | api |
| PAY30 | Doppio clic su Paga: non vengono avviate transazioni duplicate indesiderate | limite | e2e |
| PAY31 | Ripetizione della stessa richiesta API: una sola transazione viene registrata, quando è prevista l'idempotenza | limite | api |
| PAY32 | Una risposta tardiva di approvazione aggiorna correttamente lo stato della transazione | limite | api |
| PAY33 | Rifiuto del pagamento: l'ordine non viene segnato come pagato | negativo | api |
| PAY34 | Dopo un rifiuto, un nuovo tentativo valido può completare il pagamento, se consentito | positivo | e2e |

> Questa sezione riguarda un ambiente di test con un simulatore di pagamento, non una carta reale. I casi dipendono dalle risposte che il simulatore permette di configurare.

> Attenzione al timeout: non è detto che una transazione sia fallita solo perché il client non ha ricevuto la risposta. Il simulatore o il provider potrebbe averla già approvata. Il sistema deve prevedere un modo coerente per riconciliare lo stato, senza addebitare due volte.

## Esempio di scenario

PUNTO: PAY23: Carta simulata rifiutata: il pagamento non risulta completato
RIGA DEL REQUISITO: Se il simulatore rifiuta la carta, il pagamento non è completato.
TIPO: negativo
LIVELLI AMMESSI: api
Risposta:
{"livello": "api",
 "titolo": "Carta rifiutata dal simulatore",
 "dato": ["che il simulatore è impostato per rifiutare la carta"],
 "quando": ["invio la richiesta di pagamento con carta dell'ordine 'T7' da '42,00'"],
 "allora": ["la richiesta viene rifiutata", "il pagamento dell'ordine 'T7' non risulta completato"]}

## Esempio di scenario e2e

PUNTO: PAY24: Carta rifiutata: messaggio comprensibile e possibilità di riprovare, se prevista
RIGA DEL REQUISITO: Con la carta rifiutata compare il messaggio 'Pagamento non riuscito' e si può riprovare.
TIPO: negativo
LIVELLI AMMESSI: e2e
Risposta:
{"livello": "e2e",
 "titolo": "Messaggio di carta rifiutata e nuovo tentativo",
 "dato": ["che il simulatore è impostato per rifiutare la carta", "che ho aperto la schermata di pagamento dell'ordine del tavolo '7'"],
 "quando": ["premo il bottone Paga con carta"],
 "allora": ["vedo il messaggio 'Pagamento non riuscito'", "vedo il bottone Riprova"]}
