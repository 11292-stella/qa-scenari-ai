# Checklist – Ordini: magazzino e disponibilità

Solo per gestionali in cui gli ordini sono collegati a uno stock.

Applica solo i punti che il requisito permette di verificare.
Per i punti di cui il requisito non parla, NON inventare il comportamento: scrivi una domanda aperta.
Ogni scenario ha UN solo livello: se un punto ne indica due, scrivi uno scenario per livello.

Tipi ammessi: positivo, negativo, limite, sicurezza, accessibilità
Livelli ammessi: unit, api, e2e

## 6. Magazzino e disponibilità

> Questa categoria si applica solo ai gestionali in cui gli ordini sono collegati a uno stock o a una disponibilità di prodotti.

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| O63 | Creazione dell'ordine con disponibilità sufficiente | positivo | api |
| O64 | Quantità ordinata superiore alla disponibilità, quando non ammessa | negativo | api |
| O65 | Quantità disponibile esattamente uguale a quella richiesta | limite | api |
| O66 | Due ordini simultanei non superano la disponibilità residua prevista | limite | api |
| O67 | La disponibilità viene aggiornata nella fase prevista dal requisito (creazione, conferma, spedizione o altra) | positivo | api |
| O68 | Annullamento dell'ordine: eventuale ripristino della disponibilità secondo le regole definite | positivo | api |
| O69 | Prodotto esaurito o non disponibile mostrato correttamente all'utente | negativo | e2e |
| O70 | Errore durante l'aggiornamento dello stock: ordine e disponibilità non restano incoerenti | negativo | api |

> Per O67 e O68 il requisito deve specificare quando si modifica lo stock: alla creazione, alla conferma, alla spedizione oppure in un'altra fase.

## Esempio di scenario

PUNTO: O65: Quantità disponibile esattamente uguale a quella richiesta
RIGA DEL REQUISITO: Non si può ordinare una quantità maggiore di quella disponibile in magazzino.
TIPO: limite
LIVELLI AMMESSI: api
Risposta:
{"livello": "api",
 "titolo": "Ordine con quantità uguale alla disponibilità",
 "dato": ["che il prodotto ha una disponibilità di '3' pezzi"],
 "quando": ["invio la richiesta di aggiunta di una riga con quantità '3'"],
 "allora": ["la richiesta viene accettata", "la disponibilità del prodotto diventa '0'"]}
