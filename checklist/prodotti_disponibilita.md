# Checklist – Prodotti: disponibilità e stock

Solo se il catalogo gestisce quantità o stock. Come lo stock cambia con gli ordini è in ordini_magazzino.

Applica solo i punti che il requisito permette di verificare.
Per i punti di cui il requisito non parla, NON inventare il comportamento: scrivi una domanda aperta.
Ogni scenario ha UN solo livello: se un punto ne indica due, scrivi uno scenario per livello.

Tipi ammessi: positivo, negativo, limite, sicurezza, accessibilità
Livelli ammessi: unit, api, e2e

## 6. Disponibilità e magazzino

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| P67 | Creazione di un prodotto con quantità iniziale valida | positivo | api |
| P68 | Quantità disponibile negativa, se non ammessa | negativo | api |
| P69 | Quantità pari a zero: il prodotto viene rappresentato secondo le regole previste | limite | e2e |
| P70 | Quantità superiore al massimo consentito, se definito | limite | api |
| P71 | Modifica manuale della quantità disponibile dal gestionale e verifica del valore salvato | positivo | api |
| P73 | Prodotto disattivato o non vendibile non può essere ordinato, se previsto | negativo | api |
| P74 | Due modifiche manuali simultanee della disponibilità dello stesso prodotto non generano quantità incoerenti | limite | api |
| P75 | Errore durante la modifica manuale dello stock: nessun aggiornamento parziale incoerente | negativo | api |
| P76 | La disponibilità mostrata nel catalogo corrisponde al dato restituito dal servizio (disponibile, prenotata e fisica possono essere quantità diverse: usa quella indicata dal requisito) | positivo | e2e |

> Quantità disponibile, prenotata e fisicamente presente possono essere concetti diversi: se il requisito non dice quale usa, è una domanda aperta.

## Esempio di scenario

PUNTO: P68: Quantità disponibile negativa, se non ammessa
RIGA DEL REQUISITO: La quantità disponibile di un prodotto non può essere negativa.
TIPO: negativo
LIVELLI AMMESSI: api
Risposta:
{"livello": "api",
 "titolo": "Disponibilità negativa rifiutata",
 "dato": ["che il prodotto 'Coca Cola' ha una disponibilità di '5' pezzi"],
 "quando": ["invio la richiesta di modifica della disponibilità a '-1'"],
 "allora": ["la richiesta viene rifiutata", "la disponibilità del prodotto resta '5'"]}
