"""Passo C – dagli scenari agli SCHELETRI di codice: Playwright (Python), Robot Framework, Appium (Java).

Niente AI: lo scrive Python, quindi è sempre corretto e uguale ogni volta.
  - ogni passo diventa un metodo (o una keyword) del page object, con il nome preso dal testo
  - i passi "Allora" diventano VERIFICHE (verifica_... / Verifica ... / boolean verifica...)
  - i valori tra virgolette diventano PARAMETRI: 'Email non valida' → metodo(valore)
  - il test chiama i metodi nell'ordine dello scenario, con il passo Gherkin come commento
  - i corpi sono TODO che FALLISCONO: uno scheletro che passa senza fare niente sarebbe un falso verde
  - gli scenari @unit non si generano: vanno testati nel progetto frontend
"""
import re
import unicodedata
from dataclasses import dataclass

from generatore.gherkin import pulisci_passo
from generatore.schemas import Scenario

MAX_PAROLE = 10                      # nomi di metodo non infiniti
# Valori tra virgolette: "..." / “...” / ‘...’ / '...'. L'apice singolo vale solo se NON è attaccato
# a una lettera prima (così l'apostrofo di "l'email" non viene preso per una virgoletta)
VIRGOLETTE = r"\"([^\"]+)\"|“([^”]+)”|‘([^’]+)’|(?<!\w)'([^']+)'(?!\w)"


# ---------- Un passo, pronto per diventare codice ----------

@dataclass
class Passo:
    sezione: str            # "Dato", "Quando", "Allora"
    testo: str              # il passo come compare nel Gherkin (senza la parola chiave)
    parole: list[str]       # le parole che formano il nome del metodo
    valori: list[str]       # i valori tra virgolette → parametri

    @property
    def verifica(self) -> bool:
        return self.sezione == "Allora"


def senza_accenti(testo: str) -> str:
    return unicodedata.normalize("NFKD", testo).encode("ascii", "ignore").decode()


def analizza_passo(sezione: str, testo: str) -> Passo:
    testo = pulisci_passo(testo)
    valori = ["".join(gruppi) for gruppi in re.findall(VIRGOLETTE, testo)]
    senza_valori = re.sub(VIRGOLETTE, " ", testo)
    pulito = re.sub(r"[^a-z0-9]+", " ", senza_accenti(senza_valori).lower())
    # via le parole di una lettera ("l'email" → "email"), ma non i numeri ("5 tentativi")
    parole = [p for p in pulito.split() if len(p) > 1 or p.isdigit()][:MAX_PAROLE] or ["passo"]
    if sezione == "Allora" and parole[0] == "verifica":
        parole = parole[1:] or ["passo"]          # niente "verifica_verifica_..."
    return Passo(sezione, testo, parole, valori)


def passi_dello_scenario(scenario: Scenario) -> list[Passo]:
    passi = []
    for sezione, testi in (("Dato", scenario.dato), ("Quando", scenario.quando), ("Allora", scenario.allora)):
        passi += [analizza_passo(sezione, t) for t in testi]
    return passi


def riga_gherkin(passo: Passo, precedente: Passo | None) -> str:
    """'Dato ...' oppure 'E ...' se la sezione è la stessa del passo prima."""
    parola = "E" if precedente and precedente.sezione == passo.sezione else passo.sezione
    return f"{parola} {passo.testo}"


def passi_unici(scenari: list[Scenario]) -> list[Passo]:
    """Tutti i passi di tutti gli scenari, senza doppioni: un metodo per frase."""
    visti, unici = set(), []
    for scenario in scenari:
        for passo in passi_dello_scenario(scenario):
            chiave = (passo.verifica, tuple(passo.parole), len(passo.valori))
            if chiave not in visti:
                visti.add(chiave)
                unici.append(passo)
    return unici


# ---------- Nomi nei tre stili ----------

def snake(parole: list[str]) -> str:
    nome = "_".join(parole)
    return f"passo_{nome}" if nome[0].isdigit() else nome


