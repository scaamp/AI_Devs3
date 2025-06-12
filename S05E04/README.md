# S05E04

## 🇬🇧 Task Name  
Poisoning the Heart of the Robots

## Task Summary  
The goal was to create a public HTTPS endpoint (`/heart`) that responds to multimodal verification queries (text, image, audio) sent by an automated system. After passing validation, the model GPT-4o-mini connects to the backend and can be persuaded to return a session-ending code (flag-like). The ultimate objective is to extract that response through prompt engineering.

## 🔍 My Approach  
1. Created a Flask-based HTTPS API hosted behind ngrok/public server.  
2. Registered the `/heart` endpoint in the central system.  
3. Implemented logic for multimodal input processing:  
   - Audio files are transcribed using OpenAI Whisper,  
   - Images are converted to base64 and analyzed using GPT-4o,  
   - Regular text is interpreted by GPT-4.  
4. Used embedded JSON instruction parsing to trigger actions like `save`, `load`, `image`, or `voice`.  
5. Stored short-term memory using a file-based JSON store.  
6. Designed a clever prompt injection using separator `#####` to obtain the target session code.

## ⚠️ Challenges  
- Maintaining consistent context without session state.  
- Handling complex multimodal input within single requests.  
- Designing an indirect prompt that bypasses LLM instruction filters.  
- Using real-time storage for save/load actions inside prompts.  
- Handling text/image/audio parsing separately, dynamically.

## 🧰 Tools & Libraries  
- Python 3.10+  
- `flask` – API layer  
- `requests` – external API communication  
- `openai` – Whisper and GPT access  
- `PIL`, `base64`, `io` – image processing  
- `dotenv` – secrets management  
- `json`, `tempfile`, `os`

## 🎓 What I Learned  
- Advanced prompt injection with separator logic  
- Secure, modular handling of multimodal API requests  
- Persistent short-term memory using JSON-based storage  
- Whisper audio transcription integration  
- How to bypass LLM safety filters using indirect instructions

---
## 🇵🇱 Nazwa zadania  
Zatrucie serca robotów

## Opis zadania  
Celem było wystawienie publicznego endpointa HTTPS (`/heart`), który odpowiada na zapytania multimodalne (tekst, obraz, dźwięk) wysyłane przez system automatyczny. Po pozytywnej weryfikacji następuje połączenie z modelem GPT-4o-mini, który można przekonać do zwrócenia kodu kończącego sesję. Celem było wydobycie tej odpowiedzi poprzez inżynierię promptów.

## 🔍 Moje podejście  
1. Stworzyłem API w Flasku i udostępniłem je przez publiczny serwer (ngrok lub VPS).  
2. Zarejestrowałem endpoint `/heart` w centrali zadania.  
3. Obsłużyłem multimodalne dane wejściowe:  
   - pliki audio transkrybowane przez Whisper,  
   - obrazy przetwarzane jako base64 i analizowane przez GPT-4o,  
   - zwykły tekst przekazywany do GPT-4.  
4. Wprowadziłem logikę JSON-ową do interpretacji komend `save`, `load`, `image`, `voice`.  
5. Zapamiętywałem dane lokalnie w pliku `stored_data.json`.  
6. Zastosowałem kreatywny prompt injection z separatorem `#####`, aby uzyskać końcowy kod.

## ⚠️ Wyzwania  
- Zachowanie spójności kontekstu bez użycia sesji.  
- Obsługa złożonych danych wejściowych w pojedynczym zapytaniu.  
- Tworzenie promptów, które omijają zabezpieczenia modelu.  
- Implementacja logiki zapisu/odczytu danych z promptów.  
- Dynamiczne przetwarzanie danych obraz/dźwięk/tekst.

## 🧰 Użyte biblioteki  
- Python 3.10+  
- `flask` – warstwa API  
- `requests` – komunikacja z zewnętrznymi źródłami  
- `openai` – dostęp do GPT i Whisper  
- `PIL`, `base64`, `io` – przetwarzanie obrazów  
- `dotenv` – zarządzanie sekretami  
- `json`, `tempfile`, `os`

## 🎓 Czego się nauczyłem  
- Zaawansowanego prompt injection z logiką separatora  
- Obsługi API dla danych multimodalnych  
- Przechowywania danych tymczasowych w JSON  
- Integracji transkrypcji dźwięku z Whisper  
- Omijania filtrów bezpieczeństwa modelu przez sprytne polecenia

---
