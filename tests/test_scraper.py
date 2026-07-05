import pytest
import requests
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from utils.scraper import fetch_job_offer

def test_fetch_job_offer_success(mocker):
    mock_response = mocker.Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.text = """
    <html>
        <head><title>Job Offer</title><style>body {color: red;}</style></head>
        <body>
            <nav>Menu</nav>
            <h1>Software Engineer</h1>
            <p>We are looking for a Python developer.</p>
            <footer>Copyright 2024</footer>
            <script>alert('hello');</script>
        </body>
    </html>
    """
    mocker.patch("requests.get", return_value=mock_response)
    
    result = fetch_job_offer("http://example.com/job")
    
    assert "Software Engineer" in result
    assert "Python developer" in result
    assert "Menu" not in result
    assert "Copyright" not in result
    assert "alert" not in result

def test_fetch_job_offer_http_error(mocker):
    mocker.patch("requests.get", side_effect=requests.exceptions.HTTPError("404 Not Found"))
    
    with pytest.raises(ValueError, match="Błąd połączenia"):
        fetch_job_offer("http://example.com/job")
