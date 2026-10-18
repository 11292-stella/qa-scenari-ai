# Checklist – Anagrafica (clienti, fornitori, dipendenti)

Applica solo i punti che il requisito permette di verificare.
Per i punti di cui il requisito non parla, NON inventare il comportamento: scrivi una domanda aperta.
Ogni scenario ha UN solo livello: se un punto ne indica due, scrivi uno scenario per livello.

Tipi ammessi: positivo, negativo, limite, sicurezza, accessibilità
Livelli ammessi: unit, api, e2e

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| A1 | Creazione di una nuova anagrafica con tutti i campi obbligatori compilati: viene salvata | positivo | e2e |
| A2 | Dopo il salvataggio l'anagrafica compare nella lista con i dati inseriti | positivo | e2e |
| A3 | Con l'API di creazione l'anagrafica viene salvata e restituita con il suo id | positivo | api |
| A4 | Campo obbligatorio vuoto: non si può salvare e il campo viene segnalato | negativo | unit |
| A5 | Campo obbligatorio con solo spazi: viene trattato come vuoto | limite | unit |
| A6 | Annulla durante la compilazione: niente viene salvato | positivo | e2e |
| A7 | Modifica di un'anagrafica: i nuovi dati vengono salvati e mostrati | positivo | e2e |
| A8 | Eliminazione di un'anagrafica con conferma: sparisce dalla lista | positivo | e2e |
| A9 | Eliminazione annullata dalla finestra di conferma: l'anagrafica resta | negativo | e2e |
| A10 | Lunghezza massima dei campi di testo (nome, ragione sociale, indirizzo) | limite | unit, api |
| A11 | Spazi prima o dopo i valori: vengono tolti al salvataggio | limite | unit, api |
| A12 | Caratteri accentati, apostrofi e nomi composti (es. D'Angelo, Nicolò) salvati correttamente | limite | api, e2e |
| A13 | Email con formato non valido: errore sul campo | negativo | unit |
| A14 | Telefono con lettere o formato non valido: errore sul campo | negativo | unit |
| A15 | Data di nascita nel futuro: errore sul campo | negativo | unit |
| A16 | Codice fiscale: 16 caratteri, formato valido, maiuscole/minuscole gestite | negativo | unit, api |
| A17 | Partita IVA: 11 cifre e cifra di controllo valida | negativo | unit, api |
| A18 | CAP di 5 cifre e provincia con sigla di 2 lettere | negativo | unit |
| A19 | PEC e codice destinatario SDI (7 caratteri) per la fatturazione elettronica | negativo | unit, api |
| A20 | Persona fisica e azienda: i campi obbligatori cambiano in base al tipo | limite | e2e |
| A21 | Duplicato: stesso codice fiscale o partita IVA già presente → errore chiaro | negativo | api, e2e |
| A22 | Duplicato sul nome (stesso nome e cognome): avviso o permesso, come previsto | limite | e2e |
| A23 | Ricerca per nome, codice fiscale o partita IVA trova l'anagrafica | positivo | e2e |
| A24 | Ricerca senza risultati: messaggio "nessun risultato", non pagina vuota | negativo | e2e |
| A25 | Lista con molte anagrafiche: paginazione e ordinamento | limite | e2e, api |
| A26 | Anagrafica usata altrove (es. in un ordine o una fattura): non eliminabile o eliminazione gestita | negativo | api, e2e |
| A27 | Doppio clic su Salva: viene creata una sola anagrafica | limite | e2e, api |
| A28 | Modifica contemporanea da due utenti: l'ultima modifica non cancella l'altra senza avviso | limite | api |
| A29 | Utente senza permessi: non può creare, modificare o eliminare (anche dall'API) | sicurezza | api, e2e |
| A30 | API senza autenticazione: risponde 401 | sicurezza | api |
| A31 | Tentativo di injection (SQL, comandi, script) nei campi di testo: salvato come testo, nessun errore del server | sicurezza | api |
| A32 | Dati personali: non compaiono nei log, nell'URL o in messaggi di errore | sicurezza | api |
| A33 | Anagrafica inesistente aperta dall'URL o dall'API: messaggio di errore / 404 | negativo | api, e2e |
| A34 | Errore del server durante il salvataggio: messaggio comprensibile e dati del form non persi | negativo | e2e |
| A35 | Etichette dei campi leggibili dallo screen reader e form usabile solo da tastiera | accessibilità | unit, e2e |
| A36 | Ogni campo accetta solo il tipo di dato previsto (testo, numero, data, booleano) | negativo | unit |
| A37 | Campi numerici e date: valore appena sotto, uguale e appena sopra i limiti minimo e massimo | limite | unit |
| A38 | Valore null, campo assente o valore vuoto inviato direttamente all'API | negativo | api |
| A39 | Formato della data e date impossibili (es. 31/02) | negativo | unit |
| A40 | Modifica di un solo campo: gli altri dati dell'anagrafica restano invariati | positivo | api |
| A41 | Dopo il salvataggio, ricaricando la pagina, i dati aggiornati sono ancora presenti | positivo | e2e |
| A42 | Dopo l'eliminazione definitiva l'anagrafica non è più leggibile dall'API | positivo | api |
| A43 | ID inesistente o malformato nella richiesta di modifica | negativo | api |
| A44 | Eliminazione ripetuta sulla stessa anagrafica (idempotenza) | limite | api |
| A45 | Filtri combinati su più campi restituiscono solo le anagrafiche corrispondenti | positivo | api |
| A46 | Caratteri speciali nei filtri di ricerca non causano errori o risultati inattesi | limite | api |
| A47 | Paginazione: nessun elemento duplicato o perso tra una pagina e l'altra, a dati invariati | limite | api |
| A48 | Ordinamento con valori vuoti, maiuscole/minuscole e caratteri accentati | limite | api |
| A49 | Creazione ripetuta per timeout o retry: nessun duplicato indesiderato | limite | api |
| A50 | Utente che vede solo alcune anagrafiche non può leggere quelle fuori dal suo ambito (IDOR) | sicurezza | api |
| A51 | Modifica di campi protetti o privilegi con parametri non previsti (mass assignment) | sicurezza | api |
| A52 | HTML o JavaScript salvati nei campi non vengono eseguiti quando la scheda viene mostrata (XSS memorizzato) | sicurezza | e2e |
| A53 | Messaggi di validazione collegati al campo giusto e annunciati quando il focus arriva sull'errore | accessibilità | e2e |
| A54 | Se il salvataggio fallisce, un nuovo tentativo dalla UI non crea record duplicati | negativo | e2e |
| A55 | Errore di validazione dall'API: risposta strutturata, con il campo e il motivo identificabili dal client | negativo | api |


## Esempio di scenario

PUNTO: A18: CAP di 5 cifre e provincia con sigla di 2 lettere
RIGA DEL REQUISITO: Il CAP deve avere 5 cifre e la provincia va indicata con la sigla di 2 lettere.
TIPO: negativo
LIVELLI AMMESSI: unit
Risposta:
{"livello": "unit",
 "titolo": "CAP di 4 cifre non accettato",
 "dato": ["che sto compilando il form Nuovo cliente"],
 "quando": ["scrivo '5010' nel campo CAP"],
 "allora": ["vedo un messaggio di errore sotto il campo CAP"]}


## Esempio di scenario api

PUNTO: A3: Con l'API di creazione l'anagrafica viene salvata e restituita con il suo id
RIGA DEL REQUISITO: Il cliente creato riceve un codice identificativo.
TIPO: positivo
LIVELLI AMMESSI: api
Risposta:
{"livello": "api",
 "titolo": "Creazione via API con id restituito",
 "dato": ["che non esiste un cliente con codice fiscale 'RSSMRA80A01H501U'"],
 "quando": ["invio la richiesta di creazione del cliente 'Mario Rossi' con codice fiscale 'RSSMRA80A01H501U'"],
 "allora": ["la richiesta viene accettata", "la risposta contiene l'id del nuovo cliente"]}
