# 🤖 AI-Recruit-Agent V2

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-recruit-agent.streamlit.app/)

Inteligentny asystent rekrutacyjny wspomagający szukanie pracy. Analizuje Twoje CV (w formacie PDF lub wgramy ręcznie), ocenia dopasowanie do wybranej oferty pracy i generuje spersonalizowany, świetnie dopasowany list motywacyjny. 
Narzędzie obsługuje zarówno potężne, darmowe modele chmurowe (Groq, Google Gemini, DeepSeek), jak i w pełni prywatne, lokalne modele sztucznej inteligencji (Ollama).

🌐 **Przetestuj na żywo:** [https://ai-recruit-agent.streamlit.app/](https://ai-recruit-agent.streamlit.app/)

## ✨ Co nowego w V2?

- **Wgrywanie PDF:** Koniec z ręcznym wpisywaniem danych! Wgraj swoje CV w formacie `.pdf`, a Agent AI sam wyciągnie z niego odpowiednie informacje i ułoży je w ustrukturyzowany profil dla analizatora.
- **Wsparcie dla darmowych API w Chmurze:** Aplikacja obsługuje teraz błyskawiczne API chmurowe. Nie musisz posiadać mocnej karty graficznej! Dostępne integracje (do których możesz wpisać darmowy klucz):
  - **Groq** (ultraszybkie modele np. Llama 3.1 i 3.3)
  - **Google Gemini** (Gemini 2.5 Flash / Pro)
  - **DeepSeek** (DeepSeek-Chat, DeepSeek-Coder)
- **Zaawansowana konfiguracja (`config.yaml`) & Logowanie:** Ustrukturyzowana konfiguracja modeli, profesjonalny system zapisywania zdarzeń (logi w pliku `output/app.log`) oraz centralne zarządzanie kluczami API przez plik `.env`.
- **Wsparcie dla Dockera:** Gotowy plik `Dockerfile` umożliwia uruchomienie aplikacji i wdrożenie jej na własny serwer (VPS) zaledwie jedną komendą.
- **Architektura Testowa:** Dodano kompleksowe testy jednostkowe oparte na `pytest` (>70% pokrycia logiki biznesowej), zapewniając stabilność działania.

## 🚀 Jak zacząć? (Lokalnie)

### Opcja 1: Klasyczne środowisko Python

1. **Sklonuj projekt i zainstaluj zależności:**
```bash
git clone https://github.com/pawelgabrysiak/AI-Recruit-Agent-V2.git
cd AI-Recruit-Agent-V2
pip install -r requirements.txt
```

2. **Skonfiguruj klucze API (Opcjonalnie):**
Skopiuj plik `.env.example` i zmień jego nazwę na `.env`. Wklej tam swoje darmowe klucze API od [Groq](https://console.groq.com/keys), [Gemini](https://aistudio.google.com/app/apikey) lub [DeepSeek](https://platform.deepseek.com/). *(Uwaga: Możesz też podać je po prostu z poziomu interfejsu aplikacji webowej w przeglądarce).*

3. **Uruchom aplikację webową (Streamlit):**
```bash
streamlit run app.py
```

### Opcja 2: Konteneryzacja (Docker)
Jeśli preferujesz Dockera, wdrożenie jest niesamowicie szybkie:
```bash
docker build -t ai-recruit-agent .
docker run -d -p 8501:8501 ai-recruit-agent
```
Z aplikacją połączysz się w przeglądarce pod adresem: `http://localhost:8501`.

## ⚙️ Tryb offline i prywatność (Ollama)
Jeśli aplikujesz do organizacji rządowych lub preferujesz zachowanie 100% prywatności swoich danych, aplikacja może działać całkowicie lokalnie (offline).
1. Zainstaluj system [Ollama](https://ollama.com).
2. Pobierz odpowiedni model: `ollama pull mistral` lub `ollama pull llama3.2`.
3. Odpal w tle serwer: `ollama serve`.
4. Wybierz odpowiedni model Ollama z rozwijanej listy w interfejsie aplikacji.

## 📁 Struktura projektu
```
AI-Recruit-Agent V2/
├── app.py                  ← Aplikacja Streamlit (Interfejs graficzny)
├── main.py                 ← Wersja terminalowa (CLI)
├── config.yaml             ← Konfiguracja dostępnych modeli i dostawców
├── Dockerfile              ← Instrukcja budowania kontenera Docker
├── requirements.txt        ← Lista bibliotek (pdfplumber, streamlit, openai, google-generativeai, itp.)
├── .env.example            ← Szablon pliku na klucze API
├── utils/
│   ├── analyzer.py         ← Analizator oceniający dopasowanie (AI + RegEx)
│   ├── generator.py        ← Generowanie i ulepszanie listów motywacyjnych
│   ├── parser.py           ← Czytanie PDF i strukturyzowanie profilu kandydata
│   ├── llm_client.py       ← Zunifikowany mostek AI (Ollama, Groq, Gemini, DeepSeek)
│   └── logger.py           ← System logowania zdarzeń
├── tests/                  ← Testy jednostkowe z mockowaniem (pytest)
└── data/                   ← Folder z przykładowymi danymi i ofertami
```
