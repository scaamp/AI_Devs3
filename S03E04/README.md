# S03E04

## 🇬🇧 Task Name  
**Tracking Barbara Zawadzka**

## Description  
The task was to find the last known location of Barbara Zawadzka by analyzing a partial note and using two interconnected APIs (`/people` and `/places`). Each endpoint allowed querying either by name (to retrieve cities visited) or by city (to find people seen there). The data may be incomplete, so recursive and adaptive querying was required to build a graph of relations and discover where Barbara is hiding.

## My Approach  
1. I downloaded and parsed the content of the `barbara.txt` file.
2. I used GPT-4 to extract all names and cities from the note, structured as JSON.
3. For each person and city found, I queried the `/people` and `/places` endpoints.
4. The script recursively followed every new lead (new names and cities) discovered in the API responses.
5. I avoided infinite loops by storing already processed queries.
6. I sent each city found to the `/report` endpoint, hoping one of them would be Barbara's location.
7. All data was saved to a local file (`api_responses.json`) for analysis.

## Challenges  
- Avoiding infinite recursion and redundant API requests.
- Handling potentially missing or incomplete data.
- Managing delay to avoid API rate limits.
- Using GPT-4 for accurate and controlled extraction of structured data from unstructured text.

## Tools and Libraries  
- Python 3.13  
- `requests` – HTTP communication  
- `openai` – GPT-4 API  
- `dotenv` – managing environment variables  
- `json` – data processing  
- `time` – throttling requests

## What I Learned  
This task sharpened my skills in:
- working with recursive API traversal,
- prompt engineering for structured data extraction,
- writing robust scripts that loop through unpredictable data,
- simulating graph-like traversal without traditional graph libraries.

---

## 🇵🇱 Nazwa zadania  
**Namierzanie Barbary Zawadzkiej**

## Opis  
Celem zadania było znalezienie ostatniego znanego miejsca pobytu Barbary Zawadzkiej, analizując częściową notatkę oraz używając dwóch powiązanych ze sobą API (`/people` i `/places`). Każde z nich pozwalało na wyszukiwanie imienia (aby dostać miasta) lub miasta (aby dostać osoby widziane w danym miejscu). Dane mogły być niepełne, więc wymagane było rekurencyjne odpytanie i powiązanie wszystkich tropów.

## Moje podejście  
1. Pobrałem i sparsowałem zawartość pliku `barbara.txt`.
2. Za pomocą GPT-4 wyciągnąłem wszystkie imiona i miasta, formatując wynik jako JSON.
3. Dla każdej znalezionej osoby i miasta odpytuję API `/people` i `/places`.
4. Skrypt rekurencyjnie śledzi nowe tropy (imiona i miasta) znalezione w odpowiedziach.
5. Unikam zapętlenia, zapisując już przetworzone zapytania.
6. Każde znalezione miasto wysyłam do `/report`, licząc na to, że któreś z nich to miejsce pobytu Barbary.
7. Wszystkie odpowiedzi zapisałem lokalnie w `api_responses.json` do dalszej analizy.

## Problemy i wyzwania  
- Unikanie nieskończonej rekurencji i zbędnych zapytań.
- Radzenie sobie z niekompletnymi danymi z API.
- Ograniczenia szybkości zapytań (rate limit).
- Wydobycie dokładnych danych strukturalnych z tekstu z pomocą GPT-4.

## Użyte biblioteki i narzędzia  
- Python 3.13  
- `requests` – komunikacja z API  
- `openai` – użycie GPT-4  
- `dotenv` – zarządzanie kluczami środowiskowymi  
- `json` – obróbka danych  
- `time` – kontrola tempa zapytań

## Czego się nauczyłem  
Zadanie rozwinęło moje umiejętności w zakresie:
- pisania rekurencyjnych pętli analizujących dane z API,
- konstruowania promptów do wyciągania danych strukturalnych,
- zarządzania przetwarzaniem nieprzewidywalnych informacji,
- symulowania przejść grafowych bez potrzeby tworzenia struktur grafowych.
