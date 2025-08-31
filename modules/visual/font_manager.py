"""
Moduł do zarządzania czcionkami i stylami tekstu
"""
import os
import streamlit as st
from PIL import ImageFont
from config.constants import FONT_STYLES, FONT_DIR

# Cachowane funkcje dla kosztownych operacji z czcionkami
@st.cache_data(show_spinner=False)
def _cached_setup_fonts(font_dir_path):
    """
    Cachowana wersja setup_fonts - skanuje folder czcionek tylko raz.
    """
    available_fonts = []
    if os.path.exists(font_dir_path):
        available_fonts = [f for f in os.listdir(font_dir_path) if f.endswith(('.ttf', '.otf'))]
    return available_fonts

@st.cache_resource(show_spinner=False)
def _cached_load_font(font_path, size, font_style_key):
    """
    Cachowany loader czcionek - fontów nie trzeba ładować za każdym razem.
    font_style_key zapewnia, że różne style są cachowane osobno.
    """
    try:
        if os.path.exists(font_path):
            return ImageFont.truetype(font_path, size)
        else:
            # Spróbuj znaleźć alternatywną czcionkę
            if "Bold" in font_style_key or "Pogrubiony" in font_style_key:
                # Dla pogrubionych - spróbuj systemową Arial Bold
                for fallback in ["arial.ttf", "arial-bold.ttf", "calibri-bold.ttf"]:
                    try:
                        return ImageFont.truetype(fallback, size)
                    except:
                        continue
            elif "Italic" in font_style_key or "Elegancki" in font_style_key:
                # Dla kursywy - spróbuj systemową Arial Italic
                for fallback in ["arial-italic.ttf", "calibri-italic.ttf"]:
                    try:
                        return ImageFont.truetype(fallback, size)
                    except:
                        continue
            
            # Ostateczny fallback
            return ImageFont.load_default()
            
    except Exception:
        return ImageFont.load_default()

@st.cache_data(show_spinner=False)
def _cached_measure_text(text, font_path, font_size, font_style_key):
    """
    Cachowane mierzenie tekstu dla identycznych parametrów.
    font_style_key zapewnia cache dla różnych stylów fontów.
    """
    try:
        font = _cached_load_font(font_path, font_size, font_style_key)
        if hasattr(font, 'getbbox'):
            bbox = font.getbbox(text)
            return bbox[2] - bbox[0], bbox[3] - bbox[1]
        elif hasattr(font, 'getsize'):
            return font.getsize(text)
        else:
            return len(text) * (font.size // 2), font.size
    except Exception:
        return len(text) * (font_size // 2), font_size

def setup_fonts():
    """
    Sprawdza i konfiguruje czcionki systemowe z cache.
    """
    # Sprawdź czy już zostało wykonane w tej sesji
    import streamlit as st
    if hasattr(st, 'session_state') and st.session_state.get('fonts_initialized', False):
        return _cached_setup_fonts(FONT_DIR)
    
    # Sprawdź czy folder z czcionkami istnieje
    if not os.path.exists(FONT_DIR):
        try:
            os.makedirs(FONT_DIR)
            # Nie wyświetlaj komunikatu tutaj - zapisz w session_state
            if hasattr(st, 'session_state'):
                st.session_state['font_folder_created'] = f"Utworzono folder na czcionki: {FONT_DIR}"
        except Exception as e:
            # Nie wyświetlaj błędu tutaj - zapisz w session_state
            if hasattr(st, 'session_state'):
                st.session_state['font_folder_error'] = f"Nie można utworzyć folderu czcionek: {str(e)}"

    # Użyj cachowanego skanowania czcionek
    available_fonts = _cached_setup_fonts(FONT_DIR)
    
    # Oznacz jako zainicjalizowane
    if hasattr(st, 'session_state'):
        st.session_state['fonts_initialized'] = True

    # Nie wyświetlamy komunikatów tutaj - to musi czekać do po st.set_page_config()
    # Zapisujemy informacje w session_state do późniejszego wyświetlenia
    if not available_fonts:
        import streamlit as st
        if hasattr(st, 'session_state'):
            st.session_state['font_setup_message'] = {
                'type': 'warning',
                'message': f"⚠️ Brak czcionek w folderze fonts. Używane będą systemowe fonty fallback.\n📁 Aby dodać własne czcionki, umieść pliki .ttf w folderze: {FONT_DIR}"
            }
    else:
        import streamlit as st  
        if hasattr(st, 'session_state'):
            st.session_state['font_setup_message'] = {
                'type': 'success', 
                'message': f"✅ Znaleziono {len(available_fonts)} czcionek: {', '.join(available_fonts)}"
            }
        
        # Aktualizacja ścieżek czcionek w FONT_STYLES
        for style, info in FONT_STYLES.items():
            font_file = info.get("font", "").split("/")[-1] if "/" in info.get("font", "") else info.get("font", "").split("\\")[-1]
            if font_file not in available_fonts and available_fonts:
                FONT_STYLES[style]["font"] = os.path.join(FONT_DIR, available_fonts[0])

    return available_fonts

def clear_font_cache():
    """
    Czyści cache fontów - przydatne gdy użytkownik zmieni style.
    """
    try:
        _cached_load_font.clear()
        _cached_measure_text.clear()
        # Zapisz komunikat w session_state zamiast wyświetlać bezpośrednio
        import streamlit as st
        if hasattr(st, 'session_state'):
            st.session_state['cache_cleared_message'] = "🔄 Cache fontów wyczyszczony"
        return True
    except:
        return False

def load_system_font(font_info, size, font_style_name="default"):
    """
    Ładuje czcionkę systemową na podstawie informacji o stylu z cache.
    
    Args:
        font_info (dict): Informacje o czcionce z FONT_STYLES
        size (int): Rozmiar czcionki
        font_style_name (str): Nazwa stylu czcionki dla cache key
        
    Returns:
        ImageFont: Załadowana czcionka lub domyślna w przypadku błędu
    """
    font_path = font_info.get("font", "")
    # Użyj kombinacji ścieżki i nazwy stylu jako klucz cache
    cache_key = f"{font_style_name}_{font_path}"
    return _cached_load_font(font_path, size, cache_key)

def measure_text(text, font, font_style_name="default"):
    """
    Mierzy wymiary tekstu z cache dla lepszej wydajności.
    
    Args:
        text (str): Tekst do zmierzenia
        font (ImageFont): Obiekt czcionki
        font_style_name (str): Nazwa stylu czcionki dla cache
        
    Returns:
        tuple: (szerokość, wysokość) tekstu w pikselach
    """
    # Spróbuj pobrać informacje o czcionce dla cache
    font_path = getattr(font, 'path', 'default')
    font_size = getattr(font, 'size', 12)
    
    # Użyj cache jeśli mamy ścieżkę i rozmiar
    if font_path != 'default':
        cache_key = f"{font_style_name}_{font_path}"
        return _cached_measure_text(text, font_path, font_size, cache_key)
    
    # Fallback do standardowego mierzenia
    try:
        if hasattr(font, 'getbbox'):
            bbox = font.getbbox(text)
            return bbox[2] - bbox[0], bbox[3] - bbox[1]
        elif hasattr(font, 'getsize'):
            return font.getsize(text)
        else:
            return len(text) * (font_size // 2), font_size
    except Exception:
        return len(text) * (font_size // 2), font_size