# language: it
Funzionalità: Login al gestionale

  # ---------- POSITIVI ----------

  @positivo @e2e @L1
  Scenario: Login con credenziali valide porta alla dashboard
    Dato che sono sulla pagina di login
    Quando eseguo il login con le credenziali dell'utente di test
    Allora vedo la dashboard

  @positivo @api @L2
  Scenario: L'API di login restituisce un token con credenziali valide
    Quando invio a POST /api/auth/login le credenziali dell'utente di test
    Allora la risposta ha stato 200
    E la risposta contiene un token

  @positivo @e2e @L10
  Scenario: Il logout riporta alla pagina di login e chiude la sessione
    Dato che ho eseguito il login
    Quando eseguo il logout
    Allora sono sulla pagina di login
    E se apro la dashboard vengo riportato alla pagina di login

  @positivo @unit @L13
  Scenario: Il campo password nasconde i caratteri
    Dato che sono sulla pagina di login
    Quando scrivo "segreta" nel campo password
    Allora i caratteri del campo password non sono visibili

  # ---------- NEGATIVI ----------

  @negativo @e2e @L3
  Scenario: Login con password errata mostra un messaggio di errore
    Dato che sono sulla pagina di login
    Quando eseguo il login con username "mrossi" e password "password-sbagliata"
    Allora vedo il messaggio di errore
    E resto sulla pagina di login

  @negativo @api @L5
  Scenario: L'API di login rifiuta credenziali errate
    Quando invio a POST /api/auth/login username "mrossi" e password "password-sbagliata"
    Allora la risposta ha stato 401
    E la risposta non contiene un token

  # ---------- LIMITE ----------

  @limite @unit @L6
  Schema dello scenario: Il bottone Accedi è disabilitato con campi vuoti o solo spazi
    Dato che sono sulla pagina di login
    Quando scrivo username "<username>" e password "<password>"
    Allora il bottone Accedi è disabilitato

    Esempi:
      | username | password |
      |          |          |
      | mrossi   |          |
      |          | segreta  |
      | "   "    | segreta  |
      | mrossi   | "   "    |

  # ---------- SICUREZZA ----------

  @sicurezza @e2e @L4
  Scenario: Utente inesistente e password errata danno lo stesso messaggio
    Dato che sono sulla pagina di login
    Quando eseguo il login con username "utente-inesistente" e password "qualsiasi"
    Allora vedo lo stesso messaggio di errore della password errata
    E resto sulla pagina di login

  @sicurezza @e2e @L9
  Schema dello scenario: Le pagine protette non si aprono senza login
    Dato che non ho eseguito il login
    Quando apro la pagina "<pagina>"
    Allora vengo riportato alla pagina di login

    Esempi:
      | pagina    |
      | dashboard |
      | prodotti  |
      | categorie |
      | ordini    |