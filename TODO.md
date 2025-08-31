Masz absolutną rację! Przepraszam za zamieszanie. Dla aplikacji Streamlit struktura powinna być bardziej "streamlitowa". Oto poprawiona struktura:

# TODO.md - Refaktoryzacja Aplikacji Afirmator (Streamlit)

## 🔴 Priorytet KRYTYCZNY

### 1. Bezpieczeństwo API Key

- [ ] Wykorzystać `st.secrets` dla Streamlit Cloud
- [ ] Dodać plik `.streamlit/secrets.toml` do .gitignore
- [ ] Implementacja fallback: secrets -> environment variables -> user input
- [ ] Ulepszyć walidację API key (regex pattern, długość, format)
- [ ] Dodać obsługę różnych typów kluczy (OpenAI, Groq)

### 2. Restrukturyzacja projektu (Streamlit-friendly)

- [ ] Zachować strukturę płaską, ale lepiej zorganizowaną:
  ```
  afirmator/
  ├── app.py                    # Główny plik (pozostaje)
  ├── pages/                     # Jeśli chcesz multipage app
  │   ├── 1_🌟_Afirmacja_dnia.py
  │   ├── 2_🛠️_Generator.py
  │   └── 3_🎨_Wizualny_cytat.py
  ├── components/                # Reusable Streamlit components
  │   ├── affirmation_selector.py
  │   ├── audio_player.py
  │   └── history_viewer.py
  ├── services/                  # Logika biznesowa
  │   ├── openai_service.py
  │   ├── groq_service.py
  │   └── ai_factory.py
  ├── utils/                     # Pomocnicze funkcje
  │   ├── session_state.py
  │   └── validators.py
  └── config/
      └── constants.py
  ```

## 🟡 Priorytet WYSOKI

### 3. Eliminacja duplikacji kodu (Streamlit way)

- [ ] Utworzyć reusable Streamlit component dla wyboru afirmacji:
  ```python
  # components/affirmation_selector.py
  def render_affirmation_selector(key_prefix: str):
      return selected_text
  ```
- [ ] Wydzielić wspólny kod audio do `components/audio_player.py`
- [ ] Stworzyć `@st.fragment` dla powtarzających się elementów UI
- [ ] Zunifikować obsługę historii w jednym komponencie

### 4. Zarządzanie stanem aplikacji (Streamlit Session State)

- [ ] Utworzyć `utils/session_state.py` z klasą StateManager:
  ```python
  class StateManager:
      @staticmethod
      def init_state():
          if 'initialized' not in st.session_state:
              st.session_state.update(DEFAULT_STATE)

      @staticmethod
      def get(key: str, default=None):
          return st.session_state.get(key, default)
  ```
- [ ] Używać namespace dla session_state keys:
  ```python
  # Zamiast: st.session_state.editing
  # Użyj: st.session_state['generator.editing']
  ```

### 5. Lepsza obsługa błędów (Streamlit-friendly)

- [ ] Utworzyć `utils/error_handler.py`:
  ```python
  def handle_api_error(func):
      def wrapper(*args, **kwargs):
          try:
              return func(*args, **kwargs)
          except OpenAIError as e:
              st.error(f"🔴 Problem z API: {str(e)}")
              st.stop()
      return wrapper
  ```
- [ ] Używać `st.error()`, `st.warning()`, `st.info()` konsekwentnie
- [ ] Dodać `st.exception()` w trybie debug

## 🟢 Priorytet ŚREDNI

### 6. Multi-page czy Single-page?

- [ ] **Opcja A**: Pozostać przy pojedynczej stronie z zakładkami (obecne)
- [ ] **Opcja B**: Migracja do Streamlit Multipage App:

  ```python
  # pages/1_🌟_Afirmacja_dnia.py
  import streamlit as st
  from components import daily_affirmation

  st.set_page_config(page_title="Afirmacja Dnia", page_icon="🌟")
  daily_affirmation.render()
  ```

### 7. Wykorzystanie Streamlit Cache

- [ ] Dodać `@st.cache_data` dla kosztownych operacji:
  ```python
  @st.cache_data(ttl=3600)
  def generate_cached_affirmation(prompt_hash: str):
      return generate_affirmation(prompt)
  ```
- [ ] Użyć `@st.cache_resource` dla singleton services:
  ```python
  @st.cache_resource
  def get_openai_client():
      return OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
  ```

