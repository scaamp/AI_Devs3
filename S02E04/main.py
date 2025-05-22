import tkinter as tk
from tkinter import filedialog
from PIL import Image
import pytesseract
import os
import openai
from pathlib import Path
from dotenv import load_dotenv
import json
import requests

# Load environment variables from .env file
load_dotenv()

# Configure Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'

aidevs_key = os.getenv('AIDEVS_KEY')
if not aidevs_key:
    raise ValueError("AIDEVS_KEY nie został znaleziony w zmiennych środowiskowych. Upewnij się, że plik .env istnieje i zawiera klucz API.")

# Configure OpenAI API
openai.api_key = os.getenv('OPENAI_API_KEY')
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY nie został znaleziony w zmiennych środowiskowych. Upewnij się, że plik .env istnieje i zawiera klucz API.")

SYSTEM_PROMPT = """
Twoim zadaniem jest przeanalizowanie danych z fabryki (raporty dzienne w różnych formatach) i wyodrębnienie notatek zawierających informacje o schwytanych ludziach lub śladach ich obecności oraz o naprawionych usterkach hardwarowych. Na podstawie treści danego pliku (tekst z pliku TXT, wynik OCR z obrazu PNG, lub transkrypcja z pliku MP3) przypisz plik do jednej z kategorii: "people" lub "hardware".

Zasady:
- Uwzględnij tylko przypadki schwytania ludzi lub dowody ich obecności (np. ślady, zapisy z kamer, odciski).
- Uwzględnij tylko usterki sprzętowe (hardware). Pomiń informacje o problemach z oprogramowaniem (software).
- Pomiń pliki, które nie zawierają żadnych przydatnych informacji.
- Nie dodawaj żadnych innych kategorii.

Format wynikowy musi mieć dokładnie taką strukturę (przestrzegaj formatu JSON i wielkości liter w nazwach plików):

"answer": {
  "people": ["plik1.txt", "plik2.mp3", "plikN.png"],
  "hardware": ["plik4.txt", "plik5.png", "plik6.mp3"]
}

Ważne:
- Nazwy plików muszą być dokładnie takie same jak oryginalne (wielkość liter ma znaczenie).
- Nie używaj ścieżek do plików — tylko same nazwy z rozszerzeniem.
- Jeśli plik pasuje do obu kategorii, przypisz go tylko do jednej — tej, która jest bardziej dominująca tematycznie.
"""

def analyze_texts_with_gpt4(texts):
    try:
        # Przygotuj tekst do analizy
        analysis_text = "=== POŁĄCZONE TEKSTY ===\n\n"
        for file_name, text in texts.items():
            analysis_text += f"--- {file_name} ---\n{text}\n\n"

        # Wyślij request do GPT-4
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": analysis_text}
            ],
            temperature=0.1  # Niska temperatura dla bardziej deterministycznych odpowiedzi
        )

        # Pobierz odpowiedź
        result = response.choices[0].message.content
        
        # Spróbuj sparsować odpowiedź jako JSON
        try:
            # Znajdź pierwszy znak '{' i ostatni '}'
            start = result.find('{')
            end = result.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = result[start:end]
                parsed_result = json.loads(json_str)
                return parsed_result
            else:
                print("Nie znaleziono poprawnej struktury JSON w odpowiedzi")
                return None
        except json.JSONDecodeError as e:
            print(f"Błąd parsowania JSON: {e}")
            print("Odpowiedź GPT-4:", result)
            return None

    except Exception as e:
        print(f"Błąd podczas analizy tekstów: {e}")
        return None

def transcribe_audio_with_gpt4(audio_file_path):
    try:
        with open(audio_file_path, "rb") as audio_file:
            transcript = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
        return transcript
    except Exception as e:
        print(f"Błąd podczas transkrypcji pliku {audio_file_path}: {e}")
        return None

def save_transcription(audio_file_path, transcription):
    transcriptions_file = "transcriptions.txt"
    with open(transcriptions_file, "a", encoding="utf-8") as f:
        f.write(f"\n=== {os.path.basename(audio_file_path)} ===\n")
        f.write(transcription)
        f.write("\n")

def get_transcription_from_file(audio_file_path):
    transcriptions_file = "transcriptions.txt"
    if not os.path.exists(transcriptions_file):
        return None
    
    with open(transcriptions_file, "r", encoding="utf-8") as f:
        content = f.read()
        file_name = os.path.basename(audio_file_path)
        start_marker = f"=== {file_name} ==="
        
        if start_marker in content:
            start_idx = content.find(start_marker) + len(start_marker)
            next_marker = content.find("===", start_idx)
            if next_marker == -1:
                return content[start_idx:].strip()
            return content[start_idx:next_marker].strip()
    return None

