# Checklist – Pagamenti: contanti

Domande aperte tipiche: il pagamento in contanti può essere parziale? Il resto è calcolato dalla cassa? Sono ammessi pagamenti misti (contanti + carta)?

Applica solo i punti che il requisito permette di verificare.
Per i punti di cui il requisito non parla, NON inventare il comportamento: scrivi una domanda aperta.
Ogni scenario ha UN solo livello: se un punto ne indica due, scrivi uno scenario per livello.

Tipi ammessi: positivo, negativo, limite, sicurezza, accessibilità
Livelli ammessi: unit, api, e2e

## 2. Pagamento in contanti

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| PAY13 | Registrazione di un pagamento in contanti per l'importo esatto | positivo | e2e |
| PAY14 | Registrazione tramite API di un pagamento in contanti valido | positivo | api |
| PAY15 | Calcolo corretto del resto quando il contante ricevuto supera il totale | positivo | unit |
| PAY16 | Contante ricevuto inferiore al totale: comportamento previsto dal sistema | negativo | unit |
| PAY17 | Contante ricevuto pari a zero o negativo, se non ammesso | limite | api |
| PAY18 | Importo ricevuto con decimali e arrotondamenti gestiti correttamente | limite | unit |
| PAY19 | Registrazione del pagamento: il metodo risulta effettivamente contanti | positivo | api |
| PAY20 | Doppia conferma del pagamento in contanti: nessuna registrazione duplicata indesiderata | limite | api |

> Domande aperte: il pagamento in contanti può essere parziale? Il resto viene calcolato automaticamente? Sono ammessi pagamenti misti, per esempio una parte in contanti e una parte con carta?

## Esempio di scenario

PUNTO: PAY15: Calcolo corretto del resto quando il contante ricevuto supera il totale
RIGA DEL REQUISITO: Se il contante ricevuto supera il totale, la cassa calcola il resto.
TIPO: positivo
LIVELLI AMMESSI: unit
Risposta:
{"livello": "unit",
 "titolo": "Resto calcolato sul contante ricevuto",
 "dato": ["che il totale da pagare è '18,50'"],
 "quando": ["registro un contante ricevuto di '20,00'"],
 "allora": ["il resto da dare è '1,50'"]}

## Esempio di scenario api

PUNTO: PAY17: Contante ricevuto pari a zero o negativo, se non ammesso
RIGA DEL REQUISITO: Il contante ricevuto deve essere maggiore di zero.
TIPO: limite
LIVELLI AMMESSI: api
Risposta:
{"livello": "api",
 "titolo": "Contante ricevuto zero rifiutato",
 "dato": ["che il totale da pagare è '18,50'"],
 "quando": ["invio la richiesta di pagamento in contanti con contante ricevuto '0,00'"],
 "allora": ["la richiesta viene rifiutata"]}

## Esempio di scenario e2e

PUNTO: PAY13: Registrazione di un pagamento in contanti per l'importo esatto
RIGA DEL REQUISITO: Il cameriere registra il pagamento in contanti dalla cassa.
TIPO: positivo
LIVELLI AMMESSI: e2e
Risposta:
{"livello": "e2e",
 "titolo": "Pagamento in contanti dell'importo esatto",
 "dato": ["che ho aperto alla cassa l'ordine del tavolo '4' da '18,50'"],
 "quando": ["scelgo il metodo Contanti", "scrivo '18,50' nel campo Contante ricevuto", "premo il bottone Conferma"],
 "allora": ["vedo un messaggio di conferma", "l'ordine del tavolo '4' risulta pagato"]}
