# S02E01

## 🇬🇧 Task Name  
**Audio Interrogation Analysis with Whisper and GPT-4**

## Description  
The goal was to analyze a set of audio witness interrogations in order to determine **the street where professor Andrzej Maj teaches**. The audio content was ambiguous — some statements contradicted each other, others were strange, incorrect, or misleading. The exact name of the street was **not explicitly mentioned**, so the model had to infer it using its own knowledge and reasoning.

## My Approach  
1. I used a GUI file picker (`tkinter`) to load `.m4a` audio files from disk.
2. Each audio file was transcribed using OpenAI Whisper (`whisper-1`) via `openai.audio.transcriptions.create`.
3. All transcripts were joined into one combined context.
4. A GPT-4 prompt was created, instructing the model to reason based on this context and its internal knowledge to guess the street name.
5. The model's result was parsed (JSON if possible), and the street was extracted.
6. The final result was sent to the official endpoint (`/report`) using an API key.

## Challenges  
- Some transcriptions were very chaotic or inconsistent.
- The street name never appeared directly, so reasoning and inference were necessary.
- GPT response was sometimes free-form — additional handling was needed to extract clean output.

## Tools and Libraries  
- Python 3.10+  
- `openai` – Whisper + GPT-4  
- `requests` – result reporting  
- `tkinter` – file explorer  
- `dotenv` – environment variable management  
- `json` – GPT result parsing  

## What I Learned  
This task helped me integrate voice processing with large language models, including chaining Whisper with GPT-4. I practiced reasoning through ambiguous content and created a pipeline for extracting high-confidence conclusions using natural language inference.

---

## 🇵🇱 Nazwa zadania  
**Analiza przesłuchań audio z użyciem Whisper i GPT-4**

## Opis  
Celem było przeanalizowanie nagrań audio z przesłuchań świadków i określenie, **na jakiej ulicy wykłada profesor Andrzej Maj**. Wypowiedzi były niejasne — część zeznań była sprzeczna, inne absurdalne lub celowo mylące. Nazwa ulicy **nie padała wprost**, więc model musiał ją wywnioskować na podstawie swojej wiedzy i ogólnego kontekstu.

## Moje podejście  
1. Za pomocą GUI (`tkinter`) użytkownik wybiera pliki `.m4a`.
2. Każdy plik jest transkrybowany przez OpenAI Whisper (`whisper-1`).
3. Wszystkie transkrypcje są łączone w jeden wspólny kontekst.
4. GPT-4 otrzymuje prompt z instrukcją, by wykorzystać swoją wiedzę i kontekst, aby odgadnąć nazwę ulicy.
5. Odpowiedź modelu jest parsowana (najpierw jako JSON, jeśli się da) i wyciągana jest ulica.
6. Wynik zostaje wysłany do oficjalnego endpointu `/report`.

## Problemy i wyzwania  
- Transkrypcje były miejscami chaotyczne i sprzeczne.
- Nazwa ulicy nie padała wprost — potrzebne było rozumowanie i domysły.
- Odpowiedzi GPT bywały luźne — trzeba było obsłużyć różne formaty wyniku.

## Użyte biblioteki  
- Python 3.10+  
- `openai` – Whisper + GPT-4  
- `requests` – wysyłka wyników  
- `tkinter` – eksplorator plików  
- `dotenv` – zmienne środowiskowe  
- `json` – parsowanie odpowiedzi GPT  

## Czego się nauczyłem  
To zadanie pomogło mi połączyć rozpoznawanie mowy z analizą języka naturalnego. Zintegrowałem Whisper z GPT-4 i stworzyłem pipeline do wyciągania wniosków z chaotycznych danych głosowych.
