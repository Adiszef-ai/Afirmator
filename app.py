"""
app/app.py - Aplikacja Afirmator - generator spersonalizowanych afirmacji
"""
import streamlit as st

# Importy modułów
from config.constants import DEFAULT_SESSION_STATE
from config.utils import init_session_state, check_api_key
from modules.core.daily import display_daily_affirmation_section
from modules.core.generator import display_generator_interface, generate_affirmation, display_affirmation_result
from modules.core.welcome import welcome_screen, display_sidebar_with_provider
from modules.core.visual_quote import display_visual_quote_section
from modules.core.read_affirmation import display_read_affirmation_section
from modules.audio.musical_affirmation import display_musical_affirmation_section
from services.ai_factory import AIServiceFactory
from services.groq_service import GroqService
from services.openai_service import OpenAIService
from ui.styles import inject_custom_css
from ui.sidebar import display_sidebar
from ui.components import header, create_tabs, api_key_input, spacer




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
    
    # Sprawdź czy użytkownik wybrał już providera i ma odpowiedni klucz
    if 'selected_provider' not in st.session_state or not st.session_state.get('selected_provider'):
        welcome_screen()
        return
    
    # Sprawdź czy dla wybranego providera mamy klucz API
    selected_provider = st.session_state.selected_provider
    if selected_provider == 'openai' and not check_api_key('openai'):
        welcome_screen()  # Wrócić do wyboru providera
        return
    elif selected_provider == 'groq' and not check_api_key('groq'):
        st.error("Brak klucza API dla Groq w konfiguracji.")
        if st.button("Wróć do wyboru"):
            st.session_state.selected_provider = None
            st.rerun()
        return
    
    # Stworzenie serwisu AI
    ai_service = AIServiceFactory.create_service(selected_provider)
    if not ai_service:
        st.error("Nie można zainicjalizować serwisu AI")
        if st.button("Wróć do wyboru"):
            st.session_state.selected_provider = None
            st.rerun()
        return
    
    provider_name = selected_provider
    
    # Layout aplikacji
    header()
    
    # Wyświetlenie panelu bocznego z informacją o providerze
    display_sidebar_with_provider(provider_name)
    
    # Główna zawartość - pięć zakładek!
    tab1, tab2, tab3, tab4, tab5 = create_tabs()
    
    # Zakładka Afirmacja dnia
    with tab1:
        display_daily_affirmation_section(ai_service)
    
    # Zakładka Generator afirmacji
    with tab2:
        form_data = display_generator_interface()
        
        if form_data:
            generate_affirmation(form_data, ai_service)
            
        # Wyświetlenie wyniku
        display_affirmation_result(ai_service, provider_name)
    
    # Zakładka Wizualny cytat
    with tab3:
        display_visual_quote_section()
    
    # Zakładka Czytanie afirmacji
    with tab4:
        # Audio tylko dla OpenAI
        if provider_name == "openai":
            display_read_affirmation_section(ai_service)
        else:
            st.info("🎵 Funkcje audio dostępne tylko z OpenAI")
        
    # Zakładka Muzyczna afirmacja
    with tab5:
        # Muzyczna afirmacja tylko dla OpenAI
        if provider_name == "openai":
            display_musical_affirmation_section(ai_service)
        else:
            st.info("🎵 Funkcje muzyczne dostępne tylko z OpenAI")
    
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