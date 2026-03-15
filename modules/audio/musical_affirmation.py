"""
app/modules/musical_affirmation.py - Moduł obsługujący funkcję Muzycznej Afirmacji - łączenie afirmacji z podkładem muzycznym.
"""
import streamlit as st
import base64
import os
import tempfile
from pydub import AudioSegment
from config.constants import get_voice_options, get_background_sounds
from config.translations import t
from components.affirmation_selector import render_affirmation_selector, render_voice_settings
from components.audio_player import render_audio_player, generate_audio_with_spinner, render_audio_tips
from ui.components import render_section_header, render_centered_column_layout, centered_text
from utils.session_state import StateManager

def display_musical_affirmation_section(openai_service):
    """
    Wyświetla sekcję muzycznej afirmacji - afirmacje z podkładem muzycznym.

    Args:
        openai_service (OpenAIService): Instancja serwisu OpenAI.
    """
    render_section_header(
        t("music.title"),
        t("music.subtitle")
    )

    def render_content():
        BACKGROUND_SOUNDS = get_background_sounds()

        # Use reusable affirmation selector
        selected_affirmation = render_affirmation_selector("music_aff")
        if not selected_affirmation:
            return

        # Use reusable voice settings
        voice_settings = render_voice_settings("music_aff")

        # Liczba powtórzeń
        repetitions = st.slider(
            t("music.repetitions"),
            min_value=1,
            max_value=10,
            value=3,
            step=1,
            help=t("music.repetitions_help"),
            key="music_aff_repetitions"
        )

        # Przerwy między powtórzeniami
        pause_between = st.slider(
            t("music.pause"),
            min_value=1,
            max_value=10,
            value=3,
            step=1,
            help=t("music.pause_help"),
            key="music_aff_pause"
        )

        # Wybór podkładu muzycznego
        centered_text(t("music.background_title"))

        sound_source = st.radio(
            t("music.source"),
            [t("music.predefined"), t("music.upload")],
            horizontal=True,
            key="music_aff_sound_source"
        )

        background_file = None
        selected_background = None

        if sound_source == t("music.predefined"):
            selected_background = st.selectbox(
                t("music.select_background"),
                options=list(BACKGROUND_SOUNDS.keys()),
                help=t("music.select_background_help"),
                key="music_aff_bg_select"
            )
        else:
            background_file = st.file_uploader(
                t("music.upload_label"),
                type=["mp3", "wav"],
                help=t("music.upload_help"),
                key="music_aff_bg_upload"
            )

        # Głośność podkładu
        background_volume = st.slider(
            t("music.volume"),
            min_value=10,
            max_value=100,
            value=40,
            step=5,
            help=t("music.volume_help"),
            key="music_aff_bg_volume"
        )

        # Przycisk generowania
        if st.button(t("music.generate"), use_container_width=True, key="music_aff_generate_btn"):
            try:
                # Import funkcji progress bara
                from ui.components import progress_bar_context, update_progress, toast_notification

                # Tworzenie progress bara
                progress_bar, status_text = progress_bar_context(
                    [t("progress.steps.audio"), t("progress.steps.background"), t("progress.steps.mixing"), t("progress.steps.finalizing")]
                )

                # Krok 1: Generowanie audio afirmacji
                update_progress(progress_bar, status_text, 1, 4, t("music.step_audio"))
                affirmation_audio = openai_service.generate_affirmation_audio(
                    selected_affirmation,
                    voice=voice_settings['voice'],
                    speed=voice_settings['speed']
                )

                # Krok 2: Przetwarzanie podkładu
                if background_file or selected_background:
                    update_progress(progress_bar, status_text, 2, 4, t("music.step_background"))

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

                    # Krok 3: Miksowanie
                    update_progress(progress_bar, status_text, 3, 4, t("music.step_mixing"))
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

                    # Krok 4: Finalizacja
                    update_progress(progress_bar, status_text, 4, 4, t("music.step_finalizing"))
                    StateManager.set('audio.music_affirmation', mixed_audio_data)

                    # Czyszczenie progress bara
                    progress_bar.empty()
                    status_text.empty()

                    # Toast notification
                    toast_notification(t("music.ready"), "🎵")
                else:
                    # Przypadek bez podkładu - tylko afirmacja
                    update_progress(progress_bar, status_text, 2, 4, t("music.step_skip_bg"))
                    update_progress(progress_bar, status_text, 3, 4, t("music.step_skip_mix"))
                    update_progress(progress_bar, status_text, 4, 4, t("music.step_finalizing"))

                    StateManager.set('audio.music_affirmation', affirmation_audio)

                    # Czyszczenie progress bara
                    progress_bar.empty()
                    status_text.empty()

                    # Toast notification
                    toast_notification(t("music.ready_no_bg"), "🎙️")
            except Exception as e:
                st.error(f"{t('music.error')}{str(e)}")

        # Wyświetlenie odtwarzacza audio jeśli wygenerowano audio
        if StateManager.has_key('audio.music_affirmation') and StateManager.get('audio.music_affirmation'):
            bg_name = selected_background if selected_background else "custom"
            filename_base = f"muzyczna_afirmacja_{bg_name}_{repetitions}x"

            # Use custom header for musical affirmation
            st.markdown("---")
            st.markdown(f"""
                <div style="text-align: center; width: 100%;">
                    <h8> {t("music.your_music")} </h8>
                </div>
            """, unsafe_allow_html=True)
            from ui.components import spacer
            spacer("2rem")
            st.audio(StateManager.get('audio.music_affirmation'), format="audio/mp3")

            # Custom download link for musical affirmation
            b64 = base64.b64encode(StateManager.get('audio.music_affirmation')).decode()
            filename = f"{filename_base}.mp3"
            download_href = f"""
                <div style="text-align: center; margin-top: 1rem;">
                    <a href="data:file/mp3;base64,{b64}"
                       download="{filename}"
                       class="download-button">
                        {t("music.download")}
                    </a>
                </div>
            """
            st.markdown(download_href, unsafe_allow_html=True)

    # Use centered column layout
    render_centered_column_layout(render_content)

    # Use reusable audio tips with custom content for musical affirmations
    musical_tips = [
        t("music.tip_1"),
        t("music.tip_2"),
        t("music.tip_3"),
        t("music.tip_4"),
        t("music.tip_5"),
    ]
    render_audio_tips(t("music.tips_title"), musical_tips)


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
