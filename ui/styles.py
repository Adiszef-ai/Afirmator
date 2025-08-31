"""
app/ui/styles.py - Style CSS loader dla aplikacji Afirmator.
"""
import streamlit as st
import os

# Cachowane ładowanie CSS - plik CSS nie zmienia się często
@st.cache_data(show_spinner=False)
def _cached_load_css(css_path):
    """
    Cachowane ładowanie pliku CSS.
    """
    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        # Nie wyświetlaj błędu tutaj - może się dziać przed st.set_page_config()
        print(f"Warning: Błąd ładowania CSS: {str(e)}")  # Użyj print zamiast st.error
        return ""

def inject_custom_css():
    """
    Ładuje niestandardowy CSS z pliku external z cache.
    """
    # Ścieżka do pliku CSS
    css_path = os.path.join(os.path.dirname(__file__), 'static', 'style.css')
    
    # Użyj cachowanego ładowania CSS
    css_content = _cached_load_css(css_path)
    
    if css_content:
        # Dynamiczne ustawienie motywu na podstawie session_state
        theme_class = ""
        try:
            from utils.session_state import StateManager
            if StateManager.get('app.theme', 'light') == 'dark':
                theme_class = 'data-theme="dark"'
        except ImportError:
            pass  # Fallback jeśli StateManager nie jest dostępny
        
        st.markdown(f"""
            <style>
                {css_content}
            {theme_class}
            </style>
        """, unsafe_allow_html=True)
    else:
        # Fallback basic styling jeśli CSS się nie załadował
        st.markdown("""
            <style>
                .main { padding: 1rem; }
                .stButton > button { 
                    background: linear-gradient(45deg, #4A90E2, #FF6B9C);
                    color: white;
                    border: none;
                    border-radius: 8px;
                }
            </style>
        """, unsafe_allow_html=True)