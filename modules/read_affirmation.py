"""
app/modules/core/read_affirmation.py - Moduł obsługujący dedykowaną zakładkę do czytania afirmacji.
"""
import streamlit as st
from components.affirmation_selector import render_affirmation_selector, render_voice_settings
from components.audio_player import render_audio_player, generate_audio_with_spinner, render_audio_tips
from config.translations import t
from ui.components import render_section_header, render_centered_column_layout
from utils.session_state import StateManager

def display_read_affirmation_section(openai_service):
    """
    Wyświetla sekcję odtwarzacza afirmacji z zaawansowanymi opcjami audio.

    Args:
        openai_service (OpenAIService): Instancja serwisu OpenAI.
    """
    render_section_header(
        t("read.title"),
        t("read.subtitle")
    )

    def render_content():
        # Use reusable affirmation selector
        selected_affirmation = render_affirmation_selector("audio_player")
        if not selected_affirmation:
            return

        # Use reusable voice settings
        voice_settings = render_voice_settings("audio_player")

        # Generate audio button
        if st.button(t("read.generate_audio"), use_container_width=True, key="audio_player_generate_btn"):
            audio_data = generate_audio_with_spinner(
                openai_service,
                selected_affirmation,
                voice_settings['voice'],
                voice_settings['speed'],
                t("read.generating")
            )
            if audio_data:
                StateManager.set('audio.player_data', audio_data)

        # Display audio player if available
        if StateManager.has_key('audio.player_data') and StateManager.get('audio.player_data'):
            filename_base = f"afirmacja_{voice_settings['voice_label'].lower().replace(' ', '_')}_{voice_settings['speed']}"
            render_audio_player(
                StateManager.get('audio.player_data'),
                filename_base
            )

    # Use centered column layout
    render_centered_column_layout(render_content)

    # Use reusable audio tips
    render_audio_tips(t("read.tips_title"))
