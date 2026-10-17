"""Forma esatta dei dati: cosa può rispondere l'AI e cosa usa poi Python.

- l'AI sceglie il CODICE solo tra quelli della checklist (lista chiusa)
- l'AI deve CITARE la frase del requisito che giustifica ogni scenario
- il TIPO non lo sceglie l'AI: lo copia Python dalla checklist
"""
from typing import Literal, get_args

from pydantic import BaseModel, Field, create_model

# Liste chiuse: valori ammessi (scritti qui una volta sola)
Tipo = Literal["positivo", "negativo", "limite", "sicurezza", "accessibilità"]
Livello = Literal["unit", "api", "e2e"]

# Gli stessi valori come tuple, utili per i controlli in Python
TIPI = get_args(Tipo)        # ("positivo", "negativo", ...)
LIVELLI = get_args(Livello)  # ("unit", "api", "e2e")


# ---------- Cosa scrive l'AI ----------

class ScenarioAI(BaseModel):
    """Uno scenario come lo scrive l'AI (senza codice: lo aggiunge schema_risposta)."""
    livello: Livello
    citazione: str = Field(min_length=10, description="Frase copiata parola per parola dal requisito")
    titolo: str = Field(min_length=5, description="Titolo breve dello scenario, in italiano")
    dato: list[str] = Field(min_length=1, description="Passi 'Dato', senza la parola Dato")
    quando: list[str] = Field(min_length=1, description="Passi 'Quando', senza la parola Quando")
    allora: list[str] = Field(min_length=1, description="Passi 'Allora', senza la parola Allora")


class DomandaAI(BaseModel):
    """Una domanda aperta su un punto di cui il requisito non parla."""
    domanda: str = Field(min_length=10, description="Domanda per chi ha scritto il requisito")


def campi(modello: type[BaseModel]) -> dict:
    """I campi di un modello nel formato che vuole create_model: {nome: (tipo, regole)}."""
    return {nome: (campo.annotation, campo) for nome, campo in modello.model_fields.items()}


def schema_risposta(codici: list[str]) -> type[BaseModel]:
    """Crea al volo lo schema della risposta: 'codice' può essere SOLO uno dei codici della checklist."""
    Codice = Literal[tuple(codici)]  # es. Literal["L1", "L2", ..., "L32"]

    # 'codice' va messo PRIMA degli altri campi: il modello scrive il JSON in ordine,
    # quindi deve prima decidere di quale punto parla e poi scrivere il resto.
    Scenario = create_model("Scenario", codice=(Codice, ...), **campi(ScenarioAI))
    Domanda = create_model("Domanda", codice=(Codice, ...), **campi(DomandaAI))

    return create_model(
        "Risposta",
        scenari=(list[Scenario], ...),
        domande=(list[Domanda], ...),
    )


# ---------- Cosa usa Python dopo i controlli ----------

class Scenario(ScenarioAI):
    """Scenario completo: quello dell'AI + codice + tipo copiato dalla checklist."""
    codice: str
    tipo: Tipo


# ---------- Prova veloce: python -m generatore.schemas ----------

if __name__ == "__main__":
    from pydantic import ValidationError

    Risposta = schema_risposta(["L1", "L2", "L3"])

    buona = """{
      "scenari": [{
        "codice": "L1", "livello": "e2e",
        "citazione": "Con credenziali valide l'utente arriva alla dashboard.",
        "titolo": "Login valido porta alla dashboard",
        "dato": ["sono sulla pagina di login"],
        "quando": ["eseguo il login con credenziali valide"],
        "allora": ["vedo la dashboard"]
      }],
      "domande": [{"codice": "L3", "domanda": "Cosa succede dopo 5 tentativi errati?"}]
    }"""
    print("✅ Risposta buona:", Risposta.model_validate_json(buona).scenari[0].titolo)

    cattiva = """{
      "scenari": [{
        "codice": "L99", "livello": "integration",
        "citazione": "boh",
        "titolo": "Login",
        "dato": [], "quando": ["login"], "allora": ["ok"]
      }],
      "domande": []
    }"""
    try:
        Risposta.model_validate_json(cattiva)
    except ValidationError as errore:
        print(f"❌ Risposta cattiva: {errore.error_count()} errori trovati")
        for e in errore.errors():
            print("  -", ".".join(str(p) for p in e["loc"]), "→", e["msg"])