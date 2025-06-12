# 🛰️ S05E02 — GPS Agent & HTTPS Flag

## 🇬🇧 English Summary

### Task Description
In this task, we recovered logs from an old agent used by the Centrala. The agent had been previously repurposed from robot forces and helped retrieve GPS coordinates of people using a `userID`. The key steps included:
- Analyzing logs to infer the agent's behavior.
- Rebuilding the agent to mimic its decision-making and functionalities.
- Integrating two APIs:
  - `/apidb` from S03E03 for user information (getting user IDs).
  - `/places` from S03E04 to get people in a specific location.
  - `/gps` to retrieve actual GPS coordinates.

The challenge also involved ignoring GPS queries for a specific user (Barbara), as this would trigger alerts.

### Steps
1. Parse the Centrala's question.
2. Use `/places` to find all users in "Lubawa".
3. Skip "Barbara", and for each other user:
   - Retrieve their `userID` via a SQL query to `/apidb`.
   - Use the `userID` to query `/gps` and get coordinates.
4. Submit the final result to `/report` under the `gps` task.

### Secret Flag (⚠️ Optional)
The additional hidden challenge was to find a secret flag related to HTTPS. After experimenting and analyzing the certificate, headers, and brute-forcing userIDs, we found that `userID = 443` returned:
```json
{ "lat": "tego szukasz?", "lon": "https://centrala.ag3nts.org/whereis.txt" }
```
The `whereis.txt` contained a list of coordinates and a hint. Decoding the coordinates (e.g., as ASCII values or inspecting character positions) led to the secret flag.

---

## 🇵🇱 Podsumowanie po polsku

### Opis Zadania
W tym zadaniu odzyskaliśmy logi ze starego agenta używanego przez Centralę. Agent ten był wcześniej przejęty od sił robotów i służył do pobierania współrzędnych GPS osób na podstawie ich `userID`. Kluczowe kroki obejmowały:
- Analizę logów w celu zrozumienia zachowania agenta.
- Odtworzenie jego działania we własnym środowisku.
- Integrację z dwoma API:
  - `/apidb` z S03E03 — pobieranie ID użytkowników.
  - `/places` z S03E04 — ustalanie osób w danym miejscu.
  - `/gps` — pobieranie współrzędnych.

Wyjątkowym warunkiem było pominięcie Barbary — każda próba pobrania jej lokalizacji uruchamiała alarm.

### Kroki
1. Parsujemy pytanie z Centrali.
2. Za pomocą `/places` szukamy osób w miejscowości „Lubawa”.
3. Pomijamy Barbarę, a dla pozostałych:
   - Pobieramy ich `userID` zapytaniem SQL do `/apidb`.
   - Korzystamy z `/gps` aby pobrać współrzędne.
4. Wysyłamy dane do `/report` jako zadanie `gps`.

### Sekretna Flaga (⚠️ Opcjonalnie)
Dodatkowym ukrytym wyzwaniem była flaga powiązana z HTTPS. Po analizie certyfikatów, nagłówków i brute-force’ie numerów `userID`, odkryliśmy że:
```json
userID = 443
```
zwraca:
```json
{ "lat": "tego szukasz?", "lon": "https://centrala.ag3nts.org/whereis.txt" }
```
Plik `whereis.txt` zawierał współrzędne oraz wskazówki. Ich analiza (np. jako wartości ASCII) doprowadziła do flagi.

---

✅ **Final flag for main task**: submitted via `/report`  
🏁 **Secret flag**: obtained from coordinate puzzle linked to `userID = 443`