def save_combined_texts(all_texts):
    combined_file = "combined_texts.txt"
    with open(combined_file, "w", encoding="utf-8") as f:
        f.write("=== POŁĄCZONE TEKSTY ===\n\n")
        for file_name, text in all_texts.items():
            f.write(f"--- {file_name} ---\n")
            f.write(text)
            f.write("\n\n")
    print(f"\nWszystkie teksty zostały zapisane do pliku {combined_file}")

def save_analysis_result(result):
    if result:
        analysis_file = "analysis_result.json"
        with open(analysis_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\nWynik analizy został zapisany do pliku {analysis_file}")
        print("\nKategoryzacja plików:")
        print("\nLudzie:")
        for file in result.get("answer", {}).get("people", []):
            print(f"- {file}")
        print("\nHardware:")
        for file in result.get("answer", {}).get("hardware", []):
            print(f"- {file}")

def send_result_to_aidevs(result):
    if not result:
        print("Brak wyniku do wysłania")
        return
    
    url = "https://c3ntrala.ag3nts.org/report"
    
    payload = {
        "task": "kategorie",
        "apikey": aidevs_key,
        # "answer": result.get("answer", {})
        "answer": result
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Sprawdź czy nie ma błędów HTTP
        print("\nWynik wysłany do AIDevs API:")
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas wysyłania wyniku do AIDevs API: {e}")

def read_existing_analysis():
    analysis_file = "analysis_result.json"
    if os.path.exists(analysis_file):
        try:
            with open(analysis_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Błąd odczytu pliku {analysis_file}: {e}")
        except Exception as e:
            print(f"Nieoczekiwany błąd podczas odczytu pliku {analysis_file}: {e}")
    return None

# Utwórz ukryte okno tkinter (nie chcemy GUI — tylko eksplorator plików)
root = tk.Tk()
root.withdraw()

# Otwórz eksplorator plików i pozwól użytkownikowi wybrać wiele plików
file_paths = filedialog.askopenfilenames(
    title="Wybierz pliki",
    filetypes=[
        ("Wszystkie pliki", "*.*"),
        ("Pliki tekstowe", "*.txt"),
        ("Obrazy PNG", "*.png"),
        ("Pliki audio MP3", "*.mp3")
    ]
)

# Wyświetl ścieżki do wybranych plików
print("Wybrane pliki:")
for path in file_paths:
    print(path)

# Słownik do przechowywania wszystkich tekstów
all_texts = {}

# Przetwarzanie plików
for path in file_paths:
    file_name = os.path.basename(path)
    if path.endswith(".txt"):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            print(f"\nZawartość {path}:\n{content[:300]}...")  # pokazujemy fragment
            all_texts[file_name] = content
    elif path.endswith(".png"):
        print(f"\n🔍 OCR: {file_name}")
        try:
            image = Image.open(path)
            text = pytesseract.image_to_string(image, lang='pol')
            text = text.strip() if text.strip() else "(Brak tekstu)"
            print(text)
            all_texts[file_name] = text
        except Exception as e:
            print(f"Błąd podczas przetwarzania {path}: {e}")
    elif path.endswith(".mp3"):
        print(f"\n🎵 Transkrypcja: {file_name}")
        # Sprawdź czy istnieje już transkrypcja
        existing_transcription = get_transcription_from_file(path)
        if existing_transcription:
            print("Znaleziono istniejącą transkrypcję:")
            print(existing_transcription)
            all_texts[file_name] = existing_transcription
        else:
            print("Generowanie nowej transkrypcji...")
            transcription = transcribe_audio_with_gpt4(path)
            if transcription:
                save_transcription(path, transcription)
                print("Transkrypcja zapisana do pliku transcriptions.txt")
                print(transcription)
                all_texts[file_name] = transcription

# Zapisz wszystkie teksty do jednego pliku
if all_texts:
    save_combined_texts(all_texts)
    
    # Sprawdź czy istnieje już plik z wynikami analizy
    analysis_result = read_existing_analysis()
    
    if analysis_result:
        print("\nZnaleziono istniejący plik z wynikami analizy.")
        save_analysis_result(analysis_result)
    else:
        # Przeanalizuj teksty za pomocą GPT-4
        print("\nAnalizuję teksty za pomocą GPT-4...")
        analysis_result = analyze_texts_with_gpt4(all_texts)
        save_analysis_result(analysis_result)
    
    # Wyślij wynik do AIDevs API
    if analysis_result:
        send_result_to_aidevs(analysis_result)
