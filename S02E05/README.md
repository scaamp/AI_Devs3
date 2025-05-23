# S02E05

## 🇬🇧 Task Name  
**Multimodal HTML Parsing and QA with GPT-4o**

## Description  
The goal was to build an end-to-end solution that fetches a remote HTML file, extracts textual, visual, and audio content, and queries a multimodal model (GPT-4o) to answer questions based on this input. The assistant returns a structured JSON response with concise answers to predefined questions. Finally, the answers are sent to an external validation endpoint.

## My Approach  
1. I downloaded the HTML file using `requests` and parsed it with `BeautifulSoup`.
2. I extracted text, `<img>` and `<audio>` tags **in order**, maintaining their position in the document.
3. I downloaded all media assets (images, mp3) to a local folder.
4. Images were encoded to base64 and audio transcribed using OpenAI Whisper (`whisper-1`).
5. I constructed a multimodal input array and queried `gpt-4o` using the Chat Completions API.
6. I extracted the JSON response, validated it, and submitted it to the task endpoint.

## Challenges  
- Cleaning and parsing GPT's output as JSON (due to markdown formatting like ```json).
- Ensuring proper media order and context from HTML structure.
- Transcribing local mp3 files via API and formatting transcripts naturally.
- Structuring a multimodal prompt and respecting token limits.

## Tools and Libraries  
- Python 3.11  
- `requests`, `bs4`, `openai`, `json`, `dotenv`, `base64`  
- OpenAI GPT-4o & Whisper APIs

## What I Learned  
This task gave me hands-on experience with building multimodal pipelines and working with GPT-4o's vision + audio capabilities. I also practiced robust HTML indexing and prompt construction for structured output.

---

## 🇵🇱 Nazwa zadania  
**Multimodalne parsowanie HTML i odpowiedzi na pytania z GPT-4o**

## Opis  
Celem było zbudowanie kompletnego rozwiązania, które pobiera plik HTML z internetu, wyodrębnia z niego treści tekstowe, obrazki i pliki audio, a następnie na ich podstawie zadaje pytania multimodalnemu modelowi (GPT-4o). Asystent zwraca odpowiedzi w formacie JSON, które następnie są wysyłane do zewnętrznego API.

## Moje podejście  
1. Pobrałem HTML z zewnętrznego URL i sparsowałem go przez `BeautifulSoup`.
2. Wyciągnąłem teksty, obrazki i audio w **kolejności DOM**, zachowując kontekst.
3. Pobrałem wszystkie multimedia do folderu `pobrane/`.
4. Obrazki zostały zakodowane do base64, a audio przetworzyłem do tekstu przez OpenAI Whisper.
5. Zbudowałem strukturę wejściową i wysłałem ją do GPT-4o z pomocą `chat.completions`.
6. Odpowiedź w formacie JSON została sparsowana i przesłana do API zadania.

## Problemy i wyzwania  
- Parsowanie odpowiedzi modelu z usuwaniem znaczników markdown (```json).
- Zachowanie kolejności treści z HTML oraz kontekstu ich występowania.
- Transkrypcja lokalnych plików mp3 i naturalna integracja z promptem.
- Przygotowanie kompletnego, multimodalnego promptu zgodnego z limitem tokenów.

## Użyte biblioteki i narzędzia  
- Python 3.11  
- `requests`, `bs4`, `openai`, `json`, `dotenv`, `base64`  
- API OpenAI GPT-4o i Whisper

## Czego się nauczyłem  
Zadanie to nauczyło mnie budowy potoków multimodalnych oraz wykorzystania możliwości GPT-4o do analizy obrazu i dźwięku. Udoskonaliłem też parsowanie HTML i konstrukcję promptów pod odpowiedzi strukturalne.

---
