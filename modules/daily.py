"""
Moduł obsługujący funkcjonalność afirmacji dnia - wersja ulepszona.
"""
import random
import streamlit as st
from config.constants import DAILY_AFFIRMATION_TOPICS
from services.openai_service import OpenAIService
from ui.components import affirmation_card, spacer
from modules.utils import save_to_history

def generate_daily_affirmation(client, user_name):
    """
    Generuje afirmację dnia dla użytkownika.
    
    Args:
        client (OpenAIService): Instancja klienta OpenAI.
        user_name (str): Imię użytkownika.
        
    Returns:
        str: Wygenerowana afirmacja dnia lub None w przypadku braku imienia.
    """
    if not user_name:
        return None
        
    # Losowy wybór tematu afirmacji dnia
    daily_topic = random.choice(DAILY_AFFIRMATION_TOPICS)
    
    # Tworzenie promptu dla afirmacji dnia
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
    
    try:
        return client.generate_affirmation(prompt, max_tokens=120)
    except Exception as e:
        return f"Błąd podczas generowania afirmacji dnia: {str(e)}"

def display_daily_affirmation_section(openai_service):
    """
    Wyświetla sekcję afirmacji dnia z ulepszonym UI.
    
    Args:
        openai_service (OpenAIService): Instancja serwisu OpenAI.
    """
    spacer("2.5rem")
    st.markdown("<h2 style='text-align: center;'>Afirmacja Dnia</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align: center; width: 100%;">
            <h8> Rozpocznij swój dzień z pozytywną afirmacją </h8>
        </div>
    """, unsafe_allow_html=True)
    spacer("1.5rem")
    
    # Inicjalizacja zmiennych stanu dla edycji
    if 'editing' not in st.session_state:
        st.session_state.editing = False
    if 'edited_affirmation' not in st.session_state and 'daily_affirmation' in st.session_state:
        st.session_state.edited_affirmation = st.session_state.daily_affirmation
    
    # Sprawdzamy czy afirmacja już istnieje w session_state
    if 'daily_affirmation' not in st.session_state or st.session_state.daily_affirmation is None:
        _display_daily_affirmation_input(openai_service)
    else:
        _display_daily_affirmation_content(openai_service)
        
        # Wskazówki dotyczące używania afirmacji dnia - tylko gdy afirmacja jest wygenerowana
        st.markdown("---")
        st.markdown("""
            <div style="padding: 15px; border-radius: 10px; margin-top: 20px;">
                <h5 style="margin: 0;">💡 Jak używać afirmacji dnia</h5>
                <ul style="text-align: left; margin-top: 0.2rem;">
                    <li>Powtarzaj tę afirmację każdego ranka, aby rozpocząć dzień z pozytywnym nastawieniem</li>
                    <li>Możesz ją wypowiadać na głos lub zapisać w dzienniku</li>
                    <li>Wizualizuj efekty afirmacji podczas jej wypowiadania</li>
                    <li>Używaj afirmacji dnia jako intencji przewodniej na cały dzień</li>
                    <li>Wieczorem zastanów się, jak afirmacja wpłynęła na Twój dzień</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

def _display_daily_affirmation_input(openai_service):
    """
    Wyświetla formularz wprowadzania imienia dla afirmacji dnia.
    
    Args:
        openai_service (OpenAIService): Instancja serwisu OpenAI.
    """
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        name_input = st.text_input(
            "Twoje imię", 
            key="daily_name_input", 
            placeholder="Wpisz tutaj...",
            max_chars=30,
            help="Podaj swoje imię, aby otrzymać spersonalizowaną afirmację"
        )
        
        if st.button("Pokaż afirmację dnia", key="show_daily_affirmation", use_container_width=True):
            if name_input:
                with st.spinner("🌟 Tworzę Twoją afirmację dnia..."):
                    daily_affirmation = generate_daily_affirmation(openai_service, name_input)
                    st.session_state.daily_affirmation_name = name_input
                    st.session_state.daily_affirmation = daily_affirmation
                    st.session_state.edited_affirmation = daily_affirmation
                    # Zapisywanie afirmacji dnia do historii
                    save_to_history(daily_affirmation)
                    st.rerun()
            else:
                st.warning("Proszę wprowadzić swoje imię!")

def _display_daily_affirmation_content(openai_service):
    """
    Wyświetla wygenerowaną afirmację dnia i opcje audio.
    
    Args:
        openai_service (OpenAIService): Instancja serwisu OpenAI.
    """
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Obsługa trybu edycji
        if st.session_state.editing:
            st.session_state.edited_affirmation = st.text_area(
                "Edytuj afirmację:",
                value=st.session_state.edited_affirmation,
                height=150,
                key="edit_daily_affirmation_text"
            )
            if st.button("Zapisz zmiany", use_container_width=True, key="save_daily_affirmation_changes"):
                st.session_state.editing = False
                st.session_state.daily_affirmation = st.session_state.edited_affirmation
                # Dodanie edytowanej afirmacji do historii
                save_to_history(st.session_state.edited_affirmation)
                st.rerun()
        else:
            # Wyświetlenie afirmacji w eleganckiej karcie
            affirmation_card(st.session_state.edited_affirmation)
            
            # Przyciski akcji
            col_a, col_b, col_c = st.columns([1, 1, 1])
            
            with col_a:
                if st.button("Edytuj", use_container_width=True, key="edit_daily_affirmation"):
                    st.session_state.editing = True
                    st.rerun()
            
            with col_b:
                if st.button("Nowa afirmacja", key="new_daily_affirmation", use_container_width=True):
                    with st.spinner("🌟 Generuję nową afirmację dnia..."):
                        daily_affirmation = generate_daily_affirmation(openai_service, st.session_state.daily_affirmation_name)
                        st.session_state.daily_affirmation = daily_affirmation
                        st.session_state.edited_affirmation = daily_affirmation
                        # Zapisywanie nowej afirmacji dnia do historii
                        save_to_history(daily_affirmation)
                        st.rerun()
            
            with col_c:
                if st.button("Skopiuj", key="copy_affirmation", use_container_width=True):
                    st.toast("✅ Skopiowano do schowka!", icon='✨')