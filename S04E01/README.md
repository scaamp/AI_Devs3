# S04E01

## 🇬🇧 Task Name  
Photo Forensics – Barbara Sketch

## Task Summary  
The task involved analyzing low-quality or corrupted images provided by the central server using an image-enhancement bot. The final goal was to identify which photos depict Barbara, and based on those, generate a detailed verbal description of her appearance.

## 🔍 My Approach  
1. Initiated the task by sending a `POST` request with `"answer": "START"` to `/report`, retrieving four image filenames.
2. Used OpenAI Vision (GPT-4) to:
   - Analyze each image.
   - Select one of four actions: `REPAIR`, `BRIGHTEN`, `DARKEN`, or `NONE`.
   - Justify the decision using a JSON structure.
3. For `REPAIR`, `BRIGHTEN`, or `DARKEN`, the corresponding action was sent to the bot.
   - If a new image was returned, it was added to the processing queue.
4. If the action was `NONE`, I assumed the image quality was sufficient and generated a detailed Polish-language description of the person in the image.
5. If a response from the server contained a flag (pattern: `{{FLG:...}}`), the program terminated successfully and displayed the flag.

## ⚠️ Challenges  
- Handling base64 image embedding for Vision API requests.
- Parsing and extracting filenames and new images from verbose bot responses.
- Interpreting malformed or missing JSON fields.
- Loop control for iterative image enhancement and re-processing.

## 🧰 Tools & Libraries  
- Python 3.11  
- `openai` – GPT-4 Vision API  
- `requests` – HTTP communication  
- `re` – regex for image parsing  
- `dotenv` – loading secret keys  
- `base64` – for embedding image data

## 🎓 What I Learned  
- How to implement an iterative, LLM-driven image analysis and repair pipeline.
- Effective use of Vision models for multimodal feedback loops.
- Automating real-time interactions with external tools for visual data processing.

## 🇵🇱 Nazwa zadania  
Fotoforensyka – Rysopis Barbary

## Opis zadania  
Zadanie polegało na analizie uszkodzonych lub niskiej jakości zdjęć udostępnionych przez centralę. Celem końcowym było zidentyfikowanie zdjęć przedstawiających Barbarę, a następnie wygenerowanie szczegółowego rysopisu jej wyglądu na podstawie tych obrazów.

## 🔍 Moje podejście  
1. Rozpocząłem zadanie wysyłając żądanie `POST` z `"answer": "START"` na `/report`, uzyskując listę nazw czterech zdjęć.
2. Wykorzystałem OpenAI Vision (GPT-4) do:
   - Analizy każdego zdjęcia.
   - Wybrania jednej z czterech akcji: `REPAIR`, `BRIGHTEN`, `DARKEN` lub `NONE`.
   - Zwrotu decyzji i uzasadnienia w formacie JSON.
3. Dla zdjęć wymagających poprawy (`REPAIR`, `BRIGHTEN`, `DARKEN`) wysyłałem komendę do bota.
   - Jeśli pojawiały się nowe zdjęcia, dodawałem je do kolejki przetwarzania.
4. W przypadku akcji `NONE` zakładałem, że jakość zdjęcia jest wystarczająca i generowałem rysopis postaci w języku polskim.
5. Jeśli odpowiedź centrali zawierała flagę (wzorzec: `{{FLG:...}}`), program kończył działanie i wyświetlał flagę.

## ⚠️ Problemy i wyzwania  
- Obsługa kodowania obrazów do formatu base64 na potrzeby Vision API.
- Parsowanie i wyciąganie nazw plików oraz nowych zdjęć z rozbudowanych odpowiedzi bota.
- Radzenie sobie z niepoprawnym lub brakującym JSON-em.
- Pętla kontroli przetwarzania i naprawiania zdjęć w czasie rzeczywistym.

## 🧰 Użyte biblioteki  
- Python 3.11  
- `openai` – API GPT-4 Vision  
- `requests` – obsługa HTTP  
- `re` – wyrażenia regularne do analizy nazw plików  
- `dotenv` – wczytywanie kluczy API  
- `base64` – kodowanie obrazów

## 🎓 Czego się nauczyłem  
- Jak zbudować iteracyjny pipeline do analizy i naprawy zdjęć z wykorzystaniem LLM.
- Jak skutecznie wykorzystywać modele Vision do sprzężenia zwrotnego w analizie wizualnej.
- Automatyzacji interakcji z zewnętrznym systemem przetwarzania danych wizualnych.