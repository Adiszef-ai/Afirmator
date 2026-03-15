"""
app/config/constants.py - Stałe i konfiguracja dla aplikacji Afirmator.
"""
import os
from config.translations import t

# Ścieżka do folderu z czcionkami (względem głównego katalogu)
FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "fonts")


def get_voice_options():
    """Zwraca opcje głosów w aktualnym języku."""
    return {
        t("const.voice.alloy"): "alloy",
        t("const.voice.echo"): "echo",
        t("const.voice.fable"): "fable",
        t("const.voice.onyx"): "onyx",
        t("const.voice.nova"): "nova",
        t("const.voice.shimmer"): "shimmer"
    }

def get_background_sounds():
    """Zwraca podkłady muzyczne w aktualnym języku."""
    return {
        t("const.sound.ocean"): "assets/sounds/ocean_waves.mp3",
        t("const.sound.rain"): "assets/sounds/gentle_rain.mp3",
        t("const.sound.meditation"): "assets/sounds/meditation_ambient.mp3",
        t("const.sound.piano"): "assets/sounds/soft_piano.mp3",
        t("const.sound.forest"): "assets/sounds/forest_nature.mp3",
        t("const.sound.stream"): "assets/sounds/flowing_stream.mp3",
        t("const.sound.white_noise"): "assets/sounds/white_noise.mp3"
    }

def get_affirmation_length_options():
    """Zwraca opcje długości afirmacji w aktualnym języku."""
    return [t("const.length.short"), t("const.length.medium"), t("const.length.long")]

def get_daily_affirmation_topics():
    """Zwraca tematy afirmacji dnia w aktualnym języku."""
    return [
        t("const.daily_topics.positivity"),
        t("const.daily_topics.gratitude"),
        t("const.daily_topics.strength"),
        t("const.daily_topics.productivity"),
        t("const.daily_topics.peace"),
        t("const.daily_topics.confidence"),
        t("const.daily_topics.health"),
        t("const.daily_topics.relationships"),
        t("const.daily_topics.growth"),
        t("const.daily_topics.success"),
    ]

def get_focus_areas():
    """Zwraca obszary skupienia w aktualnym języku."""
    return [
        t("const.focus.confidence"),
        t("const.focus.motivation"),
        t("const.focus.calm"),
        t("const.focus.relationships"),
        t("const.focus.health"),
        t("const.focus.wealth"),
        t("const.focus.custom"),
    ]

def get_emotion_states():
    """Zwraca stany emocjonalne w aktualnym języku."""
    return [
        t("const.emotion.neutral"),
        t("const.emotion.tired"),
        t("const.emotion.discouraged"),
        t("const.emotion.stressed"),
        t("const.emotion.hopeful"),
    ]

def get_affirmation_styles():
    """Zwraca style afirmacji w aktualnym języku."""
    return [t("const.style.gentle"), t("const.style.energetic"), t("const.style.poetic"), t("const.style.scientific")]

def get_affirmation_timing():
    """Zwraca pory stosowania afirmacji w aktualnym języku."""
    return [t("const.timing.daytime"), t("const.timing.morning"), t("const.timing.evening")]

def get_affirmation_tones():
    """Zwraca tony afirmacji w aktualnym języku."""
    return [
        t("const.tone.calm"),
        t("const.tone.energetic"),
        t("const.tone.uplifting"),
        t("const.tone.strong"),
    ]

def get_image_sizes():
    """Zwraca rozmiary obrazków w aktualnym języku."""
    return {
        "Instagram (1080x1080)": (1080, 1080),
        "A4 Pionowo (2480x3508)": (2480, 3508),
        "A4 Poziomo (3508x2480)": (3508, 2480),
        "A5 Pionowo (1748x2480)": (1748, 2480),
        "A5 Poziomo (2480x1748)": (2480, 1748),
        "HD (1920x1080)": (1920, 1080),
        "Facebook Cover (820x312)": (820, 312),
        "Pinterest (1000x1500)": (1000, 1500),
        "Twitter Header (1500x500)": (1500, 500),
        t("const.size.custom"): (0, 0)
    }

def get_gradient_presets():
    """Zwraca presety gradientów w aktualnym języku."""
    return {
        "Yin Yang": [(74, 144, 226), (255, 107, 156)],
        t("const.gradient.sunset"): [(255, 94, 77), (255, 165, 0)],
        "Ocean": [(0, 116, 217), (0, 185, 185)],
        t("const.gradient.forest"): [(34, 139, 34), (144, 238, 144)],
        t("const.gradient.sky"): [(135, 206, 235), (25, 25, 112)],
        t("const.gradient.sweetness"): [(255, 182, 193), (255, 105, 180)],
        t("const.gradient.custom"): "custom"
    }

