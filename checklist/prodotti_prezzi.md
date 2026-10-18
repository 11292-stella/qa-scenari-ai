# Checklist – Prodotti: prezzi, sconti e listini

Prezzi e sconti del singolo prodotto. Gli sconti sul totale dell'ordine sono in ordini_importi.

Applica solo i punti che il requisito permette di verificare.
Per i punti di cui il requisito non parla, NON inventare il comportamento: scrivi una domanda aperta.
Ogni scenario ha UN solo livello: se un punto ne indica due, scrivi uno scenario per livello.

Tipi ammessi: positivo, negativo, limite, sicurezza, accessibilità
Livelli ammessi: unit, api, e2e

## 3. Prezzi, sconti e listini

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| P31 | Il prezzo mostrato nel dettaglio corrisponde al prezzo salvato | positivo | e2e |
| P32 | L'API restituisce il prezzo numerico corretto | positivo | api |
| P33 | Modifica del prezzo: il nuovo valore viene salvato correttamente | positivo | api |
| P34 | Il prezzo viene visualizzato con il formato monetario previsto | positivo | unit |
| P35 | Arrotondamento dei prezzi con più cifre decimali | limite | unit |
| P36 | Applicazione di uno sconto percentuale valido sul prezzo del prodotto, se previsto | positivo | unit |
| P37 | Sconto sul prezzo del prodotto superiore al limite consentito | limite | api |
| P38 | Prezzo del prodotto negativo dopo lo sconto, se non ammesso | negativo | api |
| P39 | Prezzo promozionale maggiore del prezzo originale, se vietato | negativo | api |
| P40 | Data di inizio e fine di una promozione validate secondo le regole definite | limite | unit |
| P41 | Il prezzo usato quando il prodotto entra in un ordine è quello del listino previsto per quel prodotto (non un prezzo inviato dal client) | positivo | api |
| P42 | Un utente non autorizzato non può modificare il prezzo tramite API | sicurezza | api |

> Se esistono più listini (per cliente, valuta, periodo o canale) servono test in più: non sono obbligatori nel catalogo base.

## Esempio di scenario

PUNTO: P37: Sconto sul prezzo del prodotto superiore al limite consentito
RIGA DEL REQUISITO: Lo sconto sul prezzo di un prodotto può essere al massimo del 50%.
TIPO: limite
LIVELLI AMMESSI: api
Risposta:
{"livello": "api",
 "titolo": "Sconto del 51% sul prodotto rifiutato",
 "dato": ["che il prodotto ha il prezzo di '20,00'"],
 "quando": ["invio la richiesta di sconto del '51%' sul prodotto"],
 "allora": ["la richiesta viene rifiutata", "il prezzo del prodotto resta '20,00'"]}
