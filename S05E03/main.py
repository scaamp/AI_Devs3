import requests
import threading
import openai
from dotenv import load_dotenv
import os
from markdownify import markdownify
import time

start_time = time.time()

load_dotenv()

# Ustaw swój klucz API OpenAI
# Pamiętaj, aby zastąpić 'YOUR_OPENAI_API_KEY' swoim rzeczywistym kluczem.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AIDEVS_KEY = os.getenv("AIDEVS_API_KEY")
openai.api_key = OPENAI_API_KEY # Correctly set the API key

url = "https://rafal.ag3nts.org/b46c3"
password = "NONOMNISMORIAR"

# Globalna lista na odpowiedzi i blokada
all_answers = []
answers_lock = threading.Lock()

# Funkcja do pobierania i konwertowania zawartości arxiv-draft.html do Markdown
def get_arxiv_draft_content_as_markdown(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return markdownify(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching or converting arxiv-draft.html: {e}")
        return None

# Pobierz zawartość arxiv-draft.html raz na początku
arxiv_draft_url = "https://centrala.ag3nts.org/dane/arxiv-draft.html"
arxiv_draft_content_markdown = get_arxiv_draft_content_as_markdown(arxiv_draft_url)

# Funkcja do wysyłania pytania do OpenAI LLM
def send_question_to_llm(question, context=None):
    try:
        print(f"Sending question to LLM: {question}")
        messages = [
            {"role": "system", "content": "You are a helpful assistant. Answer with 1 word if possible (but answer have to be complete). If you have to, maximum 3 words"}
        ]
        if context:
            messages.append({"role": "system", "content": f"Context: {context}"})
        messages.append({"role": "user", "content": question})

        response = openai.chat.completions.create(
            model="gpt-4.1-nano",
            messages=messages
        )
        answer = response.choices[0].message.content
        # print(f"Answer for '{question}': {answer}")
        with answers_lock:
            all_answers.append(answer)
    except openai.APIError as e:
        print(f"Error sending question to LLM '{question}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred for question '{question}': {e}")

# Krok 1 – uzyskaj hash
res1 = requests.post(url, json={"password": password})
hash_value = res1.json().get("message")

# Krok 2 – podpisz hash
if hash_value:
    res2 = requests.post(url, json={"sign": hash_value})
    data = res2.json()
    print(data)

    message_data = data.get("message", {})
    signature = message_data.get("signature")
    timestamp = message_data.get("timestamp")

    # if signature and timestamp:
    #     print(f"Signature: {signature}")
    #     print(f"Timestamp: {timestamp}")
    # else:
    #     print("Could not retrieve signature or timestamp.")

    challenges = message_data.get("challenges", [])

    def fetch_url_content(url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            content = response.json()
            questions = content.get("data", [])
            # print(f"Questions from {url}:\n{questions}")

            context_for_llm = None
            if "Źródło wiedzy https://centrala.ag3nts.org/dane/arxiv-draft.html" in content.get("task", ""):
                context_for_llm = arxiv_draft_content_markdown
                print(f"Applying context from arxiv-draft.html for URL: {url}")

            # Create a thread for each question and send to LLM
            llm_threads = []
            for question in questions:
                thread = threading.Thread(target=send_question_to_llm, args=(question, context_for_llm,))
                llm_threads.append(thread)
                thread.start()
            
            for thread in llm_threads:
                thread.join()

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")

    source_threads = []
    for challenge_url in challenges:
        thread = threading.Thread(target=fetch_url_content, args=(challenge_url,))
        source_threads.append(thread)
        thread.start()

    for thread in source_threads:
        thread.join()

    # Po zakończeniu wszystkich wątków i zebraniu wszystkich odpowiedzi
    if signature and timestamp and AIDEVS_KEY:
        final_payload = {
            "apikey": AIDEVS_KEY,
            "timestamp": timestamp,
            "signature": signature,
            "answer": all_answers
        }
        print("\nSending final payload:", final_payload)
        final_response = requests.post(url, json=final_payload)
        print("Final response:", final_response.json())
    else:
        print("❌ Brak wszystkich danych do wysłania końcowego requestu (API key, timestamp, lub signature).")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nProgram finished in {elapsed_time:.2f} seconds.")

else:
    print("❌ Nie udało się pobrać hash.")
