"""
Współdzielone komponenty interfejsu użytkownika - wersja ulepszona.
"""
import streamlit as st

def header():
    """
    Wyświetla nagłówek aplikacji z animacją.
    """
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style='text-align: center; animation: fadeIn 1s ease;'>
            AFIRMATOR
            </h1>
        </div>
    """, unsafe_allow_html=True)

def create_tabs():
    """
    Tworzy zakładki aplikacji z ikonkami.
    
    Returns:
        tuple: Obiekty zakładek (tab1, tab2, tab3, tab4, tab5).
    """
    return st.tabs(["🌟 Afirmacja dnia", "🛠️ Generator afirmacji", "🎨 Wizualny cytat", "🎧 Czytanie afirmacji", "🎵 Muzyczna afirmacja"])

def api_key_input():
    """
    Wyświetla pole do wprowadzania klucza API w ładnej karcie.
    
    Returns:
        str: Wprowadzony klucz API lub None.
    """
    st.markdown("""
        <div style="text-align: center; width: 100%;">
            <h8> Aby rozpocząć korzystanie z aplikacji, wprowadź swój klucz API OpenAI.</h8>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        api_key = st.text_input(
            "Klucz API",  # Dodaj etykietę
            type="password",
            key="api_input",
            placeholder="sk-...",
            label_visibility="hidden"  # Ukryj ją, jeśli nie chcesz by była widoczna
        )
        
        # Dodaj informację pomocniczą
        st.caption("Klucz API powinien zaczynać się od 'sk-' i zawierać minimum 40 znaków.")
        st.caption("Możesz uzyskać klucz API na stronie [platform.openai.com](https://platform.openai.com/account/api-keys)")
        
        return api_key

def loading_spinner(message="Trwa przetwarzanie..."):
    """
    Zwraca kontekst dla wskaźnika ładowania z animacją.
    
    Args:
        message (str, optional): Wiadomość do wyświetlenia.
        
    Returns:
        context: Kontekst wskaźnika ładowania.
    """
    return st.spinner(f"✨ {message} ✨")

def success_message(message):
    """
    Wyświetla komunikat sukcesu z ikonką.
    
    Args:
        message (str): Treść komunikatu.
    """
    st.success(f"✅ {message}")

def error_message(message):
    """
    Wyświetla komunikat błędu z ikonką.
    
    Args:
        message (str): Treść komunikatu.
    """
    st.error(f"❌ {message}")

def warning_message(message):
    """
    Wyświetla komunikat ostrzeżenia z ikonką.
    
    Args:
        message (str): Treść komunikatu.
    """
    st.warning(f"⚠️ {message}")

def affirmation_card(text):
    """
    Wyświetla kartę z afirmacją w eleganckim stylu.
    
    Args:
        text (str): Tekst afirmacji.
    """
    st.markdown(
        f"""
        <div class="affirmation-card">
            {text}
        </div>
        """, 
        unsafe_allow_html=True
    )

def button_with_icon(label, icon="", key=None, help=None, type="primary", use_container_width=True):
    """
    Tworzy przycisk z ikonką.
    
    Args:
        label (str): Tekst przycisku
        icon (str): Emoji ikona
        key (str): Klucz przycisku
        help (str): Tekst pomocy
        type (str): Typ przycisku
        use_container_width (bool): Czy rozciągnąć na całą szerokość
        
    Returns:
        bool: Czy przycisk został kliknięty
    """
    return st.button(
        f"{icon} {label}" if icon else label,
        key=key,
        help=help,
        type=type,
        use_container_width=use_container_width
    )

def centered_text(text, size="medium"):
    """
    Wyświetla wycentrowany tekst.
    
    Args:
        text (str): Tekst do wyświetlenia
        size (str): Rozmiar tekstu ("small", "medium", "large")
    """
    size_map = {
        "small": "1rem",
        "medium": "1.2rem",
        "large": "1.5rem"
    }
    font_size = size_map.get(size, "1rem")
    
    st.markdown(f"""
        <div style="text-align: center; font-size: {font_size}; margin: 1rem 0;">
            {text}
        </div>
    """, unsafe_allow_html=True)

def spacer(height="1rem"):
    """
    Dodaje odstęp pionowy.
    
    Args:
        height (str): Wysokość odstępu w CSS
    """
    st.markdown(f"<div style='height: {height};'></div>", unsafe_allow_html=True)