# Checklist – Pagamenti: avvio e coerenza con l'ordine

Avvio e registrazione del pagamento, e stato dell'ordine dopo il pagamento.
Da usare insieme a pagamenti_contanti, pagamenti_carta, pagamenti_rimborsi, pagamenti_ricevuta quando il requisito ne parla.
Fiscalità, registratore telematico e corrispettivi NON sono qui: andranno in una checklist separata.

Applica solo i punti che il requisito permette di verificare.
Per i punti di cui il requisito non parla, NON inventare il comportamento: scrivi una domanda aperta.
Ogni scenario ha UN solo livello: se un punto ne indica due, scrivi uno scenario per livello.

Tipi ammessi: positivo, negativo, limite, sicurezza, accessibilità
Livelli ammessi: unit, api, e2e

## 1. Avvio e registrazione del pagamento

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| PAY1 | Avvio di un pagamento per un ordine valido | positivo | e2e |
| PAY2 | Creazione del pagamento tramite API e restituzione dell'identificativo | positivo | api |
| PAY3 | Importo del pagamento corrispondente a quello dovuto | positivo | api |
| PAY4 | Tentativo di pagamento senza ordine valido | negativo | api |
| PAY5 | Importo mancante o non numerico nel form | negativo | unit |
| PAY6 | Importo mancante o non valido inviato direttamente all'API | negativo | api |
| PAY7 | Importo pari a zero, se non ammesso | limite | api |
| PAY8 | Importo negativo rifiutato | negativo | api |
| PAY9 | Importo superiore al totale dovuto, se non consentito | limite | api |
| PAY10 | Pagamento di un ordine già pagato: nessun addebito duplicato indesiderato | negativo | api |
| PAY11 | Ordine inesistente o non accessibile: pagamento rifiutato | negativo | api |
| PAY12 | Errore del server durante l'avvio: messaggio comprensibile e possibilità di gestire il nuovo tentativo | negativo | e2e |

## 6. Coerenza tra ordine e pagamento

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| PAY59 | Pagamento completato: l'ordine assume lo stato previsto | positivo | api |
| PAY60 | Pagamento rifiutato: lo stato dell'ordine rimane coerente con il processo | negativo | api |
| PAY61 | Pagamento parziale: il residuo viene calcolato correttamente, se previsto | positivo | unit |
| PAY62 | Somma di più pagamenti associati allo stesso ordine | positivo | unit |
| PAY63 | Pagamenti simultanei sullo stesso ordine: non viene superato l'importo dovuto, salvo regole diverse (se il requisito non definisce le regole di concorrenza, è una domanda aperta) | limite | api |
| PAY64 | Modifica dell'importo dell'ordine mentre il pagamento è in corso (se il requisito non dice se l'ordine viene bloccato, è una domanda aperta) | limite | api |
| PAY65 | Ricaricamento della pagina dopo il pagamento: lo stato non torna a quello precedente | positivo | e2e |
| PAY66 | Un errore di comunicazione tra pagamento e ordine non lascia i due stati incoerenti | negativo | api |
| PAY67 | Utente non autorizzato tenta di registrare o modificare un pagamento | sicurezza | api |
| PAY68 | Importo o stato del pagamento manipolati dal client non vengono accettati senza verifica lato server | sicurezza | api |

> Per PAY63 e PAY64 è essenziale definire le regole di concorrenza e di blocco dell'ordine: non tutti i gestionali permettono più pagamenti sullo stesso ordine.

## Esempio di scenario

PUNTO: PAY8: Importo negativo rifiutato
RIGA DEL REQUISITO: L'importo del pagamento deve essere maggiore di zero.
TIPO: negativo
LIVELLI AMMESSI: api
Risposta:
{"livello": "api",
 "titolo": "Pagamento con importo negativo rifiutato",
 "dato": ["che esiste l'ordine 'T12' da pagare per '35,00'"],
 "quando": ["invio la richiesta di pagamento dell'ordine 'T12' con importo '-5,00'"],
 "allora": ["la richiesta viene rifiutata", "l'ordine 'T12' resta da pagare"]}

## Esempio di scenario e2e

PUNTO: PAY1: Avvio di un pagamento per un ordine valido
RIGA DEL REQUISITO: Dalla cassa si avvia il pagamento di un ordine aperto.
TIPO: positivo
LIVELLI AMMESSI: e2e
Risposta:
{"livello": "e2e",
 "titolo": "Avvio del pagamento dalla cassa",
 "dato": ["che ho aperto alla cassa l'ordine del tavolo '12'"],
 "quando": ["premo il bottone Paga"],
 "allora": ["vedo la schermata di pagamento con l'importo dell'ordine"]}

## Esempio di scenario unit

PUNTO: PAY5: Importo mancante o non numerico nel form
RIGA DEL REQUISITO: L'importo è obbligatorio e deve essere un numero.
TIPO: negativo
LIVELLI AMMESSI: unit
Risposta:
{"livello": "unit",
 "titolo": "Importo non numerico non accettato",
 "dato": ["che sto compilando il form di pagamento"],
 "quando": ["scrivo 'dieci' nel campo Importo"],
 "allora": ["vedo un messaggio di errore sotto il campo Importo"]}
