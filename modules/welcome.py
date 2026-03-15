"""
modules/core/welcome.py - Moduł obsługujący stronę powitalną aplikacji
"""
import streamlit as st
from config.utils import check_api_key
from config.translations import t, get_language
from ui.sidebar import display_sidebar
from ui.components import spacer
from utils.session_state import StateManager


def welcome_screen():
    """
    Wyświetla ekran powitalny dla nowych użytkowników.
    """
    # Przełącznik języka na stronie powitalnej
    from ui.sidebar import display_language_switcher
    with st.sidebar:
        display_language_switcher()

    st.markdown(f"""
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="font-size: 3.5rem; margin-bottom: 1rem;">
                {t("welcome.title")}
            </h1>
            <h8 style=>
                {t("welcome.subtitle")}
            </h8>
        </div>
    """, unsafe_allow_html=True)

    # Karty z funkcjami w górnym rzędzie - 3 karty
    row1_col1, row1_col2, row1_col3 = st.columns(3)

    with row1_col1:
        st.markdown(f"""
            <div class="welcome-card">
                <div class="welcome-card-icon">🌅</div>
                <h3 class="welcome-card-title">{t("welcome.card_daily_title")}</h3>
                <p class="welcome-card-description">{t("welcome.card_daily_desc")}</p>
            </div>
        """, unsafe_allow_html=True)

    with row1_col2:
        st.markdown(f"""
            <div class="welcome-card">
                <div class="welcome-card-icon">🛠️</div>
                <h3 class="welcome-card-title">{t("welcome.card_generator_title")}</h3>
                <p class="welcome-card-description">{t("welcome.card_generator_desc")}</p>
            </div>
        """, unsafe_allow_html=True)

    with row1_col3:
        st.markdown(f"""
            <div class="welcome-card">
                <div class="welcome-card-icon">🎨</div>
                <h3 class="welcome-card-title">{t("welcome.card_visual_title")}</h3>
                <p class="welcome-card-description">{t("welcome.card_visual_desc")}</p>
            </div>
        """, unsafe_allow_html=True)

    # Drugi rząd kart - 2 karty wycentrowane
    _, row2_col1, row2_col2, _ = st.columns([1, 2, 2, 1])

    with row2_col1:
        st.markdown(f"""
            <div class="welcome-card">
                <div class="welcome-card-icon">🎧</div>
                <h3 class="welcome-card-title">{t("welcome.card_reading_title")}</h3>
                <p class="welcome-card-description">{t("welcome.card_reading_desc")}</p>
            </div>
        """, unsafe_allow_html=True)

    with row2_col2:
        st.markdown(f"""
            <div class="welcome-card">
                <div class="welcome-card-icon">🎵</div>
                <h3 class="welcome-card-title">{t("welcome.card_music_title")}</h3>
                <p class="welcome-card-description">{t("welcome.card_music_desc")}</p>
            </div>
        """, unsafe_allow_html=True)

    spacer("3rem")

    # Wybór providera AI
    display_provider_selection()