def camel(parole: list[str]) -> str:
    nome = parole[0] + "".join(p.capitalize() for p in parole[1:])
    return f"passo{nome[0].upper()}{nome[1:]}" if nome[0].isdigit() else nome


def parole_titolo(parole: list[str]) -> str:
    return " ".join(p.capitalize() for p in parole)


def nome_classe(nome: str) -> str:
    """'login' → 'Login', 'carrello_kiosk' → 'CarrelloKiosk'"""
    return "".join(p.capitalize() for p in re.split(r"[^a-zA-Z0-9]+", senza_accenti(nome)) if p) or "App"


def nome_test(titolo: str) -> list[str]:
    return re.sub(r"[^a-z0-9]+", " ", senza_accenti(titolo).lower()).split()[:MAX_PAROLE] or ["scenario"]


def valori_java(valori: list[str]) -> str:
    return ", ".join('"' + v.replace('"', '\\"') + '"' for v in valori)


def valori_python(valori: list[str]) -> str:
    return ", ".join(repr(v) for v in valori)


def parametri(valori: list[str]) -> list[str]:
    return ["valore" if i == 0 else f"valore{i + 1}" for i in range(len(valori))]


# ---------- Playwright + pytest ----------

class Playwright:
    nome = "Playwright"
    linguaggio = "python"

    def __init__(self, area: str):
        self.classe = f"{nome_classe(area)}Page"
        self.file_page = f"pages/{self.classe}.py"
        self.file_test = f"tests/test_{area.lower()}.py"

    def metodo(self, passo: Passo) -> str:
        return ("verifica_" if passo.verifica else "") + snake(passo.parole)

    def definizione(self, passo: Passo) -> str:
        argomenti = "".join(f", {p}" for p in parametri(passo.valori))
        cosa = "expect(...) sul risultato atteso" if passo.verifica else "azioni sulla pagina"
        return (f"    # {passo.sezione} {passo.testo}\n"
                f"    def {self.metodo(passo)}(self{argomenti}):\n"
                f"        raise NotImplementedError(\"TODO: {cosa}\")\n")

    def page_object(self, passi: list[Passo]) -> str:
        metodi = "\n".join(self.definizione(p) for p in passi)
        return (f"from playwright.sync_api import Page, expect\n"
                f"from pages.base_page import BasePage\n\n\n"
                f"class {self.classe}(BasePage):\n"
                f"    def __init__(self, page: Page):\n"
                f"        super().__init__(page)\n"
                f"        # TODO: locator, es.\n"
                f"        # self.btn_accedi = page.get_by_role(\"button\", name=\"Accedi\")\n\n"
                f"{metodi}")

    def test(self, scenario: Scenario) -> str:
        passi = passi_dello_scenario(scenario)
        gherkin = [riga_gherkin(p, passi[i - 1] if i else None) for i, p in enumerate(passi)]
        marker = "".join(f"    @pytest.mark.{t}\n" for t in (scenario.tipo, scenario.livello, scenario.codice))
        docstring = "\n".join(f"        {g}" for g in gherkin)
        variabile = self.classe.removesuffix("Page").lower()
        chiamate = "\n".join(f"        {variabile}.{self.metodo(p)}({valori_python(p.valori)})" for p in passi)
        nota_api = "        # livello api: usa api_context (APIRequestContext) invece della pagina\n" \
            if scenario.livello == "api" else ""
        return (f"{marker}"
                f"    def test_{scenario.codice}_{snake(nome_test(scenario.titolo))}(self, page):\n"
                f"        \"\"\"\n{docstring}\n        \"\"\"\n"
                f"{nota_api}"
                f"        {variabile} = {self.classe}(page)\n"
                f"{chiamate}\n")

    def file_dei_test(self, titolo: str, scenari: list[Scenario], esclusi: list[Scenario]) -> str:
        testa = (f"# {titolo} – generato da QA Scenari AI\n"
                 f"# Marker da registrare in pytest.ini:  markers = positivo negativo limite sicurezza "
                 f"accessibilita api e2e L1 L2 ...\n"
                 f"import pytest\n"
                 f"from pages.{self.classe} import {self.classe}\n\n\n"
                 f"class Test{self.classe.removesuffix('Page')}:\n\n")
        corpo = "\n".join(self.test(s) for s in scenari) or "    pass\n"
        return testa + corpo + nota_esclusi(esclusi, "#")


