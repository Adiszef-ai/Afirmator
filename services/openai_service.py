"""
Usługi związane z OpenAI API.
"""
import streamlit as st
from openai import OpenAI

class OpenAIService:
    """Klasa obsługująca interakcje z OpenAI API."""
    
    def __init__(self, api_key=None):
        """
        Inicjalizuje serwis OpenAI.
        
        Args:
            api_key (str, optional): Klucz API OpenAI. Jeśli None, 
                                     próbuje pobrać z st.session_state.
        """
        if api_key is None and 'api_key' in st.session_state:
            api_key = st.session_state.api_key
            
        self.client = OpenAI(api_key=api_key)
        
    def generate_affirmation(self, prompt, model="gpt-4", temperature=0.7, max_tokens=250):
        """
        Generuje afirmację za pomocą API OpenAI.
        
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
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Jesteś doświadczonym coachem specjalizującym się w tworzeniu skutecznych afirmacji."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content.strip('"')
        except Exception as e:
            raise Exception(f"Błąd podczas generowania afirmacji: {str(e)}")
    
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
            raise Exception(f"Błąd generowania audio: {str(e)}")

    def daily_affirmation_system_prompt(self):
        """
        Zwraca treść promptu systemowego dla afirmacji dnia.
        
        Returns:
            str: Prompt systemowy.
        """
        return "Jesteś ekspertem w tworzeniu krótkich, inspirujących afirmacji, które pomagają ludziom zacząć dzień pozytywnie."

    def generator_affirmation_system_prompt(self):
        """
        Zwraca treść promptu systemowego dla generatora afirmacji.
        
        Returns:
            str: Prompt systemowy.
        """
        return "Jesteś doświadczonym coachem specjalizującym się w tworzeniu skutecznych afirmacji."