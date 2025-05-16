# S01E05

## 🇬🇧 Task Name  
**Censorship of Personal Data**

## Description  
The goal was to create a censorship system for personal data. The application had to download data from a dynamic `.txt` file and censor the following details: first name and last name, age, city, street and house number — all replaced with the word `CENZURA`. The result had to be submitted to an API in a fixed JSON structure. A key constraint was preserving all punctuation and formatting in the original text.

## My Approach  
1. I downloaded the latest `cenzura.txt` from the API endpoint (changing every 60 seconds).  
2. I created a Python script using a local model (`gemma3:latest`) running in an Ollama Docker container.  
3. The prompt explicitly defined the rules, including an example, and emphasized one replacement word only.  
4. I sent the prompt to the local Ollama model via `http://localhost:11434/api/generate`.  
5. I stripped trailing newlines and sent the final output to the report API in the correct format.

## Challenges  
- The model occasionally returned `CENZURA CENZURA` instead of a single word — I refined the prompt with a strict example block.  
- The validation system is extremely sensitive to formatting (spaces, periods, commas).  
- At first, the flag response returned an error due to formatting mismatches, despite correct censorship.

## Tools and Libraries  
- Python 3.13  
- `requests` – downloading and posting to APIs  
- Ollama – running local offline models  
- `dotenv` – key management  
- Docker – containerization of local AI model  

## What I Learned  
This task improved my skills in prompt design, model control, offline inference with Ollama, and formatting-sensitive data processing. I gained insight into practical censorship tasks and learned how to enforce model behavior with examples and strict rules.

# S01E5

## 🇵🇱 Nazwa zadania  
**Cenzura danych osobowych**

## Opis  
Celem było stworzenie systemu do cenzurowania danych osobowych. Aplikacja musiała pobierać dane z dynamicznego pliku `.txt` i ocenzurować: imię i nazwisko, wiek, miasto, ulicę oraz numer domu — zamieniając każde z nich na słowo `CENZURA`. Wynik należało przesłać do API w ściśle określonym formacie JSON. Kluczowym ograniczeniem było zachowanie wszystkich znaków interpunkcyjnych i formatu oryginału.

## Moje podejście  
1. Pobierałem aktualny plik `cenzura.txt` z API (zmieniający się co 60 sekund).  
2. Napisałem skrypt w Pythonie z użyciem lokalnego modelu (`gemma3:latest`) działającego w kontenerze Docker z Ollamą.  
3. Prompt zawierał ścisłe zasady oraz przykład, wymuszając dokładne zastępowanie danymi.  
4. Zapytanie wysyłałem na lokalne API `http://localhost:11434/api/generate`.  
5. Na końcu usuwałem nadmiarowe znaki (`\n`) i przesyłałem wynik w poprawnym formacie do API raportowego.

## Problemy i wyzwania  
- Model czasami generował `CENZURA CENZURA` – dodałem sekcję z przykładem i doprecyzowałem prompt.  
- System walidacyjny był ekstremalnie czuły na interpunkcję i liczbę słów.  
- Początkowo odpowiedź nie była akceptowana przez API pomimo poprawnej cenzury – problem leżał w formatowaniu.

## Narzędzia i biblioteki  
- Python 3.13  
- `requests` – komunikacja z API  
- Ollama – lokalne uruchomienie modelu AI  
- `dotenv` – zarządzanie kluczem API  
- Docker – konteneryzacja modelu  

## Czego się nauczyłem  
Zadanie nauczyło mnie pracy z lokalnymi modelami AI, precyzyjnego projektowania promptów oraz obsługi danych, gdzie liczy się każdy znak. Praca offline nad zadaniem, gdzie wynik musi być zgodny co do znaku, była dobrą lekcją kontroli nad zachowaniem modelu.

