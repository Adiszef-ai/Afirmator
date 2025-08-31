"""
app/modules/musical_affirmation.py - Moduł obsługujący funkcję Muzycznej Afirmacji - łączenie afirmacji z podkładem muzycznym.
"""
import streamlit as st
import base64
import os
import tempfile
from pydub import AudioSegment
from config.constants import VOICE_OPTIONS, BACKGROUND_SOUNDS
from ui.components import affirmation_card, centered_text, spacer

def display_musical_affirmation_section(openai_service):
    """
    Wyświetla sekcję muzycznej afirmacji - afirmacje z podkładem muzycznym.
    
    Args:
        openai_service (OpenAIService): Instancja serwisu OpenAI.
    """
    spacer("2.5rem")
    st.markdown("<h2 style='text-align: center;'>Muzyczna Afirmacja</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align: center; width: 100%;">
            <h8> Połącz swoją afirmację z relaksującym podkładem muzycznym </h8>
        </div>
    """, unsafe_allow_html=True)
    spacer("1.5rem")
    
    centered_text("Wybór afirmacji")
    # Główna zawartość w kolumnach
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Wybór źródła tekstu
        text_source = st.radio(
            "Źródło tekstu afirmacji:",
            ["Wybierz z historii", "Wpisz własny tekst"],
            horizontal=True,
            key="music_aff_text_source"
        )
        
        # Pobranie tekstu afirmacji
        if text_source == "Wybierz z historii":
            if st.session_state.history:
                selected_affirmation = st.selectbox(
                    "Wybierz afirmację:",
                    st.session_state.history,
                    format_func=lambda x: x[:100] + "..." if len(x) > 100 else x,
                    key="music_aff_select"
                )
            else:
                st.warning("Historia jest pusta. Najpierw wygeneruj afirmację!")
                return
        else:
            selected_affirmation = st.text_area(
                "Wpisz własny tekst afirmacji:",
                height=100,
                placeholder="Wpisz swoją afirmację...",
                help="Wpisz afirmację, którą chcesz połączyć z muzyką",
                key="music_aff_custom_text",
                max_chars=300
            )
            
            # Przycisk do akceptacji własnej afirmacji
            if st.button("Akceptuj afirmację", use_container_width=True, type="primary", key="music_aff_accept_btn"):
                if not selected_affirmation or len(selected_affirmation.strip()) == 0:
                    st.warning("Proszę wpisać tekst afirmacji!")
                    return
                # Wyświetlenie wybranej afirmacji w karcie
                centered_text("Wybrana afirmacja")
                affirmation_card(selected_affirmation)
                spacer("1rem")
        
        if not selected_affirmation:
            st.warning("Proszę wybrać lub wpisać afirmację")
            return
        
        # Wyświetlenie wybranej afirmacji w karcie (dla wyboru z historii)
        if text_source == "Wybierz z historii":
            centered_text("Wybrana afirmacja")
            affirmation_card(selected_affirmation)
            spacer("1rem")
        
        # Panel ustawień muzycznych
        centered_text("Ustawienia audio")
        

        # Wybór głosu
        voice_label = st.selectbox(
            "Głos narracji:",
            options=list(VOICE_OPTIONS.keys()),
            index=2,
            help="Wybierz głos, który najbardziej Ci odpowiada",
            key="music_aff_voice_select"
        )
        selected_voice = VOICE_OPTIONS[voice_label]
        
        # Prędkość mówienia
        speed = st.slider(
            "Prędkość mówienia:",
            min_value=0.5,
            max_value=1.5,
            value=0.8,
            step=0.05,
            help="Ustaw prędkość mówienia (0.5 = wolno, 1.0 = normalnie, 1.5 = szybko)",
            key="music_aff_speed_slider"
        )
    
        # Liczba powtórzeń
        repetitions = st.slider(
            "Liczba powtórzeń afirmacji:",
            min_value=1,
            max_value=10,
            value=3,
            step=1,
            help="Ile razy afirmacja ma być powtórzona w nagraniu",
            key="music_aff_repetitions"
        )
        
        # Przerwy między powtórzeniami
        pause_between = st.slider(
            "Przerwa między powtórzeniami (sek.):",
            min_value=1,
            max_value=10,
            value=3,
            step=1,
            help="Czas ciszy między powtórzeniami afirmacji",
            key="music_aff_pause"
        )
        
        # Wybór podkładu muzycznego
        centered_text("Podkład muzyczny")
        
        sound_source = st.radio(
            "Źródło podkładu:",
            ["Wybierz predefiniowany", "Wgraj własny"],
            horizontal=True,
            key="music_aff_sound_source"
        )
        
        background_file = None
        selected_background = None
        
        if sound_source == "Wybierz predefiniowany":
            selected_background = st.selectbox(
                "Wybierz podkład:",
                options=list(BACKGROUND_SOUNDS.keys()),
                help="Wybierz dźwięk tła dla swojej afirmacji",
                key="music_aff_bg_select"
            )
        else:
            background_file = st.file_uploader(
                "Wgraj własny podkład muzyczny (MP3, WAV):",
                type=["mp3", "wav"],
                help="Maksymalny rozmiar 5MB",
                key="music_aff_bg_upload"
            )
        
        # Głośność podkładu
        background_volume = st.slider(
            "Głośność podkładu:",
            min_value=10,
            max_value=100,
            value=40,
            step=5,
            help="Ustaw głośność podkładu muzycznego jako procent głośności afirmacji",
            key="music_aff_bg_volume"
        )
        
        # Przycisk generowania
        if st.button("🎵 Wygeneruj muzyczną afirmację", use_container_width=True, key="music_aff_generate_btn"):
            try:
                with st.spinner("Generuję muzyczną afirmację..."):
                    # 1. Generowanie audio afirmacji
                    affirmation_audio = openai_service.generate_affirmation_audio(
                        selected_affirmation,
                        voice=selected_voice,
                        speed=speed
                    )
                    
                    # 2. Tworzenie zmiksowanego audio
                    if background_file or selected_background:
                        # Zapisywanie afirmacji do pliku tymczasowego
                        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_affirmation:
                            temp_affirmation.write(affirmation_audio)
                            temp_affirmation_path = temp_affirmation.name
                        
                        # Pobieranie ścieżki podkładu
                        background_path = ""
                        if background_file:
                            # Dla wgranego pliku
                            with tempfile.NamedTemporaryFile(suffix="." + background_file.name.split(".")[-1], delete=False) as temp_bg:
                                temp_bg.write(background_file.getbuffer())
                                background_path = temp_bg.name
                        else:
                            # Dla predefiniowanego dźwięku
                            background_path = BACKGROUND_SOUNDS[selected_background]
                        
                        # Miksuję audio
                        mixed_audio_data = mix_audio(
                            temp_affirmation_path, 
                            background_path, 
                            repetitions, 
                            pause_between,
                            background_volume / 100.0
                        )
                        
                        # Usuwanie plików tymczasowych
                        if os.path.exists(temp_affirmation_path):
                            os.unlink(temp_affirmation_path)
                        
                        # Jeśli był wgrany plik, usuń również tymczasowy plik podkładu
                        if background_file and os.path.exists(background_path):
                            os.unlink(background_path)
                        
                        # Zapisuję zmiksowane audio w sesji
                        st.session_state.music_affirmation_audio = mixed_audio_data
                        st.success("✅ Muzyczna afirmacja wygenerowana!")
                    else:
                        st.error("Proszę wybrać podkład muzyczny")
            except Exception as e:
                st.error(f"❌ Błąd podczas generowania muzycznej afirmacji: {str(e)}")
        
        # Wyświetlenie odtwarzacza audio jeśli wygenerowano audio
        if 'music_affirmation_audio' in st.session_state and st.session_state.music_affirmation_audio:
            st.markdown("---")    
            st.markdown("""
                <div style="text-align: center; width: 100%;">
                    <h8> Twoja muzyczna afirmacja: </h8>
                </div>
            """, unsafe_allow_html=True)
            spacer("2rem")  # Dodanie większego odstępu
            st.audio(st.session_state.music_affirmation_audio, format="audio/mp3")
            
            # Link do pobrania
            b64 = base64.b64encode(st.session_state.music_affirmation_audio).decode()
            bg_name = selected_background if selected_background else "custom"
            filename = f"muzyczna_afirmacja_{bg_name}_{repetitions}x.mp3"
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
    
    # Wskazówki na zewnątrz kolumn
    spacer("1.5rem")
    st.markdown("""
    <div style="padding: 15px; border-radius: 10px; margin-top: 20px;">
        <h5 style="margin-top: 0.0;">💡 Jak korzystać z muzycznych afirmacji</h5>
        <ul style="text-align: left; margin-top: 0.2rem;">
            <li>Słuchaj przed snem, aby wpłynąć na podświadomość</li>
            <li>Użyj podczas medytacji rano, aby ustawić pozytywną intencję na dzień</li>
            <li>Stosuj jako tło podczas jogi lub ćwiczeń relaksacyjnych</li>
            <li>Słuchaj w słuchawkach w spokojnym miejscu dla najlepszych efektów</li>
            <li>Regularne słuchanie wzmacnia efekt afirmacji</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


def mix_audio(affirmation_path, background_path, repetitions, pause_seconds, background_volume_ratio):
    """
    Miksuję afirmację z podkładem muzycznym.
    
    Args:
        affirmation_path (str): Ścieżka do pliku z afirmacją.
        background_path (str): Ścieżka do pliku z podkładem.
        repetitions (int): Liczba powtórzeń afirmacji.
        pause_seconds (int): Długość pauzy między powtórzeniami w sekundach.
        background_volume_ratio (float): Współczynnik głośności tła (0.0-1.0).
        
    Returns:
        bytes: Zmiksowane audio jako dane binarne.
    """
    try:
        # Sprawdzenie czy pliki istnieją
        if not os.path.exists(affirmation_path):
            raise Exception(f"Plik afirmacji nie istnieje: {affirmation_path}")
        if not os.path.exists(background_path):
            raise Exception(f"Plik podkładu nie istnieje: {background_path}")
            
        # Wczytanie plików audio
        affirmation_audio = AudioSegment.from_file(affirmation_path)
        background_audio = AudioSegment.from_file(background_path)
        
        # Dostosowanie głośności podkładu (jako procent głośności afirmacji)
        background_audio = background_audio - (20 * (1 - background_volume_ratio))  # -20dB = 10% głośności
        
        # Tworzenie pauzy
        pause = AudioSegment.silent(duration=pause_seconds * 1000)  # w milisekundach
        
        # Tworzenie opóźnienia początkowego (2 sekundy)
        initial_delay = AudioSegment.silent(duration=2000)  # 2 sekundy w milisekundach
        
        # Tworzenie powtórzonej afirmacji z pauzami
        repeated_affirmation = AudioSegment.empty()
        # Dodanie początkowego opóźnienia
        repeated_affirmation += initial_delay
        
        for i in range(repetitions):
            repeated_affirmation += affirmation_audio
            if i < repetitions - 1:  # Dodaj pauzę po wszystkich oprócz ostatniego
                repeated_affirmation += pause
        
        # Dodanie 2 sekund na końcu dla wyciszającego się podkładu
        final_delay = AudioSegment.silent(duration=2000)  # 2 sekundy w milisekundach
        repeated_affirmation += final_delay
        
        # Sprawdzenie długości audio
        affirmation_length = len(repeated_affirmation)
        background_length = len(background_audio)
        
        # Jeśli podkład jest za krótki, zapętl go
        if background_length < affirmation_length:
            # Ile razy trzeba powtórzyć podkład
            repeats = (affirmation_length // background_length) + 1
            extended_background = background_audio * repeats
            # Przytnij do długości afirmacji
            background_audio = extended_background[:affirmation_length]
        else:
            # Przytnij podkład do długości afirmacji
            background_audio = background_audio[:affirmation_length]
        
        # Stworzenie efektu wyciszania (fade out) na końcowych 2 sekundach podkładu
        fade_duration = 2000  # 2 sekundy w milisekundach
        background_audio = background_audio.fade_out(duration=fade_duration)
        
        # Miksowanie afirmacji z podkładem
        mixed_audio = repeated_affirmation.overlay(background_audio)
        
        # Tworzenie pliku tymczasowego z pełną ścieżką
        temp_dir = tempfile.gettempdir()
        temp_output_path = os.path.join(temp_dir, "mixed_audio.mp3")
        
        # Eksport do pliku tymczasowego
        mixed_audio.export(temp_output_path, format="mp3")
        
        # Odczytanie danych binarnych
        with open(temp_output_path, "rb") as f:
            audio_data = f.read()
        
        # Usunięcie pliku tymczasowego
        if os.path.exists(temp_output_path):
            os.unlink(temp_output_path)
        
        return audio_data
    
    except Exception as e:
        # W razie błędu, usuń pliki tymczasowe
        if 'temp_output_path' in locals() and os.path.exists(temp_output_path):
            os.unlink(temp_output_path)
        raise Exception(f"Błąd podczas miksowania audio: {str(e)}")