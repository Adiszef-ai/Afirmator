"""
app/ui/styles.py - Style CSS loader dla aplikacji Afirmator.
"""
import streamlit as st
import os

def inject_custom_css():
    """
    Ładuje niestandardowy CSS z pliku external.
    """
    # Ścieżka do pliku CSS
    css_path = os.path.join(os.path.dirname(__file__), 'static', 'style.css')
    
    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
            
        # Dynamiczne ustawienie motywu na podstawie session_state
        theme_class = ""
        if st.session_state.get('theme', 'light') == 'dark':
            theme_class = 'data-theme="dark"'
        
        st.markdown(f"""
            <style>
                {css_content}
            {theme_class}
            </style>
        """, unsafe_allow_html=True)
        
    except FileNotFoundError:
        st.error("Nie znaleziono pliku style.css")