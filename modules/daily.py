"""
app/modules/daily.py - Moduł obsługujący funkcjonalność afirmacji dnia - wersja ulepszona.
"""
import random
import streamlit as st
from config.constants import get_daily_affirmation_topics
from config.translations import t, get_language
# AI services będą przekazywane jako parametr
from ui.components import affirmation_card, spacer
from config.utils import save_to_history
from utils.session_state import StateManager

def generate_daily_affirmation(ai_service, user_name):
    """
    Generuje afirmację dnia dla użytkownika.

    Args:
        ai_service: Instancja serwisu AI (OpenAI lub Groq).
        user_name (str): Imię użytkownika.

    Returns:
        str: Wygenerowana afirmacja dnia lub None w przypadku braku imienia.
    """
    if not user_name:
        return None

    # Losowy wybór tematu afirmacji dnia
    daily_topic = random.choice(get_daily_affirmation_topics())
    lang = get_language()
    lang_name = "polskim" if lang == "pl" else "angielskim"
    lang_name_en = "Polish" if lang == "pl" else "English"

    try:
        # Sprawdź typ serwisu i wywołaj odpowiednią metodę
        if hasattr(ai_service, 'generate_daily_affirmation'):
            # Dla GroqService
            return ai_service.generate_daily_affirmation(user_name, [daily_topic], language=lang)
        elif hasattr(ai_service, 'generate_affirmation'):
            # Dla OpenAIService
            if lang == "pl":
                prompt = f"""
                Stwórz krótką, inspirującą afirmację dnia dla {user_name} w języku polskim, która:
                1. Będzie skupiona na temacie: {daily_topic}
                2. Zaczyna się od "Ja, {user_name},"
                3. Jest zwięzła (maksymalnie 2-3 zdania)
                4. Ma pozytywny, podnoszący na duchu ton
                5. Używa czasu teraźniejszego
                6. Jest sformułowana w pierwszej osobie
                7. Zawiera element, który można zastosować w codziennym życiu
                """
            else:
                prompt = f"""
                Create a short, inspiring daily affirmation for {user_name} in English, which:
                1. Focuses on the topic: {daily_topic}
                2. Starts with "I, {user_name},"
                3. Is concise (maximum 2-3 sentences)
                4. Has a positive, uplifting tone
                5. Uses the present tense
                6. Is formulated in the first person
                7. Contains an element that can be applied in daily life
                """
            return ai_service.generate_affirmation(prompt, max_tokens=120)
        else:
            # Fallback dla uniwersalnych serwisów
            if lang == "pl":
                prompt = f"Stwórz pozytywną afirmację dnia dla {user_name} na temat: {daily_topic}. Afirmacja powinna zaczynać się od 'Ja, {user_name},' i być w języku polskim."
            else:
                prompt = f"Create a positive daily affirmation for {user_name} about: {daily_topic}. The affirmation should start with 'I, {user_name},' and be in English."
            return ai_service.generate_text(prompt, max_tokens=120)

    except Exception as e:
        return f"{t('generator.error')}{str(e)}"