# ---------- Robot Framework (Browser Library) ----------

class Robot:
    nome = "Robot"
    linguaggio = "robotframework"

    def __init__(self, area: str):
        self.area = area.lower()
        self.file_page = f"resources/{self.area}_page.resource"
        self.file_test = f"tests/{self.area}.robot"

    def keyword(self, passo: Passo) -> str:
        return ("Verifica " if passo.verifica else "") + parole_titolo(passo.parole)

    def definizione(self, passo: Passo) -> str:
        righe = [self.keyword(passo), f"    [Documentation]    {passo.sezione} {passo.testo}"]
        if passo.valori:
            righe.append("    [Arguments]    " + "    ".join(f"${{{p}}}" for p in parametri(passo.valori)))
        cosa = "verifica il risultato atteso" if passo.verifica else "azioni sulla pagina"
        righe.append(f"    Fail    TODO: {cosa}")
        return "\n".join(righe) + "\n"

    def page_object(self, passi: list[Passo]) -> str:
        keyword = "\n".join(self.definizione(p) for p in passi)
        return ("*** Settings ***\n"
                f"Documentation    Keyword e selettori: {self.area} – generato da QA Scenari AI\n"
                "Library          Browser    timeout=20s\n\n\n"
                "*** Variables ***\n"
                "${BASE_URL}       http://localhost:4200\n"
                "${HEADLESS}       False\n"
                "# TODO: selettori, es.\n"
                "# ${BOTTONE_ACCEDI}    button[type=\"submit\"]\n\n\n"
                "*** Keywords ***\n"
                "Apri Browser\n"
                "    New Browser    chromium    headless=${HEADLESS}\n\n"
                f"{keyword}")

    def test(self, scenario: Scenario) -> str:
        passi = passi_dello_scenario(scenario)
        gherkin = [riga_gherkin(p, passi[i - 1] if i else None) for i, p in enumerate(passi)]
        documentazione = f"    [Documentation]    {gherkin[0]}\n" + "".join(f"    ...                {g}\n" for g in gherkin[1:])
        chiamate = "".join(f"    {self.keyword(p)}" + "".join(f"    {v}" for v in p.valori) + "\n" for p in passi)
        nota_api = "    # livello api: usa RequestsLibrary (POST On Session...) invece del browser\n" \
            if scenario.livello == "api" else ""
        return (f"{scenario.codice} {scenario.titolo.strip().rstrip('.')}\n"
                f"{documentazione}"
                f"    [Tags]    {scenario.tipo}    {scenario.livello}    {scenario.codice}\n"
                f"{nota_api}{chiamate}")

    def file_dei_test(self, titolo: str, scenari: list[Scenario], esclusi: list[Scenario]) -> str:
        testa = ("*** Settings ***\n"
                 f"Documentation     {titolo} – generato da QA Scenari AI\n"
                 f"Resource          ../{self.file_page}\n"
                 "Suite Setup       Apri Browser\n"
                 "Suite Teardown    Close Browser\n"
                 "Test Setup        New Context\n"
                 "Test Teardown     Close Context\n\n\n"
                 "*** Test Cases ***\n")
        return testa + "\n".join(self.test(s) for s in scenari) + nota_esclusi(esclusi, "#")


# ---------- Appium + Java (TestNG, senza Cucumber) ----------

