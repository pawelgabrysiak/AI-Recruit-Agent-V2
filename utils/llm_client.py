import os
import re
import json
from dotenv import load_dotenv
from utils.logger import setup_logger

logger = setup_logger("llm_client")
load_dotenv()

def call_llm(model_id: str, messages: list[dict], expected_format: str = "text", api_keys: dict = None) -> str:
    """
    Uniwersalny klient do wywoływania modeli (Ollama, Groq, Gemini).
    model_id format: "provider/model_name" np. "groq/llama3-8b-8192", "gemini/gemini-2.5-flash".
    Dla lokalnych modeli wystarczy "mistral" (domyślnie ollama).
    """
    api_keys = api_keys or {}
    
    if "/" in model_id:
        provider, model_name = model_id.split("/", 1)
    else:
        provider = "ollama"
        model_name = model_id
        
    logger.info(f"Wysyłam zapytanie do {provider} (model: {model_name})")

    if provider == "ollama":
        return _call_ollama(model_name, messages, expected_format)
    elif provider == "groq":
        key = api_keys.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
        if not key:
            raise ValueError("Brak klucza GROQ_API_KEY.")
        return _call_openai_compatible(model_name, messages, key, "https://api.groq.com/openai/v1", expected_format)
    elif provider == "gemini":
        key = api_keys.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
        if not key:
            raise ValueError("Brak klucza GEMINI_API_KEY.")
        return _call_gemini(model_name, messages, key, expected_format)
    elif provider == "deepseek":
        key = api_keys.get("DEEPSEEK_API_KEY") or os.environ.get("DEEPSEEK_API_KEY")
        if not key:
            raise ValueError("Brak klucza DEEPSEEK_API_KEY.")
        return _call_openai_compatible(model_name, messages, key, "https://api.deepseek.com", expected_format)
    else:
        raise ValueError(f"Nieznany dostawca LLM: {provider}")


def _call_ollama(model: str, messages: list[dict], expected_format: str) -> str:
    import ollama
    try:
        response = ollama.chat(model=model, messages=messages)
        return response["message"]["content"]
    except Exception as e:
        raise RuntimeError(f"Ollama error: {e}")

def _call_openai_compatible(model: str, messages: list[dict], api_key: str, base_url: str, expected_format: str) -> str:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url=base_url)
        
        kwargs = {
            "model": model,
            "messages": messages,
            "temperature": 0.3
        }
        
        # Groq obsluguje response_format={"type": "json_object"}
        if expected_format == "json":
            # Należy upewnić się, że słowo JSON jest w prompcie, ale robimy to wyżej w logice
            kwargs["response_format"] = {"type": "json_object"}
            
        response = client.chat.completions.create(**kwargs)
        return response.choices[0].message.content
    except ImportError:
        raise ImportError("Zainstaluj pakiet openai (pip install openai)")
    except Exception as e:
        raise RuntimeError(f"OpenAI API error: {e}")

def _call_gemini(model: str, messages: list[dict], api_key: str, expected_format: str) -> str:
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        generation_config = genai.types.GenerationConfig(
            temperature=0.3,
            response_mime_type="application/json" if expected_format == "json" else "text/plain"
        )
        
        # Konwersja ról OpenAI na role Gemini
        formatted_messages = []
        system_instruction = None
        
        for msg in messages:
            if msg["role"] == "system":
                system_instruction = msg["content"]
            else:
                formatted_messages.append({
                    "role": "user" if msg["role"] == "user" else "model",
                    "parts": [msg["content"]]
                })
                
        gemini_model = genai.GenerativeModel(
            model_name=model,
            system_instruction=system_instruction
        )
        
        response = gemini_model.generate_content(
            formatted_messages,
            generation_config=generation_config
        )
        return response.text
    except ImportError:
        raise ImportError("Zainstaluj pakiet google-generativeai")
    except Exception as e:
        raise RuntimeError(f"Gemini API error: {e}")