def display_provider_selection():
    """
    Wyświetla interfejs wyboru providera AI na stronie powitalnej
    """
    st.markdown(f"""
        <div style="text-align: center; width: 100%;">
            <h2 style="margin-bottom: 2rem;">{t("welcome.choose_ai")}</h2>
        </div>
    """, unsafe_allow_html=True)

    # Cztery kolumny dla wyboru providera - wyśrodkowane w kolumnach 2 i 3
    col1, col2, col3, col4 = st.columns([1, 2, 2, 1])

    with col2:
        # Karta Groq
        st.markdown(f"""
            <div class="provider-card" style="
                border: 2px solid rgba(255, 255, 255, 0.15);
                border-radius: 15px;
                padding: 2rem;
                text-align: center;
                background: linear-gradient(135deg, #4A90E2 0%, #FF6B9C 100%);
                color: white;
                margin: 1rem 0;
                box-shadow: 0 8px 16px rgba(74, 144, 226, 0.15);
                transition: all 0.3s ease;
                cursor: pointer;
            ">
                <h3 style="color: white; margin-bottom: 1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); font-weight: 700;">🆓 Groq</h3>
                <ul style="text-align: left; color: white; margin-bottom: 1.5rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">
                    <li>✅ {t("welcome.groq_free")}</li>
                    <li>✅ {t("welcome.groq_fast")}</li>
                    <li>✅ {t("welcome.groq_model")}</li>
                    <li>⚠️ {t("welcome.groq_text_only")}</li>
                </ul>
            </div>

            <style>
            .provider-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 12px 24px rgba(74, 144, 226, 0.25);
                border: 2px solid rgba(255, 255, 255, 0.3);
            }}
            </style>
        """, unsafe_allow_html=True)

        if st.button(t("welcome.use_groq"), key="select_groq", use_container_width=True, type="primary"):
            # Sprawdź czy mamy klucz Groq w secrets
            if check_api_key("groq"):
                StateManager.set('app.selected_provider', "groq")
                st.rerun()
            else:
                st.error(t("welcome.no_groq_key"))

    with col3:
        # Karta OpenAI
        st.markdown(f"""
            <div class="provider-card" style="
                border: 2px solid rgba(255, 255, 255, 0.15);
                border-radius: 15px;
                padding: 2rem;
                text-align: center;
                background: linear-gradient(135deg, #FF6B9C 0%, #4A90E2 100%);
                color: white;
                margin: 1rem 0;
                box-shadow: 0 8px 16px rgba(255, 107, 156, 0.15);
                transition: all 0.3s ease;
                cursor: pointer;
            ">
                <h3 style="color: white; margin-bottom: 1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); font-weight: 700;">💎 OpenAI</h3>
                <ul style="text-align: left; color: white; margin-bottom: 1.5rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">
                    <li>✅ {t("welcome.openai_quality")}</li>
                    <li>✅ {t("welcome.openai_full")}</li>
                    <li>✅ {t("welcome.openai_all")}</li>
                    <li>💰 {t("welcome.openai_paid")}</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

        if st.button(t("welcome.use_openai"), key="select_openai", use_container_width=True):
            # Sprawdź czy mamy klucz OpenAI w secrets/env
            if check_api_key("openai"):
                StateManager.set('app.selected_provider', "openai")
                st.rerun()
            else:
                # Pokaż formularz do wprowadzenia klucza
                StateManager.set('app.show_openai_form', True)

    # Formularz dla OpenAI API key (jeśli potrzebny)
    if StateManager.get('app.show_openai_form', False):
        st.markdown("---")
        st.markdown(f"""
            <div style="text-align: center; width: 100%;">
                <h3>{t("welcome.enter_openai_key")}</h3>
            </div>
        """, unsafe_allow_html=True)

        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            with st.form("openai_api_key_form"):
                api_key = st.text_input(
                    t("welcome.openai_key_label"),
                    type="password",
                    placeholder="sk-...",
                    help=t("welcome.openai_key_help")
                )

                col_cancel, col_submit = st.columns(2)
                with col_cancel:
                    cancel_button = st.form_submit_button(t("welcome.cancel"), use_container_width=True)
                with col_submit:
                    submit_button = st.form_submit_button(t("welcome.confirm"), use_container_width=True, type="primary")

                if cancel_button:
                    StateManager.set('app.show_openai_form', False)
                    st.rerun()

                if submit_button and api_key:
                    # Waliduj klucz
                    StateManager.set('app.api_key', api_key)
                    if check_api_key("openai"):
                        StateManager.set('app.selected_provider', "openai")
                        StateManager.set('app.show_openai_form', False)
                        st.rerun()
                    else:
                        st.error(t("welcome.invalid_key"))


def display_sidebar_with_provider(provider_name):
    """
    Wyświetla sidebar z informacją o aktualnym providerze
    """
    # Wyświetl informacje o aktualnym providerze
    if provider_name == "groq":
        st.sidebar.success(t("welcome.using_groq"))
        st.sidebar.caption(t("welcome.groq_caption"))
    else:
        st.sidebar.success(t("welcome.using_openai"))
        st.sidebar.caption(t("welcome.openai_caption"))

    # Przycisk zmiany providera
    if st.sidebar.button(t("welcome.change_model"), use_container_width=True):
        StateManager.set('app.selected_provider', None)
        StateManager.set('app.show_openai_form', False)
        st.rerun()

    st.sidebar.markdown("---")

    # Reszta sidebara
    display_sidebar()
