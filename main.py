from utils.parser import load_candidate_profile, load_job_offer
from utils.analyzer import analyze_match_ai, analyze_match
from utils.generator import generate_cover_letter_with_ollama
from utils.logger import setup_logger
from utils.config import config
from utils.exceptions import AgentError
import os
import json
import sys
from pathlib import Path

logger = setup_logger("main")

### Wersja skryptowa (CLI)
# Uruchamianie: python main.py
# Opcjonalnie z modelem: python main.py llama3

MODEL = sys.argv[1] if len(sys.argv) > 1 else config.get("models", {}).get("default", "mistral")

logger.info(f"🤖 AI RekrutAgent – wersja CLI (model: {MODEL})")

# Wczytanie danych
try:
    data_dir = config.get("paths", {}).get("data_dir", "data")
    profile = load_candidate_profile(f"{data_dir}/profil_kandydata.json")
    offer = load_job_offer(f"{data_dir}/oferta1.txt")
except (FileNotFoundError, ValueError, AgentError) as e:
    logger.error(f"Błąd wczytywania danych: {e}")
    sys.exit(1)

logger.info(f"Wczytano profil: {profile['imie']} {profile['nazwisko']}")
logger.info(f"Wczytano ogłoszenie ({len(offer)} znaków)")

# Analiza AI
logger.info("Uruchamiam analizę AI...")
try:
    analysis = analyze_match_ai(profile, offer, model=MODEL)
    use_ai = True
except Exception as e:
    logger.warning(f"Analiza AI niedostępna ({e}), używam trybu podstawowego.")
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
out_dir = config.get("paths", {}).get("output_dir", "output")
os.makedirs(out_dir, exist_ok=True)

# Zapisz wynik analizy
out_analysis_path = Path(out_dir) / "analiza_dopasowania.txt"
with open(out_analysis_path, "w", encoding="utf-8") as f:
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

logger.info(f"Analiza zakończona – wynik: {analysis['ocena_ogolna']}%")
logger.info(f"Zapisano w {out_analysis_path}")

# Wygeneruj list motywacyjny
logger.info("Generuję list motywacyjny...")
try:
    cover_letter = generate_cover_letter_with_ollama(profile, offer, model=MODEL)
    out_letter_path = Path(out_dir) / "list_motywacyjny.txt"
    with open(out_letter_path, "w", encoding="utf-8") as f:
        f.write(cover_letter)
    logger.info(f"List zapisany w {out_letter_path}")
except Exception as e:
    logger.error(f"Błąd generowania listu: {e}. Upewnij się że Ollama jest uruchomiona: ollama serve")
