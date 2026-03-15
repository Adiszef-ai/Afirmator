"""
app/modules/visual_quote.py - Moduł obsługujący generowanie wizualnych cytatów z afirmacjami - zrefaktoryzowany.
"""
import streamlit as st
import os
from PIL import Image
import io
import base64
from ui.components import spacer, centered_text, affirmation_card
from config.constants import (
    get_image_sizes, get_gradient_presets, get_font_styles,
    get_text_colors, get_dpi_options
)
from config.translations import t
from .visual.font_manager import setup_fonts
from .visual.image_composer import create_visual_quote, get_size_in_cm
from utils.session_state import StateManager

# Inicjalizacja czcionek - przenieś do funkcji aby nie uruchamiać przy imporcie
# setup_fonts()  # Będzie wywołane w display_visual_quote_section()

def display_visual_quote_section():
    """
    Wyświetla sekcję generowania wizualnych cytatów.
    """
    # Inicjalizacja czcionek - teraz gdy st.set_page_config już się wykonał
    setup_fonts()

    spacer("2.5rem")
    st.markdown(f"<h2 style='text-align: center;'>{t('visual.title')}</h2>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style="text-align: center; width: 100%;">
            <h8>{t("visual.subtitle")}</h8>
        </div>
    """, unsafe_allow_html=True)
    spacer("1.5rem")

    # Wyświetl komunikat o czcionkach (jeśli jest zapisany)
    if 'font_setup_message' in st.session_state:
        font_msg = st.session_state['font_setup_message']
        if font_msg['type'] == 'success':
            st.success(font_msg['message'])
        elif font_msg['type'] == 'warning':
            st.warning(font_msg['message'].split('\n')[0])  # Tylko pierwsza linia
            st.info(font_msg['message'].split('\n')[1])  # Druga linia jako info
        # Usuń komunikat po wyświetleniu
        del st.session_state['font_setup_message']

    # Wyświetl komunikat o czyszczeniu cache (jeśli jest)
    if 'cache_cleared_message' in st.session_state:
        st.success(st.session_state['cache_cleared_message'])
        del st.session_state['cache_cleared_message']

    # Wyświetl komunikaty o folderze fontów (jeśli są)
    if 'font_folder_created' in st.session_state:
        st.info(st.session_state['font_folder_created'])
        del st.session_state['font_folder_created']

    if 'font_folder_error' in st.session_state:
        st.error(st.session_state['font_folder_error'])
        del st.session_state['font_folder_error']

    # Inicjalizacja zmiennych stanu
    if not StateManager.has_key('visual.quote_generated'):
        StateManager.set('visual.quote_generated', False)

    # Funkcja do akceptacji własnego tekstu
    def accept_custom_text():
        custom_text = StateManager.get('visual.custom_affirmation', '')
        if not custom_text or len(custom_text.strip()) == 0:
            st.warning(t("visual.enter_text_warning"))
            return False
        return True

    centered_text(t("visual.affirmation_choice"))
    # Główna zawartość w kolumnach
    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        # Wybór źródła tekstu
        text_source = st.radio(
            t("visual.text_source"),
            [t("visual.from_history"), t("visual.custom_text")],
            horizontal=True,
            key="text_source_radio"
        )

        selected_affirmation = None

        if text_source == t("visual.from_history"):
            history = StateManager.get('generator.history', [])
            if history:
                selected_affirmation = st.selectbox(
                    t("visual.select_affirmation"),
                    history,
                    format_func=lambda x: x[:100] + "..." if len(x) > 100 else x,
                    key="history_selection"
                )
                # Wyświetlenie wybranej afirmacji w karcie
                centered_text(t("visual.selected_affirmation"))
                affirmation_card(selected_affirmation)
                spacer("1rem")
            else:
                st.warning(t("visual.history_empty"))
                return
        else:
            if not StateManager.has_key('visual.custom_affirmation'):
                StateManager.set('visual.custom_affirmation', "")

            custom_text = st.text_area(
                t("visual.enter_custom"),
                height=100,
                placeholder=t("visual.custom_placeholder"),
                max_chars=300,
                key="custom_affirmation",
                value=StateManager.get('visual.custom_affirmation', '')
            )
            StateManager.set('visual.custom_affirmation', custom_text)

            # Przycisk do akceptacji własnej afirmacji
            if st.button(t("visual.accept"), use_container_width=True, type="primary"):
                if accept_custom_text():
                    selected_affirmation = StateManager.get('visual.custom_affirmation')
                    # Wyświetlenie wybranej afirmacji w karcie
                    centered_text(t("visual.selected_affirmation"))
                    affirmation_card(selected_affirmation)
                    spacer("1rem")

        # Sprawdź czy jest afirmacja do pracy
        if selected_affirmation:
            _display_image_options(selected_affirmation)

    # Wskazówki użycia
    if StateManager.get('visual.quote_generated', False):
        _display_usage_tips()

def _display_image_options(selected_affirmation):
    """
    Wyświetla opcje konfiguracji obrazu
    """
    spacer("1rem")
    centered_text(t("visual.background_title"))
    background_type = st.radio(
        t("visual.background_type"),
        [t("visual.gradient"), t("visual.custom_image")],
        horizontal=True
    )

    gradient_colors, uploaded_image, direction = _handle_background_options(background_type)
    image_width, image_height = _handle_size_options()

    # Opcje tekstu
    text_color, font_style_selection, position, custom_x_percent, custom_y_percent = _handle_text_options()
    font_size = _handle_font_size_option()

    # Generowanie obrazu
    if st.button(t("visual.generate"), use_container_width=True):
        _generate_visual_quote(
            selected_affirmation, background_type, gradient_colors, uploaded_image,
            text_color, font_size, image_width, image_height, direction, position,
            font_style_selection, custom_x_percent, custom_y_percent
        )

def _handle_background_options(background_type):
    """
    Obsługuje opcje wyboru tła
    """
    gradient_label = t("visual.gradient")
    custom_label = t("const.gradient.custom")

    if background_type == gradient_label:
        GRADIENT_PRESETS = get_gradient_presets()
        col_a, col_b = st.columns(2)
        with col_a:
            gradient_preset = st.selectbox(
                t("visual.gradient_preset"),
                list(GRADIENT_PRESETS.keys())
            )
        with col_b:
            direction_labels = [
                t("visual.direction_vertical"),
                t("visual.direction_horizontal"),
                t("visual.direction_diagonal_br"),
                t("visual.direction_diagonal_bl"),
                t("visual.direction_radial"),
            ]
            gradient_direction = st.selectbox(
                t("visual.gradient_direction"),
                direction_labels
            )

            direction_map = {
                t("visual.direction_vertical"): "vertical",
                t("visual.direction_horizontal"): "horizontal",
                t("visual.direction_diagonal_br"): "diagonal_tl_br",
                t("visual.direction_diagonal_bl"): "diagonal_tr_bl",
                t("visual.direction_radial"): "radial"
            }
            direction = direction_map[gradient_direction]

        # Obsługa własnego gradientu
        if gradient_preset == custom_label:
            gradient_colors = _handle_custom_gradient()
        else:
            gradient_colors = GRADIENT_PRESETS[gradient_preset]

        uploaded_image = None
    else:
        uploaded_file = st.file_uploader(
            t("visual.upload_bg"),
            type=['png', 'jpg', 'jpeg'],
            help=t("visual.upload_bg_help")
        )

        uploaded_image = Image.open(uploaded_file) if uploaded_file else None
        GRADIENT_PRESETS = get_gradient_presets()
        sunset_key = t("const.gradient.sunset")
        gradient_colors = GRADIENT_PRESETS.get(sunset_key, [(255, 94, 77), (255, 165, 0)]) if not uploaded_image else None
        direction = "vertical"

    return gradient_colors, uploaded_image, direction

def _handle_custom_gradient():
    """
    Obsługuje wybór własnych kolorów gradientu
    """
    custom_col1, custom_col2, _, _ = st.columns(4)

    with custom_col1:
        custom_gradient_start = st.color_picker(
            t("visual.gradient_start"),
            "#4A90E2",
            key="gradient_start_color"
        )
        gradient_start_rgb = tuple(int(custom_gradient_start.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

    with custom_col2:
        custom_gradient_end = st.color_picker(
            t("visual.gradient_end"),
            "#FF6B9C",
            key="gradient_end_color"
        )
        gradient_end_rgb = tuple(int(custom_gradient_end.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

    return [gradient_start_rgb, gradient_end_rgb]

def _handle_size_options():
    """
    Obsługuje opcje rozmiaru obrazu
    """
    IMAGE_SIZES = get_image_sizes()
    DPI_OPTIONS = get_dpi_options()
    custom_size_label = t("const.size.custom")

    centered_text(t("visual.size_title"))
    col_a, col_b = st.columns(2)

    with col_a:
        size_preset = st.selectbox(
            t("visual.size_format"),
            list(IMAGE_SIZES.keys()),
            help=t("visual.size_help")
        )

    with col_b:
        selected_dpi_label = st.selectbox(
            t("visual.dpi_label"),
            list(DPI_OPTIONS.keys()),
            help=t("visual.dpi_help")
        )
        selected_dpi = DPI_OPTIONS[selected_dpi_label]

    # Obsługa własnego rozmiaru
    if size_preset == custom_size_label:
        with col_b:
            custom_width = st.number_input(t("visual.width"), min_value=300, max_value=5000, value=1080, step=10)
        with col_a:
            custom_height = st.number_input(t("visual.height"), min_value=300, max_value=5000, value=1080, step=10)
        image_width, image_height = custom_width, custom_height
    else:
        image_width, image_height = IMAGE_SIZES[size_preset]

    # Wyświetl informacje o rozmiarze
    width_cm_for_dpi, height_cm_for_dpi = get_size_in_cm(image_width, image_height, selected_dpi)
    st.info(t("visual.print_size_info").format(dpi=selected_dpi, w=width_cm_for_dpi, h=height_cm_for_dpi))

    return image_width, image_height

def _handle_text_options():
    """
    Obsługuje opcje tekstu
    """
    TEXT_COLORS = get_text_colors()
    FONT_STYLES = get_font_styles()
    custom_color_label = t("const.color.custom")

    centered_text(t("visual.text_options"))
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        text_color_option = st.selectbox(
            t("visual.text_color"),
            list(TEXT_COLORS.keys())
        )

        if text_color_option == custom_color_label:
            text_color, shadow_color = _handle_custom_text_color()
        else:
            text_color = TEXT_COLORS[text_color_option]
            StateManager.set('visual.shadow_color_value', (0, 0, 0, 200))

    with col_b:
        font_style_selection = st.selectbox(
            t("visual.font_style"),
            list(FONT_STYLES.keys()),
            key="font_style_selector"
        )

    with col_c:
        pos_labels = [
            t("visual.pos_center"),
            t("visual.pos_top"),
            t("visual.pos_bottom"),
            t("visual.pos_custom"),
        ]
        text_position = st.selectbox(
            t("visual.text_position"),
            pos_labels
        )
        position_map = {
            t("visual.pos_center"): "center",
            t("visual.pos_top"): "top",
            t("visual.pos_bottom"): "bottom",
            t("visual.pos_custom"): "custom"
        }
        position = position_map[text_position]

    # Obsługa niestandardowej pozycji
    custom_x_percent, custom_y_percent = _handle_custom_position(text_position)

    return text_color, font_style_selection, position, custom_x_percent, custom_y_percent

def _handle_custom_text_color():
    """
    Obsługuje wybór własnego koloru tekstu
    """
    custom_text_color = st.color_picker(
        t("visual.custom_text_color"),
        "#FFFFFF",
        key="custom_text_color_picker"
    )
    text_color = tuple(int(custom_text_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

    custom_shadow_color_hex = st.color_picker(
        t("visual.custom_shadow_color"),
        "#000000",
        key="custom_shadow_color_picker"
    )

    if isinstance(custom_shadow_color_hex, str):
        shadow_color_rgb = tuple(int(custom_shadow_color_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        shadow_color = shadow_color_rgb + (200,)
    else:
        shadow_color = custom_shadow_color_hex

    StateManager.set('visual.shadow_color_value', shadow_color)

    return text_color, shadow_color

def _handle_custom_position(text_position):
    """
    Obsługuje niestandardową pozycję tekstu
    """
    custom_pos_label = t("visual.pos_custom")
    if text_position == custom_pos_label:
        col_custom_x, col_custom_y = st.columns(2)
        with col_custom_x:
            custom_x_percent = st.slider(
                t("visual.pos_horizontal"),
                min_value=0, max_value=100, value=50,
                help=t("visual.pos_horizontal_help")
            )
        with col_custom_y:
            custom_y_percent = st.slider(
                t("visual.pos_vertical"),
                min_value=0, max_value=100, value=50,
                help=t("visual.pos_vertical_help")
            )
    else:
        custom_x_percent = custom_y_percent = 50

    return custom_x_percent, custom_y_percent

def _handle_font_size_option():
    """
    Obsługuje opcje rozmiaru czcionki
    """
    return st.slider(
        t("visual.font_size"),
        min_value=30, max_value=100, value=60, step=5,
        help=t("visual.font_size_help")
    )

def _generate_visual_quote(selected_affirmation, background_type, gradient_colors, uploaded_image,
                          text_color, font_size, image_width, image_height, direction, position,
                          font_style_selection, custom_x_percent, custom_y_percent):
    """
    Generuje wizualny cytat
    """
    gradient_label = t("visual.gradient")
    with st.spinner(t("visual.generating")):
        try:
            if background_type == gradient_label:
                shadow_color = StateManager.get('visual.shadow_color_value', (0, 0, 0, 200))

                if not isinstance(shadow_color, tuple) or len(shadow_color) != 4:
                    shadow_color = (0, 0, 0, 200)

                image = create_visual_quote(
                    text=selected_affirmation,
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
                    st.warning(t("visual.upload_bg_warning"))
                    return

                shadow_color = StateManager.get('visual.shadow_color_value', (0, 0, 0, 200))

                if not isinstance(shadow_color, tuple) or len(shadow_color) != 4:
                    shadow_color = (0, 0, 0, 200)

                image = create_visual_quote(
                    text=selected_affirmation,
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

            # Wyświetl rezultat
            _display_result(image, image_width, image_height)

        except Exception as e:
            st.error(f"{t('visual.error')}{str(e)}")

def _display_result(image, image_width, image_height):
    """
    Wyświetla wygenerowany obraz i opcje pobierania
    """
    StateManager.set('visual.quote_generated', True)
    st.markdown("---")

    st.markdown(f"""
        <div style="text-align: center; width: 100%;">
            <h8> {t("visual.your_quote")}</h8>
        </div>
    """, unsafe_allow_html=True)
    spacer("2rem")

    # Wyświetl podgląd
    st.image(image, use_container_width=True)

    # Przycisk pobierania
    buf = io.BytesIO()
    image = image.convert('RGB')
    image.save(buf, format='PNG', optimize=True)
    byte_im = buf.getvalue()

    b64 = base64.b64encode(byte_im).decode()
    filename = f"afirmacja_{image_width}x{image_height}.png"

    href = f"""
        <div style="text-align: center; margin-top: 1rem;">
            <a href="data:image/png;base64,{b64}"
               download="{filename}"
               class="download-button">
                {t("visual.download")}
            </a>
        </div>
    """
    st.markdown(href, unsafe_allow_html=True)

def _display_usage_tips():
    """
    Wyświetla wskazówki użycia
    """
    spacer("1.5rem")
    st.markdown("---")
    st.markdown(f"""
    <div style="padding: 15px; border-radius: 10px; margin-top: 20px;">
        <h5 style="margin-top: 0;">{t("visual.tips_title")}</h5>
        <ul style="text-align: left; margin-top: 0.2rem;">
            <li>{t("visual.tip_1")}</li>
            <li>{t("visual.tip_2")}</li>
            <li>{t("visual.tip_3")}</li>
            <li>{t("visual.tip_4")}</li>
            <li>{t("visual.tip_5")}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
