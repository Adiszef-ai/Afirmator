"""
Visual modules - obsługa wizualizacji, generowanie obrazów, cytaty wizualne
"""
from .visual_quote import display_visual_quote_section
from .gradient_generator import create_gradient_background
from .font_manager import setup_fonts, load_system_font, measure_text
from .text_renderer import auto_adjust_font_size, add_text_to_image
from .image_composer import create_visual_quote, get_size_in_cm

__all__ = [
    'display_visual_quote_section',
    'create_gradient_background',
    'setup_fonts',
    'load_system_font',
    'measure_text',
    'auto_adjust_font_size', 
    'add_text_to_image',
    'create_visual_quote',
    'get_size_in_cm'
]