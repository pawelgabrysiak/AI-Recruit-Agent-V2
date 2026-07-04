import pytest
from utils.analyzer import analyze_match, analyze_match_ai

def test_analyze_match_regex():
    profile = {"umiejetnosci": ["Python", "Java", "Docker"]}
    offer = "Poszukujemy programisty ze znajomością Python i chmur, czasem docker."
    result = analyze_match(profile, offer)
    assert result["Python"] == "✅"
    assert result["Docker"] == "✅"
    assert result["Java"] == "❌"

def test_analyze_match_ai_success(mocker):
    mock_call = mocker.patch("utils.analyzer.call_llm")
    mock_call.return_value = """{
                "dopasowanie": {"Python": {"status": "✅", "komentarz": "ok"}},
                "ocena_ogolna": 90,
                "mocne_strony": [],
                "braki": [],
                "rekomendacja": "test",
                "brakujace_slowa_kluczowe": []
            }"""
    
    profile = {"imie": "Jan", "nazwisko": "Kowalski", "umiejetnosci": ["Python"], "doswiadczenie": [], "projekty": [], "lokalizacja": ""}
    result = analyze_match_ai(profile, "oferta z pythonem")
    assert result["ocena_ogolna"] == 90
    assert result["dopasowanie"]["Python"]["status"] == "✅"
