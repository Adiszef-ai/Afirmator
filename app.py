"""
Aplikacja Afirmator - generator spersonalizowanych afirmacji - wersja ulepszona.
"""
import streamlit as st

# Importy modułów
from config.constants import DEFAULT_SESSION_STATE
from modules.utils import init_session_state, check_api_key
from modules.daily import display_daily_affirmation_section
from modules.generator import display_generator_interface, generate_affirmation, display_affirmation_result
from modules.visual_quote import display_visual_quote_section
from modules.audio_player import display_audio_player_section
from modules.musical_affirmation import display_musical_affirmation_section
from services.openai_service import OpenAIService
from ui.styles import inject_custom_css
from ui.sidebar import display_sidebar
from ui.components import header, create_tabs, api_key_input, spacer



def welcome_screen():
    """
    Wyświetla ekran powitalny dla nowych użytkowników.
    """
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="font-size: 3.5rem; margin-bottom: 1rem;">
                Witaj w Afirmatorze
            </h1>
            <h8 style=>
                Twój osobisty generator pozytywnych afirmacji wspomaganych przez AI
            </h8>
        </div>
    """, unsafe_allow_html=True)
    
    # Karty z funkcjami w górnym rzędzie - 3 karty
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    
    with row1_col1:
        st.markdown("""
            <div class="welcome-card">
                <div class="welcome-card-icon">🌅</div>
                <h3 class="welcome-card-title">Afirmacja dnia</h3>
                <p class="welcome-card-description">Codzienna dawka pozytywnej energii</p>
            </div>
        """, unsafe_allow_html=True)
    
    with row1_col2:
        st.markdown("""
            <div class="welcome-card">
                <div class="welcome-card-icon">🛠️</div>
                <h3 class="welcome-card-title">Generator Afirmacji</h3>
                <p class="welcome-card-description">Spersonalizuj swoją afirmacje</p>
            </div>
        """, unsafe_allow_html=True)
    
    with row1_col3:
        st.markdown("""
            <div class="welcome-card">
                <div class="welcome-card-icon">🎨</div>
                <h3 class="welcome-card-title">Wizualny cytat</h3>
                <p class="welcome-card-description">Twórz obrazy z afirmacjami</p>
            </div>
        """, unsafe_allow_html=True)
        
    # Drugi rząd kart - 2 karty wycentrowane
    _, row2_col1, row2_col2, _ = st.columns([1, 2, 2, 1])
    
    with row2_col1:
        st.markdown("""
            <div class="welcome-card">
                <div class="welcome-card-icon">🎧</div>
                <h3 class="welcome-card-title">Czytanie afirmacji</h3>
                <p class="welcome-card-description">Kontroluj prędkość czytania</p>
            </div>
        """, unsafe_allow_html=True)
        
    with row2_col2:
        st.markdown("""
            <div class="welcome-card">
                <div class="welcome-card-icon">🎵</div>
                <h3 class="welcome-card-title">Muzyczna afirmacja</h3>
                <p class="welcome-card-description">Afirmacje z podkładem muzycznym</p>
            </div>
        """, unsafe_allow_html=True)
    
    spacer("3rem")
    
    # Pole do wprowadzenia klucza API
    key = api_key_input()
    if key:
        st.session_state.api_key = key
        st.rerun()

def main():
    """
    Główna funkcja aplikacji
    """
    # Konfiguracja strony
    st.set_page_config(
        page_title="Generator Afirmacji AI",
        page_icon="✨",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Inicjalizacja stanu sesji
    init_session_state()
    
    # Wstrzykiwanie CSS
    inject_custom_css()
    
    # Sprawdzenie klucza API z ładnym ekranem powitalnym
    if not st.session_state.api_key:
        welcome_screen()
        return
    
    # Inicjalizacja serwisu OpenAI
    try:
        openai_service = OpenAIService()
    except ValueError as e:
        st.error(f"Błąd klucza API: {str(e)}")
        # Resetuj klucz API i pokaż ponownie ekran powitalny
        st.session_state.api_key = None
        welcome_screen()
        return
    except Exception as e:
        st.error(f"Nieoczekiwany błąd: {str(e)}")
        # Resetuj klucz API i pokaż ponownie ekran powitalny
        st.session_state.api_key = None
        welcome_screen()
        return
    
    # Layout aplikacji
    header()
    
    # Wyświetlenie panelu bocznego
    display_sidebar()
    
    # Główna zawartość - pięć zakładek!
    tab1, tab2, tab3, tab4, tab5 = create_tabs()
    
    # Zakładka Afirmacja dnia
    with tab1:
        display_daily_affirmation_section(openai_service)
    
    # Zakładka Generator afirmacji
    with tab2:
        form_data = display_generator_interface()
        
        if form_data:
            generate_affirmation(form_data, openai_service)
            
        # Wyświetlenie wyniku
        display_affirmation_result(openai_service)
    
    # Zakładka Wizualny cytat
    with tab3:
        display_visual_quote_section()
    
    # Zakładka Czytanie afirmacji
    with tab4:
        display_audio_player_section(openai_service)
        
    # Zakładka Muzyczna afirmacja
    with tab5:
        display_musical_affirmation_section(openai_service)
    
    # Dodajemy stopkę
    spacer("2rem")
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; opacity: 0.7;">
            <p>Afirmator V1.1 | Stworzone z ❤️ | © 2025</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()