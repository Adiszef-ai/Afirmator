"""
components/audio_player.py - Reusable audio player component with download functionality
"""
import streamlit as st
import base64
from ui.components import spacer
from utils.session_state import StateManager


@st.fragment
def render_audio_player(audio_data, filename_base: str, session_key: str = None):
    """
    Reusable component for displaying audio player with download link.
    
    Args:
        audio_data (bytes): Audio data to play
        filename_base (str): Base filename for download (without extension)
        session_key (str, optional): Session state key to store audio data
        
    Returns:
        bool: True if audio player was rendered successfully
    """
    if not audio_data:
        return False
        
    # Store in session if key provided
    if session_key:
        StateManager.set(session_key, audio_data)
    
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; width: 100%;">
            <h8> Twoja afirmacja audio: </h8>
        </div>
    """, unsafe_allow_html=True)
    spacer("2rem")
    
    # Audio player
    st.audio(audio_data, format="audio/mp3")
    
    # Download link
    b64 = base64.b64encode(audio_data).decode()
    filename = f"{filename_base}.mp3"
    download_href = f"""
        <div style="text-align: center; margin-top: 1rem;">
            <a href="data:file/mp3;base64,{b64}" 
               download="{filename}" 
               class="download-button">
                💾 Pobierz MP3
            </a>
        </div>
    """
    st.markdown(download_href, unsafe_allow_html=True)
    return True


@st.fragment
def render_audio_generation_button(button_text: str, key_prefix: str, 
                                 on_click_callback=None, disabled: bool = False):
    """
    Reusable audio generation button with loading state.
    
    Args:
        button_text (str): Text to display on button
        key_prefix (str): Unique prefix for button key
        on_click_callback (callable, optional): Callback function to execute on click
        disabled (bool): Whether button should be disabled
        
    Returns:
        bool: True if button was clicked
    """
    return st.button(
        button_text, 
        use_container_width=True, 
        key=f"{key_prefix}_generate_btn",
        disabled=disabled
    )


def generate_audio_with_spinner(openai_service, affirmation_text: str, 
                              voice: str, speed: float, spinner_text: str = "Generuję audio..."):
    """
    Helper function to generate audio with loading spinner.
    
    Args:
        openai_service: OpenAI service instance
        affirmation_text (str): Text to convert to speech
        voice (str): Voice to use
        speed (float): Speaking speed
        spinner_text (str): Text to show in spinner
        
    Returns:
        bytes: Generated audio data or None if error occurred
    """
    try:
        with st.spinner(spinner_text):
            return openai_service.generate_affirmation_audio(
                affirmation_text,
                voice=voice,
                speed=speed
            )
    except Exception as e:
        st.error(f"❌ Błąd podczas generowania audio: {str(e)}")
        return None


@st.fragment
def render_audio_tips(tips_title: str = "💡 Wskazówki audio", tips_list: list = None):
    """
    Reusable component for displaying audio usage tips.
    
    Args:
        tips_title (str): Title for the tips section
        tips_list (list): List of tip strings
    """
    if tips_list is None:
        tips_list = [
            "Słuchaj swojej afirmacji audio każdego ranka, tuż po przebudzeniu",
            "Powtarzaj wraz z nagraniem, aby wzmocnić efekt",
            "Słuchaj ponownie wieczorem, przed snem",
            "Wolniejsze tempo pomaga w lepszym przyswajaniu treści",
            "Ustaw jako dzwonek/alarm w telefonie dla regularnego przypomnienia"
        ]
    
    st.markdown("---")
    tips_html = f"""
    <div style="padding: 15px; border-radius: 10px; margin-top: 20px;">
        <h5 style="margin: 0;">{tips_title}</h5>
        <ul style="text-align: left; margin-top: 0.2rem;">
    """
    
    for tip in tips_list:
        tips_html += f"<li>{tip}</li>"
    
    tips_html += """
        </ul>
    </div>
    """
    
    st.markdown(tips_html, unsafe_allow_html=True)