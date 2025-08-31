"""
Moduł do zarządzania czcionkami i stylami tekstu
"""
import os
import streamlit as st
from PIL import ImageFont
from config.constants import FONT_STYLES, FONT_DIR

def setup_fonts():
    """
    Sprawdza i konfiguruje czcionki systemowe
    """
    # Sprawdź czy folder z czcionkami istnieje
    if not os.path.exists(FONT_DIR):
        try:
            os.makedirs(FONT_DIR)
            st.warning(f"Utworzono folder na czcionki: {FONT_DIR}")
        except Exception as e:
            st.error(f"Nie można utworzyć folderu czcionek: {str(e)}")

    # Sprawdź dostępne czcionki
    available_fonts = []
    if os.path.exists(FONT_DIR):
        available_fonts = [f for f in os.listdir(FONT_DIR) if f.endswith(('.ttf', '.otf'))]

    if not available_fonts:
        st.warning("Brak czcionek w folderze fonts. Niektóre funkcje mogą nie działać poprawnie.")
    else:
        # Aktualizacja ścieżek czcionek w FONT_STYLES
        for style, info in FONT_STYLES.items():
            font_file = info.get("font", "").split("/")[-1]
            if font_file not in available_fonts and available_fonts:
                FONT_STYLES[style]["font"] = os.path.join(FONT_DIR, available_fonts[0])

    return available_fonts

def load_system_font(font_info, size):
    """
    Ładuje czcionkę systemową na podstawie informacji o stylu
    
    Args:
        font_info (dict): Informacje o czcionce z FONT_STYLES
        size (int): Rozmiar czcionki
        
    Returns:
        ImageFont: Załadowana czcionka lub domyślna w przypadku błędu
    """
    try:
        font_path = font_info.get("font", "")
        return ImageFont.truetype(font_path, size)
    except Exception:
        return ImageFont.load_default()

def measure_text(text, font):
    """
    Mierzy wymiary tekstu
    
    Args:
        text (str): Tekst do zmierzenia
        font (ImageFont): Obiekt czcionki
        
    Returns:
        tuple: (szerokość, wysokość) tekstu w pikselach
    """
    try:
        if hasattr(font, 'getbbox'):
            bbox = font.getbbox(text)
            return bbox[2] - bbox[0], bbox[3] - bbox[1]
        elif hasattr(font, 'getsize'):
            return font.getsize(text)
        else:
            return len(text) * (font.size // 2), font.size
    except Exception:
        font_size = getattr(font, 'size', 12)
        return len(text) * (font_size // 2), font_size