"""
Moduł do renderowania tekstu na obrazach
"""
import streamlit as st
import unicodedata
from PIL import Image, ImageDraw
from .font_manager import load_system_font, measure_text
from config.constants import FONT_STYLES

def auto_adjust_font_size(text, font_style, max_font_size, max_width, max_height, padding=50):
    """
    Automatycznie dobiera rozmiar czcionki, aby tekst zmieścił się w obrazie.
    
    Args:
        text (str): Tekst do wyświetlenia
        font_style (str): Styl czcionki do użycia
        max_font_size (int): Maksymalny rozmiar czcionki
        max_width (int): Maksymalna szerokość dostępna dla tekstu
        max_height (int): Maksymalna wysokość dostępna dla tekstu
        padding (int): Margines wewnętrzny
        
    Returns:
        tuple: (font, font_size, lines) - czcionka, rozmiar czcionki i linie tekstu
    """
    font_size = max_font_size
    min_font_size = 20
    available_width = max_width - 2 * padding
    available_height = max_height - 2 * padding
    words = text.split()
    
    while font_size >= min_font_size:
        font = load_system_font(FONT_STYLES.get(font_style, FONT_STYLES["Klasyczny"]), font_size)
        lines = []
        current_line = []
        
        # Układanie słów w linie
        for word in words:
            test_line = ' '.join(current_line + [word])
            width, _ = measure_text(test_line, font)
            
            if width <= available_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    break
        
        # Dodaj ostatnią linię
        if current_line:
            lines.append(' '.join(current_line))
        
        # Sprawdź czy wszystkie słowa zostały umieszczone
        if len(lines) == 0 or sum(len(line.split()) for line in lines) < len(words):
            font_size -= 2
            continue
        
        # Sprawdź wysokość
        line_height = int(font_size * 1.3)
        total_text_height = line_height * len(lines)
        
        if total_text_height <= available_height:
            return font, font_size, lines
        
        font_size -= 2
    
    # Fallback dla minimalnego rozmiaru
    font = load_system_font(FONT_STYLES.get(font_style, FONT_STYLES["Klasyczny"]), min_font_size)
    lines = _fallback_text_layout(words, font, available_width, available_height, min_font_size)
    
    return font, min_font_size, lines

def _fallback_text_layout(words, font, available_width, available_height, min_font_size):
    """
    Ostateczny podział tekstu na linie przy minimalnej czcionce
    """
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        width, _ = measure_text(test_line, font)
        
        if width <= available_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    # Przytnij jeśli za długie
    line_height = int(min_font_size * 1.3)
    max_lines = available_height // line_height
    
    if len(lines) > max_lines:
        lines = lines[:max_lines-1]
        if len(lines) > 0:
            lines[-1] = lines[-1] + "..."
    
    return lines

def add_text_to_image(image, text, font_size=60, text_color=(255, 255, 255), position="center", 
                   padding=50, font_style="Klasyczny", custom_x_percent=50, custom_y_percent=50, 
                   shadow_color=(0, 0, 0, 200)):
    """
    Dodaje tekst do obrazu z automatycznym dopasowaniem rozmiaru
    """
    try:
        # Konwertuj obraz do RGBA
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        text_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_layer)
        
        # Normalizacja tekstu
        text = _normalize_text(text)
        
        # Automatycznie dopasuj rozmiar czcionki
        font, adjusted_font_size, lines = auto_adjust_font_size(
            text, font_style, font_size, image.width, image.height, padding
        )
        
        # Renderuj tekst
        _render_text_lines(draw, lines, font, adjusted_font_size, text_color, 
                          shadow_color, position, image.size, padding,
                          custom_x_percent, custom_y_percent)
        
        # Połącz warstwy
        result = Image.alpha_composite(image, text_layer)
        return result.convert('RGB')
    
    except Exception as e:
        st.warning(f"Błąd dodawania tekstu: {str(e)}")
        return image.convert('RGB')

def _normalize_text(text):
    """
    Normalizuje tekst do bezpiecznego formatu
    """
    if isinstance(text, bytes):
        text = text.decode('utf-8', errors='replace')
    
    text = unicodedata.normalize('NFC', text)
    text = ''.join(c for c in text if ord(c) >= 32 or c == '\n')
    
    return text

def _render_text_lines(draw, lines, font, font_size, text_color, shadow_color, 
                      position, image_size, padding, custom_x_percent, custom_y_percent):
    """
    Renderuje linie tekstu na obrazie
    """
    line_height = int(font_size * 1.3)
    total_height = line_height * len(lines)
    image_width, image_height = image_size
    
    # Określ pozycję startową Y
    if position == "center":
        start_y = (image_height - total_height) // 2
    elif position == "top":
        start_y = padding
    elif position == "bottom":
        start_y = image_height - total_height - padding
    elif position == "custom":
        available_height = image_height - total_height - 2 * padding
        start_y = padding + (available_height * custom_y_percent // 100)
    else:
        start_y = (image_height - total_height) // 2
    
    # Renderuj każdą linię
    y = start_y
    for line in lines:
        width, _ = measure_text(line, font)
        
        # Określ pozycję X
        if position == "custom":
            available_width = image_width - width - 2 * padding
            x = padding + (available_width * custom_x_percent // 100)
        else:
            x = (image_width - width) // 2
        
        # Dodaj cień/obramowanie
        _add_text_shadow(draw, x, y, line, font, shadow_color)
        
        # Rysuj tekst
        draw.text((x, y), line, font=font, fill=text_color)
        y += line_height

def _add_text_shadow(draw, x, y, text, font, shadow_color):
    """
    Dodaje cień/obramowanie do tekstu
    """
    if not isinstance(shadow_color, tuple) or len(shadow_color) != 4:
        shadow_color = (0, 0, 0, 200)
    
    shadow_offset = 2
    shadow_positions = [
        (shadow_offset, shadow_offset), (shadow_offset, -shadow_offset),
        (-shadow_offset, shadow_offset), (-shadow_offset, -shadow_offset),
        (shadow_offset, 0), (-shadow_offset, 0),
        (0, shadow_offset), (0, -shadow_offset)
    ]
    
    for dx, dy in shadow_positions:
        draw.text((x + dx, y + dy), text, font=font, fill=shadow_color)