"""
app/modules/utils.py - Funkcje pomocnicze używane w różnych modułach aplikacji - wersja ulepszona.
"""
import streamlit as st
import base64
import os
import re
from config.constants import DEFAULT_SESSION_STATE
from config.translations import t
from ui.components import warning_message, api_key_input

def init_session_state():
    """
    Inicjalizuje stan sesji z domyślnymi wartościami.
    DEPRECATED: Użyj utils.session_state.StateManager.init_state()
    """
    for key, value in DEFAULT_SESSION_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = value

def get_text_download_link(text, filename="afirmacja.txt"):
    """
    Tworzy link do pobrania tekstu jako plik.

    Args:
        text (str): Tekst do pobrania.
        filename (str, optional): Nazwa pliku. Domyślnie "afirmacja.txt".

    Returns:
        str: HTML z linkiem do pobrania.
    """
    b64 = base64.b64encode(text.encode()).decode()
    return f"""
        <a href="data:file/txt;base64,{b64}"
           download="{filename}"
           class="download-button"
           style="text-decoration: none;">
            💾 Pobierz TXT
        </a>
    """

def save_to_history(affirmation):
    """
    Zapisuje afirmację do historii, jeśli jeszcze nie istnieje.

    Args:
        affirmation (str): Afirmacja do zapisania.
    """
    if not affirmation:
        return

    # Sprawdź zarówno stary jak i nowy klucz dla zgodności wstecznej
    try:
        from utils.session_state import StateManager
        history = StateManager.get('generator.history', [])

        if affirmation not in history:
            # Dodajemy nową afirmację na początek listy
            history.insert(0, affirmation)
            # Utrzymujemy maksymalnie 50 afirmacji w historii
            if len(history) > 50:
                history.pop()
            StateManager.set('generator.history', history)
    except ImportError:
        # Fallback do starego sposobu
        if affirmation and affirmation not in st.session_state.history:
            st.session_state.history.insert(0, affirmation)
            if len(st.session_state.history) > 50:
                st.session_state.history.pop()

def get_api_key(provider="openai"):
    """
    Pobiera klucz API z różnych źródeł z fallback.
    Kolejność: st.secrets -> environment variables -> user input

    Args:
        provider (str): Nazwa providera ("openai" lub "groq")

    Returns:
        str or None: Klucz API lub None jeśli nie znaleziono
    """
    # 1. Próba pobrania z st.secrets
    try:
        if hasattr(st, 'secrets') and provider in st.secrets:
            api_key = st.secrets[provider].get("api_key")
            if api_key and api_key != f"your-{provider}-api-key-here":
                return api_key
    except Exception:
        pass

    # 2. Próba pobrania ze zmiennych środowiskowych
    env_key_map = {
        "openai": "OPENAI_API_KEY",
        "groq": "GROQ_API_KEY"
    }

    if provider in env_key_map:
        env_key = os.getenv(env_key_map[provider])
        if env_key:
            return env_key

    # 3. Fallback do session_state (user input)
    # Sprawdź nowy namespace-based klucz najpierw
    try:
        from utils.session_state import StateManager
        api_key = StateManager.get('app.api_key')
        if api_key:
            return api_key
    except ImportError:
        pass

    # Fallback do starego klucza dla zgodności wstecznej
    if hasattr(st.session_state, 'api_key') and st.session_state.api_key:
        return st.session_state.api_key

    return None

def validate_api_key(api_key, provider="openai"):
    """
    Waliduje format klucza API.

    Args:
        api_key (str): Klucz API do walidacji
        provider (str): Provider ("openai" lub "groq")

    Returns:
        bool: True jeśli klucz jest prawidłowy
    """
    if not api_key:
        return False

    # Wzorce dla różnych providerów
    patterns = {
        "openai": r"^sk-[a-zA-Z0-9_-]{40,200}$",  # Współczesne klucze OpenAI mogą być bardzo długie
        "groq": r"^gsk_[a-zA-Z0-9]{40,}$"  # Także Groq może mieć różne długości
    }

    if provider in patterns:
        return bool(re.match(patterns[provider], api_key))

    # Fallback dla nieznanych providerów
    return len(api_key) >= 20

def check_api_key(provider="openai"):
    """
    Sprawdza czy klucz API jest dostępny i ma prawidłowy format.

    Args:
        provider (str): Provider ("openai" lub "groq")

    Returns:
        str or None: Klucz API jeśli jest prawidłowy, None w przeciwnym razie.
    """
    api_key = get_api_key(provider)

    if not api_key:
        return None

    if not validate_api_key(api_key, provider):
        if provider == "openai":
            st.warning(t("validation.invalid_openai_key"))
        elif provider == "groq":
            st.warning(t("validation.invalid_groq_key"))
        return None

    return api_key
