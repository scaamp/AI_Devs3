import os
import requests
from openai import OpenAI
from dotenv import load_dotenv
import json
import time

# Load environment variables
load_dotenv()

def get_api_keys():
    openai_key = os.getenv("OPENAI_API_KEY")
    aidevs_key = os.getenv("AIDEVS_API_KEY")
    
    if not openai_key:
        print("Błąd: Nie ustawiono zmiennej środowiskowej OPENAI_API_KEY")
        return False, None, None
    
    if not aidevs_key:
        print("Błąd: Nie ustawiono zmiennej środowiskowej AIDEVS_API_KEY")
        return False, None, None
    
    return True, openai_key, aidevs_key

def download_file():
    url = "https://centrala.ag3nts.org/dane/barbara.txt"
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        with open("barbara.txt", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("Plik został pobrany pomyślnie jako 'barbara.txt'")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas pobierania pliku: {e}")
        return False

def read_file_content(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def analyze_with_gpt4(text, api_key):
    client = OpenAI(api_key=api_key)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "Jesteś asystentem analizującym tekst. Odpowiadaj TYLKO w formacie JSON. Nie dodawaj żadnych dodatkowych wyjaśnień ani tekstu."},
                {"role": "user", "content": f"Przeanalizuj poniższy tekst i zwróć JSON zawierający tylko imiona osób (bez nazwisk) i nazwy miast w formacie:\n{{\"name\": [\"imię1\", \"imię2\"], \"city\": [\"miasto1\", \"miasto2\"]}}\n\nTekst do analizy:\n{text}"}
            ],
            response_format={ "type": "json_object" }
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return f"Wystąpił błąd podczas komunikacji z API: {str(e)}"

def send_request(endpoint, query, aidevs_key):
    try:
        response = requests.post(
            f"https://centrala.ag3nts.org/{endpoint}",
            json={
                "apikey": aidevs_key,
                "query": query
            }
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(response.json()["message"])
        return None

def send_report(city, aidevs_key):
    try:
        response = requests.post(
            "https://centrala.ag3nts.org/report",
            json={
                "task": "loop",
                "apikey": aidevs_key,
                "answer": city
            }
        )
        response.raise_for_status()
        print(f"Wysłano raport dla miasta: {city}")
        return response.json()
    except Exception as e:
        print(response.json()["message"])
        return None

def process_response(response_data, aidevs_key, processed_queries=None):
    if processed_queries is None:
        processed_queries = set()
    
    results = {}
    new_queries = set()
    
    # Process each response
    for key, value in response_data.items():
        if value.get("code") == 0 and value.get("message"):
            message = value["message"]
            
            # Split message into words and process each
            words = message.split()
            for word in words:
                if word not in processed_queries:
                    new_queries.add(word)
                    processed_queries.add(word)
                    
                    # Send to both endpoints
                    if key.startswith("places_"):
                        people_response = send_request("people", word, aidevs_key)
                        if people_response:
                            results[f"people_{word}"] = people_response
                            # Send report for each city
                            send_report(word, aidevs_key)
                    
                    if key.startswith("people_"):
                        places_response = send_request("places", word, aidevs_key)
                        if places_response:
                            results[f"places_{word}"] = places_response
                            # Send report for each city found in people response
                            if places_response.get("code") == 0 and places_response.get("message"):
                                cities = places_response["message"].split()
                                for city in cities:
                                    send_report(city, aidevs_key)
    
    # If we found new queries, process them recursively
    if new_queries:
        print(f"Znaleziono nowe zapytania: {new_queries}")
        time.sleep(2)  # Add delay to avoid rate limiting
        recursive_results = process_response(results, aidevs_key, processed_queries)
        results.update(recursive_results)
    
    return results

def send_to_endpoints(data, aidevs_key):
    initial_results = {}
    
    # Send initial requests for each city
    for city in data["city"]:
        response = send_request("places", city, aidevs_key)
        if response:
            initial_results[f"places_{city}"] = response
            # Send report for initial cities
            send_report(city, aidevs_key)
    
    # Send initial requests for each name
    for name in data["name"]:
        response = send_request("people", name, aidevs_key)
        if response:
            initial_results[f"people_{name}"] = response
            # Send report for cities found in initial people response
            if response.get("code") == 0 and response.get("message"):
                cities = response["message"].split()
                for city in cities:
                    send_report(city, aidevs_key)
    
    # Process responses recursively
    all_results = process_response(initial_results, aidevs_key)
    
    # Save all results to file
    with open("api_responses.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    print("\nWszystkie odpowiedzi z API zostały zapisane do pliku 'api_responses.json'")

def main():
    # Sprawdź klucze API
    success, openai_key, aidevs_key = get_api_keys()
    if not success:
        return

    # Pobierz plik
    if not download_file():
        return

    # Wczytaj zawartość pliku
    try:
        content = read_file_content("barbara.txt")
    except FileNotFoundError:
        print("Błąd: Nie znaleziono pliku barbara.txt")
        return

    # Wyślij do API i wyświetl odpowiedź
    result = analyze_with_gpt4(content, openai_key)
    print("\nAnaliza tekstu:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Wyślij zapytania do endpointów i zapisz odpowiedzi
    send_to_endpoints(result, aidevs_key)

if __name__ == "__main__":
    main() 