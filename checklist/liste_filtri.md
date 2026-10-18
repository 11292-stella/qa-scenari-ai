# Checklist – Liste e ricerca (modulo trasversale): filtri e ordinamento

Modulo trasversale: non spuntarlo insieme a ordini_liste o prodotti_ricerca.

Applica solo i punti che il requisito permette di verificare.
Per i punti di cui il requisito non parla, NON inventare il comportamento: scrivi una domanda aperta.
Ogni scenario ha UN solo livello: se un punto ne indica due, scrivi uno scenario per livello.

Tipi ammessi: positivo, negativo, limite, sicurezza, accessibilità
Livelli ammessi: unit, api, e2e

## 3. Filtri singoli e combinati

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| LS27 | Applicazione di un filtro valido restituisce solo i record corrispondenti | positivo | api |
| LS28 | Rimozione di un filtro ripristina i risultati previsti | positivo | e2e |
| LS29 | Combinazione di due filtri restituisce record che soddisfano entrambi, se la logica prevista è AND | positivo | api |
| LS30 | Combinazione di filtri con logica OR, se prevista | positivo | api |
| LS31 | Filtro senza risultati: stato vuoto comprensibile | negativo | e2e |
| LS32 | Valore di filtro non ammesso inviato direttamente all'API | negativo | api |
| LS33 | Filtro con valore vuoto o nullo gestito secondo le regole previste | limite | api |
| LS34 | Modifica di un filtro aggiorna correttamente i risultati | positivo | e2e |
| LS35 | Reset dei filtri: vengono rimossi tutti i filtri attivi previsti | positivo | e2e |
| LS36 | Filtri combinati con paginazione: il conteggio e i record restano coerenti | limite | api |
| LS37 | Filtri combinati con ordinamento: entrambi vengono applicati correttamente | positivo | api |
| LS38 | Filtri incompatibili o combinazioni non ammesse gestite correttamente | negativo | api |

## 4. Ordinamento

| # | Cosa controllare | Tipo | Livello |
|---|---|---|---|
| LS39 | Ordinamento crescente per un campo supportato | positivo | api |
| LS40 | Ordinamento decrescente per un campo supportato | positivo | api |
| LS41 | Inversione dell'ordinamento tramite interfaccia | positivo | e2e |
| LS42 | Ordinamento numerico: i numeri non vengono ordinati come semplici stringhe (es. 2, 10, 100 e non 10, 100, 2) | limite | unit |
| LS43 | Ordinamento per data: le date sono ordinate cronologicamente | positivo | unit |
| LS44 | Ordinamento di valori testuali con maiuscole, accenti e caratteri speciali | limite | api |
| LS45 | Record con valori nulli nel campo ordinato | limite | api |
| LS46 | Più record con lo stesso valore di ordinamento: comportamento coerente tra pagine | limite | api |
| LS47 | Richiesta di ordinamento per un campo non supportato | negativo | api |
| LS48 | Ordinamento combinato con filtri e ricerca mantiene tutti i vincoli attivi | positivo | api |

> Un caso particolarmente utile è LS42: se i valori sono 2, 10 e 100, un ordinamento testuale può produrre risultati diversi da quello numerico.

## Esempio di scenario

PUNTO: LS47: Richiesta di ordinamento per un campo non supportato
RIGA DEL REQUISITO: Le fatture si possono ordinare solo per data o per importo.
TIPO: negativo
LIVELLI AMMESSI: api
Risposta:
{"livello": "api",
 "titolo": "Ordinamento per un campo non supportato",
 "dato": ["che esistono fatture nella lista"],
 "quando": ["invio la richiesta della lista delle fatture ordinata per il campo 'colore'"],
 "allora": ["la richiesta viene rifiutata"]}

## Esempio di scenario unit

PUNTO: LS42: Ordinamento numerico: i numeri non vengono ordinati come semplici stringhe (es. 2, 10, 100 e non 10, 100, 2)
RIGA DEL REQUISITO: Le fatture si ordinano per importo come numeri, dal più piccolo al più grande.
TIPO: limite
LIVELLI AMMESSI: unit
Risposta:
{"livello": "unit",
 "titolo": "Importi ordinati come numeri",
 "dato": ["che esistono fatture da '2', '10' e '100' euro"],
 "quando": ["ordino le fatture per importo crescente"],
 "allora": ["l'ordine degli importi è '2', '10', '100'"]}

## Esempio di scenario e2e

PUNTO: LS35: Reset dei filtri: vengono rimossi tutti i filtri attivi previsti
RIGA DEL REQUISITO: Il bottone Azzera filtri toglie tutti i filtri attivi.
TIPO: positivo
LIVELLI AMMESSI: e2e
Risposta:
{"livello": "e2e",
 "titolo": "Azzera filtri",
 "dato": ["che ho aperto la lista delle fatture con il filtro stato 'Pagata'"],
 "quando": ["premo il bottone Azzera filtri"],
 "allora": ["vedo tutte le fatture senza filtri attivi"]}
