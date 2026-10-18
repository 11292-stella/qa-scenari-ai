# Checklist – Liste e ricerca (modulo trasversale): paginazione e aggiornamento dei dati

Modulo trasversale: non spuntarlo insieme a ordini_liste o prodotti_ricerca.

Applica solo i punti che il requisito permette di verificare.
Per i punti di cui il requisito non parla, NON inventare il comportamento: scrivi una domanda aperta.
Ogni scenario ha UN solo livello: se un punto ne indica due, scrivi uno scenario per livello.

Tipi ammessi: positivo, negativo, limite, sicurezza, accessibilità
Livelli ammessi: unit, api, e2e

## 5. Paginazione e grandi quantità di dati

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| LS49 | Navigazione alla pagina successiva | positivo | e2e |
| LS50 | Ritorno alla pagina precedente | positivo | e2e |
| LS51 | Selezione della dimensione della pagina, se prevista | positivo | e2e |
| LS52 | Numero di record restituiti coerente con il limite richiesto | positivo | api |
| LS53 | Ultima pagina con meno record della dimensione selezionata | limite | api |
| LS54 | Pagina oltre il numero di pagine disponibili | limite | api |
| LS55 | Dimensione pagina pari a zero o negativa rifiutata o gestita secondo le regole definite | negativo | api |
| LS56 | Dimensione pagina superiore al massimo consentito | limite | api |
| LS57 | Nessun record duplicato o perso tra pagine, a dati invariati | limite | api |
| LS58 | Dopo una modifica dei dati, il numero totale di risultati viene aggiornato correttamente | positivo | api |
| LS59 | Eliminazione dell'ultimo record di una pagina: navigazione e risultati restano coerenti | limite | e2e |
| LS60 | Filtri e ricerca vengono mantenuti o resettati durante la navigazione secondo i requisiti | limite | e2e |

## 6. Aggiornamento dei dati e coerenza della lista

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| LS61 | Un nuovo record compare nella lista secondo il comportamento previsto | positivo | e2e |
| LS62 | Un record modificato mostra i dati aggiornati | positivo | api |
| LS63 | Un record eliminato non compare più nei risultati aggiornati | positivo | api |
| LS64 | Un record che non soddisfa più i filtri attivi non compare più nei risultati | positivo | api |
| LS65 | Ricaricamento della pagina: vengono recuperati i dati aggiornati dal servizio | positivo | e2e |
| LS66 | Aggiornamenti concorrenti dei dati non producono una lista incoerente | limite | api |
| LS67 | Errore durante l'aggiornamento: la lista non mostra come salvata un'operazione fallita | negativo | e2e |
| LS68 | La lista non mantiene indefinitamente dati obsoleti quando è richiesto un aggiornamento | limite | e2e |

## Esempio di scenario

PUNTO: LS53: Ultima pagina con meno record della dimensione selezionata
RIGA DEL REQUISITO: La lista delle fatture mostra 20 righe per pagina.
TIPO: limite
LIVELLI AMMESSI: api
Risposta:
{"livello": "api",
 "titolo": "Ultima pagina con meno righe",
 "dato": ["che esistono '45' fatture"],
 "quando": ["invio la richiesta della pagina '3' della lista delle fatture"],
 "allora": ["la richiesta viene accettata", "la risposta contiene '5' fatture"]}

## Esempio di scenario e2e

PUNTO: LS49: Navigazione alla pagina successiva
RIGA DEL REQUISITO: Sotto la lista c'è il bottone Pagina successiva.
TIPO: positivo
LIVELLI AMMESSI: e2e
Risposta:
{"livello": "e2e",
 "titolo": "Passaggio alla pagina successiva",
 "dato": ["che ho aperto la lista delle fatture alla pagina '1'"],
 "quando": ["premo il bottone Pagina successiva"],
 "allora": ["vedo la pagina '2' della lista delle fatture"]}
