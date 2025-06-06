# 🧠 AI_Devs3 – Task: Dokumenty / Documents

## 🇬🇧 Task Name  
**Data Validation via Supervised Fine-Tuning**

## Description  
The goal of the task was to **train a fine-tuned OpenAI model** using `correct.txt` and `incorrect.txt`, and then use it to validate a third dataset (`verify.txt`). Each line represented a research result that had to be classified as valid (`1`) or invalid (`0`), using a model fine-tuned on binary-labeled data.

The final goal was to send the **IDs of only correct entries** (classified as `1`) to the central server API.

## My Approach  
1. Created a `train.jsonl` file based on the structure required for supervised fine-tuning.
2. Fine-tuned the model using `gpt-4.1-mini-2025-04-14` on the OpenAI fine-tuning dashboard.
3. Loaded `verify.txt`, and for each line:
   - Sent it to the fine-tuned model using Chat Completion format with a fixed system message.
   - Checked whether the model answered `"1"` or `"true"`.
4. Collected the line numbers of valid results.
5. Sent the final result as JSON to the central API endpoint.

## Key Features  
- Full automation: preprocessing, training, classification, and submission
- JSONL generation for fine-tuning
- Use of `.env` for secure API key management
- Deduplicated results and structured submission

## Tools and Libraries  
- Python 3.11+  
- `openai` – API communication  
- `requests` – HTTP submission  
- `dotenv` – API key loading

## Sample Output Format  
```json
{
  "task": "research",
  "apikey": "YOUR_API_KEY",
  "answer": ["01", "02", "09", "10"]
}
```

## What I Learned  
- Fine-tuning GPT models with supervised data  
- Structuring fine-tuning datasets using JSONL  
- Ensuring deterministic behavior via `temperature=0`  
- Matching prompt structure between training and inference  
- API result validation and automated submission
---

## 🇵🇱 Nazwa zadania  
**Walidacja danych z wykorzystaniem fine-tuningu**

## Opis  
Zadanie polegało na **wytrenowaniu modelu OpenAI**, który na podstawie danych z plików `correct.txt` i `incorrect.txt` nauczy się klasyfikować wyniki badań jako poprawne (`1`) lub błędne (`0`). Następnie należało użyć tego modelu do sprawdzenia zawartości pliku `verify.txt` i wysłać do API jedynie ID tych wierszy, które model uznał za poprawne.

## Moje podejście  
1. Przygotowałem plik `train.jsonl` zgodny z dokumentacją supervised fine-tuning.
2. Przeprowadziłem fine-tuning modelu `gpt-4.1-mini-2025-04-14` w panelu OpenAI.
3. Wczytałem dane z `verify.txt` i dla każdego wiersza:
   - Wysłałem zapytanie do wytrenowanego modelu z komunikatem systemowym.
   - Sprawdziłem, czy odpowiedź to `"1"` lub `"true"`.
4. Zidentyfikowałem poprawne identyfikatory.
5. Przygotowałem finalny plik wynikowy i wysłałem go do endpointu centrali.

## Główne funkcje  
- Automatyczne tworzenie pliku JSONL do fine-tuningu  
- Pełna automatyzacja: trening, klasyfikacja, wysyłka  
- Obsługa plików `.env` z kluczami API  
- Walidacja wyników i eksport do API w poprawnym formacie

## Użyte biblioteki  
- Python 3.11+  
- `openai` – komunikacja z API  
- `requests` – zapytania HTTP  
- `dotenv` – obsługa kluczy środowiskowych

## Format końcowy  
```json
{
  "task": "research",
  "apikey": "TWÓJ_KLUCZ_API",
  "answer": ["01", "02", "09", "10"]
}
```

## Czego się nauczyłem  
- Fine-tuning modeli GPT w trybie supervised  
- Przygotowanie danych treningowych w formacie JSONL  
- Wykorzystanie temperatury 0 do stabilizacji wyników  
- Zachowanie spójności promptów między treningiem a inferencją  
- Automatyczna walidacja i wysyłka wyników na endpoint API