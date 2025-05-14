# S01E01

## 🇬🇧 Task Name  
Validation and Data Completion Using a Language Model

## 📌 Task Summary  
The goal was to process a JSON file containing test data (arithmetic operations and text questions), automatically verify the correctness of results, complete missing answers using GPT via API, and then send the corrected data to the endpoint `https://centrala.ag3nts.org/report`, where the server responded with a flag.

## 🔍 My Approach  
1. I created a Python script that allows selecting the JSON file via a GUI (`tkinter.filedialog`).
2. Each arithmetic expression (e.g., `"82 + 84"`) was verified and, if necessary, corrected using classic programming logic.
3. Only when a `"test"` field with a `"q"` (question) was present did the script send a query to GPT-3.5 and assign the result to the `"a"` field.
4. This selective approach prevented token overflow and avoided unnecessary use of an LLM where standard logic suffices.
5. After processing, the corrected data was saved locally as `poprawiony_plik.json`.
6. Finally, the data was sent via `POST` to the specified API, and the server’s response (containing the flag) was displayed in both the console and a GUI popup.

## ⚠️ Challenges  
- The response from the API wasn’t handled at first – this was later corrected, enabling flag retrieval.
- The biggest challenge was the file size – processing it entirely via an LLM exceeded token limits. This taught me that AI should be used wisely and only where it brings actual value.

## 🧰 Tools & Libraries  
- Python 3  
- `openai` – GPT-3.5 API communication  
- `requests` – HTTP data transmission  
- `dotenv` – environment variable management  
- `tkinter` – GUI for file selection and feedback  
- `json`, `os` – local file operations

## 🎓 What I Learned  
- How to effectively combine classical programming with AI models.
- When NOT to use large language models (e.g., for basic logic tasks).
- How to manage API keys securely with `.env` and `.gitignore`.
- How to avoid token overflow when working with large JSON files.
- How to build a semi-automated tool for local data processing and API communication.

## 🇵🇱 Nazwa zadania  
Walidacja i uzupełnianie danych z użyciem modelu językowego

## 📌 Opis zadania  
Zadanie polegało na przetworzeniu pliku JSON zawierającego dane testowe (działania matematyczne oraz pytania tekstowe), automatycznej walidacji poprawności wyników, uzupełnieniu brakujących odpowiedzi z użyciem modelu GPT przez API, a następnie wysłaniu poprawionych danych do endpointu `https://centrala.ag3nts.org/report`, gdzie serwer zwracał flagę.

## 🔍 Moje podejście  
1. Skrypt w Pythonie umożliwiał wybór pliku JSON z pomocą GUI (`tkinter.filedialog`).
2. Każde działanie matematyczne (np. `"82 + 84"`) zostało sprawdzone i w razie potrzeby poprawione klasycznym podejściem programistycznym.
3. Tylko w przypadku obecności pola `"test"` i pytania `"q"` uruchamiane było zapytanie do modelu GPT-3.5, a wynik przypisywany do `"a"`.
4. Takie selektywne podejście pozwoliło uniknąć przekroczenia limitów tokenów oraz niepotrzebnego angażowania modelu LLM tam, gdzie można użyć prostego kodu.
5. Po zakończeniu przetwarzania dane zostały zapisane lokalnie jako `poprawiony_plik.json`.
6. Następnie całość została wysłana metodą `POST` do wskazanego API, a odpowiedź (z flagą) została wyświetlona w konsoli i przez GUI.

## ⚠️ Problemy i wyzwania  
- Początkowo brakowało obsługi odpowiedzi z API – dopiero po poprawce możliwe było odczytanie flagi.
- Największym wyzwaniem była wielkość pliku – jego analiza w całości przez model LLM przekraczała limit tokenów. To nauczyło mnie, że AI należy stosować rozsądnie i tylko tam, gdzie faktycznie wnosi wartość.

## 🧰 Wykorzystane narzędzia i biblioteki  
- Python 3  
- `openai` – do komunikacji z GPT-3.5  
- `requests` – do wysyłki danych HTTP  
- `dotenv` – zarządzanie zmiennymi środowiskowymi  
- `tkinter` – GUI do wyboru pliku i komunikatów  
- `json`, `os` – operacje na plikach

## 🎓 Czego się nauczyłem  
- Jak efektywnie łączyć klasyczne podejście programistyczne z modelami AI.
- Kiedy NIE używać dużych modeli językowych (np. do prostych operacji).
- Jak zabezpieczać klucze API i zarządzać `.env` oraz `.gitignore`.
- Jak unikać przekroczenia limitu tokenów w przypadku dużych plików JSON.
- Jak stworzyć półautomatyczne narzędzie przetwarzające dane lokalnie i komunikujące się z API.
