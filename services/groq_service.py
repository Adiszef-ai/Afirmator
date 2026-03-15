"""
services/groq_service.py - Serwis do obsługi Groq AI API
"""
import streamlit as st
import hashlib
from groq import Groq
from config.utils import get_api_key
from config.translations import t, get_language

# Cachowane funkcje dla Groq AI
@st.cache_data(ttl=3600, show_spinner=False)  # Cache na godzinę
def _cached_groq_generate_text(prompt_hash, model, max_tokens, temperature, api_key_hash):
    """
    Cachowana wersja generowania tekstu przez Groq.
    """
    api_key = get_api_key("groq")
    if not api_key:
        st.error(t("service.no_groq_key_cache"))
        return None

    client = Groq(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt_hash}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"{t('service.groq_cache_error')}{str(e)}")
        return None

class GroqService:
    """
    Serwis do komunikacji z Groq AI API
    """

    def __init__(self):
        """
        Inicjalizuje serwis Groq AI
        """
        api_key = get_api_key("groq")
        if not api_key:
            raise ValueError(t("service.groq_no_key_init"))

        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"  # Aktualny model Groq

    def generate_text(self, prompt, max_tokens=500, temperature=0.7):
        """
        Generuje tekst używając Groq AI z cache.

        Args:
            prompt (str): Prompt dla modelu
            max_tokens (int): Maksymalna liczba tokenów
            temperature (float): Temperatura generowania (0.0-2.0)

        Returns:
            str: Wygenerowany tekst
        """
        # Tworzenie hash'y dla cache
        api_key = get_api_key("groq")
        if not api_key:
            st.error(t("service.no_groq_key"))
            return None

        api_key_hash = hashlib.md5(api_key.encode()).hexdigest()[:8]
        cache_key = f"{prompt}|{self.model}|{max_tokens}|{temperature}"

        # Sprawdź cache dla deterministycznych zapytań
        if temperature <= 0.3:
            try:
                cached_result = _cached_groq_generate_text(
                    cache_key, self.model, max_tokens, temperature, api_key_hash
                )
                if cached_result:
                    return cached_result
            except Exception:
                pass  # Fallback do normalnego API

        # Normalny API call
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            # Obsługa specyficznych błędów Groq
            error_str = str(e).lower()

            if "authentication" in error_str or "unauthorized" in error_str:
                st.error(t("service.invalid_groq_key"))
                return None
            elif "rate limit" in error_str or "quota" in error_str:
                st.warning(t("service.rate_limit_groq"))
                return None
            elif "connection" in error_str or "timeout" in error_str:
                st.error(t("service.connection_groq"))
                return None
            elif "model" in error_str and "not found" in error_str:
                st.error(t("service.model_not_found").format(model=self.model))
                return None
            else:
                st.error(f"{t('service.groq_error')}{str(e)}")
                return None

    def generate_affirmation(self, categories=None, tone="pozytywny", timing="rano",
                           context="", user_name="", language="polski", length="3-4 zdań"):
        """
        Generuje afirmację używając Groq AI

        Args:
            categories (list): Lista kategorii afirmacji
            tone (str): Ton afirmacji
            timing (str): Pora dnia
            context (str): Dodatkowy kontekst
            user_name (str): Imię użytkownika
            language (str): Język afirmacji
            length (str): Długość afirmacji

        Returns:
            str: Wygenerowana afirmacja
        """
        lang = get_language()
        # Auto-detect language from app setting if not explicitly provided
        if language == "polski" and lang == "en":
            language = "English"

        # Przygotowanie promptu
        if lang == "pl" or language == "polski":
            prompt_parts = [
                f"Wygeneruj pozytywną afirmację w języku {language}.",
            ]

            if user_name:
                prompt_parts.append(f"Afirmacja jest dla osoby o imieniu {user_name} i MUSI zaczynać się od 'Ja, {user_name},'.")

            if categories:
                categories_str = ", ".join(categories)
                prompt_parts.append(f"Kategorie: {categories_str}.")

            if tone != "pozytywny":
                prompt_parts.append(f"Ton: {tone}.")

            if timing != "rano":
                prompt_parts.append(f"Pora dnia: {timing}.")

            if context:
                prompt_parts.append(f"Dodatkowy kontekst: {context}")

            prompt_parts.extend([
                f"Długość afirmacji: {length}.",
                "Afirmacja powinna być:",
                "- Napisana w pierwszej osobie",
                "- Pozytywna i motywująca",
                "- Bez cudzysłowów",
                "",
                "Przykłady dobrych afirmacji:",
                "- Ja, Anna, jestem spokojna i pewna siebie",
                "- Ja, Tomek, wiem że moje możliwości są nieograniczone",
                "- Ja, Maria, zasługuję na szczęście i sukces",
                "",
                "Wygeneruj jedną afirmację:"
            ])
        else:
            prompt_parts = [
                f"Generate a positive affirmation in {language}.",
            ]

            if user_name:
                prompt_parts.append(f"The affirmation is for a person named {user_name} and MUST start with 'I, {user_name},'.")

            if categories:
                categories_str = ", ".join(categories)
                prompt_parts.append(f"Categories: {categories_str}.")

            if tone:
                prompt_parts.append(f"Tone: {tone}.")

            if timing:
                prompt_parts.append(f"Time of day: {timing}.")

            if context:
                prompt_parts.append(f"Additional context: {context}")

            prompt_parts.extend([
                f"Affirmation length: {length}.",
                "The affirmation should be:",
                "- Written in first person",
                "- Positive and motivating",
                "- Without quotation marks",
                "",
                "Examples of good affirmations:",
                "- I, Anna, am calm and confident",
                "- I, Tom, know that my possibilities are unlimited",
                "- I, Maria, deserve happiness and success",
                "",
                "Generate one affirmation:"
            ])

        prompt = " ".join(prompt_parts)

        # Dostosuj liczbę tokenów do wybranej długości
        token_mapping = {
            "1-2 zdania": 80,
            "3-4 zdań": 150,
            "5-6 zdań": 250,
            "1-2 sentences": 80,
            "3-4 sentences": 150,
            "5-6 sentences": 250,
        }
        max_tokens = token_mapping.get(length, 150)

        return self.generate_text(prompt, max_tokens=max_tokens, temperature=0.8)

    def generate_daily_affirmation(self, user_name="", topics=None, language=None):
        """
        Generuje afirmację dnia

        Args:
            user_name (str): Imię użytkownika
            topics (list): Lista tematów
            language (str): Kod języka (pl/en)

        Returns:
            str: Afirmacja dnia
        """
        if language is None:
            language = get_language()

        if language == "pl":
            prompt_parts = [
                "Wygeneruj inspirującą afirmację dnia w języku polskim.",
            ]

            if user_name:
                prompt_parts.append(f"Afirmacja jest dla {user_name} i MUSI zaczynać się od 'Ja, {user_name},'.")

            if topics:
                topics_str = ", ".join(topics)
                prompt_parts.append(f"Tematy do uwzględnienia: {topics_str}.")

            prompt_parts.extend([
                "Afirmacja powinna być:",
                "- Pozytywna i motywująca na cały dzień",
                "- Napisana w pierwszej osobie",
                "- Krótka i łatwa do zapamiętania",
                "- Bez cudzysłowów",
                "",
                "Przykład dobrej afirmacji dnia:",
                "- Ja, Adrian, dzisiaj jestem pełen energii i gotowy na nowe wyzwania",
                "",
                "Wygeneruj afirmację:"
            ])
        else:
            prompt_parts = [
                "Generate an inspiring daily affirmation in English.",
            ]

            if user_name:
                prompt_parts.append(f"The affirmation is for {user_name} and MUST start with 'I, {user_name},'.")

            if topics:
                topics_str = ", ".join(topics)
                prompt_parts.append(f"Topics to consider: {topics_str}.")

            prompt_parts.extend([
                "The affirmation should be:",
                "- Positive and motivating for the whole day",
                "- Written in first person",
                "- Short and easy to remember",
                "- Without quotation marks",
                "",
                "Example of a good daily affirmation:",
                "- I, Adrian, today I am full of energy and ready for new challenges",
                "",
                "Generate an affirmation:"
            ])

        prompt = " ".join(prompt_parts)

        return self.generate_text(prompt, max_tokens=100, temperature=0.9)

    def get_available_models(self):
        """
        Zwraca listę dostępnych modeli Groq

        Returns:
            list: Lista nazw modeli
        """
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except Exception as e:
            st.warning(f"{t('service.groq_models_error')}{str(e)}")
            return [self.model]

    def set_model(self, model_name):
        """
        Ustawia model do użycia

        Args:
            model_name (str): Nazwa modelu
        """
        self.model = model_name
