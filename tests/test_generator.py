import pytest
from utils.generator import generate_cover_letter_with_ollama, improve_cover_letter

def test_generate_cover_letter(mocker):
    mock_chat = mocker.patch("utils.generator.ollama.chat")
    mock_chat.return_value = {
        "message": {
            "content": "Szanowni Państwo, aplikuję na stanowisko."
        }
    }
    
    profile = {"imie": "Jan", "nazwisko": "Kowalski"}
    result = generate_cover_letter_with_ollama(profile, "Szukamy programisty")
    assert "Szanowni Państwo" in result

def test_improve_cover_letter(mocker):
    mock_chat = mocker.patch("utils.generator.ollama.chat")
    mock_chat.return_value = {
        "message": {
            "content": "Krótszy list."
        }
    }
    
    result = improve_cover_letter("Długi list.", "Zrób krótszy")
    assert result == "Krótszy list."
