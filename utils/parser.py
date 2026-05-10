import json
from pathlib import Path


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
