
# 🧠 AI_Devs3 – Task: Dokumenty / Documents

## 🇬🇧 Task Name
**Document Analysis with Cross-Referenced Fact Matching**

## Description  
The goal of this task was to generate **keyword lists for multiple reports** using **fact files** provided in `.txt` format. The model had to:
- analyze each report (TXT),
- match it with relevant facts (based on names/sectors),
- generate keywords in Polish (noun case, comma-separated, no spaces),
- and send the final answer to the API endpoint.

The facts were stored in separate `.txt` files, parsed once by GPT-4 and saved as structured JSON (`osoby` and `sektory`).

## My Approach  
1. **Selected fact `.txt` files** via file dialog and parsed them with OpenAI (GPT-4) into structured JSON.
2. Saved results as `przetworzone_fakty.json` and `przeksztalcone_fakty.json` (merged view).
3. **Selected report `.txt` files** via file dialog.
4. For each report:
   - Extracted names/sectors using GPT-4.
   - Matched them against pre-parsed JSON facts.
   - Sent a second prompt to GPT-4 to generate a final keyword list.
5. Results were saved as `wyniki_analizy.json` and submitted to `https://centrala.ag3nts.org/report`.

## Key Features  
- GUI file selection for facts and reports
- OpenAI GPT-4 used for two-step reasoning
- Automatic deduplication of sectors and persons across fact files
- Reusable cache of processed facts
- Modular structure (main task, parsing, matching, final reporting)

## Tools and Libraries  
- Python 3.11+  
- `openai` – GPT-4 API communication  
- `tkinter` – GUI for file selection  
- `requests` – POST results to endpoint  
- `dotenv` – for loading API keys

## Sample Output Format
```json
{
  "nazwa_pliku": "raport1.txt",
  "slowa_kluczowe": "roboty,technicy,test,identyfikatory"
}
```

## What I Learned  
- Designing multi-phase LLM pipelines with context chaining  
- Parsing GPT responses and ensuring valid JSON  
- Keyword deduplication and text normalization  
- Efficient use of OpenAI API via selective calls  
- Managing prompt engineering across different input formats

---

## 🇵🇱 Nazwa zadania  
**Analiza dokumentów i dobór słów kluczowych na podstawie faktów**

## Opis  
Celem zadania było wygenerowanie **list słów kluczowych dla raportów**, bazując na osobnych plikach `.txt` zawierających fakty. Model musiał:
- przeanalizować treść raportów,
- dopasować do nich fakty (na podstawie nazwisk i sektorów),
- wygenerować słowa kluczowe w języku polskim (mianownik, przecinki, bez spacji),
- i ostatecznie wysłać wynik na wskazany endpoint.

Fakty zostały przetworzone tylko raz i zapisane w postaci ustrukturyzowanego JSON-a (`osoby`, `sektory`).

## Moje podejście  
1. Wybrałem pliki `.txt` z faktami przez eksplorator plików i przetworzyłem je przez GPT-4.
2. Zapisane dane JSON: `przetworzone_fakty.json`, `przeksztalcone_fakty.json`.
3. Wybrałem pliki `.txt` z raportami.
4. Dla każdego raportu:
   - Wyodrębniłem osoby i sektory z użyciem GPT-4.
   - Dopasowałem dane z wcześniej zapisanych faktów.
   - Wygenerowałem słowa kluczowe z pomocą GPT-4.
5. Wyniki zapisano jako `wyniki_analizy.json` i wysłano do `https://centrala.ag3nts.org/report`.

## Główne funkcje  
- Wybór plików z GUI (tkinter)  
- Dwuetapowa analiza z GPT-4 (osoby/sektory ➝ słowa kluczowe)  
- Przetwarzanie i unifikacja faktów w JSON  
- Automatyczna deduplikacja  
- Wysyłka wyników do API

## Użyte biblioteki  
- Python 3.11+  
- `openai` – komunikacja z GPT-4  
- `tkinter` – GUI do wyboru plików  
- `requests` – wysyłanie POST na endpoint  
- `dotenv` – obsługa kluczy API

## Format końcowy  
```json
{
  "nazwa_pliku": "raport1.txt",
  "slowa_kluczowe": "roboty,technicy,test,identyfikatory"
}
```

## Czego się nauczyłem  
- Projektowania etapowej pracy z LLM (zachowanie kontekstu między zapytaniami)  
- Obsługi błędów parsowania JSON z odpowiedzi GPT  
- Doboru i przetwarzania słów kluczowych  
- Minimalizacji zapytań do API przez cache  
- Pracy z JSON-em i integracją OpenAI z własnym kodem
