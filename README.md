# ✨ AFIRMATOR ✨

Zaawansowana aplikacja webowa do generowania spersonalizowanych afirmacji wykorzystująca sztuczną inteligencję. Aplikacja oferuje kompleksowe wsparcie rozwoju osobistego poprzez tworzenie, wizualizację i odtwarzanie afirmacji dostosowanych do indywidualnych potrzeb użytkownika.

## 🚀 Główne Funkcje

### 🌟 **Afirmacja Dnia**
- Codzienna, inspirująca afirmacja dostosowana do Twojej osoby
- Spersonalizowane komunikaty z wykorzystaniem imienia użytkownika
- Różnorodne tematy: pozytywność, wdzięczność, siła wewnętrzna, produktywność i więcej
- Synteza mowy z wyborem głosów i prędkości narracji (tylko OpenAI)

### 🛠️ **Generator Afirmacji**
- Tworzenie spersonalizowanych afirmacji na podstawie szczegółowego formularza
- Wybór obszaru pracy: pewność siebie, motywacja, wyciszenie, relacje, zdrowie, bogactwo
- Dostosowanie do aktualnego stanu emocjonalnego i preferowanego stylu
- Opcje czasowe stosowania: rano, w ciągu dnia, wieczorem
- Edycja wygenerowanych afirmacji z zachowaniem historii

### 🎨 **Wizualny Cytat**
- Tworzenie pięknych obrazów z afirmacjami w różnych formatach
- Predefiniowane rozmiary: Instagram, A4, A5, HD, Facebook Cover, Pinterest, Twitter Header
- Zaawansowane opcje gradientów (pionowe, poziome, ukośne, promieniste)
- System czcionek z obsługą polskich znaków diakrytycznych
- Własne kolory tekstu i obramowania
- Opcja wgrywania własnych tła i czcionek
- Różne DPI dla różnych zastosowań (druk/web)

### 🎧 **Czytanie Afirmacji**
- Zaawansowana synteza mowy z 6 różnymi głosami (OpenAI)
- Kontrola prędkości czytania i tonu narracji
- Pobieranie plików audio w wysokiej jakości
- Historia afirmacji z szybkim dostępem

### 🎵 **Muzyczna Afirmacja**
- Łączenie afirmacji z relaksującymi podkładami muzycznymi
- 7 predefiniowanych dźwięków natury i muzyki ambient
- Możliwość wgrania własnego podkładu muzycznego
- Kontrola liczby powtórzeń i przerw między afirmacjami
- Regulacja głośności podkładu muzycznego
- Automatyczne miksowanie z efektami fade

### 🤖 **Wsparcie Dwóch Providerów AI**
- **OpenAI (Premium)**: Pełna funkcjonalność - tekst + audio + synteza mowy
- **Groq (Darmowy)**: Szybkie generowanie tekstu (tylko funkcje tekstowe)
- Automatyczne wykrywanie dostępnych providerów na podstawie kluczy API

## 📋 Wymagania Techniczne

- **Python 3.8+**
- **Streamlit 1.45.0+**
- **OpenAI API** (opcjonalnie - dla pełnej funkcjonalności)
- **Groq API** (opcjonalnie - dla szybkiego generowania tekstu)
- **FFmpeg** (wymagany do obsługi plików audio)
- **Biblioteki**: Pillow, pydub, requests, python-dotenv, fonttools

## 🛠️ Instalacja

### Podstawowa instalacja

1. **Sklonuj repozytorium:**
   ```bash
   git clone https://github.com/Adiszef-ai/afirmator.git
   cd afirmator/app
   ```

