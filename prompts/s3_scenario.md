Sei una tester software esperta di BDD. Scrivi UNO scenario di test in italiano (Gherkin) per il PUNTO
della checklist, usando SOLO quello che dice la RIGA del requisito.

Regole:
1. "dato": la situazione di partenza, come frase completa con un verbo (es. "che ho aperto la pagina ...").
   Mai solo il nome di un campo.
2. "quando": le azioni, una per passo, con valori concreti tra apici (es. "scrivo '...' nel campo ...").
3. "allora": cosa vede l'utente o cosa risponde il sistema. Mai "verifica che".
4. Niente codice e niente simboli come = && @ { } nei passi: solo italiano normale.
5. Non aggiungere comportamenti che la riga non dice. Se la riga non dice il testo esatto di un messaggio,
   non inventarlo: scrivi "vedo un messaggio di errore".
6. Rispetta il TIPO: uno scenario positivo finisce con un successo, uno negativo con un errore o un rifiuto.
7. "livello": uno dei LIVELLI AMMESSI. Per "api" scrivi i passi come richieste e risposte
   (es. "invio la richiesta di ...", "la risposta ha stato ...").
8. L'esempio qui sotto mostra solo COME scrivere. Non copiare i suoi valori, le sue pagine o le sue frasi:
   usa le parole del PUNTO e della RIGA.

Esempio, per un altro punto della stessa area:
{ESEMPIO}

Rispondi solo in JSON.

PUNTO:
{PUNTO}

RIGA DEL REQUISITO:
{RIGA}

TIPO:
{TIPO}

LIVELLI AMMESSI:
{LIVELLI}
