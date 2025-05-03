"""
Moduł obsługujący funkcjonalność generatora afirmacji.
"""
import streamlit as st
from config.constants import (
    AFFIRMATION_LENGTH_OPTIONS, 
    FOCUS_AREAS, 
    EMOTION_STATES, 
    AFFIRMATION_STYLES, 
    AFFIRMATION_TIMING, 
    AFFIRMATION_TONES, 
)
from services.openai_service import OpenAIService
from modules.utils import save_to_history
from ui.components import spacer

def display_generator_interface():
    """
    Wyświetla interfejs generatora afirmacji bez formularza.
    
    Returns:
        dict: Dane wprowadzone przez użytkownika.
    """
    spacer("2.5rem")
    st.markdown("<h2 style='text-align: center;'>Generator Afirmacji</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align: center; width: 100%;">
            <h8> Wypełnij poniższe pola, a AI stworzy dla Ciebie unikalną afirmację </h8>
        </div>
    """, unsafe_allow_html=True)
    spacer("1.5rem")
    # Pola bez formularza
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        user_name = st.text_input("Twoje imię:", key="generator_user_name", max_chars=30)
        focus_area = st.selectbox("Nad czym chcesz popracować?", FOCUS_AREAS, key="generator_focus_area")
        
        # Pokazuj pole "Wprowadź swój cel" tylko jeśli wybrano "Własne cele"
        specific_goal = ""
        if focus_area == "✨ Własne cele ✨":
            specific_goal = st.text_area("Wprowadź swój cel:", key="generator_specific_goal", max_chars=250, 
                                        placeholder="Np. Chcę nauczyć się medytować codziennie przez 10 minut i być bardziej świadomym swoich myśli.")
        
        emotion_state = st.selectbox("Jak się obecnie czujesz w tej kwestii?", EMOTION_STATES, key="generator_emotion_state")
        preferred_style = st.selectbox("Preferowany styl afirmacji:", AFFIRMATION_STYLES, key="generator_preferred_style")
        affirmation_length = st.selectbox("Jak długą afirmację preferujesz?", AFFIRMATION_LENGTH_OPTIONS, key="generator_affirmation_length")
        affirmation_timing = st.selectbox("Kiedy chcesz stosować afirmację?", AFFIRMATION_TIMING, key="generator_affirmation_timing")
        affirmation_tone = st.selectbox("Jaki ton powinna mieć afirmacja?", AFFIRMATION_TONES, key="generator_affirmation_tone")
    
        # Przycisk generowania
        if st.button("Stwórz afirmację", use_container_width=True, key="generator_submit"):
            if not user_name:
                st.warning("Proszę wprowadzić swoje imię!")
                return None
            
            if focus_area == "Własne cele" and not specific_goal:
                st.warning("Proszę wprowadzić swój cel!")
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

def generate_affirmation(form_data, openai_service):
    """
    Generuje afirmację na podstawie danych z formularza.
    
    Args:
        form_data (dict): Dane z formularza.
        openai_service (OpenAIService): Instancja serwisu OpenAI.
        
    Returns:
        str: Wygenerowana afirmacja lub None w przypadku błędu.
    """
    target_focus = form_data["specific_goal"] if form_data["focus_area"] == "Własne cele" else form_data["focus_area"]
    
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
    
    try:
        with st.spinner("🧠 AI tworzy Twoją unikalną afirmację..."):
            affirmation = openai_service.generate_affirmation(prompt)
            st.session_state.update({
                'affirmation': affirmation,
                'edited_affirmation': affirmation,
                'audio_data': None,
                'user_name': form_data["user_name"]  # Store user name in session state
            })
            save_to_history(affirmation)
            return affirmation
    except Exception as e:
        st.error(f"Błąd podczas generowania afirmacji: {str(e)}")
        return None

def display_affirmation_result(openai_service):
    """
    Wyświetla wynik wygenerowanej afirmacji i opcje edycji.
    
    Args:
        openai_service (OpenAIService): Instancja serwisu OpenAI.
    """
    if not st.session_state.affirmation:
        return

    st.markdown("---")
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("""
            <div style="text-align: center; width: 100%;">
                <h8> Twoja spersonalizowana afirmacja:</h8>
            </div>
        """, unsafe_allow_html=True)
        
        # Obsługa trybu edycji
        if st.session_state.editing:
            _display_affirmation_edit_mode()
        else:
            _display_affirmation_view_mode()
    
    st.markdown("---")

    # Wskazówki
    _display_affirmation_tips()

def _display_affirmation_edit_mode():
    """Wyświetla interfejs edycji afirmacji."""
    st.session_state.edited_affirmation = st.text_area(
        "Edytuj afirmację:",
        value=st.session_state.edited_affirmation,
        height=150,
        key="edit_affirmation_text"
    )
    if st.button("Zapisz zmiany", use_container_width=True, key="save_affirmation_changes"):
        st.session_state.editing = False
        st.session_state.audio_data = None
        # Dodanie edytowanej afirmacji do historii
        save_to_history(st.session_state.edited_affirmation)
        st.rerun()

def _display_affirmation_view_mode():
    """Wyświetla afirmację w trybie podglądu."""
    st.markdown(
        f"""
        <div class="affirmation-card" style="
            text-align: center;
            font-size: 18px;
        ">
            {st.session_state.edited_affirmation}
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Przyciski akcji w trzech równych kolumnach, jak w module daily
    col_a, col_b, col_c = st.columns([1, 1, 1])
    
    with col_a:
        if st.button("Edytuj", use_container_width=True, key="edit_affirmation_button"):
            st.session_state.editing = True
            st.rerun()
    
    with col_b:
        if st.button("Nowa afirmacja", use_container_width=True, key="new_generator_affirmation"):
            # Resetujemy stan edycji, ale zachowujemy dane użytkownika aby pokazać ponownie formularz
            st.session_state.affirmation = None
            st.session_state.edited_affirmation = None
            st.session_state.editing = False
            st.rerun()
    
    with col_c:
        if st.button("Skopiuj", use_container_width=True, key="copy_generator_affirmation"):
            st.toast("✅ Skopiowano do schowka!", icon='✨')

def _display_affirmation_tips():
    """Wyświetla wskazówki dotyczące stosowania afirmacji."""
    st.markdown("""
    <div style="padding: 15px; border-radius: 10px; margin-top: 20px;">
        <h5 style="margin-top: 0.2;">💡 Jak stosować afirmacje:</h5>
        <ul>
            <li>Powtarzaj afirmację co najmniej 3 razy dziennie</li>
            <li>Najlepiej działają wypowiadane na głos i z przekonaniem</li>
            <li>Możesz słuchać nagrania podczas medytacji lub relaksu</li>
            <li>Dla najlepszych rezultatów, stosuj przez minimum 21 dni</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)