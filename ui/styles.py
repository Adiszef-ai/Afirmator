"""
Style CSS dla aplikacji Afirmator - wersja z naprawionymi gradientami.
"""
import streamlit as st

def inject_custom_css():
    """
    Wstrzykuje niestandardowy CSS do aplikacji.
    """
    # Definicje kolorów dla trybów jasnego i ciemnego
    light_styles = """
    :root {
        --primary-color: #4A90E2;
        --secondary-color: #FF6B9C;
        --background-color: #F8FAFC;
        --secondary-background-color: #FFFFFF;
        --text-color: #FFFFFF;
        --card-shadow: 0 8px 16px rgba(74, 144, 226, 0.15);
        --card-shadow-hover: 0 12px 24px rgba(74, 144, 226, 0.25);
        --affirmation-bg: #FFF0F7;
        --affirmation-border: #FF6B9C;
        --button-gradient-start: #4A90E2;
        --button-gradient-end: #FF6B9C;
        --button-hover-gradient-start: #FF6B9C;
        --button-hover-gradient-end: #F687B3;
        --button-text-color: #FFFFFF;
        --button-glow-color: rgba(74, 144, 226, 0.2);
        --button-hover-glow-color: rgba(255, 107, 156, 0.3);
        --card-gradient-start: #4A90E2;
        --card-gradient-end: #FF6B9C;
        --input-border: #E2E8F0;
        --input-focus-border: #4A90E2;
        --sidebar-gradient-start: #4A90E2;
        --sidebar-gradient-end: #FF6B9C;
        --affirmation-text-color: white;
    }
    """
    
    dark_styles = """
    :root {
        --primary-color: #64B5F6;
        --secondary-color: #4A90E2;
        --background-color: #1A202C;
        --secondary-background-color: #2D3748;
        --text-color: #F7FAFC;
        --card-shadow: 0 8px 16px rgba(246, 135, 179, 0.4);
        --card-shadow-hover: 0 12px 24px rgba(246, 135, 179, 0.4);
        --affirmation-bg: #362A35;
        --affirmation-border: #4A90E2;
        --button-gradient-start: #64B5F6;
        --button-gradient-end: #4A90E2;
        --button-hover-gradient-start: #4A90E2;
        --button-hover-gradient-end: #4A90E2;
        --button-text-color: white;
        --button-glow-color: rgba(100, 181, 246, 0.3);
        --button-hover-glow-color: rgba(246, 135, 179, 0.4);
        --card-gradient-start: #E2E8F0;
        --card-gradient-end: #553C9A;
        --input-border: #4A5568;
        --input-focus-border: #64B5F6;
        --sidebar-gradient-start: #2C5282;
        --sidebar-gradient-end: #553C9A;
        --affirmation-text-color: white;
    }
    """
    
    # Wspólne style
    common_styles = """

    /* Globalne style */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        font-size: 18px !important;
    }
    
    /* Główny kontener */
    .block-container {
        max-width: 1200px !important;
        padding: 2rem 1rem !important;
    }
    
    /* Nagłówki */
    h1 {
        font-size: 5rem !important;
        font-weight: 700;
        margin-bottom: 0.5rem !important;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
    
    h2 {
        font-size: 2.5rem !important;
        font-weight: 600;
        margin-bottom: 1.5rem !important;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
    
    h3 {
        font-size: 1.5rem !important;
        font-weight: 600;
        margin-bottom: 1rem !important;
        color: var(--secondary-color);
        text-align: center;
        
    }
    h8 {
        font-size: 1.5rem !important;
        font-weight: 600;
        margin-bottom: 1rem !important;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
        
    /* Karty afirmacji */
    .affirmation-card {
        background: linear-gradient(135deg, var(--card-gradient-start), var(--card-gradient-end)) !important;
        border-left: 6px solid var(--affirmation-border);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem auto;
        font-size: 1.3rem !important;
        line-height: 1.8;
        box-shadow: var(--card-shadow);
        max-width: 800px;
        position: relative;
        transition: all 0.3s ease;
        color: var(--affirmation-text-color) !important;
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 150px;
        text-align: center;
    }
    
    .affirmation-card:hover {
        transform: translateY(-px);
        box-shadow: var(--card-shadow-hover);
    }
    
    /* Fix dla tekstu w kartach afirmacji */
    .affirmation-card p,
    .affirmation-card span,
    .affirmation-card div {
        color: var(--affirmation-text-color) !important;
        text-align: center;
        width: 100%;
        margin: 0;
        padding: 0;
    }
    
    /* Specjalny fix dla markdown w karcie afirmacji */
    .affirmation-card .element-container {
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .affirmation-card .stMarkdown {
        width: 100%;
        margin: 0;
        padding: 0;
    }
    
    /* Karty na ekranie powitalnym */
    .welcome-card {
        background: linear-gradient(135deg, var(--card-gradient-start), var(--card-gradient-end)) !important;
        border-radius: 15px;
        padding: 1.5rem 1rem;  /* Zmniejszony padding */
        height: 160px;  /* Zmniejszona wysokość */
        margin: 0.5rem 0;
        box-shadow: var(--card-shadow);
        color: white;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        transition: transform 0.5s ease, box-shadow 0.5s ease;
        position: relative;
        overflow: hidden;
        border: 2px solid rgba(255, 255, 255, 0.15);
    }
    
    .welcome-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--card-shadow-hover);
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    .welcome-card-icon {
        font-size: 1.8rem;  /* Zmniejszony rozmiar ikony */
        margin-bottom: 0.4rem;  /* Zmniejszony margines */
    }
    
    .welcome-card-title {
        font-size: 1.2rem !important;  /* Zmniejszony rozmiar tytułu */
        font-weight: 600;
        margin-bottom: 0.0rem !important;  /* Zmniejszony margines */
        color: white !important;
    }
    
    .welcome-card-description {
        font-size: 0.95rem;  /* Zmniejszony rozmiar opisu */
        opacity: 0.9;
        margin: 0;
        line-height: 0.8;  /* Zmniejszony odstęp między liniami */
    }
    

    
    /* Przyciski */
    .stButton button {
        width: 100%;
        background: linear-gradient(135deg, var(--button-gradient-start), var(--button-gradient-end));
        color: var(--button-text-color);
        margin: 1.5rem 0;
        border: none;
        border-radius: 12px;
        font-size: 1rem !important;
        font-weight: 600;
        padding: 0.75rem 1.5rem !important;
        box-shadow: 0 4px 12px var(--button-glow-color);
        transition: all 0.8s ease;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, var(--button-hover-gradient-start), var(--button-hover-gradient-end));
        color: var(--button-text-color);
        transform: translateY(-2px);
        box-shadow: 0 6px 16px var(--button-hover-glow-color);
    }
    
    /* Przycisk pobierania */
    .download-button {
        background: linear-gradient(135deg, var(--button-gradient-start), var(--button-gradient-end));
        color: var(--button-text-color);
        margin: 1.5rem 0;
        border: none;
        border-radius: 12px;
        font-size: 1rem !important;
        font-weight: 600;
        padding: 0.75rem 1.5rem !important;
        box-shadow: 0 4px 12px var(--button-glow-color);
        transition: all 0.8s ease;
        display: inline-block;
    }
    
    .download-button:hover {
        background: linear-gradient(135deg, var(--button-hover-gradient-start), var(--button-hover-gradient-end));
        transform: translateY(-2px);
        box-shadow: 0 6px 16px var(--button-hover-glow-color);
        text-decoration: none;
        color: var(--button-text-color);
    }
    
    /* Pola formularza */
    .stTextInput > div > div > input,
    .stTextArea textarea,
    .stSelectbox > div > div   {
        background: linear-gradient(135deg, var(--card-gradient-start), var(--card-gradient-end));
        border-radius: 10px;
        font-size: 1rem !important;
        color: white;
    }
    
    /* Usunięcie przedziałki w selectbox */
    .stSelectbox div[data-baseweb="select"] > div > div {
        border: none !important;
    }

    .stSelectbox div[data-baseweb="select"] > div > div > div {
        border: none !important;
    }

    .stSelectbox div[data-baseweb="select"] > div > div > div > div {
        border: none !important;
    }
    
    /* Fix dla placeholderów */
    .stTextInput > div > div > input::placeholder,
    .stTextArea textarea::placeholder {
        color: rgba(255, 255, 255, 0.7) !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea textarea:focus,
    .stSelectbox > div > div > div:focus {
        border-color: var(--input-focus-border);
        box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.25);
    }
    
    /* Licznik max_chars dla pól textarea */
    .stTextArea [data-baseweb="textarea"] + div {
        color: white !important;
        opacity: 0.8;
    }

    /* Licznik max_chars dla pól text_input */
    .stTextInput [data-baseweb="input"] + div {
        color: white !important;
        opacity: 0.8;
    }

    /* Gdy zostało mało znaków - textarea */
    .stTextArea [data-baseweb="textarea"] + div[style*="color: rgb(255, 0, 0)"] {
        color: #FFD6E8 !important;  /* Jasny różowy - bardziej widoczny w trybie ciemnym */
        opacity: 1;
    }

    /* Gdy zostało mało znaków - text_input */
    .stTextInput [data-baseweb="input"] + div[style*="color: rgb(255, 0, 0)"] {
        color: #FFD6E8 !important;  /* Jasny różowy - bardziej widoczny w trybie ciemnym */
        opacity: 1;
    }
    
/* Pojedyncza zakładka - ustaw elastyczną szerokość */
.stTabs [data-baseweb="tab"] {
    flex: 1 1 auto;
    border-radius: 10px;
    text-align: center;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0.75rem 0.5rem !important; /* Zmniejsz boczny padding */
}

/* Styl dla wybranej zakładki */
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)) !important;
    color: white !important;
    font-weight: 600;
}

/* Styl dla niewybranch zakładek - dla lepszego kontrastu */
.stTabs [aria-selected="false"] {
    background-color: rgba(220, 220, 220, 0.3);
    border: 1px solid rgba(0, 0, 0, 0.05);
}

/* Efekt hover na niewybranch zakładkach */
.stTabs [aria-selected="false"]:hover {
    background-color: rgba(220, 220, 220, 0.5);
    color: var(--secondary-color) !important;
}
    
    /* Sidebar */
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, var(--sidebar-gradient-start), var(--sidebar-gradient-end)) !important;
    }
    
    section[data-testid="stSidebar"] .element-container {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: white !important;
    }
    
    /* Przezroczyste tło dla pola wyszukiwania w historii */
    section[data-testid="stSidebar"] .stTextInput input,
    section[data-testid="stSidebar"] input[type="text"],
    section[data-testid="stSidebar"] .stTextInput > div > div > input,
    section[data-testid="stSidebar"] div[data-baseweb="input"] input {
        background: rgba(0, 0, 0, 0) !important;
        background-color: rgba(0, 0, 0, 0) !important;
        background-image: none !important;
        border: 2px solid rgba(255, 255, 255, 0.6) !important;
        color: white !important;
    }
    
    /* Nadpisanie tła dla wszystkich elementów wokół inputa */
    section[data-testid="stSidebar"] .stTextInput,
    section[data-testid="stSidebar"] .stTextInput > div,
    section[data-testid="stSidebar"] .stTextInput > div > div,
    section[data-testid="stSidebar"] div[data-baseweb="input"] {
        background: rgba(0, 0, 0, 0) !important;
        background-color: rgba(0, 0, 0, 0) !important;
    }
    
    section[data-testid="stSidebar"] .stTextInput input::placeholder,
    section[data-testid="stSidebar"] input[type="text"]::placeholder {
        color: rgba(255, 255, 255, 0.7) !important;
    }
    
    section[data-testid="stSidebar"] .stTextInput input:focus,
    section[data-testid="stSidebar"] input[type="text"]:focus,
    section[data-testid="stSidebar"] div[data-baseweb="input"] input:focus {
        border: 2px solid rgba(255, 255, 255, 0.9) !important;
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.2) !important;
        background: rgba(0, 0, 0, 0) !important;
        background-color: rgba(0, 0, 0, 0) !important;
    }
    
    /* Usunięcie wszystkich możliwych teł na inputach w sidebarze */
    section[data-testid="stSidebar"] input {
        background: rgba(0, 0, 0, 0) !important;
        background-color: rgba(0, 0, 0, 0) !important;
    }
    
    /* Nadpisanie stylu dla kontenera inputa */
    section[data-testid="stSidebar"] .stTextInput > div > div {
        background: rgba(0, 0, 0, 0) !important;
        box-shadow: none !important;
    }
    
    /* Przezroczyste tło dla selectbox w historii */
    section[data-testid="stSidebar"] .stSelectbox > div > div {
        background: transparent !important;
        border: 2px solid rgba(255, 255, 255, 0.6) !important;
        color: white !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div {
        background: transparent !important;
        border: 2px solid rgba(255, 255, 255, 0.6) !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div:hover {
        border: 2px solid rgba(255, 255, 255, 0.9) !important;
    }
    
    /* Kolor tekstu i ikon w selectbox */
    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] svg {
        fill: white !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] [data-baseweb="tag"] {
        background: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
    }
    
    /* Dropdown menu selectbox */
    .stSelectbox [data-baseweb="popover"] {
        background: rgba(46, 60, 78, 0.95) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    
    .stSelectbox [role="option"] {
        color: white !important;
    }
    
    .stSelectbox [role="option"]:hover,
    .stSelectbox [role="option"][aria-selected="true"] {
        background: rgba(255, 255, 255, 0.2) !important;
    }
    
    section[data-testid="stSidebar"] .stButton button {
        background: rgba(255, 255, 255, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
        color: white !important;
    }
    
    section[data-testid="stSidebar"] .stButton button:hover {
        background: rgba(255, 255, 255, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
    }
    
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.8) !important;
        margin: 1.5rem 0;
    }
    
    section[data-testid="stSidebar"] .stMetric label {
        color: rgba(255, 255, 255, 0.8) !important;
    }
    
    section[data-testid="stSidebar"] .stMetric [data-testid="stMetricValue"] {
        color: white !important;
        font-weight: 600 !important;
    }
    """
    
    # Wybór stylu w zależności od trybu
    if st.session_state.get('theme', 'light') == 'light':
        css = light_styles + common_styles
    else:
        css = dark_styles + common_styles
    
    st.markdown(f"""
        <style>
            {css}
        </style>
    """, unsafe_allow_html=True)