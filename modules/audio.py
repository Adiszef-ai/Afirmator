"""
app/modules/audio.py - Moduł obsługujący dedykowaną zakładkę do czytania afirmacji.
"""
import base64
import streamlit as st
from config.constants import VOICE_OPTIONS
from ui.components import button_with_icon

def display_audio_options(openai_service, text, audio_state_key='audio_data', horizontal=True):
    """
    Wyświetla interfejs wyboru głosu i generowania audio z ulepszonym UI.
    
    Args:
        openai_service (OpenAIService): Instancja serwisu OpenAI.
        text (str): Tekst do zamiany na mowę.
        audio_state_key (str, optional): Klucz stanu dla danych audio. Domyślnie 'audio_data'.
        horizontal (bool, optional): Czy wyświetlać opcje głosu poziomo. Domyślnie True.
        
    Returns:
        str: Wybrany głos.
    """
    # Wybór głosu
    voice_label = st.radio(
        "Wybierz głos narracji:",
        options=list(VOICE_OPTIONS.keys()),
        index=2,
        key=f"{audio_state_key}_voice_selection",
        horizontal=horizontal,
        help="Wybierz głos, który najbardziej Ci odpowiada"
    )
    selected_voice = VOICE_OPTIONS[voice_label]
    
    # Przycisk generowania
    if button_with_icon("Odsłuchaj", "🎧", key=f"{audio_state_key}_button"):
        try:
            with st.spinner("🎵 Generuję audio..."):
                audio_data = openai_service.generate_affirmation_audio(
                    text,
                    voice=selected_voice
                )
                st.session_state[audio_state_key] = audio_data
                st.success("✅ Audio gotowe!")
        except Exception as e:
            st.error(f"❌ Błąd generowania audio: {str(e)}")
            
    return selected_voice

def display_audio_player(audio_data_key, download_filename="afirmacja.mp3"):
    """
    Wyświetla odtwarzacz audio i link do pobrania z ulepszonym wyglądem.
    
    Args:
        audio_data_key (str): Klucz stanu sesji zawierający dane audio.
        download_filename (str, optional): Nazwa pliku do pobrania. Domyślnie "afirmacja.mp3".
        
    Returns:
        bool: True jeśli dane audio są dostępne i wyświetlone, False w przeciwnym razie.
    """
    if audio_data_key in st.session_state and st.session_state[audio_data_key]:
        # Odtwarzacz w ładnej karcie
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.audio(st.session_state[audio_data_key], format="audio/mp3")
            
            # Link do pobrania
            b64 = base64.b64encode(st.session_state[audio_data_key]).decode()
            download_href = f"""
                <div style="text-align: center; margin-top: 1rem;">
                    <a href="data:file/mp3;base64,{b64}" 
                       download="{download_filename}" 
                       class="download-button">
                        💾 Pobierz MP3
                    </a>
                </div>
            """
            st.markdown(download_href, unsafe_allow_html=True)
        
        return True
    return False