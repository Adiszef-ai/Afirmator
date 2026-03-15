"""
app/services/openai_service.py - Usługi związane z OpenAI API.
"""
import streamlit as st
import hashlib
from openai import OpenAI
from config.translations import t, get_language

# Cachowane funkcje dla kosztownych operacji AI
@st.cache_data(ttl=3600, show_spinner=False)  # Cache na godzinę
def _cached_generate_affirmation(prompt_hash, model, temperature, max_tokens, api_key_hash):
    """
    Cachowana wersja generowania afirmacji.
    Używa hash'y parametrów jako klucze cache.
    """
    from config.utils import get_api_key
    api_key = get_api_key("openai")
    client = OpenAI(api_key=api_key)

    lang = get_language()
    if lang == "pl":
        system_content = "Jesteś doświadczonym coachem specjalizującym się w tworzeniu skutecznych afirmacji."
    else:
        system_content = "You are an experienced coach specializing in creating effective affirmations."

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt_hash}  # To będzie rzeczywisty prompt
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip('"')
    except Exception as e:
        st.error(f"{t('service.cache_error')}{str(e)}")
        return None

@st.cache_data(ttl=1800, show_spinner=False)  # Cache na 30 minut
def _cached_generate_daily_affirmation(name_hash, topics_hash, api_key_hash):
    """
    Cachowana wersja afirmacji dnia - cache krótszy bo to ma być "dnia".
    """
    from config.utils import get_api_key
    api_key = get_api_key("openai")
    client = OpenAI(api_key=api_key)

    lang = get_language()
    if lang == "pl":
        prompt = "Wygeneruj krótką, pozytywną afirmację dnia w języku polskim. Afirmacja powinna być motywująca i zaczynać się od 'Ja,' "
        system_content = "Jesteś ekspertem w tworzeniu krótkich, inspirujących afirmacji, które pomagają ludziom zacząć dzień pozytywnie."
    else:
        prompt = "Generate a short, positive daily affirmation in English. The affirmation should be motivating and start with 'I,' "
        system_content = "You are an expert in creating short, inspiring affirmations that help people start the day positively."

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=120
        )
        return response.choices[0].message.content.strip('"')
    except Exception as e:
        st.error(f"{t('service.cache_daily_error')}{str(e)}")
        return None

