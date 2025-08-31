"""
app/ui/components.py - Współdzielone komponenty interfejsu użytkownika - wersja ulepszona.
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
    Wyświetla pole do wprowadzania klucza API z przyciskiem Submit.
    
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
        with st.form("api_key_form"):
            api_key = st.text_input(
                "Klucz API",
                type="password",
                placeholder="sk-...",
                label_visibility="hidden"
            )
            
            # Dodaj informację pomocniczą
            st.caption("Klucz API powinien zaczynać się od 'sk-' i zawierać minimum 40 znaków.")
            st.caption("Możesz uzyskać klucz API na stronie [platform.openai.com](https://platform.openai.com/account/api-keys)")
            
            submit_button = st.form_submit_button("Zatwierdź klucz", use_container_width=True, type="primary")
            
            if submit_button and api_key:
                return api_key
            
        return None

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

def progress_bar_context(steps, current_step=0):
    """
    Tworzy context manager z progress barem dla wieloetapowych operacji.
    
    Args:
        steps (list): Lista nazw kroków
        current_step (int): Aktualny krok (0-indexed)
        
    Returns:
        tuple: (progress_bar, status_text) - obiekty do aktualizacji
    """
    progress_container = st.empty()
    status_container = st.empty()
    
    progress_bar = progress_container.progress(0)
    status_text = status_container.empty()
    
    return progress_bar, status_text

def update_progress(progress_bar, status_text, step, total_steps, message):
    """
    Aktualizuje progress bar i status tekst.
    
    Args:
        progress_bar: Obiekt progress bara
        status_text: Obiekt status tekstu
        step (int): Aktualny krok (1-indexed)
        total_steps (int): Całkowita liczba kroków
        message (str): Wiadomość do wyświetlenia
    """
    progress = step / total_steps
    progress_bar.progress(progress)
    status_text.text(f"Krok {step}/{total_steps}: {message}")

def toast_notification(message, icon="🎉"):
    """
    Wyświetla toast notification (jeśli dostępne w Streamlit).
    
    Args:
        message (str): Treść powiadomienia
        icon (str): Ikona powiadomienia
    """
    try:
        # Używaj st.toast jeśli dostępne (Streamlit 1.27+)
        if hasattr(st, 'toast'):
            st.toast(f"{icon} {message}")
        else:
            # Fallback do success message
            st.success(f"{icon} {message}")
    except Exception:
        # Ultimate fallback
        st.info(f"{icon} {message}")

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


@st.fragment
def render_history_selector(key_prefix: str, placeholder_text: str = "Wybierz afirmację..."):
    """
    Reusable fragment for selecting from affirmation history.
    
    Args:
        key_prefix (str): Unique prefix for widget keys
        placeholder_text (str): Placeholder text for selectbox
        
    Returns:
        str: Selected affirmation or None
    """
    from utils.session_state import StateManager
    
    history = StateManager.get('generator.history', [])
    if not history:
        st.warning("Historia jest pusta. Najpierw wygeneruj afirmację!")
        return None
        
    return st.selectbox(
        "Wybierz afirmację:",
        history,
        format_func=lambda x: x[:100] + "..." if len(x) > 100 else x,
        key=f"{key_prefix}_history_select",
        placeholder=placeholder_text
    )


@st.fragment  
def render_section_header(title: str, subtitle: str = None):
    """
    Reusable fragment for section headers.
    
    Args:
        title (str): Main section title
        subtitle (str, optional): Subtitle text
    """
    spacer("2.5rem")
    st.markdown(f"<h2 style='text-align: center;'>{title}</h2>", unsafe_allow_html=True)
    
    if subtitle:
        st.markdown(f"""
            <div style="text-align: center; width: 100%;">
                <h8> {subtitle} </h8>
            </div>
        """, unsafe_allow_html=True)
        
    spacer("1.5rem")


@st.fragment
def render_centered_column_layout(content_callback, column_ratio=[1, 3, 1]):
    """
    Reusable fragment for centered column layout.
    
    Args:
        content_callback (callable): Function to render content in center column
        column_ratio (list): Column width ratios
    """
    col1, col2, col3 = st.columns(column_ratio)
    with col2:
        content_callback()


@st.fragment
def render_provider_info_message(provider_name: str, feature_name: str = "audio"):
    """
    Reusable fragment for provider-specific feature messages.
    
    Args:
        provider_name (str): Name of the provider
        feature_name (str): Name of the feature
    """
    if provider_name != "openai":
        st.info(f"🎵 Funkcje {feature_name} dostępne tylko z OpenAI")
        return True
    return False