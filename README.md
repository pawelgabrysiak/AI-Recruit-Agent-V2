# 🤖 AI RekrutAgent

Inteligentny asystent do szukania pracy. Analizuje Twój profil kandydata, ocenia dopasowanie do oferty pracy i generuje spersonalizowany list motywacyjny — wszystko lokalnie, bez chmury, przy użyciu Ollama.

## ✨ Funkcje

- **Analiza AI** — model językowy analizuje całą ofertę i ocenia każdą umiejętność z komentarzem
- **Ocena procentowa** dopasowania kandydata do stanowiska
- **Mocne strony i braki** — AI wskazuje co wzmocnić w CV
- **Słowa kluczowe** — lista terminów do dodania do CV
- **List motywacyjny** w 3 stylach: profesjonalny, entuzjastyczny, zwięzły
- **Ulepszanie listu** — AI poprawia list na podstawie Twoich uwag
- **Dwa tryby** — aplikacja webowa (Streamlit) i CLI

## 🚀 Instalacja

### 1. Zainstaluj Ollama
Pobierz z [ollama.com](https://ollama.com) i zainstaluj.

### 2. Pobierz model
```bash
ollama pull mistral
# lub lepszy do języka polskiego:
ollama pull llama3
```

### 3. Sklonuj projekt i zainstaluj zależności
```bash
pip install -r requirements.txt
```

## ▶️ Uruchomienie

### Aplikacja webowa (Streamlit)
```bash
# Upewnij się, że Ollama działa:
ollama serve

# W osobnym terminalu:
streamlit run app.py
```

### Wersja CLI
```bash
python main.py
# lub z innym modelem:
python main.py llama3
```

## 📁 Struktura projektu

```
AI-RekrutAgent/
├── app.py                  ← Aplikacja Streamlit (wielostronicowa)
├── main.py                 ← Wersja CLI
├── requirements.txt
├── README.md
├── data/
│   ├── profil_kandydata.json   ← Przykładowy profil
│   └── oferta1.txt             ← Przykładowa oferta
├── utils/
│   ├── analyzer.py         ← Analiza AI + fallback regex
│   ├── generator.py        ← Generowanie i ulepszanie listu
│   └── parser.py           ← Wczytywanie i walidacja danych
└── output/                 ← Wyniki CLI (tworzone automatycznie)
```

## 👤 Format profilu JSON

```json
{
  "imie": "Jan",
  "nazwisko": "Kowalski",
  "lokalizacja": "Warszawa",
  "umiejetnosci": ["Python", "SQL", "Machine Learning", "Git"],
  "projekty": ["System rekomendacyjny", "Analiza danych sprzedażowych"],
  "doswiadczenie": [
    {
      "firma": "Acme Corp",
      "stanowisko": "Junior Data Scientist",
      "okres": "2023-2024",
      "zadania": ["Budowa modeli predykcyjnych", "Analiza danych w Python"]
    }
  ]
}
```

## 🧠 Obsługiwane modele Ollama

| Model | Polecenie | Jakość PL |
|---|---|---|
| mistral | `ollama pull mistral` | ★★★★☆ |
| llama3 | `ollama pull llama3` | ★★★★★ |
| llama3.2 | `ollama pull llama3.2` | ★★★★★ |
| gemma2 | `ollama pull gemma2` | ★★★★☆ |
| phi3 | `ollama pull phi3` | ★★★☆☆ |

## 📦 Wymagania

```
ollama
streamlit
```
