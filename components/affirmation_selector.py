"""
components/affirmation_selector.py - Reusable Streamlit component for affirmation selection
"""
import streamlit as st
from ui.components import affirmation_card, centered_text, spacer
from utils.session_state import StateManager


@st.fragment
def render_affirmation_selector(key_prefix: str):
    """
    Reusable component for selecting affirmations from history or custom input.
    
    Args:
        key_prefix (str): Unique prefix for widget keys to avoid conflicts
        
    Returns:
        str: Selected affirmation text or None if no valid selection
    """
    centered_text("Wybór afirmacji")
    
    # Source selection
    text_source = st.radio(
        "Źródło tekstu afirmacji:",
        ["Wybierz z historii", "Wpisz własny tekst"],
        horizontal=True,
        key=f"{key_prefix}_text_source"
    )
    
    selected_affirmation = None
    
    # Handle history selection
    if text_source == "Wybierz z historii":
        history = StateManager.get('generator.history', [])
        if history:
            selected_affirmation = st.selectbox(
                "Wybierz afirmację:",
                history,
                format_func=lambda x: x[:100] + "..." if len(x) > 100 else x,
                key=f"{key_prefix}_affirmation_select"
            )
            
            # Display selected affirmation from history
            if selected_affirmation:
                centered_text("Wybrana afirmacja")
                affirmation_card(selected_affirmation)
                spacer("1rem")
        else:
            st.warning("Historia jest pusta. Najpierw wygeneruj afirmację!")
            return None
            
    # Handle custom text input
    else:
        custom_text = st.text_area(
            "Wpisz własny tekst afirmacji:",
            height=100,
            placeholder="Wpisz swoją afirmację...",
            help="Wpisz afirmację, którą chcesz użyć",
            key=f"{key_prefix}_custom_text",
            max_chars=300
        )
        
        # Accept button for custom text
        if st.button("Akceptuj afirmację", 
                    use_container_width=True, 
                    type="primary", 
                    key=f"{key_prefix}_accept_btn"):
            if not custom_text or len(custom_text.strip()) == 0:
                st.warning("Proszę wpisać tekst afirmacji!")
                return None
                
            selected_affirmation = custom_text.strip()
            # Display accepted custom affirmation
            centered_text("Wybrana afirmacja")
            affirmation_card(selected_affirmation)
            spacer("1rem")
    
    # Validation
    if not selected_affirmation:
        if text_source == "Wpisz własny tekst":
            st.info("Wpisz tekst afirmacji i kliknij 'Akceptuj afirmację'")
        return None
        
    return selected_affirmation


@st.fragment  
def render_voice_settings(key_prefix: str):
    """
    Reusable component for voice and audio settings.
    
    Args:
        key_prefix (str): Unique prefix for widget keys to avoid conflicts
        
    Returns:
        dict: Dictionary with voice settings (voice, speed)
    """
    from config.constants import VOICE_OPTIONS
    
    centered_text("Ustawienia czytania")
    
    # Voice selection
    voice_label = st.selectbox(
        "Głos:",
        options=list(VOICE_OPTIONS.keys()),
        index=2,
        help="Wybierz głos, który najbardziej Ci odpowiada",
        key=f"{key_prefix}_voice_select"
    )
    selected_voice = VOICE_OPTIONS[voice_label]
    
    # Speed setting
    speed = st.slider(
        "Prędkość:",
        min_value=0.5,
        max_value=1.5,
        value=0.8,
        step=0.05,
        help="Ustaw prędkość mówienia (0.5 = wolno, 1.0 = normalnie, 1.5 = szybko)",
        key=f"{key_prefix}_speed_slider"
    )
    
    return {
        'voice': selected_voice,
        'voice_label': voice_label,
        'speed': speed
    }