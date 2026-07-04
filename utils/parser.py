import json
from pathlib import Path
import pdfplumber
import ollama
import re


REQUIRED_FIELDS = ["imie", "nazwisko", "umiejetnosci"]


def load_candidate_profile(filepath: str) -> dict:
    """
    Wczytuje profil kandydata z pliku JSON.
    Waliduje obecność wymaganych pól.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Nie znaleziono pliku profilu: {filepath}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            profile = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Plik {filepath} nie jest poprawnym JSON-em: {e}")

    # Walidacja wymaganych pól
    missing = [field for field in REQUIRED_FIELDS if field not in profile]
    if missing:
        raise ValueError(f"Brakujące pola w profilu: {', '.join(missing)}")

    # Uzupełnij opcjonalne pola domyślnymi wartościami
    profile.setdefault("lokalizacja", "")
    profile.setdefault("projekty", [])
    profile.setdefault("doswiadczenie", [])

    return profile


def load_job_offer(filepath: str) -> str:
    """
    Wczytuje treść oferty pracy z pliku tekstowego.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Nie znaleziono pliku oferty: {filepath}")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        raise ValueError(f"Plik oferty {filepath} jest pusty.")

    return content


def profile_from_dict(data: dict) -> dict:
    """
    Waliduje i normalizuje profil przekazany jako dict (np. z uploadu w Streamlit).
    """
    missing = [field for field in REQUIRED_FIELDS if field not in data]
    if missing:
        raise ValueError(f"Brakujące pola w profilu: {', '.join(missing)}")

    data.setdefault("lokalizacja", "")
    data.setdefault("projekty", [])
    data.setdefault("doswiadczenie", [])
    return data

def parse_pdf_resume(filepath: str) -> str:
    """
    Extracts text from a PDF resume.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Nie znaleziono pliku: {filepath}")
    
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
                
    if not text.strip():
        raise ValueError(f"Plik PDF {filepath} jest pusty lub nie zawiera tekstu.")
        
    return text.strip()

def extract_profile_from_text(text: str, model: str = "mistral") -> dict:
    """
    Uses Ollama to extract structured JSON profile from raw resume text.
    """
    prompt = f"""
Przeanalizuj poniższe CV kandydata i wyodrębnij informacje do struktury JSON.
Zwróć WYŁĄCZNIE poprawny JSON (bez markdown).
Oczekiwany format:
{{
  "imie": "...",
  "nazwisko": "...",
  "lokalizacja": "...",
  "umiejetnosci": ["umiejetnosc1", "umiejetnosc2"],
  "projekty": ["projekt1", "projekt2"],
  "doswiadczenie": [
    {{
      "firma": "...",
      "stanowisko": "...",
      "okres": "...",
      "zadania": ["zadanie1", "zadanie2"]
    }}
  ]
}}

Treść CV:
{text}
"""
    try:
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": "Odpowiadasz WYŁĄCZNIE w formacie JSON."},
                {"role": "user", "content": prompt}
            ]
        )
        raw = response["message"]["content"]
        raw = re.sub(r"```json|```", "", raw).strip()
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start != -1 and end > start:
            raw = raw[start:end]
        data = json.loads(raw)
        return profile_from_dict(data)
    except Exception as e:
        raise ValueError(f"Nie udało się przetworzyć CV z użyciem AI: {e}")
