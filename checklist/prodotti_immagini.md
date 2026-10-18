# Checklist – Prodotti: immagini e allegati

Solo se il prodotto permette di caricare immagini o documenti.

Applica solo i punti che il requisito permette di verificare.
Per i punti di cui il requisito non parla, NON inventare il comportamento: scrivi una domanda aperta.
Ogni scenario ha UN solo livello: se un punto ne indica due, scrivi uno scenario per livello.

Tipi ammessi: positivo, negativo, limite, sicurezza, accessibilità
Livelli ammessi: unit, api, e2e

## 8. Immagini, allegati e visualizzazione

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| P90 | Caricamento di un'immagine in un formato supportato | positivo | e2e |
| P91 | Upload di un file con formato non consentito | negativo | api |
| P92 | File più grande della dimensione massima consentita | limite | api |
| P93 | File corrotto o non valido gestito correttamente | negativo | api |
| P94 | Immagine caricata visualizzata nella scheda prodotto | positivo | e2e |
| P95 | Prodotto senza immagine: visualizzazione del comportamento previsto | limite | e2e |
| P96 | Sostituzione o rimozione dell'immagine, se supportata | positivo | e2e |
| P97 | Nome del file contenente caratteri speciali gestito correttamente | limite | api |
| P98 | Upload di un file malevolo o con contenuto non coerente con il tipo dichiarato | sicurezza | api |
| P99 | Immagini e testi alternativi utilizzabili con tecnologie assistive, se applicabile | accessibilità | e2e |

## Esempio di scenario

PUNTO: P91: Upload di un file con formato non consentito
RIGA DEL REQUISITO: Come immagine del prodotto si possono caricare solo file JPG o PNG.
TIPO: negativo
LIVELLI AMMESSI: api
Risposta:
{"livello": "api",
 "titolo": "Caricamento di un PDF come immagine rifiutato",
 "dato": ["che esiste il prodotto 'Tiramisù'"],
 "quando": ["invio la richiesta di caricamento del file 'menu.pdf' come immagine del prodotto"],
 "allora": ["la richiesta viene rifiutata"]}
