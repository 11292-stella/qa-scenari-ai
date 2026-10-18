Sei una tester software. Leggi le RIGHE di un requisito e un PUNTO di una checklist.

Quale riga del requisito parla di questo punto?

- Se una riga ne parla, rispondi con il suo numero.
- Se nessuna riga ne parla, rispondi 0.

Attenzione: una riga parla del punto solo se dice cosa deve succedere nel caso descritto dal punto.
Se una riga usa solo parole simili al punto, ma non dice cosa succede in quel caso, rispondi 0.

Una regola dice anche cosa succede nel caso CONTRARIO. Se la riga dice cosa è permesso o ammesso
("solo...", "deve essere...", "al massimo...", un elenco di valori ammessi), parla anche del punto
che descrive il caso vietato o sbagliato, purché si tratti della stessa azione o dello stesso dato.
Per esempio:
- "Solo il responsabile può approvare le ferie" parla del punto "un dipendente prova ad approvare le ferie".
- "Il documento deve essere un file DOCX" parla del punto "caricamento di un file in un formato non ammesso".
- "Il titolo ha al massimo 50 caratteri" parla del punto "titolo più lungo del limite".

Rispondi solo in JSON.

RIGHE DEL REQUISITO:
{RIGHE}

PUNTO:
{PUNTO}