class OpenAIService:
    """Klasa obsługująca interakcje z OpenAI API."""

    def __init__(self, api_key=None):
        """
        Inicjalizuje serwis OpenAI.

        Args:
            api_key (str, optional): Klucz API OpenAI. Jeśli None,
                                     próbuje pobrać z config.utils.
        """
        if api_key is None:
            from config.utils import get_api_key
            api_key = get_api_key("openai")

        self.client = OpenAI(api_key=api_key)

    def generate_affirmation(self, prompt, model="gpt-4", temperature=0.7, max_tokens=250):
        """
        Generuje afirmację za pomocą API OpenAI z cache.

        Args:
            prompt (str): Prompt dla modelu.
            model (str, optional): Model do użycia. Domyślnie "gpt-4".
            temperature (float, optional): Wartość temperature. Domyślnie 0.7.
            max_tokens (int, optional): Maksymalna ilość tokenów. Domyślnie 250.

        Returns:
            str: Wygenerowana afirmacja.

        Raises:
            Exception: W przypadku błędu API.
        """
        # Tworzenie hash'y dla cache
        from config.utils import get_api_key
        api_key = get_api_key("openai")
        if not api_key:
            raise Exception(t("service.no_api_key"))

        api_key_hash = hashlib.md5(api_key.encode()).hexdigest()[:8]

        # Dla cache używamy kombinacji wszystkich parametrów
        cache_key = f"{prompt}|{model}|{temperature}|{max_tokens}"

        # Sprawdź cache first - jeśli temperatura jest niska (deterministyczna)
        if temperature <= 0.3:
            try:
                cached_result = _cached_generate_affirmation(
                    cache_key, model, temperature, max_tokens, api_key_hash
                )
                if cached_result:
                    return cached_result
            except Exception:
                pass  # Jeśli cache nie działa, idź do normalnego API

        lang = get_language()
        if lang == "pl":
            system_content = "Jesteś doświadczonym coachem specjalizującym się w tworzeniu skutecznych afirmacji."
        else:
            system_content = "You are an experienced coach specializing in creating effective affirmations."

        # Fallback do normalnego API call
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )

            return response.choices[0].message.content.strip('"')
        except Exception as e:
            # Importuj OpenAI errors dynamicznie
            try:
                from openai import APIError, RateLimitError, AuthenticationError, APIConnectionError

                if isinstance(e, AuthenticationError):
                    st.error(t("service.invalid_openai_key"))
                    st.stop()
                elif isinstance(e, RateLimitError):
                    st.warning(t("service.rate_limit_openai"))
                    st.stop()
                elif isinstance(e, APIConnectionError):
                    st.error(t("service.connection_openai"))
                    st.stop()
                elif isinstance(e, APIError):
                    st.error(f"{t('service.api_error_openai')}{str(e)}")
                    st.stop()
                else:
                    raise Exception(f"{t('service.unexpected_error')}{str(e)}")
            except ImportError:
                # Fallback jeśli nie ma dostępu do specyficznych błędów OpenAI
                raise Exception(f"{t('service.unexpected_error')}{str(e)}")

    def generate_affirmation_audio(self, text, voice="fable", model="tts-1", speed=0.9):
        """
        Generuje audio dla afirmacji za pomocą OpenAI API z kontrolą prędkości.

        Args:
            text (str): Tekst do zamiany na mowę.
            voice (str, optional): Typ głosu. Domyślnie "fable".
            model (str, optional): Model TTS. Domyślnie "tts-1".
            speed (float, optional): Prędkość mówienia (0.5-1.5). Domyślnie 0.9.

        Returns:
            bytes: Dane audio w formacie MP3.

        Raises:
            Exception: W przypadku błędu API.
        """
        try:
            # Bezpośrednie użycie tekstu bez żadnych modyfikacji
            audio_response = self.client.audio.speech.create(
                model=model,
                voice=voice,
                input=text,
                response_format="mp3",
                speed=speed
            )

            return audio_response.content
        except Exception as e:
            # Importuj OpenAI errors dynamicznie
            try:
                from openai import APIError, RateLimitError, AuthenticationError, APIConnectionError

                if isinstance(e, AuthenticationError):
                    st.error(t("service.invalid_openai_audio"))
                    return None
                elif isinstance(e, RateLimitError):
                    st.warning(t("service.rate_limit_audio"))
                    return None
                elif isinstance(e, APIConnectionError):
                    st.error(t("service.connection_audio"))
                    return None
                elif isinstance(e, APIError):
                    st.error(f"{t('service.api_error_audio')}{str(e)}")
                    return None
                else:
                    raise Exception(f"{t('service.unexpected_audio')}{str(e)}")
            except ImportError:
                # Fallback jeśli nie ma dostępu do specyficznych błędów OpenAI
                raise Exception(f"{t('service.audio_gen_error')}{str(e)}")

    def daily_affirmation_system_prompt(self):
        """
        Zwraca treść promptu systemowego dla afirmacji dnia.

        Returns:
            str: Prompt systemowy.
        """
        lang = get_language()
        if lang == "pl":
            return "Jesteś ekspertem w tworzeniu krótkich, inspirujących afirmacji, które pomagają ludziom zacząć dzień pozytywnie."
        else:
            return "You are an expert in creating short, inspiring affirmations that help people start the day positively."

    def generator_affirmation_system_prompt(self):
        """
        Zwraca treść promptu systemowego dla generatora afirmacji.

        Returns:
            str: Prompt systemowy.
        """
        lang = get_language()
        if lang == "pl":
            return "Jesteś doświadczonym coachem specjalizującym się w tworzeniu skutecznych afirmacji."
        else:
            return "You are an experienced coach specializing in creating effective affirmations."
