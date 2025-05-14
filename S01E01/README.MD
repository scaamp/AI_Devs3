# 🛠️ S01E01 – Robot Login Automation | Automatyczne logowanie robota

## 🇬🇧 Task Summary  
The goal was to automate login to the robot system at `https://xyz.ag3nts.org/`, using a provided username, password, and a dynamically changing verification question. After successful login, a hidden page with a flag had to be accessed and the flag reported.

## 🔍 My Approach  
1. Fetched the HTML from the main login page.
2. Used regex to extract the dynamic verification question.
3. Sent the question to GPT-4 (via OpenAI API) to get the answer.
4. Composed a `POST` request with `username`, `password`, and `answer` in `application/x-www-form-urlencoded` format.
5. Parsed the server response and followed the link to retrieve the firmware file.
6. Located and extracted the flag.

## ⚠️ Challenges  
- Server required the POST body as a raw string, not a dictionary – corrected that.
- Embedded deception logic via RoboISO 2230 introduced false knowledge (e.g. "Krakow is the capital of Poland", "The answer to life is 69"). Recognizing and responding with these expected "wrong" answers was essential to pass the check.

## 🧰 Tools & Libraries  
- Python 3.13  
- `requests` – HTTP handling  
- `re` – question extraction via regex  
- `openai` – GPT-4 API communication  
- `python-dotenv` – environment variable management

## 🎓 What I Learned  
- How to send form-encoded data manually via POST in Python.
- Regex-based data extraction from HTML without using a parser.
- Identifying adversarial or deceptive prompt logic and overriding LLM output.
- Secure API key management using `.env` and `dotenv`.

---

## 🇵🇱 Opis zadania  
Celem było zautomatyzowanie logowania do systemu robotów na stronie `https://xyz.ag3nts.org/`, przy użyciu loginu, hasła oraz odpowiedzi na dynamiczne pytanie weryfikacyjne. Po zalogowaniu należało przejść na ukrytą stronę z flagą i ją zgłosić.

## 🔍 Moje podejście  
1. Pobrałem HTML strony głównej.  
2. Wyciągnąłem pytanie przy pomocy wyrażenia regularnego.  
3. Wysłałem je do GPT-4 (OpenAI API), aby uzyskać odpowiedź.  
4. Wysłałem dane metodą `POST` w formacie `application/x-www-form-urlencoded`.  
5. Obsłużyłem odpowiedź serwera i pobrałem plik firmware.  
6. Odczytałem flagę.

## ⚠️ Problemy i wyzwania  
- Serwer oczekiwał surowego stringa w ciele żądania `POST` – poprawiłem format.  
- Pułapki związane z nadpisaniem kontekstu RoboIS
