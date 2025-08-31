"""
app/modules/visual_quote.py - Moduł obsługujący generowanie wizualnych cytatów z afirmacjami.
"""
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import os
from ui.components import spacer, centered_text, affirmation_card
# Importowanie stałych z modułu constants
from config.constants import (
    IMAGE_SIZES, GRADIENT_PRESETS, FONT_STYLES, 
    TEXT_COLORS, DPI_OPTIONS, FONT_DIR
)

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

def create_gradient_background(width, height, color1, color2, direction="vertical"):
    """
    Tworzy tło gradientowe.
    
    Args:
        width (int): Szerokość obrazu
        height (int): Wysokość obrazu
        color1 (tuple): Pierwszy kolor RGB
        color2 (tuple): Drugi kolor RGB
        direction (str): Kierunek gradientu ("vertical", "horizontal", "diagonal_tl_br", "diagonal_tr_bl", "radial")
    
    Returns:
        Image: Obraz z gradientem
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
            elif direction == "diagonal_tl_br":  # Z lewego górnego do prawego dolnego rogu
                value = int(255 * ((x / width + y / height) / 2))
            elif direction == "diagonal_tr_bl":  # Z prawego górnego do lewego dolnego rogu
                value = int(255 * ((1 - x / width + y / height) / 2))
            elif direction == "radial":  # Radialny gradient (od środka)
                center_x, center_y = width / 2, height / 2
                # Oblicz odległość od środka (znormalizowaną)
                distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                max_distance = ((width / 2) ** 2 + (height / 2) ** 2) ** 0.5  # Maksymalna odległość od środka
                value = int(255 * min(1.0, distance / max_distance))
            else:
                value = int(255 * (y / height))  # Domyślnie pionowy gradient
            mask_data.append(value)
    
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

def load_system_font(font_info, size):
    """
    Funkcja do ładowania czcionek ze stylów zdefiniowanych w FONT_STYLES.
    
    Args:
        font_info (dict): Informacje o czcionce z FONT_STYLES
        size (int): Rozmiar czcionki
        
    Returns:
        ImageFont: Załadowana czcionka lub domyślna w przypadku błędu
    """
    try:
        # Pobierz ścieżkę do czcionki z informacji o stylu
        font_path = font_info.get("font", "")
        return ImageFont.truetype(font_path, size)
    except Exception:
        # Fallback do domyślnej czcionki
        return ImageFont.load_default()

def measure_text(text, font):
    """
    Funkcja do mierzenia wymiarów tekstu.
    
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
            # Przybliżone szacowanie, gdy nie ma metod do pomiaru
            return len(text) * (font.size // 2), font.size
    except Exception:
        # Fallback dla sytuacji awaryjnych
        font_size = getattr(font, 'size', 12)
        return len(text) * (font_size // 2), font_size

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
    # Początkowy rozmiar czcionki
    font_size = max_font_size
    
    # Minimalny akceptowalny rozmiar czcionki
    min_font_size = 20
    
    # Maksymalna szerokość dostępna dla tekstu
    available_width = max_width - 2 * padding
    available_height = max_height - 2 * padding
    
    # Podziel tekst na słowa
    words = text.split()
    
    while font_size >= min_font_size:
        # Załaduj czcionkę z aktualnym rozmiarem
        font = load_system_font(FONT_STYLES.get(font_style, FONT_STYLES["Klasyczny"]), font_size)
        
        # Linie tekstu
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
                    # Jeśli pojedyncze słowo jest za długie, zmniejszamy czcionkę
                    break
        
        # Dodaj ostatnią linię
        if current_line:
            lines.append(' '.join(current_line))
        
        # Sprawdź czy wszystkie słowa zostały umieszczone w liniach
        if len(lines) == 0 or sum(len(line.split()) for line in lines) < len(words):
            # Nie wszystkie słowa się zmieściły, zmniejszamy czcionkę
            font_size -= 2
            continue
        
        # Sprawdź, czy tekst mieści się w wysokości
        line_height = int(font_size * 1.3)  # Dodajemy odstęp między liniami
        total_text_height = line_height * len(lines)
        
        if total_text_height <= available_height:
            # Tekst się mieści!
            return font, font_size, lines
        
        # Tekst nie mieści się w wysokości, zmniejszamy czcionkę
        font_size -= 2
    
    # Jeśli doszliśmy tutaj, oznacza to, że nawet z minimalnym rozmiarem czcionki
    # tekst nie mieści się. Zwracamy minimalny rozmiar i dzielimy tekst najlepiej jak się da.
    font = load_system_font(FONT_STYLES.get(font_style, FONT_STYLES["Klasyczny"]), min_font_size)
    
    # Próba ostatecznego podziału tekstu na linie
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
                # Jeśli pojedyncze słowo jest za długie, dodaj je i przejdź dalej
                lines.append(word)
    
    # Dodaj ostatnią linię
    if current_line:
        lines.append(' '.join(current_line))
    
    # Jeśli tekst wciąż jest za długi na wysokość, przytnij go
    line_height = int(min_font_size * 1.3)
    max_lines = available_height // line_height
    
    if len(lines) > max_lines:
        lines = lines[:max_lines-1]  # Zostaw miejsce na "..."
        if len(lines) > 0:
            lines[-1] = lines[-1] + "..."
    
    return font, min_font_size, lines

def add_text_to_image(image, text, font_size=60, text_color=(255, 255, 255), position="center", 
                   padding=50, font_style="Klasyczny", custom_x_percent=50, custom_y_percent=50, 
                   shadow_color=(0, 0, 0, 200)):
    try:
        # Konwertuj obraz do RGBA
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        # Stwórz warstwę dla tekstu
        text_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_layer)
        
        # Upewnij się, że tekst jest w Unicode
        if isinstance(text, bytes):
            text = text.decode('utf-8', errors='replace')
        
        # Normalizacja Unicode
        import unicodedata
        text = unicodedata.normalize('NFC', text)
        
        # Usuwamy tylko znaki kontrolne, zachowując polskie znaki
        text = ''.join(c for c in text if ord(c) >= 32 or c == '\n')
        
        # Automatycznie dopasuj rozmiar czcionki
        font, adjusted_font_size, lines = auto_adjust_font_size(
            text, 
            font_style, 
            font_size, 
            image.width, 
            image.height, 
            padding
        )
        
        # Oblicz wysokość tekstu
        line_height = int(adjusted_font_size * 1.3)
        total_height = line_height * len(lines)
        
        # Określ pozycję startową
        if position == "center":
            start_y = (image.height - total_height) // 2
        elif position == "top":
            start_y = padding
        elif position == "bottom":
            start_y = image.height - total_height - padding
        elif position == "custom":
            available_height = image.height - total_height - 2 * padding
            start_y = padding + (available_height * custom_y_percent // 100)
        else:
            start_y = (image.height - total_height) // 2
        
        # Rysuj każdą linię tekstu
        y = start_y
        for line in lines:
            width, _ = measure_text(line, font)
            
            # Określ pozycję x dla linii
            if position == "custom":
                available_width = image.width - width - 2 * padding
                x = padding + (available_width * custom_x_percent // 100)
            else:
                x = (image.width - width) // 2
            
            # Dodaj cień tekstu
            shadow_offset = 2  # Mniejszy offset dla delikatniejszej obwódki
            
            # Upewnij się, że shadow_color to tuple o 4 elementach (RGBA)
            if not isinstance(shadow_color, tuple) or len(shadow_color) != 4:
                shadow_color = (0, 0, 0, 200)  # Domyślny kolor
            
            # Rysuj cień wokół tekstu
            for dx, dy in [(shadow_offset, shadow_offset), 
                           (shadow_offset, -shadow_offset), 
                           (-shadow_offset, shadow_offset), 
                           (-shadow_offset, -shadow_offset),
                           (shadow_offset, 0), 
                           (-shadow_offset, 0), 
                           (0, shadow_offset), 
                           (0, -shadow_offset)]:
                draw.text((x + dx, y + dy), line, font=font, fill=shadow_color)
            
            # Rysuj tekst
            draw.text((x, y), line, font=font, fill=text_color)
            
            y += line_height
        
        # Połącz warstwy
        result = Image.alpha_composite(image, text_layer)
        return result.convert('RGB')
    
    except Exception as e:
        st.warning(f"Błąd dodawania tekstu: {str(e)}")
        return image.convert('RGB')

def create_visual_quote(text, background_type="gradient", gradient_colors=None, 
                       uploaded_image=None, text_color=(255, 255, 255), 
                       font_size=60, width=1080, height=1080, direction="vertical",
                       position="center", font_style="Klasyczny", custom_x_percent=50, custom_y_percent=50,
                       shadow_color=(0, 0, 0, 200)):
    """
    Tworzy wizualny cytat z afirmacją.
    
    Args:
        text (str): Tekst afirmacji
        background_type (str): Typ tła ("gradient" lub "image")
        gradient_colors (tuple): Kolory gradientu
        uploaded_image (Image): Wgrany obraz tła
        text_color (tuple): Kolor tekstu
        font_size (int): Rozmiar czcionki
        width (int): Szerokość obrazu
        height (int): Wysokość obrazu
        direction (str): Kierunek gradientu ("vertical" lub "horizontal")
        position (str): Pozycja tekstu ("center", "top", "bottom", "custom")
        font_style (str): Styl czcionki z FONT_STYLES
        custom_x_percent (int): Procentowa pozycja tekstu w poziomie (0-100)
        custom_y_percent (int): Procentowa pozycja tekstu w pionie (0-100)
        shadow_color (tuple): Kolor cienia tekstu (RGB + alpha)
    
    Returns:
        Image: Gotowy obraz z cytatem
    """
    try:
        # Upewnij się, że tekst jest typu string
        if not isinstance(text, str):
            text = str(text)
        
        # W przypadku bajtów, dekoduj do Unicode
        if isinstance(text, bytes):
            text = text.decode('utf-8', errors='replace')
        
        # Stwórz tło
        if background_type == "gradient" and gradient_colors:
            try:
                # Sprawdź, czy gradient_colors to string "custom"
                if gradient_colors == "custom":
                    # Użyj domyślnych kolorów gradientu
                    gradient_colors = [(74, 144, 226), (255, 107, 156)]
                
                image = create_gradient_background(width, height, gradient_colors[0], gradient_colors[1], direction)
            except Exception as e:
                st.error(f"Błąd tworzenia gradientu: {str(e)}")
                # Fallback do domyślnego gradientu
                image = create_gradient_background(width, height, (74, 144, 226), (255, 107, 156), "vertical")
        elif background_type == "image" and uploaded_image:
            try:
                # Dostosuj obraz do wymaganego rozmiaru
                uploaded_image = uploaded_image.resize((width, height), 
                                                    Image.Resampling.LANCZOS 
                                                    if hasattr(Image, 'Resampling') 
                                                    else Image.LANCZOS)
                image = uploaded_image
            except Exception as e:
                st.error(f"Błąd przetwarzania obrazu: {str(e)}")
                # Fallback do domyślnego gradientu
                image = create_gradient_background(width, height, (74, 144, 226), (255, 107, 156), "vertical")
        else:
            # Domyślne tło
            image = create_gradient_background(width, height, (74, 144, 226), (255, 107, 156), "vertical")
        
        # Dodaj tekst do obrazu
        final_image = add_text_to_image(
            image, text, font_size, text_color, position, 
            padding=50, font_style=font_style,
            custom_x_percent=custom_x_percent, custom_y_percent=custom_y_percent,
            shadow_color=shadow_color
        )
        return final_image
        
    except Exception as e:
        st.error(f"Błąd tworzenia obrazu: {str(e)}")
        image = Image.new('RGB', (width, height), (100, 100, 100))
        draw = ImageDraw.Draw(image)
        draw.text((width//2, height//2), "Błąd tworzenia obrazu", fill=(255, 255, 255))
        return image

def display_visual_quote_section():
    """
    Wyświetla sekcję generowania wizualnych cytatów.
    """
    spacer("2.5rem")
    st.markdown("<h2 style='text-align: center;'>Wizualny Cytat</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align: center; width: 100%;">
            <h8>Stwórz piękny obrazek ze swoją afirmacją</h8>
        </div>
    """, unsafe_allow_html=True)
    spacer("1.5rem")

    # Inicjalizacja zmiennych stanu
    if 'visual_quote_generated' not in st.session_state:
        st.session_state.visual_quote_generated = False
    
    # Funkcja do akceptacji własnego tekstu
    def accept_custom_text():
        if not st.session_state.custom_affirmation or len(st.session_state.custom_affirmation.strip()) == 0:
            st.warning("Proszę wpisać tekst afirmacji!")
            return False
        return True

    centered_text("Wybór afirmacji")
    # Główna zawartość w kolumnach
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Wybór źródła tekstu
        text_source = st.radio(
            "Źródło tekstu afirmacji:",
            ["Wybierz z historii", "Wpisz własny tekst"],
            horizontal=True,
            key="text_source_radio"
        )
        
        selected_affirmation = None
        
        if text_source == "Wybierz z historii":
            if st.session_state.history:
                selected_affirmation = st.selectbox(
                    "Wybierz afirmację:",
                    st.session_state.history,
                    format_func=lambda x: x[:100] + "..." if len(x) > 100 else x,
                    key="history_selection"
                )
                # Wyświetlenie wybranej afirmacji w karcie
                centered_text("Wybrana afirmacja")
                affirmation_card(selected_affirmation)
                spacer("1rem")
            else:
                st.warning("Historia jest pusta. Najpierw wygeneruj afirmację!")
                return
        else:
            if 'custom_affirmation' not in st.session_state:
                st.session_state.custom_affirmation = ""
                
            custom_text = st.text_area(
                "Wpisz własny tekst afirmacji:",
                height=100,
                placeholder="Wpisz swoją afirmację...",
                max_chars=300,
                key="custom_affirmation"
            )
            
            # Przycisk do akceptacji własnej afirmacji
            if st.button("Akceptuj afirmację", use_container_width=True, type="primary"):
                if accept_custom_text():
                    selected_affirmation = st.session_state.custom_affirmation
                    # Wyświetlenie wybranej afirmacji w karcie
                    centered_text("Wybrana afirmacja")
                    affirmation_card(selected_affirmation)
                    spacer("1rem")
            
        # Sprawdź czy jest afirmacja do pracy
        if selected_affirmation:
            # Opcje tworzenia obrazu
            spacer("1rem")
            centered_text("Tło obrazka")
            background_type = st.radio(
                "Typ tła:",
                ["Gradient", "Własny obraz"],
                horizontal=True
            )
            
            if background_type == "Gradient":
                col_a, col_b = st.columns(2)
                with col_a:
                    gradient_preset = st.selectbox(
                        "Wybierz preset gradientu:",
                        list(GRADIENT_PRESETS.keys())
                    )
                with col_b:
                    gradient_direction = st.selectbox(
                        "Kierunek gradientu:",
                        ["Pionowy", "Poziomy", "Ukośny ↘", "Ukośny ↙", "Promienisty"]
                    )
                    
                    # Mapowanie polskich nazw kierunków na wartości techniczne
                    direction_map = {
                        "Pionowy": "vertical",
                        "Poziomy": "horizontal",
                        "Ukośny ↘": "diagonal_tl_br",  # Z lewego górnego do prawego dolnego
                        "Ukośny ↙": "diagonal_tr_bl",  # Z prawego górnego do lewego dolnego
                        "Promienisty": "radial"
                    }
                    direction = direction_map[gradient_direction]
                
                # Sprawdź, czy wybrano własny gradient
                if gradient_preset == "Własny":
                    # Pokaż dwa color pickery w dwóch kolumnach
                    custom_col1, custom_col2, custom_col3, custom_col4 = st.columns(4)
                    with custom_col1:
                        custom_gradient_start = st.color_picker(
                            "Kolor początkowy:",
                            "#4A90E2",  # Domyślny niebieski
                            key="gradient_start_color"
                        )
                        # Konwersja hex koloru na RGB
                        gradient_start_rgb = tuple(int(custom_gradient_start.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
                    
                    with custom_col2:
                        custom_gradient_end = st.color_picker(
                            "Kolor końcowy:",
                            "#FF6B9C",  # Domyślny różowy
                            key="gradient_end_color"
                        )
                        # Konwersja hex koloru na RGB
                        gradient_end_rgb = tuple(int(custom_gradient_end.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
                    
                    # Ustaw kolory gradientu
                    gradient_colors = [gradient_start_rgb, gradient_end_rgb]
                else:
                    gradient_colors = GRADIENT_PRESETS[gradient_preset]
                
                uploaded_image = None
            else:
                uploaded_file = st.file_uploader(
                    "Wgraj własne tło",
                    type=['png', 'jpg', 'jpeg'],
                    help="Zalecany rozmiar: 1080x1080px"
                )
                
                if uploaded_file:
                    uploaded_image = Image.open(uploaded_file)
                else:
                    uploaded_image = None
                    gradient_colors = GRADIENT_PRESETS["Zachód słońca"]
            
            # Opcje rozmiaru
            centered_text("Rozmiar obrazka")
            col_a, col_b = st.columns(2)
            
            with col_a:
                size_preset = st.selectbox(
                    "Wybierz format:",
                    list(IMAGE_SIZES.keys()),
                    help="Rozmiary dostosowane do różnych zastosowań"
                )
            
            with col_b:
                # Opcja wyboru rozdzielczości
                selected_dpi_label = st.selectbox(
                    "Zastosowanie:",
                    list(DPI_OPTIONS.keys()),
                    help="Wybierz przeznaczenie obrazka"
                )
                selected_dpi = DPI_OPTIONS[selected_dpi_label]
            
            # Jeśli wybrano własny rozmiar
            if size_preset == "Własny rozmiar":
                with col_b:
                    custom_width = st.number_input("Szerokość (px):", min_value=300, max_value=5000, value=1080, step=10)
                with col_a:
                    custom_height = st.number_input("Wysokość (px):", min_value=300, max_value=5000, value=1080, step=10)
                
                image_width, image_height = custom_width, custom_height
                
                # Wyświetl rozmiar w cm dla własnego rozmiaru
                width_cm, height_cm = get_size_in_cm(image_width, image_height)
            else:
                image_width, image_height = IMAGE_SIZES[size_preset]
                
                # Wyświetl rozmiar w pikselach i centymetrach
                width_cm, height_cm = get_size_in_cm(image_width, image_height)
            
            # Przelicz rozmiary dla wybranego DPI
            width_cm_for_dpi, height_cm_for_dpi = get_size_in_cm(image_width, image_height, selected_dpi)
            st.info(f"📏Rozmiar do druku przy {selected_dpi} DPI: {width_cm_for_dpi:.1f} x {height_cm_for_dpi:.1f} cm")
            
            # Opcje tekstu
            centered_text("Opcje tekstu")
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                text_color_option = st.selectbox(
                    "Kolor tekstu:",
                    list(TEXT_COLORS.keys())
                )
                
                # Obsługa własnego koloru tekstu
                if text_color_option == "Własny":
                    
                    custom_text_color = st.color_picker(
                        "Wybierz kolor tekstu:",
                        "#FFFFFF",  # Domyślny kolor - biały
                        key="custom_text_color_picker"
                    )
                    # Konwersja hex koloru na RGB
                    text_color = tuple(int(custom_text_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
                    
                    # Dodaj wybór koloru obramowania/cienia
                    custom_shadow_color_hex = st.color_picker(
                        "Wybierz kolor obramowania:",
                        "#000000",  # Domyślny kolor cienia - czarny
                        key="custom_shadow_color_picker"
                    )
                    # Sprawdź, czy custom_shadow_color_hex jest stringiem (wartością z color_picker)
                    if isinstance(custom_shadow_color_hex, str):
                        # Konwersja hex koloru na RGB z dodaniem kanału alpha
                        shadow_color_rgb = tuple(int(custom_shadow_color_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
                        # Dodajemy kanał alpha (przezroczystość)
                        shadow_color = shadow_color_rgb + (200,)  # Alpha 200 (częściowo przezroczysty)
                    else:
                        # Jeśli to już tuple, użyj go bezpośrednio
                        shadow_color = custom_shadow_color_hex
                    
                    # Zapisujemy kolor cienia w zmiennej sesji do późniejszego wykorzystania
                    st.session_state['shadow_color_value'] = shadow_color
                else:
                    text_color = TEXT_COLORS[text_color_option]
                    # Przywracamy domyślny kolor cienia (czarny z przezroczystością)
                    st.session_state['shadow_color_value'] = (0, 0, 0, 200)
            with col_b:            
                font_style_selection = st.selectbox(
                    "Styl czcionki:",
                    list(FONT_STYLES.keys()),
                    key="font_style_selector"
                )
            
            with col_c:
                text_position = st.selectbox(
                    "Pozycja tekstu:",
                    ["Środek", "Góra", "Dół", "Niestandardowa"]
                )
                position_map = {"Środek": "center", "Góra": "top", "Dół": "bottom", "Niestandardowa": "custom"}
                position = position_map[text_position]
                
            # Dodatkowe opcje dla niestandardowej pozycji tekstu
            if text_position == "Niestandardowa":
                col_custom_x, col_custom_y = st.columns(2)
                with col_custom_x:
                    custom_x_percent = st.slider(
                        "Pozycja pozioma (%):",
                        min_value=0,
                        max_value=100,
                        value=50,
                        help="0% = lewa krawędź, 100% = prawa krawędź"
                    )
                with col_custom_y:
                    custom_y_percent = st.slider(
                        "Pozycja pionowa (%):",
                        min_value=0,
                        max_value=100,
                        value=50,
                        help="0% = góra, 100% = dół"
                    )
            else:
                custom_x_percent = 50
                custom_y_percent = 50
                      
            # Maksymalny rozmiar czcionki
            font_size = st.slider(
                "Preferowany rozmiar czcionki (maksymalny):",
                min_value=30,
                max_value=100,
                value=60,
                step=5,
                help="Jeśli tekst nie zmieści się, rozmiar zostanie automatycznie zmniejszony"
            )
            
            # Generowanie obrazu
            if st.button("Wygeneruj wizualny cytat", use_container_width=True):
                with st.spinner("Generuję obrazek..."):
                    try:
                        if background_type == "Gradient":
                            # Używamy zmapowanego kierunku gradientu
                            
                            # Zabezpieczamy tekst przed problemami z kodowaniem
                            # Wstępna normalizacja tekstu do zastosowania w obrazie
                            norm_text = selected_affirmation
                            if isinstance(norm_text, bytes):
                                norm_text = norm_text.decode('utf-8', errors='replace')
                            
                            # Pobierz kolor cienia z sesji
                            shadow_color = st.session_state.get('shadow_color_value', (0, 0, 0, 200))
                            
                            # Upewnij się, że kolor cienia jest tuplem o 4 elementach (RGBA)
                            if not isinstance(shadow_color, tuple) or len(shadow_color) != 4:
                                shadow_color = (0, 0, 0, 200)  # Domyślny kolor cienia
                            
                            image = create_visual_quote(
                                text=norm_text,
                                background_type="gradient",
                                gradient_colors=gradient_colors,
                                uploaded_image=None,
                                text_color=text_color,
                                font_size=font_size,
                                width=image_width,
                                height=image_height,
                                direction=direction,
                                position=position,
                                font_style=font_style_selection,
                                custom_x_percent=custom_x_percent,
                                custom_y_percent=custom_y_percent,
                                shadow_color=shadow_color
                            )
                        else:  # Własny obraz
                            if uploaded_image is None:
                                st.warning("Proszę wgrać obraz tła!")
                                return
                                
                            # Zabezpieczamy tekst przed problemami z kodowaniem
                            norm_text = selected_affirmation
                            if isinstance(norm_text, bytes):
                                norm_text = norm_text.decode('utf-8', errors='replace')
                                
                            # Pobierz kolor cienia z sesji
                            shadow_color = st.session_state.get('shadow_color_value', (0, 0, 0, 200))
                            
                            # Upewnij się, że kolor cienia jest tuplem o 4 elementach (RGBA)
                            if not isinstance(shadow_color, tuple) or len(shadow_color) != 4:
                                shadow_color = (0, 0, 0, 200)  # Domyślny kolor cienia
                            
                            image = create_visual_quote(
                                text=norm_text,
                                background_type="image",
                                gradient_colors=None,
                                uploaded_image=uploaded_image,
                                text_color=text_color,
                                font_size=font_size,
                                width=image_width,
                                height=image_height,
                                position=position,
                                font_style=font_style_selection,
                                custom_x_percent=custom_x_percent,
                                custom_y_percent=custom_y_percent,
                                shadow_color=shadow_color
                            )
                        
                        # Ustawienie flagi wygenerowanego obrazu
                        st.session_state.visual_quote_generated = True
                        st.markdown("---")

                        st.markdown("""
                            <div style="text-align: center; width: 100%;">
                                <h8> Twój wizualny cytat:</h8>
                            </div>
                        """, unsafe_allow_html=True)
                        spacer("2rem")  # Dodanie większego odstępu
                        # Wyświetl podgląd
                        st.image(image, use_container_width=True)

                        # Przycisk pobierania
                        buf = io.BytesIO()
                        
                        # Zapisujemy obraz bezpośrednio bez żadnych dodatkowych metadanych
                        # To powinno uniknąć problemów z kodowaniem znaków
                        image = image.convert('RGB')  # Upewnij się, że obraz jest w formacie RGB
                        image.save(buf, format='PNG', optimize=True)
                        byte_im = buf.getvalue()
                        
                        b64 = base64.b64encode(byte_im).decode()
                        
                        # Używamy prostej nazwy pliku bez znaków specjalnych
                        filename = f"afirmacja_{image_width}x{image_height}.png"
                        
                        href = f"""
                            <div style="text-align: center; margin-top: 1rem;">
                                <a href="data:image/png;base64,{b64}" 
                                   download="{filename}" 
                                   class="download-button">
                                    💾 Pobierz obrazek
                                </a>
                            </div>
                        """
                        st.markdown(href, unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.error(f"Błąd podczas generowania obrazka: {str(e)}")
    
    # Wskazówki użycia - wyświetlane tylko po wygenerowaniu obrazu
    if st.session_state.visual_quote_generated:
        spacer("1.5rem")
        st.markdown("---")
        st.markdown("""
        <div style="padding: 15px; border-radius: 10px; margin-top: 20px;">
            <h5 style="margin-top: 0;">💡 Jak korzystać z wizualnych cytatów</h5>
            <ul style="text-align: left; margin-top: 0.2rem;">
                <li>Umieść obrazek z afirmacją w miejscu, które często widzisz (np. tapeta telefonu, ekran komputera)</li>
                <li>Używaj różnych formatów - mniejsze do social media, większe do wydruku</li>
                <li>Dopasuj kolory i czcionkę do swoich preferencji</li>
                <li>Wydrukuj afirmację i umieść ją w widocznym miejscu (np. lodówka, lustro, biurko)</li>
                <li>Zmień wizualny cytat co tydzień, aby utrzymać świeżość przekazu</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)