# 🎧 Secret Audio Message Decoder

> 🇬🇧 Transcribes hidden messages from reversed and slowed-down audio recordings  
> 🇵🇱 Transkrybuje ukryte wiadomości z odwróconych i spowolnionych nagrań audio

---

## 🧠 Description / Opis

This script is designed to process secret audio recordings by:
1. Cutting silence from the beginning and end
2. Slowing down the audio (2x and 3x)
3. Reversing the audio
4. Transcribing the content using Whisper AI

It was used to solve a challenge where the clue was hidden in an unclear audio file.  

---

Ten skrypt przetwarza tajne nagrania audio przez:
1. Usuwanie ciszy z początku i końca
2. Spowolnienie nagrania (2x i 3x)
3. Odwrócenie nagrania
4. Transkrypcję treści za pomocą Whisper AI

Został wykorzystany do rozwiązania zagadki, w której wskazówka była ukryta w nieczytelnym nagraniu.  

---

## 🚀 How to Run / Jak uruchomić

### ✅ Requirements / Wymagania

```bash
pip install numpy librosa soundfile pydub openai-whisper
