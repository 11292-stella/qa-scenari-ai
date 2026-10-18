# Checklist – Prodotti: varianti e attributi

Solo se il catalogo ha varianti (taglia, colore, formato, peso, gusto, capacità).

Applica solo i punti che il requisito permette di verificare.
Per i punti di cui il requisito non parla, NON inventare il comportamento: scrivi una domanda aperta.
Ogni scenario ha UN solo livello: se un punto ne indica due, scrivi uno scenario per livello.

Tipi ammessi: positivo, negativo, limite, sicurezza, accessibilità
Livelli ammessi: unit, api, e2e

## 5. Varianti e attributi del prodotto

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| P55 | Creazione di una variante con attributi validi | positivo | api |
| P56 | Visualizzazione delle varianti disponibili nella scheda prodotto | positivo | e2e |
| P57 | Variante senza un attributo obbligatorio | negativo | unit |
| P58 | Valore di un attributo non previsto tra quelli consentiti | negativo | api |
| P59 | Combinazione di attributi duplicata, se non ammessa | negativo | api |
| P60 | Ogni variante mantiene il proprio identificativo univoco, se previsto | positivo | api |
| P61 | Modifica di una variante senza alterare involontariamente le altre | positivo | api |
| P62 | Prezzo diverso tra varianti dello stesso prodotto gestito secondo le regole previste (non presumere che tutte le varianti abbiano lo stesso prezzo) | limite | api |
| P63 | Disponibilità diversa tra varianti dello stesso prodotto gestita correttamente (non presumere che tutte le varianti abbiano lo stesso stock) | positivo | api |
| P64 | Selezione di una variante non disponibile dall'interfaccia | negativo | e2e |
| P65 | Eliminazione di una variante associata a ordini o altri record | limite | api |
| P66 | Variante inesistente richiesta tramite API | negativo | api |

> Esempio: con le varianti S, M e L servono controlli separati per l'esistenza, il prezzo e la disponibilità di ciascuna.

## Esempio di scenario

PUNTO: P62: Prezzo diverso tra varianti dello stesso prodotto gestito secondo le regole previste (non presumere che tutte le varianti abbiano lo stesso prezzo)
RIGA DEL REQUISITO: Ogni formato della bevanda ha il suo prezzo: 33 cl costa 2,50 e 50 cl costa 3,50.
TIPO: limite
LIVELLI AMMESSI: api
Risposta:
{"livello": "api",
 "titolo": "Il formato 50 cl ha il suo prezzo",
 "dato": ["che il prodotto 'Coca Cola' ha le varianti '33 cl' e '50 cl'"],
 "quando": ["invio la richiesta di dettaglio della variante '50 cl'"],
 "allora": ["la richiesta viene accettata", "il prezzo della variante è '3,50'"]}