class Appium:
    nome = "Appium"
    linguaggio = "java"
    pacchetto = "com.stellamarucelli.app"

    def __init__(self, area: str):
        self.classe = f"{nome_classe(area)}Page"
        self.classe_test = f"{nome_classe(area)}Test"
        self.file_page = f"pages/{self.classe}.java"
        self.file_test = f"tests/{self.classe_test}.java"

    def metodo(self, passo: Passo) -> str:
        nome = camel(passo.parole)
        return f"verifica{nome[0].upper()}{nome[1:]}" if passo.verifica else nome

    def definizione(self, passo: Passo) -> str:
        argomenti = ", ".join(f"String {p}" for p in parametri(passo.valori))
        tipo = "boolean" if passo.verifica else "void"
        cosa = "controlla il risultato atteso" if passo.verifica else "azioni sulla schermata"
        return (f"    // {passo.sezione} {passo.testo}\n"
                f"    public {tipo} {self.metodo(passo)}({argomenti}) {{\n"
                f"        throw new UnsupportedOperationException(\"TODO: {cosa}\");\n"
                f"    }}\n")

    def page_object(self, passi: list[Passo]) -> str:
        azioni = "\n".join(self.definizione(p) for p in passi if not p.verifica)
        verifiche = "\n".join(self.definizione(p) for p in passi if p.verifica)
        return (f"package {self.pacchetto}.pages;\n\n"
                "import io.appium.java_client.AppiumBy;\n"
                "import io.appium.java_client.AppiumDriver;\n"
                "import org.openqa.selenium.By;\n\n"
                f"public class {self.classe} {{\n\n"
                "    private final AppiumDriver driver;\n\n"
                "    // ---- DOVE sono gli elementi ----  TODO, es.\n"
                "    // private final By btnAccedi = AppiumBy.accessibilityId(\"btn_accedi\");\n\n"
                f"    public {self.classe}(AppiumDriver driver) {{\n"
                "        this.driver = driver;\n"
                "    }\n\n"
                "    // ---- COSA FAI ----\n\n"
                f"{azioni}\n"
                "    // ---- COSA VEDI ----\n\n"
                f"{verifiche}"
                "}\n")

    def test(self, scenario: Scenario) -> str:
        passi = passi_dello_scenario(scenario)
        righe = []
        variabile = self.classe.removesuffix("Page")[0].lower() + self.classe.removesuffix("Page")[1:]
        for i, passo in enumerate(passi):
            righe.append(f"        // {riga_gherkin(passo, passi[i - 1] if i else None)}")
            chiamata = f"{variabile}.{self.metodo(passo)}({valori_java(passo.valori)})"
            if passo.verifica:
                messaggio = f"Non verificato: {passo.testo}".replace('"', "'")
                righe.append(f"        assertTrue({chiamata},\n                \"{messaggio}\");")
            else:
                righe.append(f"        {chiamata};")
        nota_api = "        // livello api: usa REST Assured (ApiClient) invece dell'app\n" \
            if scenario.livello == "api" else ""
        descrizione = scenario.titolo.strip().rstrip(".").replace('"', "'")
        return (f"    @Test(groups = {{\"{scenario.tipo}\", \"{scenario.livello}\", \"{scenario.codice}\"}},\n"
                f"          description = \"{descrizione}\")\n"
                f"    public void {scenario.codice}_{camel(nome_test(scenario.titolo))}() {{\n"
                f"{nota_api}" + "\n".join(righe) + "\n    }\n")

    def file_dei_test(self, titolo: str, scenari: list[Scenario], esclusi: list[Scenario]) -> str:
        variabile = self.classe.removesuffix("Page")[0].lower() + self.classe.removesuffix("Page")[1:]
        testa = (f"package {self.pacchetto}.tests;\n\n"
                 f"// {titolo} – generato da QA Scenari AI\n"
                 f"import {self.pacchetto}.pages.{self.classe};\n"
                 f"import {self.pacchetto}.support.DriverManager;\n"
                 "import org.testng.annotations.AfterMethod;\n"
                 "import org.testng.annotations.BeforeMethod;\n"
                 "import org.testng.annotations.Test;\n\n"
                 "import static org.testng.Assert.assertTrue;\n\n"
                 f"public class {self.classe_test} {{\n\n"
                 f"    private {self.classe} {variabile};\n\n"
                 "    @BeforeMethod\n"
                 "    public void setUp() {\n"
                 "        DriverManager.avvia();\n"
                 f"        {variabile} = new {self.classe}(DriverManager.getDriver());\n"
                 "    }\n\n"
                 "    @AfterMethod\n"
                 "    public void tearDown() {\n"
                 "        DriverManager.chiudi();\n"
                 "    }\n\n")
        return testa + "\n".join(self.test(s) for s in scenari) + nota_esclusi(esclusi, "    //") + "}\n"


