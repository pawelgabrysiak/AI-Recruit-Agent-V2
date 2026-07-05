import requests
from bs4 import BeautifulSoup
from utils.logger import setup_logger

logger = setup_logger("scraper")

def fetch_job_offer(url: str) -> str:
    """
    Fetches the HTML content of a given URL and extracts readable text.
    Uses a standard browser User-Agent to bypass basic scraping protections.
    """
    logger.info(f"Fetching job offer from: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Remove script and style elements
        for script in soup(["script", "style", "noscript", "header", "footer", "nav"]):
            script.decompose()
            
        # Get text and clean it up
        text = soup.get_text(separator="\n", strip=True)
        
        # Remove consecutive blank lines
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        cleaned_text = "\n".join(lines)
        
        logger.info(f"Successfully extracted {len(cleaned_text)} characters from {url}")
        return cleaned_text
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching URL {url}: {e}")
        raise ValueError(f"Nie udało się pobrać ogłoszenia. Błąd połączenia: {e}")
    except Exception as e:
        logger.error(f"Error parsing HTML from {url}: {e}")
        raise ValueError(f"Nie udało się przetworzyć strony: {e}")
