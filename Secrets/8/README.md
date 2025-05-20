## 🇬🇧 Task Name  
**OCR Puzzle Decoder — Find the Hidden Word**

## Description  
The task was to extract a hidden flag encoded in the form of references like `A1S22` (paragraph 1, word 22) embedded in a visual note. The image contained a poetic text and a list of such position codes. These referred to another text (a separate scanned letter) that had to be analyzed via OCR.

The flag (i.e., the answer) was the name of a place — a concept described metaphorically in the decoded message. It could be deduced only by understanding the story.

## My Approach  
1. I created a Python app that lets the user select one or more image files.
2. I sent those images to GPT-4o Vision with a system prompt to extract full OCR text with **preserved paragraph structure**.
3. I split the OCR result into paragraphs and tokenized each word, labeling them in the format `AxSy`.
4. Based on the original puzzle reference list (`A1S53`, `A2S27`, etc.), I extracted the corresponding words and grouped them by rows.
5. The final extracted phrases formed a metaphorical message — describing a lost ideal world — leading to the answer.

## Challenges  
- Ensuring OCR accuracy despite varied formatting and fonts.
- Preserving logical paragraph grouping and word indexing to match puzzle references precisely.
- Handling text cleanup, token mapping, and edge cases (e.g., punctuation vs. words).
- Decoding the hidden meaning behind the extracted sentence.

## Tools and Libraries  
- `Python 3.13`  
- `openai` – GPT-4o API with Vision  
- `dotenv` – API key management  
- `tkinter` – GUI for file selection  
- `base64`, `os`, `text parsing`  

## What I Learned  
- How to perform OCR with GPT-4o while enforcing strict formatting constraints.
- How to tokenize and map natural language text into symbolic reference form (`AxSy`).
- How to decode metaphorical clues through symbolic extraction.
- How to build a complete AI pipeline: input image → vision + logic → decoded result.

---

## 🇵🇱 Nazwa zadania  
**Dekoder OCR — Znajdź Ukryte Hasło**

## Opis  
Zadanie polegało na odnalezieniu ukrytej flagi, zakodowanej jako odniesienia `A1S22` (akapit 1, słowo 22) w notatce. Na obrazie znajdował się tekst i zestaw zakodowanych pozycji. Odnosiły się one do innego obrazu z listem, który należało odczytać za pomocą OCR.

Flaga (czyli odpowiedź) to nazwa miejsca, ukryta symbolicznie w przesłaniu wynikającym z odczytanych słów.

## Moje podejście  
1. Stworzyłem aplikację w Pythonie z GUI do wyboru obrazów.
2. Przesłałem wybrane obrazy do modelu GPT-4o z prośbą o wykonanie OCR z zachowaniem akapitów.
3. Rozdzieliłem wynik na paragrafy i nadałem każdemu słowu indeks w formacie `AxSy`.
4. Na podstawie listy referencyjnej z notatki wydobyłem konkretne słowa i posortowałem je według układu.
5. Finalna wiadomość miała formę poetyckiego opisu — prowadzącego do hasła: **Atlantyda**.

## Problemy i wyzwania  
- Zachowanie dokładności OCR i pełnej struktury tekstu.
- Prawidłowa numeracja słów i akapitów (ważna dla poprawnego dekodowania).
- Obsługa znaków interpunkcyjnych i niejednoznacznych tokenów.
- Wydobycie sensu metaforycznego z rozszyfrowanej wiadomości.

## Użyte biblioteki i narzędzia  
- `Python 3.13`  
- `openai` – Vision GPT-4o API  
- `dotenv`, `tkinter`, `base64`, `os`

## Czego się nauczyłem  
- Jak korzystać z GPT-4o do OCR z zachowaniem formatowania.
- Jak zmapować słowa w tekście do indeksów (`A1S22`) i odtworzyć ukrytą treść.
- Jak tworzyć narzędzia dekodujące symbole i znaczenia ukryte w tekście.
- Jak zbudować kompletny pipeline: obraz → OCR + przetwarzanie → wynik.

---

🧩 Zadanie zakończone sukcesem — OCR + interpretacja + AI + logika

