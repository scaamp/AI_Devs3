# S05E01

# 🔍 phone (AI_DEVS3)

## 🇬🇧 Task Name  
Phone – Agent Conversations Analysis

## Task Summary  
This task involved analyzing five incomplete conversations between agents. Each dialogue was fragmented – only the first and last sentence were known, and the rest were scattered in a shared pool. The goal was to reconstruct the conversations, detect a liar based on inconsistencies, and answer six logic-based questions using information from the chats, external facts, or API responses.

## 🔍 My Approach  
1. Downloaded sorted and raw phone data from the API.
2. Iteratively reconstructed each of the 5 conversations using GPT-4 by:
   - Starting from the known first line.
   - Predicting the next sentence using LLM.
   - Removing matched sentence from the shared pool.
   - Repeating until reaching the final line.
3. Validated the number of lines per conversation.
4. Analyzed all completed conversations and inferred:
   - Who was lying.
   - Who said what to whom.
   - Who knew the API password and endpoint.
   - What facts were true or false.
5. Answered 6 questions:
   - If needed, scanned `.txt` files from the `facts/` folder.
   - Sent POST requests to the API to verify passwords.
6. Created a retry mechanism that:
   - Analyzes incorrect answers.
   - Remembers wrong guesses.
   - Adds facts or history to the next re-evaluation context.
   - Automatically fixes and resends.

## ⚠️ Challenges  
- Fragmented nature of conversation data.
- Sentence-by-sentence assembly using GPT.
- Handling indirect and ambiguous statements.
- Reanalysis logic with history and facts integration.

## 🧰 Tools & Libraries  
- Python 3.11  
- `openai` – GPT-4 for logic, prediction and JSON validation  
- `requests`, `json` – API and data transport  
- `dotenv` – key management  
- `glob`, `re` – file matching and extraction  
- `retry` logic for OpenAI and report handling

## 🎓 What I Learned  
- How to design a controlled sentence-by-sentence assembly system with LLM.
- How to track and fix incorrect answers iteratively.
- How to dynamically inject facts and feedback for reanalysis.
- How to manage state across retries and prevent loss of correct responses.

---

## 🇵🇱 Nazwa zadania  
Phone – Analiza rozmów agentów

## Opis zadania  
Zadanie polegało na analizie pięciu niepełnych rozmów między agentami. Każda rozmowa zawierała tylko pierwsze i ostatnie zdanie, a reszta zdań była pomieszana w jednej puli. Należało zrekonstruować każdą rozmowę, znaleźć osobę, która kłamie, i odpowiedzieć na sześć logicznych pytań korzystając z rozmów, plików `facts/*.txt`, oraz endpointów API.

## 🔍 Moje podejście  
1. Pobrałem dane (posegregowane i surowe) z API.
2. Używając GPT-4, iteracyjnie składałem każdą rozmowę:
   - Startując od pierwszego zdania.
   - Prosząc LLM o tylko jedno kolejne zdanie.
   - Usuwając dopasowane zdanie z puli.
   - Kończąc na ostatnim znanym zdaniu.
3. Sprawdzałem, czy długość rozmowy jest zgodna z oczekiwaniami.
4. Po złożeniu rozmów:
   - Identyfikowałem kłamcę.
   - Przypisywałem imiona do rozmówców.
   - Wyciągałem logiczne wnioski.
5. Odpowiadałem na pytania:
   - Jeśli potrzeba – czytałem pliki `.txt` z folderu `facts`.
   - Wysyłałem POST z hasłem na podany endpoint API.
6. Stworzyłem mechanizm poprawy:
   - Analizował niepoprawne odpowiedzi.
   - Zapamiętywał błędy.
   - Dodawał nowe konteksty (fakty, historia prób).
   - Poprawiał odpowiedzi i wysyłał ponownie.

## ⚠️ Problemy i wyzwania  
- Konieczność iteracyjnego składania zdań w rozmowie.
- Niektóre informacje były tylko zasugerowane – trzeba było je wywnioskować.
- Obsługa API i odczyt z plików faktów.
- Poprawianie błędnych odpowiedzi bez nadpisania poprawnych.

## 🧰 Użyte biblioteki  
- Python 3.11  
- `openai` – GPT-4 do logiki, przewidywania, i weryfikacji JSON  
- `requests`, `json` – komunikacja z API  
- `dotenv` – obsługa kluczy API  
- `glob`, `re` – obsługa plików i ekstrakcji danych  
- retry & feedback loop na etapie raportowania

## 🎓 Czego się nauczyłem  
- Jak zbudować system krokowego składania tekstu z pomocą LLM.
- Jak tworzyć stabilne strategie poprawiania błędów z pamięcią kontekstu.
- Jak adaptacyjnie używać faktów i historii prób w promptach.
- Jak zarządzać pełnym stanem odpowiedzi i uniknąć nadpisywania poprawnych danych.


