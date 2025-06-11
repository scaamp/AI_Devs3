# S05E03

## 🇬🇧 Task Name  
Time-Locked Access Challenge

## Task Summary  
The goal was to solve a high-speed task (under 6 seconds) using LLMs. The process involved a time-based cryptographic challenge and dynamic question answering powered by AI. After authentication, two sets of questions were retrieved and had to be answered correctly and instantly using external context.

## 🔍 My Approach  
1. Sent password to obtain secure hash.
2. Used hash to receive a signed timestamp and two dynamic challenge URLs.
3. Retrieved the HTML-based knowledge source and converted it to markdown.
4. Downloaded question sets from two challenge URLs.
5. Sent all questions to OpenAI GPT model using **multithreading** for speed.
6. Compiled and returned all answers in one payload within the time limit.

## ⚠️ Challenges  
- All answers had to be provided **in Polish** and **under 6 seconds**.
- OpenAI requests were parallelized to reduce latency.
- Questions and endpoints changed dynamically, requiring real-time parsing.
- Contextual information (HTML) was preprocessed to markdown for LLM compatibility.

## 🧰 Tools & Libraries  
- Python 3.10  
- `requests` – API handling  
- `threading` – concurrent calls to LLM  
- `openai` – GPT model interface  
- `markdownify` – HTML to markdown conversion  
- `dotenv` – secrets management

## 🎓 What I Learned  
- Effective optimization of Python scripts for real-time execution  
- Concurrency using threading for ultra-fast LLM querying  
- Leveraging markdown-based context for improved LLM accuracy  
- Dealing with rapidly changing endpoints and questions

---

## 🇵🇱 Nazwa zadania  
Wyzwanie z czasowym dostępem

## Opis zadania  
Celem było rozwiązanie zadania z blokadą czasową (poniżej 6 sekund!) przy pomocy modeli językowych. Po autoryzacji należało pobrać dynamicznie zmieniające się pytania i odpowiedzieć na nie poprawnie oraz błyskawicznie, korzystając z kontekstu zawartego w pliku HTML.

## 🔍 Moje podejście  
1. Wysłałem hasło, aby uzyskać hash.  
2. Podpisałem hash, otrzymując `timestamp` i dwa adresy z pytaniami.  
3. Pobrałem i przekonwertowałem plik HTML do markdowna jako kontekst.  
4. Równolegle pobrałem pytania z dwóch źródeł.  
5. Każde pytanie wysłałem do modelu GPT w osobnym wątku.  
6. Zebrałem odpowiedzi i odesłałem całość w jednym zapytaniu.

## ⚠️ Wyzwania  
- Wszystkie odpowiedzi musiały być **po polsku** i w czasie < 6s.  
- Konieczne było równoległe zapytanie do LLM.  
- Kontekst (plik HTML) musiał być przekształcony do formatu zrozumiałego dla modelu (markdown).  
- Dynamiczne pytania i linki wymagały odporności kodu na zmiany.

## 🧰 Użyte biblioteki  
- Python 3.10  
- `requests`, `threading`, `openai`, `markdownify`, `dotenv`

## 🎓 Czego się nauczyłem  
- Optymalizacji kodu pod kątem ekstremalnej szybkości działania  
- Obsługi zapytań równoległych do modelu GPT  
- Konwersji HTML do markdown jako efektywnej formy kontekstu  
- Obsługi dynamicznych danych i endpointów w czasie rzeczywistym

---