def get_font_styles():
    """Zwraca style czcionek w aktualnym języku."""
    return {
        t("const.font.classic"): {"font": os.path.join(FONT_DIR, "Lato-Regular.ttf"), "style": "normal"},
        t("const.font.elegant"): {"font": os.path.join(FONT_DIR, "Lato-Italic.ttf"), "style": "italic"},
        t("const.font.bold"): {"font": os.path.join(FONT_DIR, "Lato-Bold.ttf"), "style": "bold"},
        t("const.font.decorative"): {"font": os.path.join(FONT_DIR, "Lato-Light.ttf"), "style": "normal"}
    }

def get_text_colors():
    """Zwraca opcje kolorów tekstu w aktualnym języku."""
    return {
        t("const.color.white"): (255, 255, 255),
        t("const.color.black"): (0, 0, 0),
        t("const.color.gold"): (255, 215, 0),
        t("const.color.silver"): (192, 192, 192),
        t("const.color.custom"): "custom"
    }

def get_dpi_options():
    """Zwraca opcje DPI w aktualnym języku."""
    return {
        t("const.dpi.high"): 300,
        t("const.dpi.standard"): 200,
        t("const.dpi.screen"): 72
    }

# === Backward compatibility - static defaults for imports that don't need translation ===
VOICE_OPTIONS = {
    "Jasny klarowny": "alloy",
    "Głęboki dramatyczny": "echo",
    "Ciepły narracyjny": "fable",
    "Mocny autorytatywny": "onyx",
    "Delikatny kobiecy": "nova",
    "Spokojny uspokajający": "shimmer"
}

BACKGROUND_SOUNDS = {
    "Szum morza": "assets/sounds/ocean_waves.mp3",
    "Deszcz": "assets/sounds/gentle_rain.mp3",
    "Medytacyjny ambient": "assets/sounds/meditation_ambient.mp3",
    "Delikatny fortepian": "assets/sounds/soft_piano.mp3",
    "Natura - las": "assets/sounds/forest_nature.mp3",
    "Strumień": "assets/sounds/flowing_stream.mp3",
    "Biały szum": "assets/sounds/white_noise.mp3"
}

AFFIRMATION_LENGTH_OPTIONS = ["1-2 zdania", "3-4 zdań", "5-6 zdań"]

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

GRADIENT_PRESETS = {
    "Yin Yang": [(74, 144, 226), (255, 107, 156)],
    "Zachód słońca": [(255, 94, 77), (255, 165, 0)],
    "Ocean": [(0, 116, 217), (0, 185, 185)],
    "Las": [(34, 139, 34), (144, 238, 144)],
    "Niebo": [(135, 206, 235), (25, 25, 112)],
    "Słodycz": [(255, 182, 193), (255, 105, 180)],
    "Własny": "custom"
}

FONT_STYLES = {
    "Klasyczny": {"font": os.path.join(FONT_DIR, "Lato-Regular.ttf"), "style": "normal"},
    "Elegancki": {"font": os.path.join(FONT_DIR, "Lato-Italic.ttf"), "style": "italic"},
    "Pogrubiony": {"font": os.path.join(FONT_DIR, "Lato-Bold.ttf"), "style": "bold"},
    "Dekoracyjny": {"font": os.path.join(FONT_DIR, "Lato-Light.ttf"), "style": "normal"}
}

TEXT_COLORS = {
    "Biały": (255, 255, 255),
    "Czarny": (0, 0, 0),
    "Złoty": (255, 215, 0),
    "Srebrny": (192, 192, 192),
    "Własny": "custom"
}

DPI_OPTIONS = {
    "Druk wysokiej jakości (300 DPI)": 300,
    "Druk standardowy (200 DPI)": 200,
    "Ekran/Web (72 DPI)": 72
}

# Początkowe wartości sesji (stary format dla zgodności wstecznej)
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
    'daily_audio_data': None,
    'player_audio_data': None,
    'music_affirmation_audio': None,
    'current_tab': "daily",  # Domyślnie pokazujemy zakładkę "Afirmacja dnia"
    'selected_provider': None,  # Wybór providera AI
    'show_openai_form': False  # Czy pokazać formularz OpenAI
}

# Nowy namespace-based stan sesji (zalecany sposób użycia)
DEFAULT_NAMESPACED_STATE = {
    # Generator namespace
    'generator.editing': False,
    'generator.edited_affirmation': "",
    'generator.affirmation': "",
    'generator.history': [],
    
    # Audio namespace
    'audio.data': None,
    'audio.selected_voice': "fable",
    'audio.daily_data': None,
    'audio.player_data': None,
    'audio.music_affirmation': None,
    
    # Daily namespace
    'daily.affirmation': None,
    'daily.affirmation_name': "",
    'daily.show_input': True,
    
    # App namespace
    'app.current_tab': "daily",
    'app.selected_provider': None,
    'app.show_openai_form': False,
    'app.api_key': "",
    'app.language': "pl"
}