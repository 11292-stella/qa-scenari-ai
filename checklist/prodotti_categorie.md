# Checklist – Prodotti: categorie e organizzazione del catalogo

Applica solo i punti che il requisito permette di verificare.
Per i punti di cui il requisito non parla, NON inventare il comportamento: scrivi una domanda aperta.
Ogni scenario ha UN solo livello: se un punto ne indica due, scrivi uno scenario per livello.

Tipi ammessi: positivo, negativo, limite, sicurezza, accessibilità
Livelli ammessi: unit, api, e2e

## 4. Categorie e organizzazione del catalogo

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| P43 | Creazione di una categoria valida | positivo | e2e |
| P44 | Creazione della categoria tramite API | positivo | api |
| P45 | Assegnazione di un prodotto a una categoria esistente | positivo | api |
| P46 | Categoria inesistente indicata nella richiesta di assegnazione | negativo | api |
| P47 | Modifica del nome della categoria | positivo | e2e |
| P48 | Filtraggio del catalogo per categoria | positivo | e2e |
| P49 | Filtro per categoria tramite API | positivo | api |
| P50 | Categoria senza prodotti: visualizzazione dello stato vuoto | negativo | e2e |
| P51 | Eliminazione di una categoria associata a prodotti | limite | api |
| P52 | Assegnazione di un prodotto a più categorie, se supportata | limite | api |
| P53 | Categoria duplicata, se il nome deve essere univoco nel relativo ambito | negativo | api |
| P54 | Modifica o eliminazione di una categoria da parte di un utente senza permessi | sicurezza | api |

> Domande aperte tipiche: un prodotto può stare in più categorie? Una categoria con prodotti si può eliminare? Esistono categorie padre e figlie?

## Esempio di scenario

PUNTO: P46: Categoria inesistente indicata nella richiesta di assegnazione
RIGA DEL REQUISITO: Un prodotto può essere assegnato solo a una categoria già esistente.
TIPO: negativo
LIVELLI AMMESSI: api
Risposta:
{"livello": "api",
 "titolo": "Assegnazione a una categoria inesistente rifiutata",
 "dato": ["che la categoria 'Dolci' non esiste"],
 "quando": ["invio la richiesta di assegnazione del prodotto alla categoria 'Dolci'"],
 "allora": ["la richiesta viene rifiutata"]}
