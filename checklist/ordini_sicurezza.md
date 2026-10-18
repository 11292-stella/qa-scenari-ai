# Checklist – Ordini: errori, sicurezza e accessibilità

Autenticazione, autorizzazione, injection, dati sensibili, errori di rete, accessibilità.

Applica solo i punti che il requisito permette di verificare.
Per i punti di cui il requisito non parla, NON inventare il comportamento: scrivi una domanda aperta.
Ogni scenario ha UN solo livello: se un punto ne indica due, scrivi uno scenario per livello.

Tipi ammessi: positivo, negativo, limite, sicurezza, accessibilità
Livelli ammessi: unit, api, e2e

## 8. Errori, sicurezza e accessibilità

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| O81 | API degli ordini invocata senza autenticazione | sicurezza | api |
| O82 | Utente senza permessi tenta di creare, modificare o annullare un ordine | sicurezza | api |
| O83 | Un utente non può accedere a ordini appartenenti a un altro ambito organizzativo, se previsto | sicurezza | api |
| O84 | Input contenenti tentativi di SQL injection non alterano la query o i dati | sicurezza | api |
| O85 | Contenuti HTML o JavaScript inseriti nei campi non vengono eseguiti quando visualizzati | sicurezza | e2e |
| O86 | I dati sensibili dell'ordine non vengono esposti in URL o messaggi di errore impropri | sicurezza | api |
| O87 | Errori di rete o timeout durante il caricamento degli ordini gestiti con un feedback comprensibile | negativo | e2e |
| O88 | Errore temporaneo durante il salvataggio: l'utente può riprovare senza creare duplicati indesiderati | negativo | e2e |
| O89 | Form e azioni principali sono utilizzabili da tastiera | accessibilità | e2e |
| O90 | Etichette, campi obbligatori, errori e stato dell'ordine sono esposti correttamente alle tecnologie assistive | accessibilità | e2e |
| O91 | Pulsanti e azioni hanno nomi accessibili e stati comprensibili | accessibilità | unit |

> Per la sicurezza, ricorda che autenticazione e autorizzazione sono controlli distinti: essere autenticati non significa essere autorizzati a operare su qualsiasi ordine.

## Esempio di scenario

PUNTO: O81: API degli ordini invocata senza autenticazione
RIGA DEL REQUISITO: Solo gli utenti autenticati possono vedere gli ordini.
TIPO: sicurezza
LIVELLI AMMESSI: api
Risposta:
{"livello": "api",
 "titolo": "Lista ordini senza autenticazione rifiutata",
 "dato": ["che non ho eseguito il login"],
 "quando": ["invio la richiesta della lista degli ordini senza token"],
 "allora": ["la richiesta viene rifiutata", "non ricevo nessun ordine"]}
