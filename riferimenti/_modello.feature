# Scenari scritti A MANO da me per il requisito con lo stesso nome (requisiti/_modello.txt).
# Servono come "risposta giusta" per misurare quello che scrive l'AI.

Feature: Aggiunta di un prodotto al carrello

  # positivo
  Scenario: Aggiunta di un prodotto disponibile
    Given il cliente è nella pagina del menu
    When tocca "Aggiungi" su "Margherita"
    Then il carrello contiene "Margherita"
    And il totale del carrello è aggiornato

  # negativo
  Scenario: Prodotto esaurito non aggiungibile
    Given il prodotto "Tiramisù" è esaurito
    When il cliente apre la pagina del menu
    Then il pulsante "Aggiungi" di "Tiramisù" è disattivato

  # limite
  Scenario: Aggiunta dello stesso prodotto due volte
    Given il cliente è nella pagina del menu
    When tocca "Aggiungi" su "Margherita" due volte
    Then il carrello contiene 2 "Margherita"
    And il totale corrisponde a 2 volte il prezzo
