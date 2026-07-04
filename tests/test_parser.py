import pytest
from utils.parser import load_candidate_profile, load_job_offer, profile_from_dict
import json
import tempfile
from pathlib import Path

def test_load_candidate_profile_success():
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", suffix=".json") as f:
        json.dump({"imie": "Jan", "nazwisko": "Kowalski", "umiejetnosci": ["Python"]}, f)
        path = f.name
    try:
        profile = load_candidate_profile(path)
        assert profile["imie"] == "Jan"
        assert profile["lokalizacja"] == ""
    finally:
        Path(path).unlink()

def test_load_candidate_profile_missing_fields():
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", suffix=".json") as f:
        json.dump({"imie": "Jan"}, f)
        path = f.name
    try:
        with pytest.raises(ValueError) as exc:
            load_candidate_profile(path)
        assert "Brakujące pola" in str(exc.value)
    finally:
        Path(path).unlink()

def test_profile_from_dict():
    profile = profile_from_dict({"imie": "Anna", "nazwisko": "Nowak", "umiejetnosci": []})
    assert profile["projekty"] == []
