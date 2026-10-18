# Checklist – Ordini

Creazione, righe e quantità, cliente collegato, stati e ciclo di vita.
Da usare insieme a ordini_importi, ordini_magazzino, ordini_liste, ordini_sicurezza quando il requisito ne parla.

Applica solo i punti che il requisito permette di verificare.
Per i punti di cui il requisito non parla, NON inventare il comportamento: scrivi una domanda aperta.
Ogni scenario ha UN solo livello: se un punto ne indica due, scrivi uno scenario per livello.

Tipi ammessi: positivo, negativo, limite, sicurezza, accessibilità
Livelli ammessi: unit, api, e2e

## 1. Creazione e gestione dell'ordine

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| O1 | Creazione di un ordine con i dati obbligatori validi | positivo | e2e |
| O2 | L'API crea l'ordine e restituisce il suo identificativo | positivo | api |
| O3 | L'ordine appena creato compare nella lista degli ordini | positivo | e2e |
| O4 | Apertura del dettaglio di un ordine esistente | positivo | e2e |
| O5 | Recupero dell'ordine tramite API con tutti i dati previsti | positivo | api |
| O6 | Campo obbligatorio mancante: il form segnala l'errore | negativo | unit |
| O7 | Richiesta API con campo obbligatorio mancante | negativo | api |
| O8 | Annullamento della compilazione prima del salvataggio: nessun ordine creato | negativo | e2e |
| O9 | Modifica di un ordine modificabile: i nuovi dati vengono salvati | positivo | e2e |
| O10 | Dopo il salvataggio e il ricaricamento, i dati dell'ordine restano corretti | positivo | e2e |
| O11 | Apertura di un ordine inesistente tramite URL | negativo | e2e |
| O12 | Recupero tramite API di un ordine inesistente | negativo | api |
| O13 | Doppio clic su Salva: non vengono creati ordini duplicati indesiderati | limite | e2e |
| O14 | Richiesta di creazione ripetuta dopo timeout o retry | limite | api |
| O15 | Errore del server durante il salvataggio: feedback comprensibile e dati del form preservati, se previsto | negativo | e2e |

## 2. Righe d'ordine, prodotti e quantità

> Questa è una delle aree più importanti, perché molti errori nei gestionali riguardano le righe dell'ordine, le quantità e i prezzi.

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| O16 | Aggiunta di un prodotto valido all'ordine | positivo | e2e |
| O17 | Aggiunta di una riga d'ordine tramite API con dati validi | positivo | api |
| O18 | Quantità pari a zero, se non ammessa | limite | unit |
| O19 | Quantità negativa non ammessa | negativo | api |
| O20 | Quantità decimale gestita secondo le regole previste | limite | unit |
| O21 | Quantità superiore al massimo consentito, se definito | limite | api |
| O22 | Prodotto inesistente o non identificabile | negativo | api |
| O23 | Rimozione di una riga dall'ordine prima del salvataggio | positivo | e2e |
| O24 | Modifica della quantità di una riga già inserita | positivo | e2e |
| O25 | Rimozione di una riga tramite API e verifica dell'ordine aggiornato | positivo | api |
| O26 | Inserimento dello stesso prodotto su più righe: accorpato o tenuto separato come dice il requisito (non presumere che sia vietato) | limite | api |
| O27 | Prodotto non più attivo o non acquistabile | negativo | api |
| O28 | Prezzo unitario non valido o negativo inviato direttamente all'API | negativo | api |
| O29 | Modifica del prezzo nel client non autorizzata dal sistema | sicurezza | api |
| O30 | Descrizione o nome del prodotto contenente caratteri speciali | limite | unit |

> Nota per il generatore: O26 non deve presumere che due righe uguali siano vietate. Il sistema potrebbe accorparle oppure mantenerle separate. Il comportamento atteso va ricavato dai requisiti.

## 4. Cliente, indirizzo e dati collegati

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| O43 | Associazione di un cliente esistente all'ordine | positivo | api |
| O44 | Creazione di un ordine senza cliente, se consentita | limite | e2e |
| O45 | Associazione di un cliente inesistente | negativo | api |
| O46 | Modifica del cliente associato e verifica del riferimento salvato | positivo | api |
| O47 | Cliente disattivato o non selezionabile | negativo | api |
| O48 | I dati del cliente mostrati nel dettaglio corrispondono a quelli associati all'ordine | positivo | e2e |
| O49 | Eliminazione o modifica di un cliente collegato a ordini già esistenti: cosa succede agli ordini storici | limite | api |
| O50 | Utente non autorizzato a visualizzare i dati del cliente collegato | sicurezza | api |

> Per O49 la domanda aperta potrebbe essere: cosa deve succedere agli ordini storici quando il cliente viene disattivato, modificato o cancellato? La risposta dipende dal modello dei dati e dalle regole di conservazione.

## 5. Stati e ciclo di vita dell'ordine

> Questa sezione è molto importante per il tuo generatore, perché un ordine non è soltanto un record: spesso attraversa diverse fasi.

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| O51 | Un nuovo ordine riceve lo stato iniziale previsto | positivo | api |
| O52 | Visualizzazione dello stato corrente nel dettaglio dell'ordine | positivo | e2e |
| O53 | Modifica dello stato tramite un'operazione autorizzata | positivo | api |
| O54 | Tentativo di impostare uno stato non previsto dal sistema | negativo | api |
| O55 | Transizione da uno stato a uno incompatibile con le regole definite | negativo | api |
| O56 | Annullamento di un ordine ancora annullabile | positivo | e2e |
| O57 | Tentativo di annullare un ordine in uno stato che non lo consente | negativo | api |
| O58 | Modifica di un ordine dopo la conferma, se non consentita | negativo | api |
| O59 | Un ordine completato non torna a uno stato precedente senza una transizione autorizzata | sicurezza | api |
| O60 | Aggiornamento dello stato: il nuovo valore viene mostrato nella lista dopo il salvataggio | positivo | e2e |
| O61 | Richieste simultanee di cambio stato non producono transizioni incoerenti | limite | api |
| O62 | Un errore durante il cambio di stato non lascia l'ordine in uno stato parziale o incoerente | negativo | api |

> Non darei per scontata una sequenza universale come Bozza → Confermato → Spedito → Completato: in un gestionale di ristorazione, per esempio, gli stati potrebbero essere completamente diversi.

## Esempio di scenario

PUNTO: O19: Quantità negativa non ammessa
RIGA DEL REQUISITO: La quantità di ogni riga dell'ordine deve essere maggiore di zero.
TIPO: negativo
LIVELLI AMMESSI: api
Risposta:
{"livello": "api",
 "titolo": "Riga con quantità negativa rifiutata",
 "dato": ["che esiste un ordine aperto"],
 "quando": ["invio la richiesta di aggiunta di una riga con quantità '-2'"],
 "allora": ["la richiesta viene rifiutata", "l'ordine non contiene la nuova riga"]}
