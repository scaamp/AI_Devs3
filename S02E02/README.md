# S02E02

## 🇬🇧 Task Name  
**City Map Recognition via GPT-4 Vision**

## Description  
The task was to analyze **four map fragments** (as image files) and identify the city they originate from. One of the fragments could intentionally be **incorrect** — i.e., from another city. The result had to be returned as a **JSON object** including the model's **reasoning process** (step-by-step) and final guess (`city`).

The solution required using GPT-4 Vision (`gpt-4o`) and sending **multiple base64-encoded images** in one request.  

## My Approach  
1. I created a GUI file selector using `tkinter`, allowing users to pick multiple `.jpg/.png` map fragments.
2. Each selected file was read and encoded in Base64.
3. A detailed **system prompt** was prepared instructing the model to analyze all four fragments and detect inconsistent one if needed.
4. I built the OpenAI API payload (`gpt-4o`) including the prompt and multiple image inputs.
5. The response (in JSON format with `_thinking` and `city`) was saved to `analysis_result.txt`.

## Challenges  
- Ensuring image ordering and encoding were correct.
- Structuring a strong prompt that guided the model toward geospatial reasoning and rejecting false positives.
- Avoiding token overflow when passing multiple high-resolution images.
- Handling one potentially fake fragment and letting the model identify it logically.

## Tools and Libraries  
- `Python 3.13`  
- `openai` – GPT-4o API  
- `base64` – file encoding  
- `tkinter` – file selector GUI  
- `dotenv` – API key management  
- `json`, `os` – utility libs

## What I Learned  
- How to interact with GPT-4o Vision using multiple base64 images in one request.
- How to create clean prompts that encourage step-by-step thinking and structured output.
- How to use GPT for visual analysis with high-quality reasoning.
- Improved file handling and GUI automation in Python for LLM-driven apps.

---

## 🇵🇱 Nazwa zadania  
**Rozpoznawanie miasta na podstawie mapy (Vision GPT-4)**

## Opis  
Zadanie polegało na analizie **czterech fragmentów mapy** (obrazy) i określeniu, z jakiego miasta pochodzą. Jeden z fragmentów mógł być **fałszywy** i pochodzić z innego miasta. Model miał zwrócić **nazwę miasta** oraz szczegółowy proces myślowy w formacie JSON (`_thinking`, `city`).

Całość zrealizowana została za pomocą GPT-4o (Vision).

## Moje podejście  
1. Stworzyłem GUI do wyboru plików z pomocą `tkinter`.
2. Wczytałem każdy obraz i zakodowałem go do Base64.
3. Przygotowałem prompt opisujący dokładne wymagania (rozpoznawanie obiektów, ulic, porównanie układu).
4. Wysłałem dane do modelu GPT-4o i uzyskałem odpowiedź w formacie JSON.
5. Wynik analizy został zapisany do pliku `analysis_result.txt`.

## Problemy i wyzwania  
- Weryfikacja spójności danych graficznych i ich kolejności.
- Doprecyzowanie promptu tak, aby model był zmotywowany do myślenia krok po kroku.
- Obsługa fragmentu, który był błędny – trzeba było zadbać, by model go odrzucił.
- Ograniczenia tokenów i jakości obrazu w Base64.

## Użyte biblioteki i narzędzia  
- `Python 3.13`  
- `openai` – komunikacja z GPT-4 Vision  
- `tkinter` – wybór plików  
- `dotenv`, `json`, `os`, `base64`

## Czego się nauczyłem  
- Jak wysyłać wiele obrazów do GPT-4o w jednym zapytaniu.
- Jak tworzyć prompty, które prowadzą model do przemyślanej analizy.
- Jak kodować pliki graficzne do Base64 i zintegrować je z API.
- Jak zaprojektować aplikację CLI/GUI do przetwarzania danych dla modelu.

---

> Finalna flaga została odnaleziona i zwrócona poprawnie.  
> 💡 Tip: sprawdzaj mapy z podziałem na warstwy i nazwy ulic – GPT-4 Vision rozpoznaje znaki, układ i topografię!

