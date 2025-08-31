"""
services/ai_factory.py - Fabryka serwisów AI do zarządzania różnymi providerami
"""
import streamlit as st
import hashlib
from .openai_service import OpenAIService
from .groq_service import GroqService
from config.utils import check_api_key, get_api_key

# Cachowane singleton serwisy
@st.cache_resource(show_spinner=False)
def get_openai_service(_api_key_hash):
    """
    Cachowany singleton OpenAI Service.
    _api_key_hash jest używane tylko do invalidacji cache przy zmianie klucza.
    """
    try:
        return OpenAIService()
    except Exception as e:
        st.error(f"Błąd inicjalizacji OpenAI Service: {str(e)}")
        return None

@st.cache_resource(show_spinner=False)
def get_groq_service(_api_key_hash):
    """
    Cachowany singleton Groq Service.
    _api_key_hash jest używane tylko do invalidacji cache przy zmianie klucza.
    """
    try:
        return GroqService()
    except Exception as e:
        st.error(f"Błąd inicjalizacji Groq Service: {str(e)}")
        return None

class AIServiceFactory:
    """
    Fabryka do tworzenia i zarządzania serwisami AI
    """
    
    @staticmethod
    def get_available_providers():
        """
        Zwraca listę dostępnych providerów AI na podstawie dostępnych kluczy API
        
        Returns:
            dict: Słownik z dostępnymi providerami {provider_name: display_name}
        """
        providers = {}
        
        # Sprawdź OpenAI
        if check_api_key("openai"):
            providers["openai"] = "💎 OpenAI (Premium)"
        
        # Sprawdź Groq
        if check_api_key("groq"):
            providers["groq"] = "🆓 Groq (Darmowy)"
        
        return providers
    
    @staticmethod
    def create_service(provider="openai"):
        """
        Tworzy cachowany serwis AI dla wybranego providera (singleton).
        
        Args:
            provider (str): Nazwa providera ("openai" lub "groq")
            
        Returns:
            Service object: Serwis AI lub None jeśli błąd
        """
        try:
            # Pobierz API key dla invalidacji cache
            api_key = get_api_key(provider)
            if not api_key:
                st.error(f"Brak klucza API dla {provider}")
                return None
                
            # Utwórz hash klucza do invalidacji cache
            api_key_hash = hashlib.md5(api_key.encode()).hexdigest()
            
            if provider == "openai":
                return get_openai_service(api_key_hash)
            elif provider == "groq":
                return get_groq_service(api_key_hash)
            else:
                raise ValueError(f"Nieznany provider: {provider}")
        except Exception as e:
            st.error(f"Błąd tworzenia serwisu {provider}: {str(e)}")
            return None
    
    @staticmethod
    def get_provider_capabilities(provider):
        """
        Zwraca możliwości danego providera
        
        Args:
            provider (str): Nazwa providera
            
        Returns:
            dict: Słownik z możliwościami
        """
        capabilities = {
            "openai": {
                "text_generation": True,
                "audio_generation": True,
                "models": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
                "description": "Pełna funkcjonalność - tekst + audio"
            },
            "groq": {
                "text_generation": True,
                "audio_generation": False,
                "models": ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
                "description": "Tylko tekst, bardzo szybkie"
            }
        }
        
        return capabilities.get(provider, {})
    
    @staticmethod
    def display_provider_selection():
        """
        Wyświetla interfejs wyboru providera AI w sidebarze
        
        Returns:
            tuple: (provider_name, service_object)
        """
        available_providers = AIServiceFactory.get_available_providers()
        
        if not available_providers:
            st.error("Brak dostępnych providerów AI. Sprawdź konfigurację kluczy API.")
            return None, None
        
        if len(available_providers) == 1:
            # Jeśli tylko jeden provider, użyj go automatycznie
            provider_name = list(available_providers.keys())[0]
            st.sidebar.info(f"Używany model AI: {available_providers[provider_name]}")
        else:
            # Jeśli więcej providerów, daj wybór
            provider_display_names = list(available_providers.values())
            provider_names = list(available_providers.keys())
            
            selected_display = st.sidebar.radio(
                "🤖 Model AI",
                provider_display_names,
                help="Groq - szybki i darmowy (tylko tekst)\nOpenAI - premium (tekst + audio)"
            )
            
            # Znajdź odpowiedni provider_name
            provider_name = provider_names[provider_display_names.index(selected_display)]
        
        # Pokaż możliwości wybranego providera
        capabilities = AIServiceFactory.get_provider_capabilities(provider_name)
        if capabilities:
            st.sidebar.caption(f"✨ {capabilities['description']}")
        
        # Stwórz serwis
        service = AIServiceFactory.create_service(provider_name)
        
        return provider_name, service