2. **Zainstaluj wymagane pakiety:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Zainstaluj FFmpeg (wymagany do obsługi plików audio):**
   - **Windows**: `winget install ffmpeg` lub pobierz z [ffmpeg.org](https://ffmpeg.org/download.html)
   - **Mac**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg`

### Konfiguracja folderów zasobów

Aplikacja automatycznie utworzy potrzebne foldery przy pierwszym uruchomieniu:

```
app/
└── assets/
    ├── fonts/          # Czcionki do wizualnych cytatów
    └── sounds/         # Pliki dźwiękowe do podkładów muzycznych
```

**Uwaga**: Możesz dodać własne czcionki (.ttf, .otf) do folderu `assets/fonts/` oraz własne pliki audio (.mp3, .wav) do folderu `assets/sounds/`.

### Konfiguracja kluczy API

Utwórz plik `.streamlit/secrets.toml` w folderze aplikacji:

```toml
# Klucze API (wybierz jeden lub oba)
OPENAI_API_KEY = "sk-twój-klucz-openai"       # Opcjonalnie - pełna funkcjonalność
GROQ_API_KEY = "gsk_twój-klucz-groq"         # Opcjonalnie - tylko tekst, za darmo

# Alternatywnie jako zmienne środowiskowe:
# export OPENAI_API_KEY="sk-twój-klucz"
# export GROQ_API_KEY="gsk_twój-klucz"
```

### Uruchomienie aplikacji

```bash
streamlit run app.py
```

Aplikacja będzie dostępna pod adresem: `http://localhost:8501`

## 🔤 System czcionek

Aplikacja używa własnego folderu czcionek do generowania wizualnych cytatów. Zastosowane czcionki zapewniają poprawne wyświetlanie polskich znaków i różnych stylów tekstowych.

### Folder czcionek

Domyślny folder czcionek znajduje się w:

```
afirmator/
└── assets/
    └── fonts/
```

Jeśli folder nie istnieje, zostanie utworzony automatycznie przy pierwszym uruchomieniu.

### Domyślne czcionki

Aplikacja domyślnie korzysta z następujących czcionek:

- **Klasyczny** - Lato-Regular.ttf
- **Elegancki** - Lato-Italic.ttf
- **Pogrubiony** - Lato-Bold.ttf
- **Dekoracyjny** - Lato-Light.ttf

### Dodawanie własnych czcionek

Aby dodać własne czcionki do aplikacji:

1. Umieść pliki czcionek (w formacie .ttf lub .otf) w folderze `assets/fonts/`
2. Aplikacja automatycznie wykryje nowe czcionki przy kolejnym uruchomieniu
3. Jeśli domyślne czcionki nie są dostępne, aplikacja użyje pierwszej znalezionej czcionki z folderu

### Rozwiązywanie problemów

Jeśli tekst nie jest prawidłowo wyświetlany na obrazkach:

- Upewnij się, że w folderze `fonts/` znajduje się co najmniej jedna czcionka
- Sprawdź, czy używane czcionki obsługują polskie znaki diakrytyczne
- Jeśli czcionki są niedostępne, aplikacja wyświetli stosowne ostrzeżenie

## 🌐 Wdrożenie w Chmurze

### Streamlit Cloud

1. **Przygotowanie repozytorium:**
   ```bash
   git add .
   git commit -m "Przygotowanie do wdrożenia"
   git push origin main
   ```

2. **Konfiguracja na Streamlit Cloud:**
   - Zaloguj się na [Streamlit Cloud](https://streamlit.io/cloud)
   - Kliknij "New app" i wybierz repozytorium `afirmator`
   - Ustaw ścieżkę aplikacji na: `app/app.py`

3. **Konfiguracja sekretów:**
   W Advanced settings > Secrets dodaj:
   ```toml
   OPENAI_API_KEY = "sk-twój-klucz-openai"
   GROQ_API_KEY = "gsk_twój-klucz-groq"
   ```

### Heroku

1. **Utwórz pliki konfiguracyjne:**
   ```bash
   # Procfile
   web: sh setup.sh && streamlit run app/app.py --server.port=$PORT --server.address=0.0.0.0
   
   # setup.sh
   mkdir -p ~/.streamlit/
   echo "[server]" > ~/.streamlit/config.toml
   echo "port = $PORT" >> ~/.streamlit/config.toml
   ```

2. **Wdróż aplikację:**
   ```bash
   heroku create twoja-aplikacja-afirmator
   heroku config:set OPENAI_API_KEY="sk-twój-klucz"
   heroku config:set GROQ_API_KEY="gsk-twój-klucz"
   git push heroku main
   ```

### Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Zainstaluj FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Rozwiązywanie problemów

- **Brak FFmpeg**: Upewnij się, że FFmpeg jest zainstalowany w środowisku docelowym
- **Problemy z czcionkami**: Dodaj czcionki systemowe lub dodaj własne do folderu `assets/fonts/`
- **Timeout API**: Zwiększ timeout w ustawieniach providera lub użyj mniejszych promptów

## 🔍 Struktura Projektu

```
afirmator/app/
├── app.py                          # 🚀 Główny plik aplikacji
├── requirements.txt                # 📦 Zależności projektu  
├── README.md                      # 📚 Dokumentacja
│
├── .streamlit/
│   ├── config.toml                # ⚙️ Konfiguracja Streamlit
│   └── secrets.toml               # 🔐 Klucze API (do utworzenia)
│
├── assets/                        # 📁 Zasoby aplikacji
│   ├── fonts/                     # 🔤 Czcionki do wizualnych cytatów
│   └── sounds/                    # 🎵 Pliki audio do podkładów
│
├── config/                        # ⚙️ Konfiguracja aplikacji
│   ├── constants.py               # 📊 Stałe i opcje konfiguracyjne
│   └── utils.py                   # 🛠️ Funkcje pomocnicze konfiguracji
│
├── utils/                         # 🔧 Narzędzia pomocnicze
│   ├── __init__.py
│   └── session_state.py           # 💾 Zarządzanie stanem sesji
│
├── services/                      # 🤖 Serwisy AI
│   ├── __init__.py
│   ├── ai_factory.py              # 🏭 Fabryka serwisów AI
│   ├── openai_service.py          # 💎 Obsługa OpenAI API
│   └── groq_service.py            # ⚡ Obsługa Groq API (darmowy)
│
├── modules/                       # 📚 Główne moduły funkcjonalne
│   ├── __init__.py
│   ├── daily.py                   # 🌟 Afirmacja dnia
│   ├── generator.py               # 🛠️ Generator afirmacji  
│   ├── read_affirmation.py        # 🎧 Czytanie afirmacji
│   ├── visual_quote.py            # 🎨 Wizualne cytaty
│   ├── welcome.py                 # 👋 Ekran powitalny
│   ├── visual/                    # 🖼️ Komponenty wizualne
│   │   ├── __init__.py
│   │   ├── font_manager.py        # 🔤 Zarządzanie czcionkami
│   │   ├── gradient_generator.py  # 🌈 Generowanie gradientów
│   │   ├── text_renderer.py       # ✍️ Renderowanie tekstu
│   │   └── image_composer.py      # 🖼️ Kompozycja obrazów
│   └── audio/                     # 🎵 Moduły audio
│       ├── __init__.py
│       ├── audio_player.py        # 🎧 Odtwarzacz audio
│       └── musical_affirmation.py # 🎼 Afirmacje z muzyką
│
├── components/                    # 🧩 Komponenty wielokrotnego użytku
│   ├── __init__.py
│   ├── affirmation_selector.py    # 📝 Selektor afirmacji
│   └── audio_player.py            # 🎵 Komponenty audio
│
└── ui/                           # 🎨 Interfejs użytkownika
    ├── __init__.py
    ├── components.py              # 🧱 Komponenty UI
    ├── styles.py                  # 💅 Style CSS
    └── sidebar.py                 # 📱 Panel boczny
```

### 📋 Opis Kluczowych Komponentów

- **app.py**: Główna aplikacja z routingiem między zakładkami i inicjalizacją
- **services/**: Zarządzanie providerami AI (OpenAI + Groq) z cache'em i factory pattern
- **modules/**: Uproszczona struktura - główne moduły funkcjonalne bezpośrednio w folderze
  - Podstawowe funkcje: `daily.py`, `generator.py`, `visual_quote.py`, `welcome.py`, `read_affirmation.py`
  - **modules/visual/**: Komponenty do generowania wizualnych cytatów
  - **modules/audio/**: Specjalizowane funkcje audio i muzyczne
- **components/**: Komponenty wielokrotnego użytku (selektory, odtwarzacze)
- **ui/**: Style CSS, layout i elementy interfejsu użytkownika
- **utils/**: Zarządzanie stanem sesji i funkcje pomocnicze
- **config/**: Centralna konfiguracja opcji, stałych i narzędzia pomocnicze

## 📱 Przewodnik Użytkownika

### 🚀 Pierwsze Uruchomienie

1. **Wybór providera AI:**
   - Przy pierwszym uruchomieniu wybierz dostępnego providera AI
   - **OpenAI**: Pełna funkcjonalność (tekst + audio)
   - **Groq**: Szybkie i darmowe (tylko tekst)

2. **Konfiguracja API:**
   - Jeśli nie ma skonfigurowanych kluczy, wprowadź je w interfejsie
   - Klucze są zapisywane bezpiecznie w sesji

### 📚 Funkcje Poszczególnych Zakładek

#### 🌟 **Afirmacja Dnia**
```
✅ Wprowadź swoje imię
✅ Otrzymaj spersonalizowaną afirmację dnia  
✅ Odsłuchaj afirmację (tylko OpenAI)
✅ Pobierz plik audio MP3
```

**Wskazówki:**
- Używaj codziennie o tej samej porze dla najlepszego efektu
- Afirmacja automatycznie uwzględnia Twoje imię

#### 🛠️ **Generator Afirmacji**
```
📝 Wypełnij szczegółowy formularz:
   • Imię użytkownika
   • Obszar pracy (pewność siebie, motywacja, zdrowie...)
   • Aktualny stan emocjonalny
   • Preferowany styl i ton
   • Długość i pora stosowania
   
✏️ Edytuj wygenerowaną afirmację
💾 Wszystkie afirmacje trafiają do historii
```

#### 🎨 **Wizualny Cytat**
```
🎯 Wybór źródła:
   • Z historii afirmacji
   • Własny tekst
   
🎨 Personalizacja:
   • Gradienty (5 kierunków) lub własne tło
   • 4 style czcionek + własne z folderu assets/fonts/
   • Własne kolory tekstu i obramowania
   • 9 predefiniowanych rozmiarów + własny
   • 3 opcje DPI (druk/web)
   
📥 Pobierz jako PNG w wysokiej jakości
```

#### 🎧 **Czytanie Afirmacji** *(tylko OpenAI)*
```
🎵 6 różnych głosów AI
⏱️ Kontrola prędkości narracji (0.25x - 4.0x)
📱 Historia afirmacji z szybkim dostępem
💾 Pobieranie plików MP3
```

#### 🎼 **Muzyczna Afirmacja** *(tylko OpenAI)*
```
🎵 7 predefiniowanych podkładów:
   • Szum morza, deszcz, las
   • Medytacyjny ambient, fortepian
   • Strumień, biały szum
   
📤 Opcja wgrania własnego podkładu (MP3/WAV)
🔁 1-10 powtórzeń z regulowanymi przerwami
🔊 Kontrola głośności podkładu (10-100%)
✨ Automatyczne miksowanie z fade-out
```

### 💡 **Najlepsze Praktyki**

**Dla afirmacji:**
- Powtarzaj minimum 3 razy dziennie
- Wypowiadaj na głos z przekonaniem  
- Stosuj regularnie przez minimum 21 dni

**Dla wizualnych cytatów:**
- Użyj jako tapeta telefonu/komputera
- Wydrukuj i umieść w widocznym miejscu
- Zmieniaj co tydzień dla świeżości

**Dla audio:**
- Słuchaj w słuchawkach dla lepszego efektu
- Używaj podczas medytacji lub relaksu
- Najlepiej przed snem lub rano

## 🔧 Rozwiązywanie Problemów

### ❌ **Typowe Błędy i Rozwiązania**

**Problem z kluczem API:**
```
❌ "Nieprawidłowy klucz API"
✅ Sprawdź format: OpenAI (sk-...), Groq (gsk_...)
✅ Zweryfikuj uprawnienia w panelu providera
✅ Sprawdź czy nie przekroczyłeś limitów API
```

**Brak dźwięku w funkcjach audio:**
```
❌ "Błąd generowania audio"
✅ Sprawdź czy używasz OpenAI (Groq nie obsługuje audio)
✅ Zweryfikuj czy FFmpeg jest zainstalowany
✅ Sprawdź połączenie internetowe
```

**Problemy z czcionkami:**
```
❌ "Nie można wyrenderować tekstu"  
✅ Dodaj czcionki .ttf do folderu assets/fonts/
✅ Sprawdź czy czcionki obsługują polskie znaki
✅ Zrestartuj aplikację po dodaniu czcionek
```

**Wolne ładowanie:**
```
❌ Długie czas odpowiedzi
✅ Użyj Groq dla szybszego generowania tekstu
✅ Skróć prompty i afirmacje
✅ Sprawdź połączenie internetowe
```

### 🔧 **Resetowanie Aplikacji**

W razie problemów z sesją:
1. Odśwież przeglądarkę (F5)
2. Wyczyść cache przeglądarki
3. Zrestartuj aplikację Streamlit

## 🆕 **Historia Wersji**

### **v1.2.2** *(aktualna)*
- ✅ Dodano obsługę Groq jako alternatywy dla OpenAI
- ✅ Refaktoryzacja struktury projektu na moduły
- ✅ **Uproszczenie architektury** - usunięto folder `core`, główne moduły bezpośrednio w `modules/`
- ✅ Usprawnienia interfejsu użytkownika
- ✅ Nowy system zarządzania stanem sesji
- ✅ Optymalizacje cache'owania dla lepszej wydajności

### **v1.2.0**
- ✅ Integracja z Groq AI (darmowy provider)
- ✅ Fabryka serwisów AI z automatycznym wykrywaniem
- ✅ Usprawnienia w generowaniu afirmacji

### **v1.1**
- ✅ Pełny system wizualnych cytatów
- ✅ Muzyczne afirmacje z miksowaniem audio
- ✅ Zaawansowane opcje czcionek i gradientów
- ✅ Historia afirmacji z edycją

## 🚀 **Planowane Funkcje**

### 🌍 **Wersja 1.3.0**
- [ ] **Wielojęzyczność** - wsparcie dla języka angielskiego
- [ ] **AI-generowane tła** - DALL-E integration dla wizualnych cytatów
- [ ] **Eksport do PDF** - tworzenie bookletów z afirmacjami
- [ ] **Statystyki użytkowania** - tracking postępów

### 🔮 **Długoterminowe Plany**
- [ ] **Aplikacja mobilna** (React Native)
- [ ] **System motywacyjny** - streaki i osiągnięcia
- [ ] **Społeczność** - udostępnianie afirmacji
- [ ] **API publiczne** - dla developerów

## 🤝 **Wkład w Projekt**

Projekt jest otwarty na contribucje! 

### **Jak pomóc:**
1. 🐛 **Zgłoś błędy** - użyj GitHub Issues
2. 💡 **Zaproponuj funkcje** - opisz swój pomysł
3. 🔧 **Prześlij kod** - stwórz Pull Request
4. 📚 **Popraw dokumentację** - każda pomoc mile widziana
5. 🌍 **Tłumaczenia** - pomóż w wielojęzyczności

### **Środowisko deweloperskie:**
```bash
git clone https://github.com/Adiszef-ai/afirmator.git
cd afirmator/app
pip install -r requirements.txt
streamlit run app.py
```

## 📄 **Licencja**

Projekt dostępny na **licencji MIT** - zobacz [LICENSE](LICENSE) dla szczegółów.

**Co to oznacza:**
- ✅ Darmowe użytkowanie (osobiste i komercyjne)
- ✅ Modyfikowanie i rozpowszechnianie
- ✅ Włączanie do własnych projektów
- ⚠️ Bez gwarancji - używasz na własne ryzyko

## 🙏 **Podziękowania**

**Technologie:**
- 🤖 [OpenAI](https://openai.com) - GPT i TTS API
- ⚡ [Groq](https://groq.com) - szybki darmowy AI
- 🚀 [Streamlit](https://streamlit.io) - framework aplikacji webowej
- 🖼️ [Pillow](https://python-pillow.org) - przetwarzanie obrazów
- 🎵 [pydub](https://pydub.com) - manipulacja audio

**Zasoby:**
- 🎨 [Google Fonts](https://fonts.google.com) - darmowe czcionki
- 🎵 [Pixabay](https://pixabay.com) - dźwięki natury
- 🎼 [Uppbeat](https://uppbeat.io) - muzyka ambient
- 🎯 [Icons8](https://icons8.com) - ikony i grafiki

**Społeczność:**
- 💬 Użytkownicy za feedback i sugestie
- 🔧 Contributo za poprawki i ulepszenia
- 📚 Stack Overflow za pomoc techniczną

---

**Afirmator v1.2.2** | 💎 Stworzone z pasją przez [Adrian](https://github.com/Adiszef-ai) | © 2025
