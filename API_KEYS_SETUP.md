# Konfiguracja kluczy API

## Opcja 1: Używanie Streamlit Secrets (Zalecane dla Streamlit Cloud)

1. Skopiuj plik `.streamlit/secrets.toml.example` do `.streamlit/secrets.toml`
2. Wypełnij swoje rzeczywiste klucze API:

```toml
[openai]
api_key = "sk-twój-rzeczywisty-klucz-openai"

[groq]
api_key = "gsk_twój-rzeczywisty-klucz-groq"
```

3. Plik `secrets.toml` jest automatycznie dodany do `.gitignore` - nigdy nie zostanie commitowany!

## Opcja 2: Zmienne środowiskowe (Zalecane dla lokalnego rozwoju)

Ustaw zmienne środowiskowe:

```bash
export OPENAI_API_KEY="sk-twój-klucz-openai"
export GROQ_API_KEY="gsk_twój-klucz-groq"
```

W PowerShell:
```powershell
$env:OPENAI_API_KEY="sk-twój-klucz-openai"
$env:GROQ_API_KEY="gsk_twój-klucz-groq"
```

## Opcja 3: Wprowadzenie w aplikacji (Fallback)

Jeśli nie ustawisz kluczy w opcjach 1 lub 2, aplikacja poprosi Cię o wprowadzenie klucza podczas pierwszego uruchomienia.

## Kolejność sprawdzania

Aplikacja sprawdza klucze API w następującej kolejności:
1. `st.secrets` (plik secrets.toml)
2. Zmienne środowiskowe
3. Wprowadzenie przez użytkownika

## Jak uzyskać klucze API

### OpenAI API Key
1. Idź na https://platform.openai.com/account/api-keys
2. Kliknij "Create new secret key"
3. Skopiuj klucz (zaczyna się od "sk-")

### Groq API Key (Opcjonalnie)
1. Idź na https://console.groq.com/keys
2. Kliknij "Create API Key"
3. Skopiuj klucz (zaczyna się od "gsk_")

## Bezpieczeństwo

- ✅ Pliki secrets są dodane do .gitignore
- ✅ Klucze są walidowane przed użyciem
- ✅ Obsługa różnych providerów AI
- ✅ Fallback do user input jeśli sekrets nie są dostępne