def display_daily_affirmation_section(ai_service):
    """
    Wyświetla sekcję afirmacji dnia z ulepszonym UI.

    Args:
        openai_service (OpenAIService): Instancja serwisu OpenAI.
    """
    spacer("2.5rem")
    st.markdown(f"<h2 style='text-align: center;'>{t('daily.title')}</h2>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style="text-align: center; width: 100%;">
            <h8> {t("daily.subtitle")} </h8>
        </div>
    """, unsafe_allow_html=True)
    spacer("1.5rem")

    # Inicjalizacja zmiennych stanu dla edycji - przez StateManager
    if not StateManager.has_key('generator.editing'):
        StateManager.set('generator.editing', False)
    if not StateManager.has_key('generator.edited_affirmation') and StateManager.has_key('daily.affirmation'):
        StateManager.set('generator.edited_affirmation', StateManager.get('daily.affirmation'))

    # Sprawdzamy czy afirmacja już istnieje w StateManager
    if not StateManager.has_key('daily.affirmation') or StateManager.get('daily.affirmation') is None:
        _display_daily_affirmation_input(ai_service)
    else:
        _display_daily_affirmation_content(ai_service)

        # Wskazówki dotyczące używania afirmacji dnia - tylko gdy afirmacja jest wygenerowana
        st.markdown("---")
        st.markdown(f"""
            <div style="padding: 15px; border-radius: 10px; margin-top: 20px;">
                <h5 style="margin: 0;">{t("daily.tips_title")}</h5>
                <ul style="text-align: left; margin-top: 0.2rem;">
                    <li>{t("daily.tip_1")}</li>
                    <li>{t("daily.tip_2")}</li>
                    <li>{t("daily.tip_3")}</li>
                    <li>{t("daily.tip_4")}</li>
                    <li>{t("daily.tip_5")}</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

def _display_daily_affirmation_input(ai_service):
    """
    Wyświetla formularz wprowadzania imienia dla afirmacji dnia.

    Args:
        openai_service (OpenAIService): Instancja serwisu OpenAI.
    """
    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        name_input = st.text_input(
            t("daily.your_name"),
            key="daily_name_input",
            placeholder=t("daily.name_placeholder"),
            max_chars=30,
            help=t("daily.name_help")
        )

        if st.button(t("daily.show_affirmation"), key="show_daily_affirmation", use_container_width=True):
            if name_input:
                with st.spinner(t("daily.creating")):
                    daily_affirmation = generate_daily_affirmation(ai_service, name_input)
                    StateManager.set('daily.affirmation_name', name_input)
                    StateManager.set('daily.affirmation', daily_affirmation)
                    StateManager.set('generator.edited_affirmation', daily_affirmation)
                    # Zapisywanie afirmacji dnia do historii
                    save_to_history(daily_affirmation)
                    st.rerun()
            else:
                st.warning(t("daily.enter_name"))

def _display_daily_affirmation_content(ai_service):
    """
    Wyświetla wygenerowaną afirmację dnia i opcje audio.

    Args:
        openai_service (OpenAIService): Instancja serwisu OpenAI.
    """
    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        # Obsługa trybu edycji
        if StateManager.get('generator.editing', False):
            edited_text = st.text_area(
                t("daily.edit_label"),
                value=StateManager.get('generator.edited_affirmation', ''),
                height=150,
                key="edit_daily_affirmation_text"
            )
            StateManager.set('generator.edited_affirmation', edited_text)
            if st.button(t("daily.save_changes"), use_container_width=True, key="save_daily_affirmation_changes"):
                StateManager.set('generator.editing', False)
                StateManager.set('daily.affirmation', StateManager.get('generator.edited_affirmation'))
                # Dodanie edytowanej afirmacji do historii
                save_to_history(StateManager.get('generator.edited_affirmation'))
                st.rerun()
        else:
            # Wyświetlenie afirmacji w eleganckiej karcie
            affirmation_card(StateManager.get('generator.edited_affirmation', ''))

            # Przyciski akcji
            col_a, col_b, col_c = st.columns([1, 1, 1])

            with col_a:
                if st.button(t("daily.edit"), use_container_width=True, key="edit_daily_affirmation"):
                    StateManager.set('generator.editing', True)
                    st.rerun()

            with col_b:
                if st.button(t("daily.new_affirmation"), key="new_daily_affirmation", use_container_width=True):
                    with st.spinner(t("daily.generating_new")):
                        daily_affirmation = generate_daily_affirmation(ai_service, StateManager.get('daily.affirmation_name'))
                        StateManager.set('daily.affirmation', daily_affirmation)
                        StateManager.set('generator.edited_affirmation', daily_affirmation)
                        # Zapisywanie nowej afirmacji dnia do historii
                        save_to_history(daily_affirmation)
                        st.rerun()

            with col_c:
                if st.button(t("daily.copy"), key="copy_affirmation", use_container_width=True):
                    st.toast(t("daily.copied"), icon='✨')
