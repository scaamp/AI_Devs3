from dotenv import load_dotenv
import os
import requests
import openai
import json

load_dotenv()

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
AIDEVS_KEY=os.getenv("AIDEVS_API_KEY")
QUESTIONS_URL="https://c3ntrala.ag3nts.org/data/{AIDEVS_KEY}/phone_questions.json"
DATA_URL="https://c3ntrala.ag3nts.org/data/{AIDEVS_KEY}/phone.json"

# Configure OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def fetch_questions():
    """
    Fetches questions from the API endpoint and returns them as a dictionary.
    Returns the dictionary with questions where keys are question numbers and values are questions.
    """
    url = QUESTIONS_URL.format(AIDEVS_KEY=AIDEVS_KEY)
    response = requests.get(url)
    response.raise_for_status()
    questions = response.json()
    return questions

def fetch_and_save_phone_data():
    """
    Fetches phone data from the API endpoint and saves it locally as a JSON file.
    Returns the phone data as a dictionary.
    """
    url = DATA_URL.format(AIDEVS_KEY=AIDEVS_KEY)
    response = requests.get(url)
    response.raise_for_status()
    phone_data = response.json()
    
    with open('phone_data.json', 'w', encoding='utf-8') as f:
        json.dump(phone_data, f, ensure_ascii=False, indent=2)
    
    return phone_data

def analyze_conversation(conversation_start, conversation_end, remaining_parts, conversation_length):
    """
    Analyzes a conversation using LLM to match missing parts.
    Returns the matched parts and updated remaining parts.
    """
    prompt = f"""Przeanalizuj poniższą rozmowę i dopasuj brakujące fragmenty z listy.
    
    Początek rozmowy: {conversation_start}
    Koniec rozmowy: {conversation_end}
    Długość rozmowy (liczba linii): {conversation_length}
    
    Dostępne fragmenty do dopasowania:
    {json.dumps(remaining_parts, ensure_ascii=False, indent=2)}
    
    Zwróć listę dopasowanych fragmentów w kolejności chronologicznej, które pasują do tej rozmowy.
    Zwróć tylko fragmenty, które na pewno pasują do tej rozmowy.
    Pamiętaj, że łączna liczba linii (początek + dopasowane fragmenty + koniec) powinna być równa {conversation_length}.
    Zwróć odpowiedź w formacie JSON array.
    """
    
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "Jesteś asystentem analizującym rozmowy telefoniczne. Twoim zadaniem jest dopasowanie brakujących fragmentów do rozmowy na podstawie kontekstu i długości rozmowy."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )
    
    try:
        matched_parts = json.loads(response.choices[0].message.content)
        # Usuń dopasowane fragmenty z listy remaining_parts
        updated_remaining = [part for part in remaining_parts if part not in matched_parts]
        return matched_parts, updated_remaining
    except json.JSONDecodeError:
        print("Error: Could not parse LLM response as JSON")
        return [], remaining_parts

def save_analyzed_conversations(analyzed_conversations):
    """
    Saves analyzed conversations to a JSON file.
    """
    output_file = 'analyzed_conversations.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analyzed_conversations, f, ensure_ascii=False, indent=2)
    print(f"\nPrzeanalizowane konwersacje zostały zapisane do pliku: {output_file}")

def process_conversations():
    """
    Process all conversations and match missing parts.
    """
    # Wczytaj dane z pliku
    with open('phone_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Pobierz listę pozostałych fragmentów
    remaining_parts = data['reszta']
    
    # Słownik do przechowywania przeanalizowanych konwersacji
    analyzed_conversations = {}
    
    # Przetwórz każdą rozmowę
    for i in range(1, 6):
        conversation_key = f"rozmowa{i}"
        conversation = data[conversation_key]
        
        print(f"\nAnalizuję rozmowę {i}:")
        print(f"Start: {conversation['start']}")
        print(f"Koniec: {conversation['end']}")
        print(f"Długość rozmowy: {conversation['length']} linii")
        
        # Analizuj rozmowę i dopasuj brakujące fragmenty
        matched_parts, remaining_parts = analyze_conversation(
            conversation['start'],
            conversation['end'],
            remaining_parts,
            conversation['length']
        )
        
        # Zapisz przeanalizowaną konwersację
        analyzed_conversations[conversation_key] = {
            "start": conversation['start'],
            "matched_parts": matched_parts,
            "end": conversation['end'],
            "length": conversation['length']
        }
        
        print("\nDopasowane fragmenty:")
        for part in matched_parts:
            print(f"- {part}")
        
        print(f"\nPozostało {len(remaining_parts)} fragmentów do dopasowania")
    
    # Zapisz przeanalizowane konwersacje do pliku
    save_analyzed_conversations(analyzed_conversations)
    
    # Zapisz pozostałe fragmenty
    if remaining_parts:
        print("\nPozostałe niedopasowane fragmenty:")
        for part in remaining_parts:
            print(f"- {part}")

# Example usage
if __name__ == "__main__":
    # Fetch and save phone data if not exists
    if not os.path.exists('phone_data.json'):
        fetch_and_save_phone_data()
    
    # Process conversations
    process_conversations()