import json
import openai
import os
import requests
from dotenv import load_dotenv


load_dotenv()
# Wprowadź tutaj swoje dane:
API_KEY = os.getenv("OPENAI_API_KEY")
AIDEVS_API_KEY = os.getenv("AIDEVS_API_KEY")
MODEL_NAME = "ft:gpt-4.1-mini-2025-04-14:personal:lab-checker:BfTtVLQ7"
VERIFY_PATH = "verify.txt"

openai.api_key = API_KEY

def create_jsonl(correct_path, incorrect_path, output_path):
    def make_record(line, label):
        return {
            "messages": [
                {"role": "system", "content": "validate data"},
                {"role": "user", "content": line.strip()},
                {"role": "assistant", "content": label}
            ]
        }

    with open(output_path, "w", encoding="utf-8") as out_file:
        # Process correct.txt
        with open(correct_path, "r", encoding="utf-8") as correct_file:
            for line in correct_file:
                record = make_record(line, "1")
                out_file.write(json.dumps(record, ensure_ascii=False) + "\n")

        # Process incorrect.txt
        with open(incorrect_path, "r", encoding="utf-8") as incorrect_file:
            for line in incorrect_file:
                record = make_record(line, "0")
                out_file.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"✅ Plik {output_path} został utworzony.")

# Ścieżki do plików
if not os.path.exists("train.jsonl"):
    create_jsonl("correct.txt", "incorrect.txt", "train.jsonl")
else:
    print("✅ Plik train.jsonl już istnieje, pomijam tworzenie.")

def classify_line(index, content):
    response = openai.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "validate data"},
            {"role": "user", "content": content.strip()}
        ],
        temperature=0  # aby wynik był stabilny
    )
    answer = response.choices[0].message.content.strip()
    return answer

correct_ids = []

with open(VERIFY_PATH, "r", encoding="utf-8") as file:
    for i, line in enumerate(file, start=1):
        line_id = f"{i:02d}"  # np. 01, 02, 03...
        result = classify_line(i, line)
        print(f"{line_id}: {result}")
        if result in ["1", "true", "True"]:
            correct_ids.append(line_id)

# Finalna odpowiedź do wysłania:
output = {
    "task": "research",
    "apikey": AIDEVS_API_KEY,
    "answer": correct_ids
}

if os.path.exists("final_result.json"):
    print("✅ Plik final_result.json już istnieje, wysyłam request do endpointu...")
    response = requests.post(
        "https://c3ntrala.ag3nts.org/report",
        json=output
    )
    print(f"Status odpowiedzi: {response.status_code}")
    print(f"Treść odpowiedzi: {response.text}")
else:
    # Zapisz wynik do pliku:
    with open("final_result.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print("✅ Gotowe! Wynik zapisany w 'final_result.json'")
