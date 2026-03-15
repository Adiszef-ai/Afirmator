"""
components/audio_player.py - Reusable audio player component with download functionality
"""
import streamlit as st
import base64
from ui.components import spacer
from config.translations import t
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
    st.markdown(f"""
        <div style="text-align: center; width: 100%;">
            <h8> {t("audio.your_affirmation")} </h8>
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
                {t("audio.download")}
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
                              voice: str, speed: float, spinner_text: str = None):
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
    if spinner_text is None:
        spinner_text = t("components.loading")
    try:
        with st.spinner(spinner_text):
            return openai_service.generate_affirmation_audio(
                affirmation_text,
                voice=voice,
                speed=speed
            )
    except Exception as e:
        st.error(f"{t('audio.error')}{str(e)}")
        return None


@st.fragment
def render_audio_tips(tips_title: str = None, tips_list: list = None):
    """
    Reusable component for displaying audio usage tips.

    Args:
        tips_title (str): Title for the tips section
        tips_list (list): List of tip strings
    """
    if tips_title is None:
        tips_title = t("audio.default_tips_title")

    if tips_list is None:
        tips_list = [
            t("audio.tip_1"),
            t("audio.tip_2"),
            t("audio.tip_3"),
            t("audio.tip_4"),
            t("audio.tip_5"),
        ]

    st.markdown("---")
    tips_html = f"""
    <div style="padding: 15px; border-radius: 10px; margin-top: 20px;">
        <h5 style="margin: 0;">{tips_title}</h5>
        <ul style="text-align: left; margin-top: 0.2rem;">
    """

    for tip_item in tips_list:
        tips_html += f"<li>{tip_item}</li>"

    tips_html += """
        </ul>
    </div>
    """

    st.markdown(tips_html, unsafe_allow_html=True)
