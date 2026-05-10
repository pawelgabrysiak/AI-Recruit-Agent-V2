import ollama
import json
import re

# Słownik synonimów jako fallback
ALIASES = {
    "Machine Learning": ["ML", "machine learning", "uczenie maszynowe", "modele predykcyjne"],
    "Scikit-learn": ["sklearn", "scikit-learn", "scikit"],
    "Python": ["python", "py"],
    "SQL": ["sql", "bazy danych", "database"],
    "Pandas": ["pandas", "dataframe"],
    "NumPy": ["numpy", "np"],
    "Git": ["git", "github", "gitlab", "kontrola wersji"],
    "Power BI": ["power bi", "powerbi", "bi"],
    "TensorFlow": ["tensorflow", "tf", "keras"],
    "PyTorch": ["pytorch", "torch"],
}


def analyze_match(profile: dict, offer_text: str) -> dict:
    """
    Prosta analiza regex jako fallback.
    Zwraca dict: umiejętność -> ✅ lub ❌
    """
    results = {}
    offer_lower = offer_text.lower()
    for skill in profile["umiejetnosci"]:
        terms = ALIASES.get(skill, [skill])
        match = any(t.lower() in offer_lower for t in terms)
        results[skill] = "✅" if match else "❌"
    return results


def analyze_match_ai(profile: dict, offer_text: str, model: str = "mistral") -> dict:
    """
    Pełna analiza AI przez Ollama.
    Zwraca słownik z kluczami:
    - 'dopasowanie': dict umiejętność -> status (✅/⚠️/❌)
    - 'ocena_ogolna': int 0-100
    - 'mocne_strony': list[str]
    - 'braki': list[str]
    - 'rekomendacja': str
    - 'brakujace_slowa_kluczowe': list[str]
    """
    prompt = f"""
Jesteś ekspertem HR i rekrutacji w Polsce. Przeanalizuj dopasowanie kandydata do oferty pracy.

### Oferta pracy:
{offer_text}

### Profil kandydata:
Imię i nazwisko: {profile['imie']} {profile['nazwisko']}
Lokalizacja: {profile.get('lokalizacja', 'brak')}
Umiejętności: {', '.join(profile['umiejetnosci'])}
Projekty: {', '.join(profile.get('projekty', []))}
Doświadczenie: {json.dumps(profile.get('doswiadczenie', []), ensure_ascii=False)}

### Twoje zadanie:
Odpowiedz WYŁĄCZNIE w formacie JSON (bez żadnego tekstu przed ani po):

{{
  "dopasowanie": {{
    "NAZWA_UMIEJETNOSCI": {{
      "status": "✅" lub "⚠️" lub "❌",
      "komentarz": "krótkie wyjaśnienie po polsku"
    }}
  }},
  "ocena_ogolna": 85,
  "mocne_strony": ["punkt 1", "punkt 2"],
  "braki": ["brak 1", "brak 2"],
  "rekomendacja": "Krótki paragraf z rekomendacją czy warto aplikować i co wzmocnić.",
  "brakujace_slowa_kluczowe": ["słowo1", "słowo2"]
}}

Dla każdej umiejętności z profilu kandydata oceń:
- ✅ = kandydat ma tę umiejętność i jest ona wymagana w ofercie
- ⚠️ = kandydat ma podobną umiejętność lub oferta wspomina ją jako mile widzianą
- ❌ = kandydat nie ma tej umiejętności lub nie jest ona istotna dla oferty

Odpowiedz TYLKO w JSON, bez markdown, bez komentarzy.
""".strip()

    try:
        response = ollama.chat(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "Jesteś ekspertem HR. Odpowiadasz WYŁĄCZNIE w formacie JSON, bez żadnego tekstu poza JSON-em. Używasz języka polskiego w wartościach."
                },
                {"role": "user", "content": prompt}
            ]
        )
        raw = response["message"]["content"]

        # Wyczyść ewentualne backticki markdown
        raw = re.sub(r"```json|```", "", raw).strip()

        # Znajdź pierwszy { i ostatni }
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start != -1 and end > start:
            raw = raw[start:end]

        data = json.loads(raw)
        return data

    except json.JSONDecodeError:
        # Fallback do prostej analizy
        simple = analyze_match(profile, offer_text)
        return {
            "dopasowanie": {k: {"status": v, "komentarz": ""} for k, v in simple.items()},
            "ocena_ogolna": sum(1 for v in simple.values() if v == "✅") * 100 // max(len(simple), 1),
            "mocne_strony": [],
            "braki": [],
            "rekomendacja": "Nie udało się przeprowadzić pełnej analizy AI.",
            "brakujace_slowa_kluczowe": []
        }
    except Exception as e:
        raise RuntimeError(f"Błąd połączenia z Ollama: {e}")
