"""Il form della pagina: titolo, requisito, checklist e versioni dei prompt.

Le scelte dei menu a tendina NON sono scritte qui: le legge il servizio
dalle cartelle checklist/ e prompts/. Se aggiungi checklist/crud.md,
compare da sola nel menu.
"""
from django import forms

from generatore.servizio import PROMPT_DECIDI, PROMPT_SCENARIO, checklist_disponibili, prompt_disponibili


def scelte(valori: list[str]) -> list[tuple[str, str]]:
    return [(v, v) for v in valori]


class AnalisiForm(forms.Form):
    titolo = forms.CharField(
        label="Titolo", max_length=120,
        widget=forms.TextInput(attrs={"placeholder": "es. Login del negozio online"}),
    )
    requisito = forms.CharField(
        label="Requisito (una regola per riga)",
        widget=forms.Textarea(attrs={"rows": 10, "placeholder":
            "Il cliente accede con email e password.\n"
            "Con credenziali valide torna alla pagina da cui era partito.\n..."}),
    )
    checklist = forms.MultipleChoiceField(
        label="Checklist (una o più)",
        widget=forms.CheckboxSelectMultiple,
        error_messages={"required": "Scegli almeno una checklist adatta al requisito."},
    )
    prompt_decidi = forms.ChoiceField(label="Prompt passo A (quale riga?)")
    prompt_scenario = forms.ChoiceField(label="Prompt passo B (scenario)")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Nessuna checklist preselezionata: una checklist sbagliata dà un'analisi sbagliata SENZA errori,
        # quindi la scelta deve farla la tester (se resta vuota, il form non è valido)
        # nessuna preselezionata: la sceglie la tester; la PRIMA scelta dà il nome agli scheletri
        self.fields["checklist"].choices = scelte(checklist_disponibili())
        decidi = prompt_disponibili("decidi")
        scenario = prompt_disponibili("scenario")
        self.fields["prompt_decidi"].choices = scelte(decidi)
        self.fields["prompt_scenario"].choices = scelte(scenario)
        # di default la versione MIGLIORE (misurata), non l'ultima: l'ultima può essere un esperimento fallito
        self.fields["prompt_decidi"].initial = PROMPT_DECIDI
        self.fields["prompt_scenario"].initial = PROMPT_SCENARIO

    def clean_requisito(self):
        righe = [r for r in self.cleaned_data["requisito"].splitlines() if r.strip()]
        if len(righe) < 2:
            raise forms.ValidationError("Scrivi almeno 2 righe: una regola per riga.")
        return self.cleaned_data["requisito"]
