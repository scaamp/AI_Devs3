import requests
import re
import time
from openai import OpenAI

# === Ustawienia ===
URL = "https://xyz.ag3nts.org/"
LOGIN = "tester"
PASSWORD = "574e112a"
OPENAI_API_KEY = "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"  # podaj swój klucz
MODEL = "gpt-4"  # lub tańszy np. gpt-3.5-turbo

# === Funkcja: pobieranie pytania z HTML ===
def get_question():
    response = requests.get(URL)
    html = response.text
    match = re.search(r"Question:\s*(.+?)<", html)
    return match.group(1).strip() if match else None

# === Funkcja: zapytanie do LLM ===
def ask_llm(question):
    client = OpenAI(api_key=OPENAI_API_KEY)
    # openai.api_key = OPENAI_API_KEY
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Odpowiadaj zwięźle na pytania faktograficzne."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content.strip()

# === Funkcja: logowanie ===
def login_with_answer(answer):
    payload = {
        "username": LOGIN,
        "password": PASSWORD,
        "answer": answer
    }
    payload = f"username={LOGIN}&password={PASSWORD}&answer={answer}"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(URL, data=payload, headers=headers)

    return response.text

# === Główna logika ===
if __name__ == "__main__":
    question = get_question()
    if not question:
        print("❌ Nie udało się pobrać pytania.")
    else:
        print(f"❓ Pytanie: {question}")
        answer = ask_llm(question)
        print(f"✅ Odpowiedź LLM: {answer}")
        result = login_with_answer(answer)
        print(f"🎯 Odpowiedź serwera:\n{result}")
