# Checklist – Login

Applica solo i punti che il requisito permette di verificare.
Per i punti di cui il requisito non parla, NON inventare il comportamento: scrivi una domanda aperta.
Ogni scenario ha UN solo livello: se un punto ne indica due, scrivi uno scenario per livello.

Tipi ammessi: positivo, negativo, limite, sicurezza, accessibilità
Livelli ammessi: unit, api, e2e

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| L1 | Login con credenziali valide porta all'area riservata | positivo | e2e |
| L2 | Con credenziali valide l'API restituisce token o sessione | positivo | api |
| L3 | Password errata: messaggio di errore, si resta sulla pagina di login | negativo | e2e |
| L4 | Utente inesistente: STESSO messaggio della password errata | sicurezza | e2e |
| L5 | Con credenziali errate l'API risponde con errore e senza token | negativo | api |
| L6 | Campi vuoti, uno solo compilato o solo spazi: non si può inviare | limite | unit |
| L7 | Maiuscole/minuscole in username e password | limite | api |
| L8 | Lunghezza massima dei campi | limite | unit |
| L9 | Le pagine protette senza login riportano alla pagina di login | sicurezza | e2e |
| L10 | Il logout chiude la sessione (anche con il tasto "indietro" del browser) | positivo | e2e |
| L11 | Sessione o token scaduto: si torna alla pagina di login | negativo | api |
| L12 | Blocco o attesa dopo troppi tentativi errati | sicurezza | api |
| L13 | La password nel campo è nascosta | positivo | unit |
| L14 | Email o username con formato non valido | negativo | unit |
| L15 | Spazi prima o dopo username/email | limite | unit, api |
| L16 | Invio del form premendo Invio dalla tastiera | positivo | e2e |
| L17 | Doppio clic sul pulsante di login: nessuna richiesta o azione duplicata | limite | e2e, api |
| L18 | Durante l'invio il pulsante si disabilita o compare un caricamento, se previsto | positivo | unit, e2e |
| L19 | Errore di rete o server non raggiungibile: messaggio comprensibile | negativo | api, e2e |
| L20 | Risposta lenta del server: l'attesa è gestita correttamente | limite | api, e2e |
| L21 | Errore del server (es. HTTP 500): messaggio gestito correttamente | negativo | api, e2e |
| L22 | Token non valido, manipolato o malformato: accesso negato | sicurezza | api |
| L23 | Utente autenticato ma senza i permessi necessari | negativo | api, e2e |
| L24 | Ricaricando la pagina dopo il login si resta autenticati | positivo | e2e |
| L25 | Apertura di una pagina protetta in una seconda scheda | limite | e2e |
| L26 | Password con caratteri speciali, Unicode o spazi, se ammessi dal requisito | limite | unit, api |
| L27 | Accesso con account disabilitato, sospeso o non verificato | negativo | api, e2e |
| L28 | Tentativo di injection nei campi di login | sicurezza | api |
| L29 | La password non compare in chiaro nei log, nell'URL o nelle risposte dell'API | sicurezza | api |
| L30 | Login con una sessione già attiva | limite | e2e |
| L31 | Sessione dopo chiusura e riapertura del browser | limite | e2e |
| L32 | Messaggi di errore accessibili da tastiera e screen reader | accessibilità | unit, e2e |


## Esempio di scenario

PUNTO: L3: Password errata: messaggio di errore, si resta sulla pagina di login
RIGA DEL REQUISITO: Con username o password errati compare lo stesso messaggio di errore e l'utente resta sulla pagina di login.
TIPO: negativo
LIVELLI AMMESSI: e2e
Risposta:
{"livello": "e2e",
 "titolo": "Login con password errata mostra un messaggio di errore",
 "dato": ["che sono sulla pagina di login"],
 "quando": ["eseguo il login con username 'mrossi' e password 'password-sbagliata'"],
 "allora": ["vedo il messaggio di errore", "resto sulla pagina di login"]}


## Esempio di scenario api

PUNTO: L22: Token non valido, manipolato o malformato: accesso negato
RIGA DEL REQUISITO: Le API del gestionale accettano solo richieste con un token valido.
TIPO: sicurezza
LIVELLI AMMESSI: api
Risposta:
{"livello": "api",
 "titolo": "Token manipolato rifiutato",
 "dato": ["che ho un token di accesso modificato a mano"],
 "quando": ["invio la richiesta della lista degli ordini con quel token"],
 "allora": ["la richiesta viene rifiutata con codice '401'", "la risposta non contiene dati degli ordini"]}
