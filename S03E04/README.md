# 🧠 AI_devs3 — S03E03: Hybrid Database Reasoning

## 🇬🇧 Task Name
`database`

## 🎯 Goal  
Query a real company database (BanAN) via provided API to identify IDs of **active datacenters** managed by **inactive employees (on leave)**.

## 🧩 My Approach  
1. Used the `show tables` and `show create table` SQL commands via the API to dynamically retrieve structure of all available tables.
2. Parsed the table schemas: `users`, `datacenters`, and `connections`.
3. Sent the structures and the natural language task to OpenAI's GPT-4 to generate a precise SQL query.
4. Executed the generated query via the API and received a list of matching datacenter IDs.
5. Reported the result to the central server to obtain the flag.
6. Additionally explored the `correct_order` table to find a potential hidden message using ordered letters.

## 📦 Technologies Used  
- Python 3  
- `requests` – for HTTP API calls  
- `dotenv` – to handle environment variables  
- `openai` – to generate SQL via GPT-4  
- JSON handling & dynamic code generation  

## ⚠️ Challenges  
- Required dynamic analysis of unknown DB structure.
- Avoided hardcoding by leveraging GPT-4 for context-based SQL generation.
- Ensured flexibility and scalability for future database tasks.

## ✅ What I Learned  
- Using OpenAI to automate SQL query writing based on schema and intent.
- Building general-purpose SQL agents with LLMs.
- API-driven database querying with full feedback cycle.

---

## 🇵🇱 Nazwa zadania
`database`

## 🎯 Cel  
Wykonanie zapytania do prawdziwej bazy danych firmy BanAN, aby znaleźć ID **aktywnych centrów danych**, którymi zarządzają **nieaktywni pracownicy (na urlopie)**.

## 🧩 Moje podejście  
1. Wysłałem zapytanie `show tables` i `show create table`, by dynamicznie pobrać strukturę wszystkich dostępnych tabel.
2. Przeanalizowałem schematy tabel: `users`, `datacenters` i `connections`.
3. Przesłałem strukturę oraz pytanie w języku naturalnym do GPT-4, aby wygenerował odpowiednie zapytanie SQL.
4. Wykonałem zapytanie poprzez API i otrzymałem listę pasujących ID centrów danych.
5. Odpowiedź została przesłana do centrali i uzyskałem flagę.
6. Dodatkowo przeszukałem tabelę `correct_order`, aby odkryć potencjalną ukrytą wiadomość na podstawie posortowanych liter.

## 📦 Technologie  
- Python 3  
- `requests` – komunikacja z API  
- `dotenv` – obsługa zmiennych środowiskowych  
- `openai` – generowanie SQL przez GPT-4  
- Obsługa JSON i dynamiczne generowanie kodu  

## ⚠️ Wyzwania  
- Dynamiczna analiza nieznanej struktury bazy.
- Unikanie hardcodowania zapytań – pełna elastyczność.
- Automatyzacja komunikacji z API i analiza odpowiedzi.

## ✅ Czego się nauczyłem  
- Automatyzacja pisania zapytań SQL za pomocą GPT-4.
- Budowa uniwersalnego agenta SQL z wykorzystaniem LLM.
- Obsługa zadań bazodanowych w sposób dynamiczny i skalowalny.
