"""
app/ui/sidebar.py - Komponenty interfejsu dla panelu bocznego - wersja ulepszona.
"""
import streamlit as st
from ui.components import button_with_icon
from utils.session_state import StateManager
from config.translations import t, get_language, set_language


def display_language_switcher():
    """Wyświetla przełącznik języka w sidebarze."""
    lang = get_language()
    lang_options = ["Polski", "English"]
    current_index = 0 if lang == "pl" else 1

    selected = st.sidebar.selectbox(
        t("lang.label"),
        lang_options,
        index=current_index,
        key="language_selector"
    )

    new_lang = "pl" if selected == "Polski" else "en"
    if new_lang != lang:
        set_language(new_lang)
        st.rerun()


def display_sidebar():
    """
    Wyświetla zawartość panelu bocznego z ulepszonym wyglądem.
    """
    with st.sidebar:
        # Przełącznik języka
        display_language_switcher()

        st.markdown("---")

        st.markdown(f"""
            <h3 style='text-align: center; margin-top: -8px; color: white;'>{t("sidebar.subtitle")}</h3>

        """, unsafe_allow_html=True)

        st.markdown("---")

        # Historia afirmacji
        _display_history_section()

        st.markdown("---")

        # Statystyki
        _display_stats_section()

        st.markdown("---")

        # Pomoc i wsparcie
        _display_help_section()

        # Footer
        st.markdown(f"""
            <div class="sidebar-footer">
                <p style='font-size: 0.9rem; color: rgba(255, 255, 255, 0.7); margin: 0;'>
                    {t("sidebar.footer")}
                </p>
            </div>
        """, unsafe_allow_html=True)

def _display_history_section():
    """
    Wyświetla sekcję historii afirmacji z ulepszoną funkcjonalnością.
    """
    st.markdown(f"<h3 style='color: white; a'>{t('sidebar.history_title')}</h3>", unsafe_allow_html=True)

    if StateManager.get('generator.history', []):
        # Filtrowanie i wyszukiwanie
        search_term = st.text_input(
            "Szukaj w historii",
            placeholder=t("sidebar.search_placeholder"),
            key="history_search",
            label_visibility="collapsed"
        )
        st.markdown("<div style='margin-bottom: 0.rem;'></div>", unsafe_allow_html=True)  # Spacer

        # Filtrowanie historii
        history = StateManager.get('generator.history', [])
        filtered_history = [
            aff for aff in history
            if search_term.lower() in aff.lower()
        ] if search_term else history

        if filtered_history:
            selected = st.selectbox(
                t("sidebar.select_affirmation"),
                filtered_history,
                key="history_select",
                format_func=lambda x: x[:50] + "..." if len(x) > 50 else x,
                label_visibility="collapsed"
            )

            # Podgląd zaznaczonej afirmacji
            with st.expander(t("sidebar.preview"), expanded=True):
                st.markdown(f"""
                    <div style='
                        font-style: italic;
                        padding: 8px;
                        background-color: rgba(255, 255, 255, 0.1);
                        border-radius: 8px;
                        font-size: 0.9rem;
                        color: white;
                    '>
                        {selected}
                    </div>
                """, unsafe_allow_html=True)

                if button_with_icon(t("sidebar.use_affirmation"), "▶️", key="use_history_affirmation"):
                    StateManager.set('generator.edited_affirmation', selected)
                    StateManager.set('generator.affirmation', selected)
                    StateManager.set('audio.data', None)
                    StateManager.set('app.current_tab', "generator")
                    st.rerun()
        else:
            st.markdown(f"<p style='color: rgba(255, 255, 255, 0.8);'>{t('sidebar.no_results')}</p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p style='color: rgba(255, 255, 255, 0.8);'>{t('sidebar.history_empty')}</p>", unsafe_allow_html=True)

def _display_stats_section():
    """
    Wyświetla statystyki użytkowania aplikacji.
    """
    st.markdown(f"<h3 style='color: white;'>{t('sidebar.stats_title')}</h3>", unsafe_allow_html=True)

    total_affirmations = len(StateManager.get('generator.history', []))

    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label=t("sidebar.generated"),
            value=total_affirmations,
            help=t("sidebar.generated_help")
        )

    with col2:
        st.metric(
            label=t("sidebar.today"),
            value=1 if StateManager.get('daily.affirmation') else 0,
            help=t("sidebar.today_help")
        )

def _display_help_section():
    """
    Wyświetla sekcję pomocy i wsparcia.
    """
    st.markdown(f"<h3 style='color: white;'>{t('sidebar.help_title')}</h3>", unsafe_allow_html=True)

    with st.expander(t("sidebar.how_it_works")):
        st.markdown(f"""
        <div style='color: white;'>
            <ol style='margin: 0; padding-left: 1.2rem;'>
                <li>{t("sidebar.help_daily")}</li>
                <li>{t("sidebar.help_generator")}
                    <ul style='margin: 0; padding-left: 1.2rem;'>
                        <li>{t("sidebar.help_generator_areas")}</li>
                        <li>{t("sidebar.help_generator_goal")}</li>
                        <li>{t("sidebar.help_generator_emotion")}</li>
                        <li>{t("sidebar.help_generator_style")}</li>
                        <li>{t("sidebar.help_generator_tone")}</li>
                    </ul>
                </li>
                <li>{t("sidebar.help_visual")}</li>
                <li>{t("sidebar.help_reading")}</li>
                <li>{t("sidebar.help_music")}
                    <ul style='margin: 0; padding-left: 1.2rem;'>
                        <li>{t("sidebar.help_music_voice")}</li>
                        <li>{t("sidebar.help_music_reps")}</li>
                        <li>{t("sidebar.help_music_bg")}</li>
                        <li>{t("sidebar.help_music_vol")}</li>
                    </ul>
                </li>
                <li>{t("sidebar.help_history")}</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

    with st.expander(t("sidebar.tips")):
        st.markdown(f"""
        <div style='color: white;'>
            <ul style='margin: 0; padding-left: 1.2rem;'>
                <li>{t("sidebar.tips_regular")}</li>
                <li>{t("sidebar.tips_personalize")}</li>
                <li>{t("sidebar.tips_loud")}</li>
                <li>{t("sidebar.tips_visualize")}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with st.expander(t("sidebar.contact")):
        st.markdown(f"""
        <div style='color: white;'>
            <p>{t("sidebar.contact_question")}</p>
            <p>📧 Email: adiszefai@gmail.com</p>
            <p>💻 GitHub: <a href='https://github.com/Adiszef-ai' style='color: white; text-decoration: underline;'>github.com/Adiszef-ai</a></p>
            <p>❤️ Wspomóż projekt: <a href='https://www.buymeacoffee.com/adiszefai' style='color: white; text-decoration: underline;'>Buy me a coffee</a></p>
        </div>
        """, unsafe_allow_html=True)
