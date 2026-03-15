"""
components/affirmation_selector.py - Reusable Streamlit component for affirmation selection
"""
import streamlit as st
from ui.components import affirmation_card, centered_text, spacer
from config.translations import t
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
    centered_text(t("selector.affirmation_choice"))

    # Source selection
    text_source = st.radio(
        t("selector.text_source"),
        [t("selector.from_history"), t("selector.custom_text")],
        horizontal=True,
        key=f"{key_prefix}_text_source"
    )

    selected_affirmation = None

    # Handle history selection
    if text_source == t("selector.from_history"):
        history = StateManager.get('generator.history', [])
        if history:
            selected_affirmation = st.selectbox(
                t("selector.select"),
                history,
                format_func=lambda x: x[:100] + "..." if len(x) > 100 else x,
                key=f"{key_prefix}_affirmation_select"
            )

            # Display selected affirmation from history
            if selected_affirmation:
                centered_text(t("selector.selected"))
                affirmation_card(selected_affirmation)
                spacer("1rem")
        else:
            st.warning(t("selector.history_empty"))
            return None

    # Handle custom text input
    else:
        custom_text = st.text_area(
            t("selector.custom_label"),
            height=100,
            placeholder=t("selector.custom_placeholder"),
            help=t("selector.custom_help"),
            key=f"{key_prefix}_custom_text",
            max_chars=300
        )

        # Accept button for custom text
        if st.button(t("selector.accept"),
                    use_container_width=True,
                    type="primary",
                    key=f"{key_prefix}_accept_btn"):
            if not custom_text or len(custom_text.strip()) == 0:
                st.warning(t("selector.enter_text_warning"))
                return None

            selected_affirmation = custom_text.strip()
            # Display accepted custom affirmation
            centered_text(t("selector.selected"))
            affirmation_card(selected_affirmation)
            spacer("1rem")

    # Validation
    if not selected_affirmation:
        if text_source == t("selector.custom_text"):
            st.info(t("selector.enter_text_info"))
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
    from config.constants import get_voice_options

    VOICE_OPTIONS = get_voice_options()

    centered_text(t("voice.settings_title"))

    # Voice selection
    voice_label = st.selectbox(
        t("voice.label"),
        options=list(VOICE_OPTIONS.keys()),
        index=2,
        help=t("voice.help"),
        key=f"{key_prefix}_voice_select"
    )
    selected_voice = VOICE_OPTIONS[voice_label]

    # Speed setting
    speed = st.slider(
        t("voice.speed"),
        min_value=0.5,
        max_value=1.5,
        value=0.8,
        step=0.05,
        help=t("voice.speed_help"),
        key=f"{key_prefix}_speed_slider"
    )

    return {
        'voice': selected_voice,
        'voice_label': voice_label,
        'speed': speed
    }
