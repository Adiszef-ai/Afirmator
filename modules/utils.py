"""
Funkcje pomocnicze używane w różnych modułach aplikacji - wersja ulepszona.
"""
import streamlit as st
import base64
from config.constants import DEFAULT_SESSION_STATE
from ui.components import warning_message, api_key_input

def init_session_state():
    """
    Inicjalizuje stan sesji z domyślnymi wartościami.
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
    if affirmation and affirmation not in st.session_state.history:
        # Dodajemy nową afirmację na początek listy
        st.session_state.history.insert(0, affirmation)
        # Utrzymujemy maksymalnie 50 afirmacji w historii
        if len(st.session_state.history) > 50:
            st.session_state.history.pop()

def check_api_key():
    """
    Sprawdza czy klucz API jest dostępny i ma prawidłowy format.
    
    Returns:
        bool: True jeśli klucz API jest dostępny i prawidłowy, False w przeciwnym razie.
    """
    api_key = st.session_state.api_key
    
    if not api_key:
        return False
    
    # Sprawdzanie wzorca OpenAI API key (zazwyczaj zaczyna się od "sk-" i zawiera 51 znaków)
    if not api_key.startswith("sk-") or len(api_key) < 40:
        st.warning("Wprowadzony klucz API ma nieprawidłowy format. Klucz OpenAI powinien zaczynać się od 'sk-'.")
        st.session_state.api_key = None
        return False
        
    return True