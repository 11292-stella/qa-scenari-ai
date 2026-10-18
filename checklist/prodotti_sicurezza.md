# Checklist – Prodotti: sicurezza, autorizzazioni e accessibilità

Applica solo i punti che il requisito permette di verificare.
Per i punti di cui il requisito non parla, NON inventare il comportamento: scrivi una domanda aperta.
Ogni scenario ha UN solo livello: se un punto ne indica due, scrivi uno scenario per livello.

Tipi ammessi: positivo, negativo, limite, sicurezza, accessibilità
Livelli ammessi: unit, api, e2e

## 9. Sicurezza, autorizzazioni e robustezza

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| P100 | API del catalogo invocata senza autenticazione, quando l'autenticazione è richiesta | sicurezza | api |
| P101 | Utente senza permessi tenta di creare un prodotto | sicurezza | api |
| P102 | Utente senza permessi tenta di modificare o eliminare un prodotto | sicurezza | api |
| P103 | Un utente non può accedere a prodotti di un'altra organizzazione, se esiste questa separazione | sicurezza | api |
| P104 | Tentativi di SQL injection nei campi di ricerca e modifica non compromettono i dati | sicurezza | api |
| P105 | HTML o JavaScript nei campi testuali non vengono eseguiti quando il prodotto è visualizzato | sicurezza | e2e |
| P106 | Campi protetti o interni non possono essere modificati tramite parametri aggiuntivi non autorizzati | sicurezza | api |
| P107 | Errori API non espongono dettagli interni, credenziali o informazioni sensibili | sicurezza | api |
| P108 | Navigazione e operazioni principali del catalogo utilizzabili da tastiera | accessibilità | e2e |
| P109 | Campi, messaggi di errore, pulsanti e immagini hanno nomi o etichette accessibili dove necessari | accessibilità | e2e |

## Esempio di scenario

PUNTO: P101: Utente senza permessi tenta di creare un prodotto
RIGA DEL REQUISITO: Solo gli amministratori possono creare prodotti.
TIPO: sicurezza
LIVELLI AMMESSI: api
Risposta:
{"livello": "api",
 "titolo": "Il cameriere non può creare prodotti",
 "dato": ["che ho fatto l'accesso come utente 'cameriere'"],
 "quando": ["invio la richiesta di creazione di un prodotto"],
 "allora": ["la richiesta viene rifiutata", "il prodotto non è presente nel catalogo"]}
