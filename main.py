from utils.parser import load_candidate_profile, load_job_offer
from utils.analyzer import analyze_match_ai, analyze_match
from utils.generator import generate_cover_letter_with_ollama
import os
import json
import sys

### Wersja skryptowa (CLI)
# Uruchamianie: python main.py
# Opcjonalnie z modelem: python main.py llama3

MODEL = sys.argv[1] if len(sys.argv) > 1 else "mistral"

print(f"🤖 AI RekrutAgent – wersja CLI (model: {MODEL})\n")

# Wczytanie danych
try:
    profile = load_candidate_profile("data/profil_kandydata.json")
    offer = load_job_offer("data/oferta1.txt")
except (FileNotFoundError, ValueError) as e:
    print(f"❌ Błąd wczytywania danych: {e}")
    sys.exit(1)

print(f"✅ Wczytano profil: {profile['imie']} {profile['nazwisko']}")
print(f"✅ Wczytano ogłoszenie ({len(offer)} znaków)\n")

# Analiza AI
print("🧠 Uruchamiam analizę AI...")
try:
    analysis = analyze_match_ai(profile, offer, model=MODEL)
    use_ai = True
except Exception as e:
    print(f"⚠️ Analiza AI niedostępna ({e}), używam trybu podstawowego.")
    simple = analyze_match(profile, offer)
    analysis = {
        "dopasowanie": {k: {"status": v, "komentarz": ""} for k, v in simple.items()},
        "ocena_ogolna": sum(1 for v in simple.values() if v == "✅") * 100 // max(len(simple), 1),
        "mocne_strony": [],
        "braki": [],
        "rekomendacja": "",
        "brakujace_slowa_kluczowe": []
    }
    use_ai = False

# Upewnij się, że folder output istnieje
os.makedirs("output", exist_ok=True)

# Zapisz wynik analizy
with open("output/analiza_dopasowania.txt", "w", encoding="utf-8") as f:
    f.write(f"📊 Analiza dopasowania (model: {MODEL if use_ai else 'regex fallback'})\n")
    f.write(f"Wynik ogólny: {analysis['ocena_ogolna']}%\n\n")
    f.write("Umiejętności:\n")
    for skill, data in analysis["dopasowanie"].items():
        if isinstance(data, dict):
            status = data["status"]
            comment = data.get("komentarz", "")
            f.write(f"  {status} {skill}: {comment}\n")
        else:
            f.write(f"  {data} {skill}\n")
    if analysis.get("mocne_strony"):
        f.write("\nMocne strony:\n")
        for m in analysis["mocne_strony"]:
            f.write(f"  ✅ {m}\n")
    if analysis.get("braki"):
        f.write("\nBraki:\n")
        for b in analysis["braki"]:
            f.write(f"  ❌ {b}\n")
    if analysis.get("rekomendacja"):
        f.write(f"\nRekomendacja:\n{analysis['rekomendacja']}\n")

print(f"✅ Analiza zakończona – wynik: {analysis['ocena_ogolna']}%")
print("   Zapisano w output/analiza_dopasowania.txt\n")

# Wygeneruj list motywacyjny
print("✍️ Generuję list motywacyjny...")
try:
    cover_letter = generate_cover_letter_with_ollama(profile, offer, model=MODEL)
    with open("output/list_motywacyjny.txt", "w", encoding="utf-8") as f:
        f.write(cover_letter)
    print("📄 List zapisany w output/list_motywacyjny.txt")
except Exception as e:
    print(f"❌ Błąd generowania listu: {e}")
    print("   Upewnij się że Ollama jest uruchomiona: ollama serve")
