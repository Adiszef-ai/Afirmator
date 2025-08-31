"""
services/groq_service.py - Serwis do obsługi Groq AI API
"""
import streamlit as st
from groq import Groq
from config.utils import get_api_key

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
            raise ValueError("Brak klucza API dla Groq. Ustaw go w secrets.toml lub zmiennych środowiskowych.")
        
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"  # Aktualny model Groq
    
    def generate_text(self, prompt, max_tokens=500, temperature=0.7):
        """
        Generuje tekst używając Groq AI
        
        Args:
            prompt (str): Prompt dla modelu
            max_tokens (int): Maksymalna liczba tokenów
            temperature (float): Temperatura generowania (0.0-2.0)
            
        Returns:
            str: Wygenerowany tekst
        """
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
            error_msg = f"Błąd generowania tekstu z Groq: {str(e)}"
            try:
                st.error(error_msg)
            except:
                print(error_msg)  # Fallback dla testów
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
        # Przygotowanie promptu
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
        
        prompt = " ".join(prompt_parts)
        
        # Dostosuj liczbę tokenów do wybranej długości
        token_mapping = {
            "1-2 zdania": 80,
            "3-4 zdań": 150,
            "5-6 zdań": 250
        }
        max_tokens = token_mapping.get(length, 150)
        
        return self.generate_text(prompt, max_tokens=max_tokens, temperature=0.8)
    
    def generate_daily_affirmation(self, user_name="", topics=None):
        """
        Generuje afirmację dnia
        
        Args:
            user_name (str): Imię użytkownika
            topics (list): Lista tematów
            
        Returns:
            str: Afirmacja dnia
        """
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
            st.warning(f"Nie można pobrać listy modeli: {str(e)}")
            return [self.model]
    
    def set_model(self, model_name):
        """
        Ustawia model do użycia
        
        Args:
            model_name (str): Nazwa modelu
        """
        self.model = model_name