# Checklist – Liste e ricerca (modulo trasversale): permessi, sicurezza e accessibilità

Modulo trasversale: non spuntarlo insieme a ordini_liste o prodotti_ricerca.

Applica solo i punti che il requisito permette di verificare.
Per i punti di cui il requisito non parla, NON inventare il comportamento: scrivi una domanda aperta.
Ogni scenario ha UN solo livello: se un punto ne indica due, scrivi uno scenario per livello.

Tipi ammessi: positivo, negativo, limite, sicurezza, accessibilità
Livelli ammessi: unit, api, e2e

## 7. Permessi, sicurezza e accessibilità

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| LS69 | Utente senza autenticazione: accesso alla lista protetta rifiutato | sicurezza | api |
| LS70 | Utente senza permessi: richiesta API di lettura rifiutata | sicurezza | api |
| LS71 | L'utente visualizza solo i record del proprio ambito autorizzato, se previsto | sicurezza | api |
| LS72 | Parametri di ricerca manipolati non permettono di aggirare i permessi | sicurezza | api |
| LS73 | Errori della ricerca non espongono query interne o dati sensibili | sicurezza | api |
| LS74 | Navigazione della lista tramite tastiera | accessibilità | e2e |
| LS75 | Campo di ricerca con etichetta accessibile e nome comprensibile | accessibilità | unit |
| LS76 | Intestazioni delle colonne e ordinamento identificabili dalle tecnologie assistive | accessibilità | e2e |
| LS77 | Messaggi di caricamento, errore e lista vuota accessibili alle tecnologie assistive | accessibilità | e2e |
| LS78 | Indicatori di pagina corrente e navigazione tra pagine accessibili alle tecnologie assistive | accessibilità | e2e |

## Esempio di scenario

PUNTO: LS69: Utente senza autenticazione: accesso alla lista protetta rifiutato
RIGA DEL REQUISITO: La lista delle fatture è visibile solo agli utenti che hanno fatto l'accesso.
TIPO: sicurezza
LIVELLI AMMESSI: api
Risposta:
{"livello": "api",
 "titolo": "Lista senza autenticazione rifiutata",
 "dato": ["che non ho fatto l'accesso"],
 "quando": ["invio la richiesta della lista delle fatture"],
 "allora": ["la richiesta viene rifiutata con codice '401'"]}

## Esempio di scenario e2e

PUNTO: LS74: Navigazione della lista tramite tastiera
RIGA DEL REQUISITO: La lista delle fatture si può usare tutta da tastiera.
TIPO: accessibilità
LIVELLI AMMESSI: e2e
Risposta:
{"livello": "e2e",
 "titolo": "Lista usabile da tastiera",
 "dato": ["che ho aperto la lista delle fatture"],
 "quando": ["premo il tasto Tab fino alla prima fattura della lista", "premo il tasto Invio"],
 "allora": ["vedo il dettaglio della prima fattura"]}
