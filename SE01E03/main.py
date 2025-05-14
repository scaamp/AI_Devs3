import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from tkinter import Tk, filedialog, messagebox

import requests

# Wczytaj zmienne środowiskowe z pliku .env
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Otwórz okno wyboru pliku
root = Tk()
root.withdraw()  # Ukryj główne okno
file_path = filedialog.askopenfilename(
    title="Wybierz plik JSON z danymi testowymi",
    filetypes=[("JSON files", "*.json")]
)

if not file_path:
    print("❌ Nie wybrano pliku. Zamykanie programu.")
    exit()

# Wczytaj plik JSON
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Iteracja po danych testowych
for item in data.get('test-data', []):
    # Weryfikacja działań matematycznych
    try:
        if '+' in item['question']:
            parts = item['question'].split('+')
            left = int(parts[0].strip())
            right = int(parts[1].strip())
            correct_answer = left + right

            if item['answer'] != correct_answer:
                print(f"Błąd: {item['question']} = {item['answer']} -> poprawiam na {correct_answer}")
                item['answer'] = correct_answer
    except Exception as e:
        print(f"Błąd przy przetwarzaniu: {item}, {e}")

    # Obsługa pola "test"
    if 'test' in item and 'q' in item['test']:
        question = item['test']['q']
        try:
            response = client.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=[
                    {"role": "user", "content": question}
                ]
            )
            answer = response.choices[0].message.content.strip()
            item['test']['a'] = answer
            print(f"Odpowiedź na pytanie '{question}': {answer}")
        except Exception as e:
            print(f"Błąd API dla pytania '{question}': {e}")

# Zapisz lokalnie poprawiony plik
output_path = os.path.join(os.path.dirname(file_path), 'poprawiony_plik.json')
with open('poprawiony_plik.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ Plik został zapisany: {output_path}")

# Przygotuj dane do wysyłki
post_payload = {
    "task": "JSON",
    "apikey": "7b1d918f-a190-4f2a-a56b-8303d28d5609",
    "answer": data
}

try:
    response = requests.post("https://centrala.ag3nts.org/report", json=post_payload)
    response.raise_for_status()

    # Parsowanie odpowiedzi JSON
    response_data = response.json()
    print("✅ Poprawiony JSON został wysłany pomyślnie!")
    print("📥 Odpowiedź z serwera:")
    print(json.dumps(response_data, indent=2, ensure_ascii=False))

    # Wyświetl flagę lub inną wiadomość
    flag = response_data.get("flag") or response_data.get("message") or str(response_data)
    messagebox.showinfo("Odpowiedź z serwera", f"Otrzymano:\n{flag}")

except requests.RequestException as e:
    print(f"❌ Wystąpił błąd przy wysyłaniu danych: {e}")
    messagebox.showerror("Błąd", f"Nie udało się wysłać danych:\n{e}")

