"""
modules/core/welcome.py - Moduł obsługujący stronę powitalną aplikacji
"""
import streamlit as st
from config.utils import check_api_key
from ui.sidebar import display_sidebar
from ui.components import spacer


def welcome_screen():
    """
    Wyświetla ekran powitalny dla nowych użytkowników.
    """
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="font-size: 3.5rem; margin-bottom: 1rem;">
                Witaj w Afirmatorze
            </h1>
            <h8 style=>
                Twój osobisty generator pozytywnych afirmacji wspomaganych przez AI
            </h8>
        </div>
    """, unsafe_allow_html=True)
    
    # Karty z funkcjami w górnym rzędzie - 3 karty
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    
    with row1_col1:
        st.markdown("""
            <div class="welcome-card">
                <div class="welcome-card-icon">🌅</div>
                <h3 class="welcome-card-title">Afirmacja dnia</h3>
                <p class="welcome-card-description">Codzienna dawka pozytywnej energii</p>
            </div>
        """, unsafe_allow_html=True)
    
    with row1_col2:
        st.markdown("""
            <div class="welcome-card">
                <div class="welcome-card-icon">🛠️</div>
                <h3 class="welcome-card-title">Generator Afirmacji</h3>
                <p class="welcome-card-description">Spersonalizuj swoją afirmacje</p>
            </div>
        """, unsafe_allow_html=True)
    
    with row1_col3:
        st.markdown("""
            <div class="welcome-card">
                <div class="welcome-card-icon">🎨</div>
                <h3 class="welcome-card-title">Wizualny cytat</h3>
                <p class="welcome-card-description">Twórz obrazy z afirmacjami</p>
            </div>
        """, unsafe_allow_html=True)
        
    # Drugi rząd kart - 2 karty wycentrowane
    _, row2_col1, row2_col2, _ = st.columns([1, 2, 2, 1])
    
    with row2_col1:
        st.markdown("""
            <div class="welcome-card">
                <div class="welcome-card-icon">🎧</div>
                <h3 class="welcome-card-title">Czytanie afirmacji</h3>
                <p class="welcome-card-description">Kontroluj prędkość czytania</p>
            </div>
        """, unsafe_allow_html=True)
        
    with row2_col2:
        st.markdown("""
            <div class="welcome-card">
                <div class="welcome-card-icon">🎵</div>
                <h3 class="welcome-card-title">Muzyczna afirmacja</h3>
                <p class="welcome-card-description">Afirmacje z podkładem muzycznym</p>
            </div>
        """, unsafe_allow_html=True)
    
    spacer("3rem")
    
    # Wybór providera AI
    display_provider_selection()


def display_provider_selection():
    """
    Wyświetla interfejs wyboru providera AI na stronie powitalnej
    """
    st.markdown("""
        <div style="text-align: center; width: 100%;">
            <h2 style="margin-bottom: 2rem;">Wybierz model AI</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Cztery kolumny dla wyboru providera - wyśrodkowane w kolumnach 2 i 3
    col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
    
    with col2:
        # Karta Groq
        st.markdown("""
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
                    <li>✅ Całkowicie darmowy</li>
                    <li>✅ Bardzo szybki</li>
                    <li>✅ Model LLaMA</li>
                    <li>⚠️ Tylko tekst (bez audio)</li>
                </ul>
            </div>
            
            <style>
            .provider-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 12px 24px rgba(74, 144, 226, 0.25);
                border: 2px solid rgba(255, 255, 255, 0.3);
            }
            </style>
        """, unsafe_allow_html=True)
        
        if st.button("Użyj Groq", key="select_groq", use_container_width=True, type="primary"):
            # Sprawdź czy mamy klucz Groq w secrets
            if check_api_key("groq"):
                st.session_state.selected_provider = "groq"
                st.rerun()
            else:
                st.error("Brak klucza Groq w konfiguracji. Dodaj klucz do secrets.toml lub zmiennych środowiskowych.")
    
    with col3:
        # Karta OpenAI
        st.markdown("""
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
                    <li>✅ Najwyższa jakość</li>
                    <li>✅ Pełne funkcje</li>
                    <li>✅ Tekst + Audio + Muzyka</li>
                    <li>💰 Wymaga klucza API</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Użyj OpenAI", key="select_openai", use_container_width=True):
            # Sprawdź czy mamy klucz OpenAI w secrets/env
            if check_api_key("openai"):
                st.session_state.selected_provider = "openai"
                st.rerun()
            else:
                # Pokaż formularz do wprowadzenia klucza
                st.session_state.show_openai_form = True
    
    # Formularz dla OpenAI API key (jeśli potrzebny)
    if st.session_state.get('show_openai_form', False):
        st.markdown("---")
        st.markdown("""
            <div style="text-align: center; width: 100%;">
                <h3>Wprowadź klucz API OpenAI</h3>
            </div>
        """, unsafe_allow_html=True)
        
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            with st.form("openai_api_key_form"):
                api_key = st.text_input(
                    "Klucz API OpenAI",
                    type="password",
                    placeholder="sk-...",
                    help="Możesz uzyskać klucz API na https://platform.openai.com/account/api-keys"
                )
                
                col_cancel, col_submit = st.columns(2)
                with col_cancel:
                    cancel_button = st.form_submit_button("Anuluj", use_container_width=True)
                with col_submit:
                    submit_button = st.form_submit_button("Zatwierdź", use_container_width=True, type="primary")
                
                if cancel_button:
                    st.session_state.show_openai_form = False
                    st.rerun()
                
                if submit_button and api_key:
                    # Waliduj klucz
                    st.session_state.api_key = api_key
                    if check_api_key("openai"):
                        st.session_state.selected_provider = "openai"
                        st.session_state.show_openai_form = False
                        st.rerun()
                    else:
                        st.error("Nieprawidłowy klucz API. Sprawdź format.")


def display_sidebar_with_provider(provider_name):
    """
    Wyświetla sidebar z informacją o aktualnym providerze
    """
    # Wyświetl informacje o aktualnym providerze
    if provider_name == "groq":
        st.sidebar.success("🆓 Używasz: **Groq (Darmowy)**")
        st.sidebar.caption("✨ Szybkie generowanie tekstu")
    else:
        st.sidebar.success("💎 Używasz: **OpenAI (Premium)**") 
        st.sidebar.caption("✨ Pełne funkcje - tekst + audio")
    
    # Przycisk zmiany providera
    if st.sidebar.button("🔄 Zmień model AI", use_container_width=True):
        st.session_state.selected_provider = None
        st.session_state.show_openai_form = False
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Reszta sidebara
    display_sidebar()