### 8. Konfiguracja Streamlit

- [ ] Ulepszyć `.streamlit/config.toml`:

  ```toml
  [theme]
  primaryColor = "#4A90E2"
  backgroundColor = "#FFFFFF"
  secondaryBackgroundColor = "#F0F2F6"

  [server]
  maxUploadSize = 5
  enableCORS = false
  ```

- [ ] Dodać custom theme switching (light/dark)

## 💡 Nowe funkcjonalności (Streamlit-specific)

### 9. Integracja z Groq AI

- [ ] Dodać toggle w sidebar:
  ```python
  provider = st.sidebar.radio(
      "Model AI",
      ["🆓 Groq (Darmowy)", "💎 OpenAI (Premium)"],
      help="Groq - tylko tekst, OpenAI - tekst + audio"
  )
  ```
- [ ] Warunkowo pokazywać opcje audio tylko dla OpenAI

### 10. Lepsze wykorzystanie Streamlit Components

- [ ] Użyć `st.columns()` bardziej efektywnie
- [ ] Implementować `st.expander()` dla zaawansowanych opcji
- [ ] Dodać `st.progress()` dla długich operacji
- [ ] Wykorzystać `st.toast()` dla notyfikacji

## 🧹 Czyszczenie i optymalizacja

### 11. Optymalizacja dla Streamlit

- [ ] Zmniejszyć re-run'y przez lepsze użycie `key` w komponentach
- [ ] Użyć `st.form()` gdzie to możliwe aby zredukować interakcje
- [ ] Implementować `st.fragment()` dla niezależnych części UI (Streamlit 1.33+)

### 12. Streamlit-friendly CSS

- [ ] Przenieść style do `style.css` i ładować przez:
  ```python
  def load_css(file_name):
      with open(file_name) as f:
          st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
  ```
- [ ] Użyć Streamlit theme variables zamiast hardcoded colors

## 📝 Deployment (Streamlit Cloud specific)

### 13. Przygotowanie do Streamlit Cloud

- [ ] Dodać `packages.txt` dla system dependencies:
  ```
  ffmpeg
  ```
- [ ] Upewnić się że `requirements.txt` jest minimalny
- [ ] Dodać badge deployment status do README

### 14. Secrets Management

- [ ] Dokumentacja jak ustawić secrets w Streamlit Cloud
- [ ] Przykładowy `.streamlit/secrets.toml.example`
- [ ] Instrukcja dla użytkowników self-hosting

## 🚀 Streamlit Best Practices

### 15. Performance Optimization

- [ ] Lazy loading heavy components:
  ```python
  if st.button("Generuj obraz"):
      from modules import visual_quote
      visual_quote.generate()
  ```
- [ ] Użyć `st.empty()` containers dla dynamic content
- [ ] Implementować pagination dla historii

### 16. User Experience

- [ ] Dodać `st.balloons()` lub `st.snow()` dla special moments
- [ ] Użyć `st.metric()` dla statystyk
- [ ] Implementować dark mode toggle:
  ```python
  if st.sidebar.checkbox("🌙 Tryb ciemny"):
      st.markdown('<style>...</style>', unsafe_allow_html=True)
  ```

## 📊 Kolejność implementacji (Streamlit-focused)

### Faza 1 (Tydzień 1)

1. Secrets management (st.secrets)
2. Session state refactor
3. Reusable components

### Faza 2 (Tydzień 2)

4. Groq integration z toggle w UI
5. Cachowanie z @st.cache_data
6. Error handling

### Faza 3 (Tydzień 3)

7. UI/UX improvements
8. Performance optimization
9. Multipage app (opcjonalnie)

### Faza 4 (Tydzień 4)

10. Deployment preparation
11. Documentation
12. Testing w Streamlit Cloud

## 📌 Notatki Streamlit-specific

- Pamiętaj o `st.rerun()` vs `st.experimental_rerun()` (w zależności od wersji)
- Testuj lokalnie z `streamlit run app.py --server.headless true`
- Używaj `st.spinner()` zamiast custom loading animations
- Streamlit Cloud ma limit 1GB RAM dla free tier

---

_Framework: Streamlit 1.32.0+_
_Deployment: Streamlit Cloud_
_Ostatnia aktualizacja: [DATA]_
