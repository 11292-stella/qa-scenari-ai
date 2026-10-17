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


# ---------- Passo A (un punto alla volta): il requisito ne parla? ----------

class Decisione(BaseModel):
    """Risposta del passo A. Prima la prova (citazione), poi il verdetto."""
    citazione: str = Field(description="Frase copiata dal requisito, oppure stringa vuota se non ne parla")
    ne_parla: bool


def schema_riga(numero_righe: int) -> type[BaseModel]:
    """Passo A con righe numerate: l'AI sceglie SOLO un numero di riga (0 = nessuna riga ne parla)."""
    Riga = Literal[tuple(range(numero_righe + 1))]  # es. Literal[0, 1, 2, ..., 8]
    return create_model(
        "DecisioneRiga",
        riga=(Riga, Field(description="Numero della riga che parla del punto, 0 se nessuna")),
    )


# ---------- Passo B (un punto alla volta): lo scenario ----------

def schema_scenario(livelli: tuple[str, ...]) -> type[BaseModel]:
    """Lo scenario di UN punto: livello solo tra quelli ammessi per quel punto.

    Niente codice e niente citazione: il codice lo sa già Python,
    e la "citazione" è la riga scelta nel passo A.
    """
    LivelloPunto = Literal[livelli]  # es. Literal["unit", "api"]
    altri_campi = {nome: c for nome, c in campi(ScenarioAI).items() if nome not in ("livello", "citazione")}
    return create_model("ScenarioPunto", livello=(LivelloPunto, ...), **altri_campi)


# ---------- Cosa usa Python dopo i controlli ----------

class Scenario(ScenarioAI):
    """Scenario completo: quello dell'AI + codice + tipo copiato dalla checklist."""
    codice: str
    tipo: Tipo
    citazione: str  # è una riga vera del requisito: niente lunghezza minima (anche "Max 20 caratteri." va bene)


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
