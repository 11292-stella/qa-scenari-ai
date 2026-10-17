"""Una sola pagina: GET mostra il form, POST lancia l'analisi e mostra i risultati."""
import base64

import httpx
from django.shortcuts import render

from generatore.servizio import analizza

from .forms import AnalisiForm


def home(request):
    if request.method != "POST":
        return render(request, "analisi/home.html", {"form": AnalisiForm()})

    form = AnalisiForm(request.POST)
    if not form.is_valid():
        return render(request, "analisi/home.html", {"form": form})

    dati = form.cleaned_data
    try:
        risultato = analizza(
            titolo=dati["titolo"],
            requisito=dati["requisito"],
            checklist=dati["checklist"],
            prompt_decidi=dati["prompt_decidi"],
            prompt_scenario=dati["prompt_scenario"],
        )
    except (httpx.ConnectError, ConnectionError):
        form.add_error(None, "Non riesco a parlare con Ollama: è acceso? (prova 'ollama list' nel terminale)")
        return render(request, "analisi/home.html", {"form": form})
    except Exception as errore:  # qualsiasi altro problema lo mostro nella pagina, non come pagina gialla
        form.add_error(None, f"Errore durante l'analisi: {errore}")
        return render(request, "analisi/home.html", {"form": form})

    return render(request, "analisi/risultato.html", {
        "form": form,
        "analisi": risultato,
        "numero_coperti": sum(d.coperto for d in risultato.decisioni),
        "schede": risultato.schede(),
        "framework": ["Gherkin", "Playwright", "Robot", "Appium"],
        # lo zip va dentro il link stesso (data:...;base64), come il .feature: niente vista in più
        "zip_base64": base64.b64encode(risultato.zip_scheletri()).decode(),
        "nome_file": f"{dati['titolo'].strip().lower().replace(' ', '_') or 'scenari'}",
    })
