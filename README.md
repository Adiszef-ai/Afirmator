# ✨ AFIRMATOR ✨

Aplikacja do generowania spersonalizowanych afirmacji wspierających rozwój osobisty, wykorzystująca sztuczną inteligencję do tworzenia unikalnych i motywujących komunikatów.

## 🚀 Funkcje

- **Generator afirmacji** - tworzenie spersonalizowanych afirmacji dostosowanych do Twoich potrzeb, celów i emocji
- **Afirmacja dnia** - codzienna, inspirująca afirmacja dostosowana do Twojej osoby
- **Synteza mowy** - zamiana tekstu na mowę z wyborem różnych głosów i prędkości czytania
- **Czytanie afirmacji** - zaawansowana kontrola nad sposobem narracji i odtwarzania
- **Wizualny cytat** - tworzenie obrazów z afirmacjami w różnych formatach i rozmiarach
- **Muzyczna afirmacja** - łączenie afirmacji z relaksującymi podkładami muzycznymi
- **Historia afirmacji** - łatwy dostęp do wcześniej wygenerowanych afirmacji
- **Statystyki** - śledzenie liczby wygenerowanych afirmacji i aktywności

## 📋 Wymagania

- Python 3.8+
- Streamlit 1.32.0+
- OpenAI API (do generowania tekstu i mowy)
- Pillow (do obsługi obrazów)
- Pydub i FFmpeg (do obsługi plików audio)

## 🛠️ Instalacja

1. Sklonuj repozytorium:

   ```bash
   git clone https://github.com/twoj-username/afirmator.git
   cd afirmator
   ```

2. Zainstaluj wymagane pakiety:

   ```bash
   pip install -r requirements.txt
   ```

