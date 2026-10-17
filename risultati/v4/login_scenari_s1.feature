# language: it
Funzionalità: Login al gestionale

  @positivo @e2e @L1
  Scenario: Login e accesso alla dashboard
    Dato utente con credenziali valide
    Quando l'utente effettua il login con le credenziali valide
    Allora l'utente viene portato alla dashboard

  @positivo @api @L2
  Scenario: Password nascondita
    Dato utente inserisce password nella API
    Quando aPI riceve password dall'utente
    Allora aPI nasconde i caratteri della password

  @negativo @e2e @L3
  Scenario: Login con password errata
    Dato username o password errati
    Quando l'utente inserisce username e password errati
    Allora si visualizza lo stesso messaggio di errore e l'utente rimane sulla pagina di login

  @sicurezza @e2e @L4
  Scenario: Utente inesistente: STESSO messaggio della password errata
    Dato utente esistente con credenziali valide
    Quando utente tenta di accedere alla dashboard con credenziali valide
    Allora si riceve un messaggio di errore con il testo 'Password errata'

  @limite @unit @L6
  Scenario: Bottone Accedi disabilitato
    Dato username ' ' e Password ' '
    Quando utente compila Username con solo spazi e Password con solo spazi
    Allora bottone Accedi è disabilitato

  @sicurezza @e2e @L9
  Scenario: Pagina di login aperta senza login
    Dato dashboard, Prodotti, Categorie, Ordini
    Quando utente tenta di accedere a una pagina del gestionale senza essere loggato
    Allora utente viene riportato alla pagina di login

  @positivo @e2e @L10
  Scenario: Logout e Indietro
    Dato utente
    E pagina gestionale
    Quando utente fa logout
    E utente fa click indietro
    Allora utente torna alla pagina di login
    E non può più accedere alle pagine del gestionale

  @negativo @api @L11
  Scenario: Login con credenziali non valide
    Dato utente inizia login con credenziali non valide
    Quando utente invia login POST /api/auth/login
    Allora aPI restituisce errore 401 senza token

  @positivo @unit @L13
  Scenario: Login utente ristorante
    Dato utente accede al gestionale dalla pagina di login
    Quando inserisce username e password
    Allora la password è nascosta

  @negativo @unit @L14
  Scenario: Login con username o email non valido
    Dato utente accede al gestionale dalla pagina di login
    Quando inserisce username o email non validi
    Allora la pagina di login non accetta l'input e mostra un messaggio di errore

  @sicurezza @api @L22
  Scenario: Password non visibile
    Dato utente inserisce una password
    Quando l'utente inserisce una password
    Allora l'accesso viene negato

  @limite @api @L26
  Scenario: Password con caratteri speciali
    Dato password con caratteri speciali
    Quando utente inserisce una password con caratteri speciali
    Allora la password viene mostrata in modo non cifrato

  @sicurezza @api @L29
  Scenario: Password non visibile nei log
    Dato utente inserisce una password nel campo di input
    Quando sistema nasconde i caratteri della password
    Allora la password non appare in chiaro nei log

  # ---------- DOMANDE APERTE ----------
  # L5: Con credenziali errate l'API risponde con errore e senza token
  # L7: Maiuscole/minuscole in username e password
  # L8: Lunghezza massima dei campi
  # L12: Blocco o attesa dopo troppi tentativi errati
  # L15: Spazi prima o dopo username/email
  # L16: Invio del form premendo Invio dalla tastiera
  # L17: Doppio clic sul pulsante di login: nessuna richiesta o azione duplicata
  # L18: Durante l'invio il pulsante si disabilita o compare un caricamento, se previsto
  # L19: Errore di rete o server non raggiungibile: messaggio comprensibile
  # L20: Risposta lenta del server: l'attesa è gestita correttamente
  # L21: Errore del server (es. HTTP 500): messaggio gestito correttamente
  # L23: Utente autenticato ma senza i permessi necessari
  # L24: Ricaricando la pagina dopo il login si resta autenticati
  # L25: Apertura di una pagina protetta in una seconda scheda
  # L27: Accesso con account disabilitato, sospeso o non verificato
  # L28: Tentativo di injection nei campi di login
  # L30: Login con una sessione già attiva
  # L31: Sessione dopo chiusura e riapertura del browser
  # L32: Messaggi di errore accessibili da tastiera e screen reader
