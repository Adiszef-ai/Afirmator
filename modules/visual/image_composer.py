"""
Moduł do komponowania ostatecznych obrazów z afirmacjami
"""
import streamlit as st
from PIL import Image
from .gradient_generator import create_gradient_background
from .text_renderer import add_text_to_image
from .font_manager import setup_fonts

def get_size_in_cm(width_px, height_px, dpi=300):
    """
    Przelicza rozmiar w pikselach na centymetry.
    
    Args:
        width_px (int): Szerokość w pikselach
        height_px (int): Wysokość w pikselach
        dpi (int): Rozdzielczość DPI
    
    Returns:
        tuple: (szerokość w cm, wysokość w cm)
    """
    width_cm = (width_px / dpi) * 2.54
    height_cm = (height_px / dpi) * 2.54
    return width_cm, height_cm

def create_visual_quote(text, background_type="gradient", gradient_colors=None, 
                       uploaded_image=None, text_color=(255, 255, 255), 
                       font_size=60, width=1080, height=1080, direction="vertical",
                       position="center", font_style="Klasyczny", custom_x_percent=50, 
                       custom_y_percent=50, shadow_color=(0, 0, 0, 200)):
    """
    Tworzy wizualny cytat z afirmacją.
    
    Returns:
        Image: Gotowy obraz z cytatem
    """
    try:
        # Normalizacja tekstu
        text = _normalize_input_text(text)
        
        # Stwórz tło
        image = _create_background(background_type, gradient_colors, uploaded_image, 
                                 width, height, direction)
        
        # Dodaj tekst do obrazu
        final_image = add_text_to_image(
            image, text, font_size, text_color, position, 
            padding=50, font_style=font_style,
            custom_x_percent=custom_x_percent, 
            custom_y_percent=custom_y_percent,
            shadow_color=shadow_color
        )
        return final_image
        
    except Exception as e:
        st.error(f"Błąd tworzenia obrazu: {str(e)}")
        return _create_error_image(width, height)

def _normalize_input_text(text):
    """
    Normalizuje tekst wejściowy
    """
    if not isinstance(text, str):
        text = str(text)
    
    if isinstance(text, bytes):
        text = text.decode('utf-8', errors='replace')
    
    return text

def _create_background(background_type, gradient_colors, uploaded_image, 
                      width, height, direction):
    """
    Tworzy tło obrazu na podstawie wybranego typu
    """
    if background_type == "gradient" and gradient_colors:
        try:
            if gradient_colors == "custom":
                gradient_colors = [(74, 144, 226), (255, 107, 156)]
            
            return create_gradient_background(
                width, height, gradient_colors[0], gradient_colors[1], direction
            )
        except Exception as e:
            st.error(f"Błąd tworzenia gradientu: {str(e)}")
            return create_gradient_background(
                width, height, (74, 144, 226), (255, 107, 156), "vertical"
            )
    
    elif background_type == "image" and uploaded_image:
        try:
            return uploaded_image.resize(
                (width, height), 
                Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.LANCZOS
            )
        except Exception as e:
            st.error(f"Błąd przetwarzania obrazu: {str(e)}")
            return create_gradient_background(
                width, height, (74, 144, 226), (255, 107, 156), "vertical"
            )
    
    else:
        # Domyślne tło
        return create_gradient_background(
            width, height, (74, 144, 226), (255, 107, 156), "vertical"
        )

def _create_error_image(width, height):
    """
    Tworzy obrazek błędu w przypadku problemów
    """
    from PIL import ImageDraw
    
    image = Image.new('RGB', (width, height), (100, 100, 100))
    draw = ImageDraw.Draw(image)
    draw.text((width//2, height//2), "Błąd tworzenia obrazu", fill=(255, 255, 255))
    return image