3. Zainstaluj FFmpeg (wymagany do obsługi plików audio):

   - **Windows**: Pobierz z [ffmpeg.org](https://ffmpeg.org/download.html) lub użyj `winget install ffmpeg`
   - **Mac**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg`

4. Utwórz strukture katalogów dla plików dźwiękowych:

   ```
   afirmator/
   └── assets/
       └── sounds/
   ```

5. Pobierz pliki dźwiękowe i umieść je w folderze `assets/sounds/`

6. Uruchom aplikację:
   ```bash
   streamlit run app.py
   ```

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
- **Ręczny** - OpenSans-Regular.ttf

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

## 🌐 Wdrożenie na Streamlit Cloud

Aby wdrożyć aplikację na Streamlit Cloud, wykonaj następujące kroki:

1. Umieść kod w repozytorium GitHub
2. Zaloguj się na [Streamlit Cloud](https://streamlit.io/cloud)
3. Kliknij "New app" i wybierz swoje repozytorium

### Konfiguracja klucza API

Na Streamlit Cloud możesz ustawić klucz API OpenAI na dwa sposoby:

1. **Za pomocą zmiennych środowiskowych** (zalecane):

   - W panelu aplikacji na Streamlit Cloud, przejdź do "Advanced settings" > "Secrets"
   - Dodaj swój klucz API w formacie TOML:
     ```toml
     OPENAI_API_KEY = "sk-twój-klucz-api"
     ```

2. **Ręcznie w aplikacji**:
   - Uruchom aplikację i wprowadź klucz API w interfejsie użytkownika
   - Uwaga: Ten sposób wymaga ponownego wprowadzenia klucza po każdym restarcie aplikacji

### Rozwiązywanie problemów z wdrożeniem

Jeśli występują problemy z kluczem API:

- Upewnij się, że klucz zaczyna się od "sk-" i ma prawidłowy format
- Sprawdź, czy Twój klucz API ma wystarczające uprawnienia
- Zweryfikuj, czy limit API nie został przekroczony

Jeśli pojawiają się błędy związane z biblioteką OpenAI:

- **UWAGA**: Aplikacja używa bezpośrednich zapytań HTTP do API OpenAI zamiast oficjalnej biblioteki, co rozwiązuje problem z argumentem 'proxies' na Streamlit Cloud
- W przypadku błędów związanych z API OpenAI, sprawdź w logach dokładny komunikat błędu
- Po zaktualizowaniu kodu, przebuduj aplikację na Streamlit Cloud (Manage app > Reboot app)

Jeśli aplikacja nadal nie działa po wdrożeniu:

1. Upewnij się, że zmiany zostały wysłane do repozytorium GitHub
2. W Streamlit Cloud, wybierz "Manage app" > "Advanced settings" i sprawdź, czy wybrana jest właściwa gałąź repozytorium
3. Spróbuj całkowicie usunąć aplikację i wdrożyć ją ponownie

## 🔍 Struktura projektu

```
afirmator/
├── app.py                 # Główny plik aplikacji
├── config.toml            # Konfiguracja Streamlit
├── requirements.txt       # Zależności
├── README.md              # Dokumentacja aplikacji
├── assets/
│   ├── sounds/            # Pliki dźwiękowe do podkładów
│   └── fonts/             # Folder z czcionkami dla wizualnych cytatów
├── config/
│   └── constants.py       # Stałe i konfiguracja
├── modules/
│   ├── __init__.py        # Inicjalizacja pakietu
│   ├── daily.py           # Moduł afirmacji dnia
│   ├── generator.py       # Moduł generatora afirmacji
│   ├── audio.py           # Funkcje związane z audio
│   ├── audio_player.py    # Zaawansowane czytanie afirmacji
│   ├── musical_affirmation.py # Afirmacje z podkładem muzycznym
│   ├── visual_quote.py    # Tworzenie obrazów z afirmacjami
│   └── utils.py           # Funkcje pomocnicze
├── services/
│   ├── __init__.py        # Inicjalizacja pakietu
│   └── openai_service.py  # Obsługa OpenAI API
└── ui/
    ├── __init__.py        # Inicjalizacja pakietu
    ├── styles.py          # Style CSS
    ├── components.py      # Komponenty interfejsu
    └── sidebar.py         # Elementy panelu bocznego
```

## 📱 Używanie aplikacji

1. Po uruchomieniu aplikacji, wprowadź swój klucz API OpenAI
2. Wybierz jedną z pięciu zakładek:
   - **🌟 Afirmacja dnia** - Otrzymaj codzienną dawkę pozytywnej energii
   - **🛠️ Generator afirmacji** - Stwórz spersonalizowaną afirmację
   - **🎨 Wizualny cytat** - Twórz obrazy z afirmacjami w różnych formatach
   - **🎧 Czytanie afirmacji** - Kontroluj prędkość czytania afirmacji
   - **🎵 Muzyczna afirmacja** - Połącz afirmacje z podkładem muzycznym

### Afirmacja dnia

- Wprowadź swoje imię
- Otrzymaj codzienną afirmację dostosowaną do Twojej osoby
- Możliwość odsłuchania i pobrania afirmacji w formie audio

### Generator afirmacji

- Wypełnij formularz z Twoimi preferencjami
- Dostosuj styl, ton i długość afirmacji
- Odsłuchaj lub pobierz audio z afirmacją

### Wizualny cytat

- Wybierz afirmację z historii lub wprowadź własną
- Dostosuj tło, kolory, czcionkę i rozmiar obrazu
- Wybierz spośród różnych stylów czcionek lub dodaj własne do folderu `assets/fonts/`
- Korzystaj z własnych kolorów tekstu i obramowania dla większej personalizacji
- Wybierz kierunek gradientu (pionowy, poziomy, ukośny, promienisty) dla tła
- Pobierz gotowy obraz w formacie PNG

### Czytanie afirmacji

- Wybierz afirmację do odtworzenia
- Dostosuj prędkość i głos narracji
- Odsłuchaj i pobierz spersonalizowane audio

### Muzyczna afirmacja

- Połącz afirmację z relaksującym podkładem muzycznym
- Wybierz z predefiniowanych dźwięków natury lub wgraj własny
- Ustaw liczbę powtórzeń i głośność podkładu

## 🌱 Zalecenia dotyczące stosowania afirmacji

- Powtarzaj afirmację co najmniej 3 razy dziennie
- Wypowiadaj afirmacje na głos i z przekonaniem
- Słuchaj nagrania podczas medytacji lub relaksu
- Dla najlepszych rezultatów, stosuj przez minimum 21 dni
- Używaj wizualnych cytatów jako elementów przypominających w Twoim otoczeniu
- Ustaw muzyczne afirmacje jako podkład do medytacji

## 🔮 Planowane zmiany i rozwój

- **Wielojęzyczność** - dodanie obsługi języka angielskiego i możliwości generowania afirmacji w różnych językach
- **AI-generowane tła** - wykorzystanie sztucznej inteligencji do tworzenia unikalnego tła dla wizualnych cytatów
- **Restrukturyzacja kodu** - optymalizacja i poprawa organizacji kodu dla lepszej wydajności i łatwiejszego rozwoju
- **Nowe funkcje** - ciągłe dodawanie nowych funkcjonalności i ulepszeń w oparciu o potrzeby użytkowników

## 📝 Licencja

Ten projekt jest dostępny na licencji MIT. Zobacz plik `LICENSE` dla szczegółów.

## 🙏 Podziękowania

- OpenAI za API do generowania tekstu i mowy
- Streamlit za framework do tworzenia aplikacji webowych
- pixabay.com i uppbeat.io za darmowe pliki dźwiękowe
- Ikony od [Icons8](https://icons8.com/)
