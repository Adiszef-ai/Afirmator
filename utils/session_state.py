"""
app/utils/session_state.py - Zarządzanie stanem aplikacji (Streamlit Session State)
"""
import streamlit as st
from typing import Any, Optional, Dict
from config.constants import DEFAULT_SESSION_STATE


class StateManager:
    """
    Klasa zarządzająca stanem sesji Streamlit z obsługą namespace'ów.
    
    Przykład użycia:
        StateManager.init_state()
        StateManager.set('generator.editing', True)
        editing = StateManager.get('generator.editing', False)
    """
    
    @staticmethod
    def init_state():
        """
        Inicjalizuje stan sesji z domyślnymi wartościami używając namespace'ów.
        """
        if 'initialized' not in st.session_state:
            # Konwertuj istniejące klucze na namespace'y
            namespaced_state = StateManager._convert_to_namespaced_state(DEFAULT_SESSION_STATE)
            st.session_state.update(namespaced_state)
            st.session_state.initialized = True
    
    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """
        Pobiera wartość z session_state używając klucza z namespace'em.
        
        Args:
            key (str): Klucz z namespace'em (np. 'generator.editing')
            default (Any): Wartość domyślna jeśli klucz nie istnieje
            
        Returns:
            Any: Wartość z session_state lub wartość domyślna
        """
        return st.session_state.get(key, default)
    
    @staticmethod
    def set(key: str, value: Any) -> None:
        """
        Ustawia wartość w session_state używając klucza z namespace'em.
        
        Args:
            key (str): Klucz z namespace'em (np. 'generator.editing')
            value (Any): Wartość do ustawienia
        """
        st.session_state[key] = value
    
    @staticmethod
    def delete(key: str) -> None:
        """
        Usuwa klucz z session_state.
        
        Args:
            key (str): Klucz z namespace'em do usunięcia
        """
        if key in st.session_state:
            del st.session_state[key]
    
    @staticmethod
    def has_key(key: str) -> bool:
        """
        Sprawdza czy klucz istnieje w session_state.
        
        Args:
            key (str): Klucz z namespace'em do sprawdzenia
            
        Returns:
            bool: True jeśli klucz istnieje
        """
        return key in st.session_state
    
    @staticmethod
    def get_namespace(namespace: str) -> Dict[str, Any]:
        """
        Pobiera wszystkie klucze z danego namespace'a.
        
        Args:
            namespace (str): Nazwa namespace'a (np. 'generator')
            
        Returns:
            Dict[str, Any]: Słownik z kluczami i wartościami z namespace'a
        """
        result = {}
        prefix = f"{namespace}."
        
        for key in st.session_state:
            if key.startswith(prefix):
                # Usuń prefix namespace'a z klucza
                clean_key = key[len(prefix):]
                result[clean_key] = st.session_state[key]
        
        return result
    
    @staticmethod
    def clear_namespace(namespace: str) -> None:
        """
        Usuwa wszystkie klucze z danego namespace'a.
        
        Args:
            namespace (str): Nazwa namespace'a do wyczyszczenia
        """
        prefix = f"{namespace}."
        keys_to_delete = [key for key in st.session_state if key.startswith(prefix)]
        
        for key in keys_to_delete:
            del st.session_state[key]
    
    @staticmethod
    def update_namespace(namespace: str, data: Dict[str, Any]) -> None:
        """
        Aktualizuje wszystkie klucze w namespace'ie.
        
        Args:
            namespace (str): Nazwa namespace'a
            data (Dict[str, Any]): Dane do zaktualizowania
        """
        for key, value in data.items():
            StateManager.set(f"{namespace}.{key}", value)
    
    @staticmethod
    def _convert_to_namespaced_state(default_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Konwertuje domyślny stan na stan z namespace'ami.
        
        Args:
            default_state (Dict[str, Any]): Domyślny stan aplikacji
            
        Returns:
            Dict[str, Any]: Stan z namespace'ami
        """
        namespaced_state = {}
        
        # Mapowanie starych kluczy na nowe z namespace'ami
        namespace_mapping = {
            # Generator namespace
            'editing': 'generator.editing',
            'edited_affirmation': 'generator.edited_affirmation',
            'affirmation': 'generator.affirmation',
            'history': 'generator.history',
            
            # Audio namespace
            'audio_data': 'audio.data',
            'selected_voice': 'audio.selected_voice',
            'daily_audio_data': 'audio.daily_data',
            'player_audio_data': 'audio.player_data',
            'music_affirmation_audio': 'audio.music_affirmation',
            
            # Daily namespace
            'daily_affirmation': 'daily.affirmation',
            'daily_affirmation_name': 'daily.affirmation_name',
            'show_daily_affirmation_input': 'daily.show_input',
            
            # App namespace
            'current_tab': 'app.current_tab',
            'selected_provider': 'app.selected_provider',
            'show_openai_form': 'app.show_openai_form',
            'api_key': 'app.api_key'
        }
        
        # Konwertuj klucze używając mapowania
        for old_key, value in default_state.items():
            new_key = namespace_mapping.get(old_key, old_key)
            namespaced_state[new_key] = value
        
        return namespaced_state
    
    @staticmethod
    def migrate_legacy_state():
        """
        Migruje stary stan bez namespace'ów do nowego z namespace'ami.
        Użyj tej funkcji jednorazowo przy aktualizacji aplikacji.
        """
        if StateManager.get('migrated', False):
            return  # Już zmigrowane
            
        # Mapowanie starych kluczy na nowe
        migration_map = StateManager._convert_to_namespaced_state(DEFAULT_SESSION_STATE)
        
        # Migruj każdy klucz
        for old_key in list(st.session_state.keys()):
            if old_key in migration_map:
                # Znajdź nowy klucz dla tego starego klucza
                for new_key, default_value in migration_map.items():
                    if old_key in DEFAULT_SESSION_STATE and new_key.endswith('.' + old_key.split('.')[-1]):
                        st.session_state[new_key] = st.session_state[old_key]
                        # Usuń stary klucz
                        del st.session_state[old_key]
                        break
        
        # Oznacz jako zmigrowane
        StateManager.set('migrated', True)


# Backwards compatibility - aliasy dla starych funkcji
def init_session_state():
    """Alias dla StateManager.init_state() - zgodność wsteczna."""
    StateManager.init_state()


def get_state(key: str, default: Any = None) -> Any:
    """Alias dla StateManager.get() - zgodność wsteczna."""
    return StateManager.get(key, default)


def set_state(key: str, value: Any) -> None:
    """Alias dla StateManager.set() - zgodność wsteczna."""
    StateManager.set(key, value)