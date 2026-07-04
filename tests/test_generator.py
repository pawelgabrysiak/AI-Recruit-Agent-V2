import pytest
from utils.generator import generate_cover_letter_with_ollama, improve_cover_letter

def test_generate_cover_letter(mocker):
    mock_call = mocker.patch("utils.generator.call_llm")
    mock_call.return_value = "Szanowni Państwo, aplikuję na stanowisko."
    
    profile = {"imie": "Jan", "nazwisko": "Kowalski"}
    result = generate_cover_letter_with_ollama(profile, "Szukamy programisty")
    assert "Szanowni Państwo" in result

def test_improve_cover_letter(mocker):
    mock_call = mocker.patch("utils.generator.call_llm")
    mock_call.return_value = "Krótszy list."
    
    result = improve_cover_letter("Długi list.", "Zrób krótszy")
    assert result == "Krótszy list."