FRAMEWORK = (Playwright, Robot, Appium)


def nota_esclusi(esclusi: list[Scenario], commento: str) -> str:
    if not esclusi:
        return ""
    righe = [f"\n{commento} Scenari @unit NON generati (vanno testati nel progetto frontend):"]
    righe += [f"{commento}   {s.codice} – {s.titolo}" for s in esclusi]
    return "\n".join(righe) + "\n"


# ---------- Quello che usano la pagina Django e lo zip ----------

def da_generare(scenari: list[Scenario]) -> tuple[list[Scenario], list[Scenario]]:
    """(scenari da trasformare in codice, scenari @unit esclusi)"""
    return [s for s in scenari if s.livello != "unit"], [s for s in scenari if s.livello == "unit"]


def per_scenario(scenario: Scenario, area: str) -> dict[str, str]:
    """Lo scheletro di UN solo scenario, per ogni framework: i metodi che usa + il test."""
    if scenario.livello == "unit":
        nota = "Scenario @unit: non si genera codice E2E, va testato nel progetto frontend (unit test)."
        return {f.nome: nota for f in FRAMEWORK}
    risultato = {}
    for Framework in FRAMEWORK:
        f = Framework(area)
        metodi = "\n".join(f.definizione(p) for p in passi_unici([scenario]))
        commento = "#" if f.linguaggio in ("python", "robotframework") else "//"
        risultato[f.nome] = (f"{commento} ---- {f.file_page} (metodi usati) ----\n{metodi}\n"
                             f"{commento} ---- {f.file_test} ----\n{f.test(scenario)}")
    return risultato


def file_completi(titolo: str, scenari: list[Scenario], area: str) -> dict[str, str]:
    """Tutti i file, pronti per lo zip: {"playwright/pages/LoginPage.py": "...", ...}"""
    generati, esclusi = da_generare(scenari)
    passi = passi_unici(generati)
    file = {}
    for Framework in FRAMEWORK:
        f = Framework(area)
        cartella = f.nome.lower()
        file[f"{cartella}/{f.file_page}"] = f.page_object(passi)
        file[f"{cartella}/{f.file_test}"] = f.file_dei_test(titolo, generati, esclusi)
    return file


# ---------- Prova veloce: python -m generatore.scheletri ----------

if __name__ == "__main__":
    prova = [
        Scenario(codice="L1", tipo="positivo", livello="e2e", citazione="riga 4",
                 titolo="Login e ritorno alla pagina di partenza",
                 dato=["utente con credenziali valide"], quando=["il cliente effettua il login"],
                 allora=["il cliente viene portato alla pagina da cui era partito"]),
        Scenario(codice="L14", tipo="negativo", livello="e2e", citazione="riga 2",
                 titolo="Email non valida", dato=["sono sulla pagina di login"],
                 quando=["inserisco l'email 'mario@'"], allora=["compare il messaggio 'Email non valida'"]),
        Scenario(codice="L6", tipo="limite", livello="unit", citazione="riga 3",
                 titolo="Bottone disabilitato", dato=["campi vuoti"], quando=["guardo il bottone"],
                 allora=["è disabilitato"]),
    ]
    for nome, testo in file_completi("Login del negozio online", prova, "login").items():
        print(f"\n===================== {nome}\n{testo}")