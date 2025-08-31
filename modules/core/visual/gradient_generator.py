"""
Moduł do generowania gradientów dla wizualnych cytatów
"""
import streamlit as st
import hashlib
from PIL import Image

# Cachowane generowanie gradientów - kosztowna operacja
@st.cache_data(show_spinner=False, max_entries=20)  # Limit cache entries aby nie zużywać za dużo pamięci
def _cached_create_gradient_background(width, height, color1_hash, color2_hash, direction):
    """
    Cachowana wersja tworzenia gradientu.
    Używa hash'y kolorów żeby cache działał poprawnie.
    """
    # Rekonstruuj kolory z hash'y (uproszczone - kolory są przekazane jako tuple)
    # W rzeczywistości tutaj możemy przekazać kolory bezpośrednio
    return _generate_gradient_image(width, height, color1_hash, color2_hash, direction)

def _generate_gradient_image(width, height, color1, color2, direction):
    """
    Faktyczna implementacja generowania gradientu.
    """
    base = Image.new('RGB', (width, height), color1)
    top = Image.new('RGB', (width, height), color2)
    mask = Image.new('L', (width, height))
    mask_data = []
    
    for y in range(height):
        for x in range(width):
            if direction == "vertical":
                value = int(255 * (y / height))
            elif direction == "horizontal":
                value = int(255 * (x / width))
            elif direction == "diagonal_tl_br":
                value = int(255 * ((x / width + y / height) / 2))
            elif direction == "diagonal_tr_bl":
                value = int(255 * ((1 - x / width + y / height) / 2))
            elif direction == "radial":
                center_x, center_y = width / 2, height / 2
                distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                max_distance = ((width / 2) ** 2 + (height / 2) ** 2) ** 0.5
                value = int(255 * min(1.0, distance / max_distance))
            else:
                value = int(255 * (y / height))
            mask_data.append(value)
    
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

def create_gradient_background(width, height, color1, color2, direction="vertical"):
    """
    Tworzy tło gradientowe z cache dla lepszej wydajności.
    
    Args:
        width (int): Szerokość obrazu
        height (int): Wysokość obrazu
        color1 (tuple): Pierwszy kolor RGB
        color2 (tuple): Drugi kolor RGB
        direction (str): Kierunek gradientu ("vertical", "horizontal", "diagonal_tl_br", "diagonal_tr_bl", "radial")
    
    Returns:
        Image: Obraz z gradientem
    """
    # Używamy cachowanej wersji - przekazujemy kolory bezpośrednio
    # Cache będzie działał dla identycznych parametrów
    try:
        return _cached_create_gradient_background(width, height, color1, color2, direction)
    except Exception:
        # Fallback do standardowego generowania jeśli cache nie działa
        return _generate_gradient_image(width, height, color1, color2, direction)