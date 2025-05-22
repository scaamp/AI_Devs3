# 🧠 S02E04 — Categories / Kategorie (AIDevs 3)

## 🇬🇧 English Version

### 📝 Task Description

The goal was to process a set of daily factory reports and extract:

- any signs of **captured humans** or **traces of their presence**,
- any **fixed hardware failures** (excluding software).

The task required multimodal data processing across formats: `.txt`, `.png`, `.mp3`.

---

### ⚙️ Technologies & Tools

- Python 3.11+
- `openai` — GPT-4o and Whisper APIs
- `pytesseract` + Tesseract OCR
- `Pillow` — image handling
- `tkinter` — file selection dialog
- `dotenv` — managing API keys
- `requests` — API communication

---

### 🧪 Execution Flow

1. 🗂️ **File Selection** — User selects `.txt`, `.png`, `.mp3` files.
2. 📖 **Text Extraction**:
   - TXT: plain text read.
   - PNG: OCR via Tesseract.
   - MP3: transcription via Whisper (`whisper-1`).
3. 🧠 **Content Analysis** — Combined text is sent to GPT-4o with a system prompt to classify into `people` and `hardware`.
4. 💾 **Saving Output**:
   - All merged text: `combined_texts.txt`
   - Analysis result: `analysis_result.json`
   - Audio transcripts: `transcriptions.txt`
5. 📤 **Submission** — Result sent as JSON to:  
   `https://c3ntrala.ag3nts.org/report`

---

### 📁 JSON Result Structure

```json
{
  "task": "kategorie",
  "apikey": "YOUR_AIDEVS_KEY",
  "answer": {
    "people": ["file1.txt", "file2.mp3"],
    "hardware": ["file4.png", "file5.mp3"]
  }
}
```

---

### ✅ Running the Script

1. Create `.env` file with your keys:

   ```
   OPENAI_API_KEY=sk-...
   AIDEVS_KEY=...
   ```

2. Make sure you have installed:

   - Tesseract OCR ([UB Mannheim build for Windows](https://github.com/UB-Mannheim/tesseract/wiki))
   - FFMPEG (required for Whisper)

3. Install Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the script:

   ```bash
   python main.py
   ```

---

### ✨ Features

- Transcription caching in `transcriptions.txt`
- Error handling for OCR, Whisper, and API calls
- Auto reuse of previous analysis if files are unchanged

---

### 📚 What I Learned

- Integrating OCR + STT + LLM in one pipeline
- Practical use of GPT-4o for data extraction & classification
- Working with multimodal formats
- Automating and safeguarding analysis logic in RAG-like tasks

---

## 🇵🇱 Wersja Polska

### 📝 Opis zadania

Celem było przetworzenie dziennych raportów z fabryki i wyodrębnienie informacji:

- o **schwytanych ludziach** lub **śladach ich obecności**,
- o **naprawionych usterkach sprzętowych** (bez softu).

Zadanie wymagało przetwarzania danych w formatach: `.txt`, `.png`, `.mp3`.

---

### ⚙️ Technologie i narzędzia

- Python 3.11+
- `openai` — API GPT-4o i Whisper
- `pytesseract` + Tesseract OCR
- `Pillow` — obsługa obrazów
- `tkinter` — okno wyboru plików
- `dotenv` — zarządzanie kluczami API
- `requests` — komunikacja z API

---

### 🧪 Przebieg działania

1. 🗂️ **Wybór plików** — użytkownik wybiera pliki `.txt`, `.png`, `.mp3`.
2. 📖 **Odczyt treści**:
   - TXT: odczyt jako tekst.
   - PNG: OCR przy użyciu Tesseract.
   - MP3: transkrypcja przez Whisper (`whisper-1`).
3. 🧠 **Analiza danych** — tekst trafia do GPT-4o z promptem do klasyfikacji (`people`, `hardware`).
4. 💾 **Zapis wyników**:
   - Scalone teksty: `combined_texts.txt`
   - Wynik analizy: `analysis_result.json`
   - Transkrypcje MP3: `transcriptions.txt`
5. 📤 **Wysłanie odpowiedzi** — JSON wysyłany do:  
   `https://c3ntrala.ag3nts.org/report`

---

### 📁 Struktura pliku JSON

```json
{
  "task": "kategorie",
  "apikey": "YOUR_AIDEVS_KEY",
  "answer": {
    "people": ["plik1.txt", "plik2.mp3"],
    "hardware": ["plik4.png", "plik5.mp3"]
  }
}
```

---

### ✅ Uruchomienie

1. Utwórz plik `.env` z kluczami:

   ```
   OPENAI_API_KEY=sk-...
   AIDEVS_KEY=...
   ```

2. Zainstaluj wymagania:

   - Tesseract OCR ([UB Mannheim dla Windows](https://github.com/UB-Mannheim/tesseract/wiki))
   - FFMPEG (dla Whisper)

3. Zainstaluj zależności:

   ```bash
   pip install -r requirements.txt
   ```

4. Uruchom skrypt:

   ```bash
   python main.py
   ```

---

### ✨ Dodatkowe funkcje

- Buforowanie transkrypcji w `transcriptions.txt`
- Obsługa błędów OCR/Whisper/API
- Ponowne wykorzystanie wcześniejszej analizy

---

### 📚 Czego się nauczyłem

- Integracja OCR + STT + LLM w jednym pipeline
- Klasyfikacja danych multimodalnych
- Praktyczne zastosowanie GPT-4o do ekstrakcji informacji
- Automatyzacja i zabezpieczenie procesu analitycznego (RAG)

