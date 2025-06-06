import json

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
create_jsonl("correct.txt", "incorrect.txt", "train.jsonl")
