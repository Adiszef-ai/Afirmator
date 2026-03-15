"""
app/modules/generator.py - Moduł obsługujący funkcjonalność generatora afirmacji.
"""
import streamlit as st
from config.constants import (
    get_affirmation_length_options,
    get_focus_areas,
    get_emotion_states,
    get_affirmation_styles,
    get_affirmation_timing,
    get_affirmation_tones,
)
from config.translations import t, get_language
from services.openai_service import OpenAIService
from config.utils import save_to_history
from ui.components import spacer
from utils.session_state import StateManager

def display_generator_interface():
    """
    Wyświetla interfejs generatora afirmacji bez formularza.

    Returns:
        dict: Dane wprowadzone przez użytkownika.
    """
    spacer("2.5rem")
    st.markdown(f"<h2 style='text-align: center;'>{t('generator.title')}</h2>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style="text-align: center; width: 100%;">
            <h8> {t("generator.subtitle")} </h8>
        </div>
    """, unsafe_allow_html=True)
    spacer("1.5rem")
    # Pola bez formularza
    col1, col2, col3 = st.columns([1, 3, 1])

    focus_areas = get_focus_areas()
    custom_goals_label = t("const.focus.custom")

    with col2:
        user_name = st.text_input(t("generator.your_name"), key="generator_user_name", max_chars=30)
        focus_area = st.selectbox(t("generator.focus_area"), focus_areas, key="generator_focus_area")

        # Pokazuj pole "Wprowadź swój cel" tylko jeśli wybrano "Własne cele"
        specific_goal = ""
        if focus_area == custom_goals_label:
            specific_goal = st.text_area(t("generator.enter_goal"), key="generator_specific_goal", max_chars=250,
                                        placeholder=t("generator.goal_placeholder"))

        emotion_state = st.selectbox(t("generator.emotion_state"), get_emotion_states(), key="generator_emotion_state")
        preferred_style = st.selectbox(t("generator.preferred_style"), get_affirmation_styles(), key="generator_preferred_style")
        affirmation_length = st.selectbox(t("generator.affirmation_length"), get_affirmation_length_options(), key="generator_affirmation_length")
        affirmation_timing = st.selectbox(t("generator.affirmation_timing"), get_affirmation_timing(), key="generator_affirmation_timing")
        affirmation_tone = st.selectbox(t("generator.affirmation_tone"), get_affirmation_tones(), key="generator_affirmation_tone")

        # Przycisk generowania
        if st.button(t("generator.create"), use_container_width=True, key="generator_submit"):
            if not user_name:
                st.warning(t("generator.enter_name"))
                return None

            if focus_area == custom_goals_label and not specific_goal:
                st.warning(t("generator.enter_goal_warning"))
                return None

            return {
                "user_name": user_name,
                "focus_area": focus_area,
                "specific_goal": specific_goal,
                "emotion_state": emotion_state,
                "preferred_style": preferred_style,
                "affirmation_length": affirmation_length,
                "affirmation_timing": affirmation_timing,
                "affirmation_tone": affirmation_tone
            }

        return None

def generate_affirmation(form_data, ai_service):
    """
    Generuje afirmację na podstawie danych z formularza.

    Args:
        form_data (dict): Dane z formularza.
        ai_service: Instancja serwisu AI (OpenAI lub Groq).

    Returns:
        str: Wygenerowana afirmacja lub None w przypadku błędu.
    """
    custom_goals_label = t("const.focus.custom")
    target_focus = form_data["specific_goal"] if form_data["focus_area"] == custom_goals_label else form_data["focus_area"]

    lang = get_language()

    if lang == "pl":
        prompt = f"""
        Stwórz spersonalizowaną afirmację dla {form_data["user_name"]} w języku polskim, która:
        1. Skoncentruje się na: {target_focus}
        2. Zaczyna się od \"Ja, {form_data["user_name"]}\"
        3. Uwzględni obecny stan emocjonalny: {form_data["emotion_state"]}
        4. Odniesie się do konkretnego celu: {form_data["specific_goal"]}
        5. Będzie w stylu: {form_data["preferred_style"]}
        6. Użyje pozytywnego języka w czasie teraźniejszym
        7. Będzie miała długość: {form_data["affirmation_length"]}
        8. Powinna być stosowana: {form_data["affirmation_timing"]}
        9. Powinna mieć ton: {form_data["affirmation_tone"]}
        10. Zawiera elementy wizualizacji i emocji
        """
    else:
        prompt = f"""
        Create a personalized affirmation for {form_data["user_name"]} in English, which:
        1. Focuses on: {target_focus}
        2. Starts with \"I, {form_data["user_name"]}\"
        3. Takes into account the current emotional state: {form_data["emotion_state"]}
        4. Relates to the specific goal: {form_data["specific_goal"]}
        5. Is in the style: {form_data["preferred_style"]}
        6. Uses positive language in the present tense
        7. Has the length: {form_data["affirmation_length"]}
        8. Should be used: {form_data["affirmation_timing"]}
        9. Should have the tone: {form_data["affirmation_tone"]}
        10. Contains elements of visualization and emotion
        """

    try:
        with st.spinner(t("generator.creating")):
            # Sprawdź typ serwisu i wywołaj odpowiednią metodę
            if hasattr(ai_service, 'generate_affirmation') and callable(getattr(ai_service, 'generate_affirmation')):
                # Dla GroqService z dodatkowymi parametrami
                if hasattr(ai_service, 'model') and 'llama' in str(ai_service.model):
                    language = "polski" if lang == "pl" else "English"
                    affirmation = ai_service.generate_affirmation(
                        categories=[form_data["focus_area"]],
                        tone=form_data["affirmation_tone"],
                        timing=form_data["affirmation_timing"],
                        context=form_data.get("specific_goal", ""),
                        user_name=form_data["user_name"],
                        length=form_data["affirmation_length"],
                        language=language
                    )
                else:
                    # Dla OpenAIService
                    affirmation = ai_service.generate_affirmation(prompt)
            else:
                # Fallback dla uniwersalnych serwisów
                affirmation = ai_service.generate_text(prompt)
            StateManager.set('generator.affirmation', affirmation)
            StateManager.set('generator.edited_affirmation', affirmation)
            StateManager.set('audio.data', None)
            StateManager.set('generator.user_name', form_data["user_name"])
            save_to_history(affirmation)
            return affirmation
    except Exception as e:
        st.error(f"{t('generator.error')}{str(e)}")
        return None

def display_affirmation_result(ai_service, provider_name="openai"):
    """
    Wyświetla wynik wygenerowanej afirmacji i opcje edycji.

    Args:
        ai_service: Instancja serwisu AI.
        provider_name (str): Nazwa providera AI.
    """
    if not StateManager.get('generator.affirmation'):
        return

    st.markdown("---")
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown(f"""
            <div style="text-align: center; width: 100%;">
                <h8> {t("generator.your_affirmation")}</h8>
            </div>
        """, unsafe_allow_html=True)

        # Obsługa trybu edycji
        if StateManager.get('generator.editing', False):
            _display_affirmation_edit_mode()
        else:
            _display_affirmation_view_mode()

    st.markdown("---")

    # Wskazówki
    _display_affirmation_tips()

def _display_affirmation_edit_mode():
    """Wyświetla interfejs edycji afirmacji."""
    edited_text = st.text_area(
        t("generator.edit_label"),
        value=StateManager.get('generator.edited_affirmation', ''),
        height=150,
        key="edit_affirmation_text"
    )
    StateManager.set('generator.edited_affirmation', edited_text)
    if st.button(t("generator.save_changes"), use_container_width=True, key="save_affirmation_changes"):
        StateManager.set('generator.editing', False)
        StateManager.set('audio.data', None)
        # Dodanie edytowanej afirmacji do historii
        save_to_history(StateManager.get('generator.edited_affirmation'))
        st.rerun()

def _display_affirmation_view_mode():
    """Wyświetla afirmację w trybie podglądu."""
    st.markdown(
        f"""
        <div class="affirmation-card" style="
            text-align: center;
            font-size: 18px;
        ">
            {StateManager.get('generator.edited_affirmation', '')}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Przyciski akcji w trzech równych kolumnach, jak w module daily
    col_a, col_b, col_c = st.columns([1, 1, 1])

    with col_a:
        if st.button(t("generator.edit"), use_container_width=True, key="edit_affirmation_button"):
            StateManager.set('generator.editing', True)
            st.rerun()

    with col_b:
        if st.button(t("generator.new_affirmation"), use_container_width=True, key="new_generator_affirmation"):
            # Resetujemy stan edycji, ale zachowujemy dane użytkownika aby pokazać ponownie formularz
            StateManager.set('generator.affirmation', None)
            StateManager.set('generator.edited_affirmation', None)
            StateManager.set('generator.editing', False)
            st.rerun()

    with col_c:
        if st.button(t("generator.copy"), use_container_width=True, key="copy_generator_affirmation"):
            st.toast(t("generator.copied"), icon='✨')

def _display_affirmation_tips():
    """Wyświetla wskazówki dotyczące stosowania afirmacji."""
    st.markdown(f"""
    <div style="padding: 15px; border-radius: 10px; margin-top: 20px;">
        <h5 style="margin-top: 0.2;">{t("generator.tips_title")}</h5>
        <ul>
            <li>{t("generator.tip_1")}</li>
            <li>{t("generator.tip_2")}</li>
            <li>{t("generator.tip_3")}</li>
            <li>{t("generator.tip_4")}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
