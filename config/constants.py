"""
Stałe i konfiguracja dla aplikacji Afirmator.
"""

# Opcje głosów dla TTS
VOICE_OPTIONS = {
    "Jasny klarowny": "alloy",
    "Głęboki dramatyczny": "echo",
    "Ciepły narracyjny": "fable",
    "Mocny autorytatywny": "onyx",
    "Delikatny kobiecy": "nova",
    "Spokojny uspokajający": "shimmer"
}

# Predefiniowane podkłady muzyczne
BACKGROUND_SOUNDS = {
    "Szum morza": "assets/sounds/ocean_waves.mp3",
    "Deszcz": "assets/sounds/gentle_rain.mp3",
    "Medytacyjny ambient": "assets/sounds/meditation_ambient.mp3",
    "Delikatny fortepian": "assets/sounds/soft_piano.mp3",
    "Natura - las": "assets/sounds/forest_nature.mp3",
    "Strumień": "assets/sounds/flowing_stream.mp3",
    "Biały szum": "assets/sounds/white_noise.mp3"
}

# Opcje długości afirmacji
AFFIRMATION_LENGTH_OPTIONS = ["1-2 zdania", "3-4 zdań", "5-6 zdań"]

# Predefiniowane tematy dla afirmacji dnia
DAILY_AFFIRMATION_TOPICS = [
    "ogólna pozytywność i dobry nastrój",
    "wdzięczność i docenianie życia",
    "siła wewnętrzna i odporność",
    "produktywność i kreatywność",
    "spokój umysłu i redukcja stresu",
    "pewność siebie i samoakceptacja",
    "zdrowie i dobre samopoczucie",
    "relacje z innymi ludźmi",
    "rozwój osobisty i samodoskonalenie",
    "sukces i osiąganie celów"
]

# Opcje dla formularza generowania afirmacji
FOCUS_AREAS = ["Pewność siebie", "Motywacja", "Wyciszenie", "Relacje", "Zdrowie", "Bogactwo", "✨ Własne cele ✨"]

EMOTION_STATES = [
    "Neutralnie", 
    "Zmęczony/a", 
    "Zniechęcony/a", 
    "Zestresowany/a", 
    "Pełen/Pełna nadziei"
]

AFFIRMATION_STYLES = ["Łagodny", "Energiczny", "Poetycki", "Naukowy"]

AFFIRMATION_TIMING = ["W ciągu dnia", "Rano", "Wieczorem"]

AFFIRMATION_TONES = [
    "Spokojny", 
    "Energiczny", 
    "Podnoszący na duchu", 
    "Mocny i stanowczy"
]

# Predefiniowane rozmiary obrazków
IMAGE_SIZES = {
    "Instagram (1080x1080)": (1080, 1080),
    "A4 Pionowo (2480x3508)": (2480, 3508),
    "A4 Poziomo (3508x2480)": (3508, 2480),
    "A5 Pionowo (1748x2480)": (1748, 2480),
    "A5 Poziomo (2480x1748)": (2480, 1748),
    "HD (1920x1080)": (1920, 1080),
    "Facebook Cover (820x312)": (820, 312),
    "Pinterest (1000x1500)": (1000, 1500),
    "Twitter Header (1500x500)": (1500, 500),
    "Własny rozmiar": (0, 0)
}

# Predefiniowane gradienty
GRADIENT_PRESETS = {
    "Yin Yang": [(74, 144, 226), (255, 107, 156)],
    "Zachód słońca": [(255, 94, 77), (255, 165, 0)],
    "Ocean": [(0, 116, 217), (0, 185, 185)],
    "Las": [(34, 139, 34), (144, 238, 144)],
    "Niebo": [(135, 206, 235), (25, 25, 112)],
    "Słodycz": [(255, 182, 193), (255, 105, 180)],
    "Własny": "custom"  # Specjalna wartość wskazująca na wybór własny
}

import os

# Ścieżka do folderu z czcionkami (względem głównego katalogu)
FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "fonts")

# Predefiniowane style czcionek
FONT_STYLES = {
    "Klasyczny": {"font": os.path.join(FONT_DIR, "Lato-Regular.ttf"), "style": "normal"},
    "Elegancki": {"font": os.path.join(FONT_DIR, "Lato-Italic.ttf"), "style": "italic"},
    "Pogrubiony": {"font": os.path.join(FONT_DIR, "Lato-Bold.ttf"), "style": "bold"},
    "Dekoracyjny": {"font": os.path.join(FONT_DIR, "Lato-Light.ttf"), "style": "normal"}
}

# Opcje kolorów tekstu
TEXT_COLORS = {
    "Biały": (255, 255, 255),
    "Czarny": (0, 0, 0),
    "Złoty": (255, 215, 0),
    "Srebrny": (192, 192, 192),
    "Własny": "custom"  # Specjalna wartość wskazująca na wybór własny
}

# Opcje DPI
DPI_OPTIONS = {
    "Druk wysokiej jakości (300 DPI)": 300,
    "Druk standardowy (200 DPI)": 200,
    "Ekran/Web (72 DPI)": 72
}

# Początkowe wartości sesji
DEFAULT_SESSION_STATE = {
    'editing': False,
    'edited_affirmation': "",
    'audio_data': None,
    'affirmation': "",
    'selected_voice': "fable",
    'api_key': "",
    'history': [],
    'daily_affirmation': None,
    'daily_affirmation_name': "",
    'show_daily_affirmation_input': True,
    'show_daily_affirmation': False,
    'daily_audio_data': None,
    'player_audio_data': None,
    'music_affirmation_audio': None,
    'current_tab': "daily"  # Domyślnie pokazujemy zakładkę "Afirmacja dnia"
}