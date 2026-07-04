from utils.llm_client import call_llm


STYLE_PROMPTS = {
    "profesjonalny": "Styl ma być formalny, rzeczowy i profesjonalny. Bez ozdobników.",
    "entuzjastyczny": "Styl ma być energiczny, pełen entuzjazmu, ale nadal profesjonalny.",
    "zwiezly": "List ma być bardzo zwięzły – maksymalnie 3 krótkie akapity. Bez zbędnych słów.",
}


def generate_cover_letter_with_ollama(
    profile: dict,
    offer_text: str,
    model: str = "mistral",
    style: str = "profesjonalny",
    extra_notes: str = "",
    api_keys: dict = None
) -> str:
    """
    Generuje list motywacyjny przy pomocy lokalnego modelu Ollama.

    Parametry:
    - profile: dict z danymi kandydata
    - offer_text: treść ogłoszenia o pracę
    - model: nazwa modelu Ollama (domyślnie 'mistral')
    - style: styl listu ('profesjonalny', 'entuzjastyczny', 'zwiezly')
    - extra_notes: dodatkowe wskazówki od użytkownika

    Zwraca:
    - str: gotowy tekst listu motywacyjnego
    """
    style_instruction = STYLE_PROMPTS.get(style, STYLE_PROMPTS["profesjonalny"])

    doswiadczenie_str = "\n".join([
        f"  - {x['stanowisko']} w {x['firma']} ({x.get('okres', '')}): {', '.join(x.get('zadania', []))}"
        for x in profile.get('doswiadczenie', [])
    ])

    extra = f"\nDodatkowe wskazówki od kandydata: {extra_notes}" if extra_notes.strip() else ""

    prompt = f"""
Napisz profesjonalny list motywacyjny w języku polskim dla kandydata aplikującego na poniższe stanowisko.

### Instrukcje stylistyczne:
{style_instruction}
- Pisz w pierwszej osobie
- List powinien być naturalny i autentyczny – unikaj korporacyjnego żargonu
- Nie zaczynaj od "Szanowni Państwo" – zacznij od mocniejszego, bardziej osobistego otwarcia
- Zakończ uprzejmym zaproszeniem do rozmowy
- Unikaj angielskich sformułowań
- NIE używaj placeholderów w nawiasach kwadratowych jak [firma] – użyj nazwy firmy jeśli jest znana, lub pomiń
{extra}

### Ogłoszenie o pracę:
{offer_text}

### Dane kandydata:
Imię i nazwisko: {profile['imie']} {profile['nazwisko']}
Lokalizacja: {profile.get('lokalizacja', '')}
Umiejętności: {', '.join(profile.get('umiejetnosci', []))}
Projekty: {', '.join(profile.get('projekty', []))}
Doświadczenie:
{doswiadczenie_str}

Wygeneruj TYLKO treść listu motywacyjnego – bez tytułu, bez nagłówka "List motywacyjny", bez komentarzy.
""".strip()

    try:
        messages = [
            {
                "role": "system",
                "content": (
                    "Jesteś doświadczonym doradcą kariery w Polsce. "
                    "Piszesz listy motywacyjne wyłącznie w języku polskim. "
                    "Twoje listy są naturalne, konkretne i skuteczne."
                )
            },
            {"role": "user", "content": prompt}
        ]
        return call_llm(model, messages, expected_format="text", api_keys=api_keys)

    except Exception as e:
        raise RuntimeError(f"Błąd generowania listu przez AI: {e}")


def improve_cover_letter(
    original_letter: str,
    feedback: str,
    model: str = "mistral",
    api_keys: dict = None
) -> str:
    """
    Ulepsza istniejący list motywacyjny na podstawie uwag użytkownika.
    """
    prompt = f"""
Masz poniższy list motywacyjny i uwagi do poprawy. Przepisz list uwzględniając uwagi.

### Oryginalny list:
{original_letter}

### Uwagi do poprawy:
{feedback}

Zwróć TYLKO poprawiony list, bez komentarzy ani wyjaśnień.
""".strip()

    try:
        messages = [
            {
                "role": "system",
                "content": "Jesteś ekspertem od pisania listów motywacyjnych po polsku."
            },
            {"role": "user", "content": prompt}
        ]
        return call_llm(model, messages, expected_format="text", api_keys=api_keys)
    except Exception as e:
        raise RuntimeError(f"Błąd ulepszania listu: {e}")
