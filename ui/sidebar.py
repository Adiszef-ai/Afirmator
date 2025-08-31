"""
app/ui/sidebar.py - Komponenty interfejsu dla panelu bocznego - wersja ulepszona.
"""
import streamlit as st
from ui.components import button_with_icon
from utils.session_state import StateManager

def display_sidebar():
    """
    Wyświetla zawartość panelu bocznego z ulepszonym wyglądem.
    """
    with st.sidebar:

        st.markdown("""
            <h3 style='text-align: center; margin-top: -8px; color: white;'>Twój osobisty generator pozytywnych myśli</h3>

        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Historia afirmacji
        _display_history_section()
        
        st.markdown("---")
        
        # Statystyki
        _display_stats_section()
        
        st.markdown("---")
        
        # Pomoc i wsparcie
        _display_help_section()
        
        # Footer
        st.markdown("""
            <div class="sidebar-footer">
                <p style='font-size: 0.9rem; color: rgba(255, 255, 255, 0.7); margin: 0;'>
                    Stworzone z ❤️ w 2025
                </p>
            </div>
        """, unsafe_allow_html=True)

def _display_history_section():
    """
    Wyświetla sekcję historii afirmacji z ulepszoną funkcjonalnością.
    """
    st.markdown("<h3 style='color: white; a'>📚 Historia afirmacji</h3>", unsafe_allow_html=True)
    
    if StateManager.get('generator.history', []):
        # Filtrowanie i wyszukiwanie
        search_term = st.text_input(
            "Szukaj w historii", 
            placeholder="Wpisz frazę...",
            key="history_search",
            label_visibility="collapsed"
        )
        st.markdown("<div style='margin-bottom: 0.rem;'></div>", unsafe_allow_html=True)  # Spacer
        
        # Filtrowanie historii
        history = StateManager.get('generator.history', [])
        filtered_history = [
            aff for aff in history 
            if search_term.lower() in aff.lower()
        ] if search_term else history
        
        if filtered_history:
            # Dodajemy własny styl dla selectbox

            
            selected = st.selectbox(
                "Wybierz afirmację:",
                filtered_history,
                key="history_select",
                format_func=lambda x: x[:50] + "..." if len(x) > 50 else x,
                label_visibility="collapsed"
            )
            
            # Podgląd zaznaczonej afirmacji
            with st.expander("Podgląd", expanded=True):
                st.markdown(f"""
                    <div style='
                        font-style: italic; 
                        padding: 8px; 
                        background-color: rgba(255, 255, 255, 0.1);
                        border-radius: 8px;
                        font-size: 0.9rem;
                        color: white;
                    '>
                        {selected}
                    </div>
                """, unsafe_allow_html=True)
                
                if button_with_icon("Użyj tej afirmacji", "▶️", key="use_history_affirmation"):
                    StateManager.set('generator.edited_affirmation', selected)
                    StateManager.set('generator.affirmation', selected)
                    StateManager.set('audio.data', None)
                    StateManager.set('app.current_tab', "generator")
                    st.rerun()
        else:
            st.markdown("<p style='color: rgba(255, 255, 255, 0.8);'>Nie znaleziono afirmacji pasujących do wyszukiwania.</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='color: rgba(255, 255, 255, 0.8);'>Historia jest pusta. Stwórz swoją pierwszą afirmację!</p>", unsafe_allow_html=True)

def _display_stats_section():
    """
    Wyświetla statystyki użytkowania aplikacji.
    """
    st.markdown("<h3 style='color: white;'>📊 Statystyki</h3>", unsafe_allow_html=True)
    
    total_affirmations = len(StateManager.get('generator.history', []))
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="Wygenerowane",
            value=total_affirmations,
            help="Łączna liczba wygenerowanych afirmacji"
        )
    
    with col2:
        # Można dodać więcej statystyk w przyszłości
        st.metric(
            label="Dzisiaj",
            value=1 if StateManager.get('daily.affirmation') else 0,
            help="Afirmacje wygenerowane dzisiaj"
        )

def _display_help_section():
    """
    Wyświetla sekcję pomocy i wsparcia.
    """
    st.markdown("<h3 style='color: white;'>❓ Pomoc</h3>", unsafe_allow_html=True)
    
    with st.expander("Jak to działa?"):
        st.markdown("""
        <div style='color: white;'>
            <ol style='margin: 0; padding-left: 1.2rem;'>
                <li><strong>Afirmacja dnia</strong> - Otrzymaj codzienną, inspirującą afirmację wygenerowaną przez AI, która pomoże Ci zacząć dzień pozytywnie</li>
                <li><strong>Generator afirmacji</strong> - Stwórz spersonalizowaną afirmację dostosowaną do Twoich potrzeb. Możesz wybrać:
                    <ul style='margin: 0; padding-left: 1.2rem;'>
                        <li>Obszar, nad którym chcesz pracować</li>
                        <li>Konkretny cel</li>
                        <li>Obecny stan emocjonalny</li>
                        <li>Preferowany styl i długość afirmacji</li>
                        <li>Ton i czas stosowania afirmacji</li>
                    </ul>
                </li>
                <li><strong>Wizualny cytat</strong> - Stwórz piękny obraz z Twoją afirmacją w różnych formatach i rozmiarach</li>
                <li><strong>Czytanie afirmacji</strong> - Odsłuchaj swoją afirmację z wybranym głosem i dostosowaną prędkością czytania</li>
                <li><strong>Muzyczna afirmacja</strong> - Połącz swoją afirmację z relaksującym podkładem muzycznym:
                    <ul style='margin: 0; padding-left: 1.2rem;'>
                        <li>Wybierz głos i prędkość narracji</li>
                        <li>Ustaw liczbę powtórzeń i przerwy między nimi</li>
                        <li>Dodaj podkład muzyczny z biblioteki lub wgraj własny</li>
                        <li>Dostosuj głośność podkładu</li>
                    </ul>
                </li>
                <li><strong>Historia</strong> - Wracaj do wcześniejszych afirmacji, przeszukuj je i ponownie wykorzystuj</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("Wskazówki"):
        st.markdown("""
        <div style='color: white;'>
            <ul style='margin: 0; padding-left: 1.2rem;'>
                <li>Używaj afirmacji regularnie dla najlepszych efektów</li>
                <li>Personalizuj afirmacje do swoich potrzeb</li>
                <li>Powtarzaj na głos i z przekonaniem</li>
                <li>Łącz z wizualizacją i oddychaniem</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("Kontakt i wsparcie"):
        st.markdown("""
        <div style='color: white;'>
            <p>Masz pytania lub sugestie?</p>
            <p>📧 Email: adiszefai@gmail.com</p>
            <p>💻 GitHub: <a href='https://github.com/Adiszef-ai' style='color: white; text-decoration: underline;'>github.com/Adiszef-ai</a></p>
            <p>❤️ Wspomóż projekt: <a href='https://www.buymeacoffee.com/adiszefai' style='color: white; text-decoration: underline;'>Buy me a coffee</a></p>
        </div>
        """, unsafe_allow_html=True)