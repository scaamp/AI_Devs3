# S04E04

## 🇬🇧 Task Name  
Autonomous Drone Navigation – Webhook Map Challenge

## Task Summary  
The goal was to build an HTTPS API (webhook) that would receive natural language drone navigation instructions and return a description of the final location on a 4x4 grid map. The drone always starts from the top-left corner. The challenge tested LLM integration, precise parsing, and correct routing.

## 🔍 My Approach  
1. I prepared a 4x4 map as a dictionary of coordinates to place descriptions.
2. Built a Flask API with `/drone` POST endpoint to receive instructions.
3. Used OpenAI's GPT-4 to convert natural language into structured movement (`up/down/left/right`).
4. Computed the drone’s final position from `(0,0)` based on parsed movement.
5. Returned a short two-word description of the final field.
6. Hosted the API on Azyl under a public HTTPS URL (port 54236).
7. Submitted the URL to the central server at `/report`.

## ⚠️ Challenges  
- GPT occasionally returned invalid JSON → added error handling and fallback.
- Had to ensure boundaries were enforced (map limits 0–3).
- Deployment on Azyl required careful port binding and virtualenv setup.
- Required strict adherence to output format (`{"description": "..."}`).

## 🧰 Tools & Libraries  
- Python 3.11  
- `Flask` – API server  
- `openai` – GPT-4 integration  
- `python-dotenv` – env variables  
- `requests`, `json`, `os`, `re`  

## 🎓 What I Learned  
- How to integrate GPT-4 to extract structured data from natural text.
- Building a secure, stateless webhook service.
- Hosting Python API apps on remote servers (Azyl SSH).
- Error control, fallback logic, map boundary handling, and instruction parsing.

---

## 🇵🇱 Nazwa zadania  
Autonomiczna nawigacja drona – wyzwanie webhook + mapa

## Opis zadania  
Celem było zbudowanie webhooka HTTPS, który odbiera instrukcje lotu drona zapisane w języku naturalnym i zwraca opis końcowej lokalizacji na mapie 4x4. Dron zawsze startuje z pozycji `(0,0)`. Kluczowe było poprawne parsowanie, bezstanowość oraz dokładność odpowiedzi.

## 🔍 Moje podejście  
1. Przygotowałem mapę 4x4 jako słownik współrzędnych i opisów miejsc.
2. Zbudowałem API we Flasku z endpointem `/drone` (POST).
3. Do parsowania instrukcji użyłem GPT-4 (model chat completions).
4. Na podstawie odpowiedzi JSON wyliczałem pozycję końcową drona.
5. Zwracałem dwuwyrazowy opis pola na tej pozycji.
6. Udostępniłem aplikację na Azylu (port 54236) pod HTTPS.
7. Wysłałem adres webhooka do centrali `/report`.

## ⚠️ Problemy i wyzwania  
- GPT czasem zwracał niepoprawny JSON – obsłużyłem wyjątki i ustawiłem fallback.
- Trzeba było ograniczyć ruch drona do granic mapy (0–3).
- Hosting na Azylu wymagał dokładnego ustawienia środowiska i portu.
- Format odpowiedzi musiał być ściśle przestrzegany: `{"description": "..."}`.

## 🧰 Użyte biblioteki  
- Python 3.11  
- `Flask` – serwer API  
- `openai` – integracja z GPT-4  
- `dotenv` – zmienne środowiskowe  
- `requests`, `json`, `os`, `re`

## 🎓 Czego się nauczyłem  
- Jak używać GPT-4 do ekstrakcji strukturalnych danych z tekstu naturalnego.
- Budowanie bezpiecznego, bezstanowego webhooka.
- Hosting aplikacji Pythonowych na zdalnym serwerze (Azyl).
- Obsługa błędów, granic mapy, fallback i parsowanie instrukcji z LLM.
