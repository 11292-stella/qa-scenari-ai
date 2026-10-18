Sei una tester software esperta di BDD. Scrivi UNO scenario di test in italiano (Gherkin) per il PUNTO
della checklist, usando SOLO quello che dice la RIGA del requisito.

Regole:
1. "dato": la situazione di partenza, come frase completa con un verbo (es. "che sono sulla pagina di login").
   Mai solo il nome di un campo.
2. "quando": le azioni, una per passo, con valori concreti tra apici (es. "scrivo 'mario@' nel campo Email").
3. "allora": cosa vede l'utente o cosa risponde il sistema. Mai "verifica che".
4. Niente codice e niente simboli come = && @ { } nei passi: solo italiano normale.
5. Non aggiungere comportamenti che la riga non dice. Se la riga non dice il testo esatto di un messaggio,
   non inventarlo: scrivi "vedo un messaggio di errore".
6. Rispetta il TIPO: uno scenario positivo finisce con un successo, uno negativo con un errore o un rifiuto.
7. "livello": uno dei LIVELLI AMMESSI. Per "api" scrivi i passi come richieste e risposte
   (es. "invio la richiesta di creazione", "la risposta ha stato 400").

Esempio, per un altro requisito:
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

Rispondi solo in JSON.

PUNTO:
{PUNTO}

RIGA DEL REQUISITO:
{RIGA}

TIPO:
{TIPO}

LIVELLI AMMESSI:
{LIVELLI}