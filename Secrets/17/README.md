
# S05E02 – GPS Agent

## 🇵🇱 Wersja polska

### Zadanie

Celem było odtworzenie agenta GPS, który wcześniej działał w Centrali. Agent ten miał za zadanie:

- Zinterpretować pytanie z `gps_question.json`.
- Zidentyfikować osoby, które znajdują się w Lubawie (z wykorzystaniem `/places`).
- Odfiltrować Barbarę (monitorowana przez roboty).
- Pobrać `userID` z bazy danych przez `/apidb`.
- Pobrać współrzędne GPS przez endpoint `/gps`.
- Zwrócić dane w odpowiednim formacie JSON do Centrali.

### Podejście

Zbudowano pełnego agenta w Pythonie, który:
- Parsuje pytanie i dane z logów (`gps.txt`).
- Łączy się z wszystkimi wymaganymi API.
- Wyklucza Barbarę z wyników.
- Pobiera współrzędne GPS dla pozostałych osób.
- Wysyła wynik do `/report`.

### Format odpowiedzi

```json
{
  "RAFAL": { "lat": 53.451974, "lon": 18.759189 },
  "AZAZEL": { "lat": 50.064851, "lon": 19.949881 },
  "SAMUEL": { "lat": 53.503570, "lon": 19.745866 }
}
```

### ✅ Flaga główna

Została poprawnie odesłana do `/report`.

---

### 🕵️‍♂️ Sekretna flaga – "HTTPS to miejsce. Gdzie ono jest?"

#### Trop:

- Wysłanie zapytania do `/gps` z `userID = 443`.
- Odpowiedź: `{"lat": "tego szukasz?", "lon": "https://centrala.ag3nts.org/whereis.txt"}`.
- Plik zawierał ciąg liczb i ukryty akrostych: **ASCII**.
- Po przeliczeniu wartości float na znaki ASCII otrzymano:

## 🇬🇧 English version

### Task

Recreate a broken GPS agent previously used by the Central. The agent's mission:

- Parse the prompt in `gps_question.json`.
- Identify people currently located in "Lubawa" via `/places`.
- Filter out Barbara (monitored).
- Get each user's `userID` via `/apidb`.
- Retrieve GPS coordinates via `/gps`.
- Return a final JSON response to the `/report` endpoint.

### Approach

A Python agent was developed which:
- Parsed the prompt and logs (`gps.txt`).
- Integrated with all required APIs.
- Excluded Barbara from GPS lookups.
- Queried GPS coordinates for the remaining users.
- Posted the final answer to Central.

### Final response format

```json
{
  "RAFAL": { "lat": 53.451974, "lon": 18.759189 },
  "AZAZEL": { "lat": 50.064851, "lon": 19.949881 },
  "SAMUEL": { "lat": 53.503570, "lon": 19.745866 }
}
```

### ✅ Main Flag

Successfully submitted to `/report`.

---

### 🕵️‍♂️ Secret Flag – "HTTPS is a place. Where is it?"

#### The path:

- Queried `/gps` with `userID = 443`.
- Response: `{"lat": "tego szukasz?", "lon": "https://centrala.ag3nts.org/whereis.txt"}`.
- The file contained a list of coordinates + the clue: **ASCII**.
- Decoding float values as ASCII characters gave:

