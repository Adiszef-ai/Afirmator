"""
Moduł obsługujący dedykowaną zakładkę do czytania afirmacji.
"""
import streamlit as st
import base64
from config.constants import VOICE_OPTIONS
from ui.components import affirmation_card, centered_text, spacer

def display_audio_player_section(openai_service):
    """
    Wyświetla sekcję odtwarzacza afirmacji z zaawansowanymi opcjami audio.
    
    Args:
        openai_service (OpenAIService): Instancja serwisu OpenAI.
    """
    spacer("2.5rem")
    st.markdown("<h2 style='text-align: center;'> Czytanie Afirmacji</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align: center; width: 100%;">
            <h8> Dostosuj sposób czytania afirmacji do swoich potrzeb </h8>
        </div>
    """, unsafe_allow_html=True)    
    spacer("1.5rem")
    
    # Główna zawartość w kolumnach
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Wybór źródła tekstu
        centered_text("Wybór afirmacji")
        text_source = st.radio(
            "Źródło tekstu afirmacji:",
            ["Wybierz z historii", "Wpisz własny tekst"],
            horizontal=True,
            key="audio_player_text_source"
        )
        
        # Pobranie tekstu afirmacji
        if text_source == "Wybierz z historii":
            if st.session_state.history:
                selected_affirmation = st.selectbox(
                    "Wybierz afirmację:",
                    st.session_state.history,
                    format_func=lambda x: x[:100] + "..." if len(x) > 100 else x,
                    key="audio_player_affirmation_select"
                )
            else:
                st.warning("Historia jest pusta. Najpierw wygeneruj afirmację!")
                return
        else:
            selected_affirmation = st.text_area(
                "Wpisz własny tekst afirmacji:",
                height=100,
                placeholder="Wpisz swoją afirmację...",
                help="Wpisz afirmację, którą chcesz odsłuchać",
                key="audio_player_custom_text",
                max_chars=300
            )
            
            # Przycisk do akceptacji własnej afirmacji
            if st.button("Akceptuj afirmację", use_container_width=True, type="primary", key="audio_player_accept_btn"):
                if not selected_affirmation or len(selected_affirmation.strip()) == 0:
                    st.warning("Proszę wpisać tekst afirmacji!")
                    return
                # Wyświetlenie wybranej afirmacji w karcie
                centered_text("Wybrana afirmacja")
                affirmation_card(selected_affirmation)
                spacer("1rem")
        
        if not selected_affirmation:
            st.warning("Proszę wybrać lub wpisać afirmację do odtworzenia")
            return
        
        # Wyświetlenie wybranej afirmacji w karcie (dla wyboru z historii)
        if text_source == "Wybierz z historii":
            centered_text("Wybrana afirmacja")
            affirmation_card(selected_affirmation)
            spacer("1rem")
        
        # Ustawienia audio - podzielone na kolumny dla lepszego wyglądu
        centered_text("Ustawienia czytania")
        

        # Wybór głosu
        voice_label = st.selectbox(
            "Głos:",
            options=list(VOICE_OPTIONS.keys()),
            index=2,
            help="Wybierz głos, który najbardziej Ci odpowiada",
            key="audio_player_voice_select"
        )
        selected_voice = VOICE_OPTIONS[voice_label]
        

        # Prędkość mówienia - zmieniona domyślna prędkość na 0.8
        speed = st.slider(
            "Prędkość:",
            min_value=0.5,
            max_value=1.5,
            value=0.8,  # Domyślna prędkość 0.8
            step=0.05,
            help="Ustaw prędkość mówienia (0.5 = wolno, 1.0 = normalnie, 1.5 = szybko)",
            key="audio_player_speed_slider"
        )
        
        # Przycisk generowania
        if st.button("🎵 Generuj Audio", use_container_width=True, key="audio_player_generate_btn"):
            try:
                with st.spinner("Generuję audio z Twoją afirmacją..."):
                    audio_data = openai_service.generate_affirmation_audio(
                        selected_affirmation,
                        voice=selected_voice,
                        speed=speed
                    )
                    st.session_state.player_audio_data = audio_data
            except Exception as e:
                st.error(f"❌ Błąd podczas generowania audio: {str(e)}")
        
        # Wyświetlenie odtwarzacza audio jeśli wygenerowano audio
        if 'player_audio_data' in st.session_state and st.session_state.player_audio_data:
            st.markdown("---")
            st.markdown("""
                <div style="text-align: center; width: 100%;">
                    <h8> Twoja afirmacja audio: </h8>
                </div>
            """, unsafe_allow_html=True)
            spacer("2rem")  # Dodanie większego odstępu
            st.audio(st.session_state.player_audio_data, format="audio/mp3")
            
            # Link do pobrania
            b64 = base64.b64encode(st.session_state.player_audio_data).decode()
            filename = f"afirmacja_{voice_label.lower().replace(' ', '_')}_{speed}.mp3"
            download_href = f"""
                <div style="text-align: center; margin-top: 1rem;">
                    <a href="data:file/mp3;base64,{b64}" 
                       download="{filename}" 
                       class="download-button">
                        💾 Pobierz MP3
                    </a>
                </div>
            """
            st.markdown(download_href, unsafe_allow_html=True)
    
    # Wskazówki dotyczące używania afirmacji audio - poza kolumnami
    st.markdown("---")
    st.markdown("""
    <div style="padding: 15px; border-radius: 10px; margin-top: 20px;">
        <h5 style="margin: 0;">💡 Jak efektywnie używać afirmacji audio</h5>
        <ul style="text-align: left; margin-top: 0.2rem;">
            <li>Słuchaj swojej afirmacji audio każdego ranka, tuż po przebudzeniu</li>
            <li>Powtarzaj wraz z nagraniem, aby wzmocnić efekt</li>
            <li>Słuchaj ponownie wieczorem, przed snem</li>
            <li>Wolniejsze tempo pomaga w lepszym przyswajaniu treści</li>
            <li>Ustaw jako dzwonek/alarm w telefonie dla regularnego przypomnienia</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)