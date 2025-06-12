from dotenv import load_dotenv
import os
import requests
import openai
import json
import glob
import time
import re
from openai import RateLimitError, APIError, APITimeoutError

load_dotenv()

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
AIDEVS_KEY=os.getenv("AIDEVS_API_KEY")
QUESTIONS_URL="https://c3ntrala.ag3nts.org/data/{AIDEVS_KEY}/phone_questions.json"
DATA_URL="https://c3ntrala.ag3nts.org/data/{AIDEVS_KEY}/phone.json"
DATA_SORTED_URL="https://c3ntrala.ag3nts.org/data/{AIDEVS_KEY}/phone_sorted.json"
REPORT_URL="https://centrala.ag3nts.org/report"

# Configure OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def retry_with_backoff(func, max_retries=5, initial_delay=1):
    """
    Retry a function with exponential backoff.
    """
    retries = 0
    delay = initial_delay
    
    while retries < max_retries:
        try:
            return func()
        except (RateLimitError, APIError, APITimeoutError) as e:
            retries += 1
            if retries == max_retries:
                raise e
            
            print(f"API error occurred: {str(e)}")
            print(f"Retrying in {delay} seconds... (attempt {retries}/{max_retries})")
            time.sleep(delay)
            delay *= 2  # Exponential backoff
        except Exception as e:
            raise e

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

def fetch_and_save_sorted_data():
    """
    Fetches sorted phone data from the API endpoint and saves it locally as a JSON file.
    Returns the sorted phone data as a dictionary.
    """
    url = DATA_SORTED_URL.format(AIDEVS_KEY=AIDEVS_KEY)
    response = requests.get(url)
    response.raise_for_status()
    sorted_data = response.json()
    
    with open('phone_data_sorted.json', 'w', encoding='utf-8') as f:
        json.dump(sorted_data, f, ensure_ascii=False, indent=2)
    
    print("Posortowane dane zostały zapisane do pliku: phone_data_sorted.json")
    return sorted_data

def analyze_next_sentence(conversation_start, current_parts, remaining_parts, conversation_length):
    """
    Analyzes conversation and finds the next matching sentence.
    Returns the matched sentence and updated remaining parts.
    """
    current_conversation = [conversation_start] + current_parts
    
    prompt = f"""Przeanalizuj poniższą rozmowę i znajdź JEDNO następne zdanie, które pasuje do kontekstu.
    
    Aktualna rozmowa:
    {json.dumps(current_conversation, ensure_ascii=False, indent=2)}
    
    Dostępne fragmenty do dopasowania:
    {json.dumps(remaining_parts, ensure_ascii=False, indent=2)}
    
    Zwróć TYLKO JEDNO zdanie, które powinno być następne w tej rozmowie.
    Zwróć odpowiedź w formacie JSON array z jednym elementem.
    """
    
    def make_api_call():
        return client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "Jesteś asystentem analizującym rozmowy telefoniczne. Twoim zadaniem jest znalezienie jednego następnego zdania pasującego do kontekstu rozmowy."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
    
    try:
        response = retry_with_backoff(make_api_call)
        matched_sentence = json.loads(response.choices[0].message.content)[0]
        # Usuń dopasowane zdanie z listy remaining_parts
        updated_remaining = [part for part in remaining_parts if part != matched_sentence]
        return matched_sentence, updated_remaining
    except (json.JSONDecodeError, IndexError) as e:
        print(f"Error: Could not parse LLM response as JSON or no sentence was returned: {str(e)}")
        print("Raw response:", response.choices[0].message.content)
        return None, remaining_parts

def validate_conversation_length(conversation_parts, expected_length):
    """
    Validates if the conversation has the correct number of lines.
    """
    actual_length = len(conversation_parts)
    if actual_length != expected_length:
        raise ValueError(f"Nieprawidłowa długość konwersacji! Oczekiwano {expected_length}, otrzymano {actual_length}")

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
        
        # Lista do przechowywania dopasowanych fragmentów
        matched_parts = []
        
        # Dopasuj kolejne zdania aż do osiągnięcia oczekiwanej długości
        while len(matched_parts) + 2 < conversation['length']:  # +2 dla początku i końca
            matched_sentence, remaining_parts = analyze_next_sentence(
                conversation['start'],
                matched_parts,
                remaining_parts,
                conversation['length']
            )
            
            if matched_sentence is None:
                print("Nie udało się dopasować kolejnego zdania!")
                break
                
            matched_parts.append(matched_sentence)
            print(f"\nDopasowano zdanie: {matched_sentence}")
            print(f"Pozostało {len(remaining_parts)} fragmentów do dopasowania")
        
        # Dodaj koniec rozmowy
        matched_parts.append(conversation['end'])
        
        # Waliduj długość konwersacji
        try:
            validate_conversation_length([conversation['start']] + matched_parts, conversation['length'])
        except ValueError as e:
            print(f"\nBŁĄD: {str(e)}")
            print("Przerywam działanie programu!")
            return
        
        # Zapisz przeanalizowaną konwersację
        analyzed_conversations[conversation_key] = {
            "start": conversation['start'],
            "matched_parts": matched_parts[:-1],  # Bez ostatniego elementu (koniec rozmowy)
            "end": conversation['end'],
            "length": conversation['length']
        }
    
    # Zapisz przeanalizowane konwersacje do pliku
    save_analyzed_conversations(analyzed_conversations)
    
    # Zapisz pozostałe fragmenty
    if remaining_parts:
        print("\nPozostałe niedopasowane fragmenty:")
        for part in remaining_parts:
            print(f"- {part}")

def read_facts():
    """
    Reads all .txt files from the facts directory.
    Returns a dictionary with file names as keys and their contents as values.
    """
    facts = {}
    for file_path in glob.glob('facts/*.txt'):
        with open(file_path, 'r', encoding='utf-8') as f:
            facts[os.path.basename(file_path)] = f.read()
    return facts

def make_api_request(endpoint, password):
    """
    Makes a POST request to the API endpoint with the password.
    Returns the response.
    """
    try:
        print(f"Sending POST request to: {endpoint} with password: {password}")
        response = requests.post(endpoint, json={"password": password})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {str(e)}")
        return None

def analyze_conversations_and_answer_questions(sorted_data, questions, reanalysis_context=None):
    """
    Analyzes sorted conversations and answers questions using LLM.
    """
    system_prompt = """Twoim zadaniem jest przeanalizowanie pięciu rozmów pomiędzy unikalnymi rozmówcami (każda rozmowa to dwie osoby, wypowiadające się naprzemiennie). Wszystkie rozmowy dotyczą bezpośrednio lub pośrednio Rafała. 

Każda rozmowa zawiera informacje, z których część może być sprzeczna z innymi lub z faktami z wcześniejszych zadań. Twoje zadanie to:

1. Dla każdej rozmowy:
   - Ustal imiona rozmówców (każde imię jest unikalne).
   - Zidentyfikuj temat rozmowy i istotne fakty.
   - Określ, czy padają tam sprzeczne informacje.
   - Jeśli są sprzeczności — zidentyfikuj osobę, która kłamie. Może to wymagać użycia wiedzy powszechnej lub wcześniejszych dokumentów (folder `facts`).

2. Kiedy znajdziesz osobę, która ewidentnie kłamie — uznaj ją za **niewiarygodną** i **odrzuć całą jej wersję wydarzeń**.

3. Następnie, odpowiedz na **6 pytań od centrali**, korzystając wyłącznie z informacji:
   - zawartych w rozmowach (z pominięciem wersji kłamcy),
   - znajdujących się w plikach z faktami (`facts/*.txt`),
   - możliwych do uzyskania poprzez wykonanie zapytania POST z hasłem na podany endpoint (patrz pytanie 05).

4. Dla każdej odpowiedzi zwróć obiekt JSON w jednym z trzech formatów:
   - Jeśli znasz odpowiedź:  
     `{ "answer": "twoja odpowiedź" }`
   - Jeśli odpowiedź wymaga wykonania zapytania POST do API (pytanie 05) Musisz wyodrębnic hasło z kontekstu!:  
     `{ "action": "request",
        "password": "example_password" 
      }`
   - Jeśli odpowiedź wymaga przeszukania folderu z faktami (np. brak wystarczających informacji):  
     `{ "action": "read_facts" }`

---

Oto pytania, na które masz odpowiedzieć:

01: Jeden z rozmówców skłamał podczas rozmowy. Kto to był?  
02: Jaki jest prawdziwy endpoint do API podany przez osobę, która NIE skłamała?  
03: Jakim przezwiskiem określany jest chłopak Barbary?  
04: Jakie dwie osoby rozmawiają ze sobą w pierwszej rozmowie? Podaj ich imiona.  
05: Co odpowiada poprawny endpoint API po wysłaniu do niego hasła w polu "password" jako JSON?  
06: Jak ma na imię osoba, która dostarczyła dostęp do API, ale nie znała do niego hasła, jednak nadal pracuje nad jego zdobyciem?

WAŻNE: Twoja odpowiedź MUSI być poprawnie sformatowanym obiektem JSON, bez żadnych dodatkowych wyjaśnień ani tekstu. Format odpowiedzi:

```json
{
  "01": { "answer": "..." },
  "02": { "answer": "..." },
  "03": { "answer": "..." },
  "04": { "answer": "..." },
  "05": { "action": "request" },
  "06": { "answer": "..." }
}
```

Nie dodawaj żadnego tekstu przed ani po tym obiekcie JSON. Zwróć TYLKO ten obiekt JSON."""

    user_prompt = f"""Przeanalizuj poniższe rozmowy i odpowiedz na pytania. Zwróć TYLKO obiekt JSON z odpowiedziami, bez żadnych dodatkowych wyjaśnień.

Rozmowy:
{json.dumps(sorted_data, ensure_ascii=False, indent=2)}

Pytania:
{json.dumps(questions, ensure_ascii=False, indent=2)}"""

    if reanalysis_context and "facts" in reanalysis_context:
        user_prompt += f"\n\nDODATKOWE FAKTY DO WYKORZYSTANIA:\n{json.dumps(reanalysis_context['facts'], ensure_ascii=False, indent=2)}"

    if reanalysis_context and "incorrect_answers_history" in reanalysis_context and len(reanalysis_context["incorrect_answers_history"]) > 0:
        user_prompt += f"\n\nWAŻNE: Następujące odpowiedzi dla tego pytania zostały uznane za NIEPRAWIDŁOWE w poprzednich próbach. Upewnij się, że Twoja nowa odpowiedź jest inna i poprawna:\n{json.dumps(reanalysis_context['incorrect_answers_history'], ensure_ascii=False, indent=2)}"

    def make_api_call_for_llm():
        return client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1
        )

    try:
        response = retry_with_backoff(make_api_call_for_llm)
        
        # Spróbuj wyczyścić odpowiedź z ewentualnych dodatkowych znaków
        content = response.choices[0].message.content.strip()
        # Znajdź pierwszy { i ostatni }
        start = content.find('{')
        end = content.rfind('}') + 1
        if start == -1 or end == 0:
            raise ValueError("No JSON object found in response")
        
        json_str = content[start:end]
        answers = json.loads(json_str)
        
        # Sprawdź czy odpowiedź ma poprawny format
        if not isinstance(answers, dict):
            raise ValueError("Response is not a dictionary")
        
        # Sprawdź czy wszystkie odpowiedzi mają poprawny format
        for question_id, answer in answers.items():
            if not isinstance(answer, dict):
                raise ValueError(f"Answer for question {question_id} is not a dictionary")
            if "answer" not in answer and "action" not in answer:
                raise ValueError(f"Answer for question {question_id} has neither 'answer' nor 'action' key")
            if "action" in answer and answer["action"] not in ["request", "read_facts"]:
                raise ValueError(f"Invalid action value for question {question_id}")
        
        return answers
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error processing LLM response: {str(e)}")
        print("Raw response:", response.choices[0].message.content)
        return None

def process_answers(answers, sorted_data, questions):
    """
    Processes answers and performs necessary actions (API requests, reading facts).
    Returns final answers.
    """
    final_answers = {}
    
    for question_id, answer in answers.items():
        if "action" in answer:
            if answer["action"] == "request":
                # Znajdź endpoint z odpowiedzi na pytanie 02
                endpoint = answers["02"]["answer"]
                # Hasło powinno być dostarczone razem z akcją "request"
                password = answer["password"]
                
                print(f"DEBUG: Sending POST request to: {endpoint} with password: {password}")
                # Wykonaj zapytanie do API
                api_response = make_api_request(endpoint, password)
                if api_response:
                    final_answers[question_id] = {"answer": str(api_response)}
                else:
                    final_answers[question_id] = {"error": "Failed to get API response"}
                    
            elif answer["action"] == "read_facts":
                # Pobierz listę plików z folderu facts
                fact_files = glob.glob('facts/*.txt')
                
                # Dla każdego pliku z faktami
                for fact_file in fact_files:
                    # Wczytaj zawartość pliku
                    with open(fact_file, 'r', encoding='utf-8') as f:
                        fact_content = f.read()
                    
                    # Przygotuj prompt dla LLM
                    fact_prompt = f"""Przeanalizuj poniższy fakt i odpowiedz na pytanie. Jeśli znasz odpowiedź, zwróć ją w formacie JSON {{ \"answer\": \"twoja odpowiedź\" }}. Jeśli nie znasz odpowiedzi, zwróć {{ \"answer\": \"none\" }}. Zwróć TYLKO obiekt JSON, bez żadnych dodatkowych wyjaśnień.\n\nPytanie: {questions[question_id]}\nFakt: {fact_content}"""
                    
                    def make_fact_api_call():
                        return client.chat.completions.create(
                            model="gpt-4.1",
                            messages=[
                                {"role": "system", "content": "Jesteś asystentem analizującym fakty i odpowiadającym na pytania. Zwracaj odpowiedzi w formacie JSON. Zwróć TYLKO obiekt JSON."},
                                {"role": "user", "content": fact_prompt}
                            ],
                            temperature=0.1
                        )

                    try:
                        response_fact = retry_with_backoff(make_fact_api_call)
                        fact_answer_content = response_fact.choices[0].message.content.strip()
                        start_fact = fact_answer_content.find('{')
                        end_fact = fact_answer_content.rfind('}') + 1
                        if start_fact == -1 or end_fact == 0:
                            raise ValueError("No JSON object found in fact response")
                        json_fact_str = fact_answer_content[start_fact:end_fact]
                        fact_answer = json.loads(json_fact_str)
                        
                        # Jeśli znaleziono odpowiedź, zapisz ją i zakończ przeszukiwanie
                        if fact_answer.get("answer") != "none":
                            final_answers[question_id] = fact_answer
                            break
                    except (json.JSONDecodeError, ValueError) as e:
                        print(f"Error: Could not parse LLM response as JSON for file {fact_file}: {str(e)}")
                        print("Raw response for fact:", response_fact.choices[0].message.content)
                        continue
                
                # Jeśli nie znaleziono odpowiedzi w żadnym pliku
                if question_id not in final_answers:
                    final_answers[question_id] = {"answer": "none"}
        else:
            final_answers[question_id] = answer
    
    return final_answers

def extract_simple_answers(final_answers):
    simple_answers = {}
    for q_id, q_data in final_answers.items():
        if "answer" in q_data:
            answer_value = q_data["answer"]
            if q_id == "05":
                try:
                    # Attempt to parse it as JSON and get the 'message'
                    # Replace single quotes with double quotes for valid JSON parsing
                    parsed_json = json.loads(answer_value.replace("'", "\""))
                    simple_answers[q_id] = parsed_json.get("message", answer_value)
                except json.JSONDecodeError:
                    simple_answers[q_id] = answer_value
            else:
                simple_answers[q_id] = answer_value
        elif "action" in q_data:
            # This case should ideally not happen for final_answers if actions were processed
            # but as a fallback, explicitly state action was needed.
            simple_answers[q_id] = f"Action needed: {q_data['action']}"
        else:
            simple_answers[q_id] = "No answer"
    return simple_answers

def send_answers_to_report_endpoint(answers_to_send, aidevs_key):
    payload = {
        "apikey": aidevs_key,
        "answer": answers_to_send,
        "task": "phone"
    }
    print(f"\nSending payload to report endpoint:")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    try:
        response = requests.post(REPORT_URL, json=payload)
        
        # Zamiast raise_for_status(), sprawdzamy status code i odczytujemy JSON
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error sending answers to report endpoint. Status code: {response.status_code}")
            try:
                error_response = response.json()
                print(f"Error details: {json.dumps(error_response, ensure_ascii=False, indent=2)}")
                return error_response # Zwracamy obiekt błędu, aby móc go analizować
            except json.JSONDecodeError:
                print(f"Could not decode JSON from error response. Raw content: {response.text}")
                return {"code": response.status_code, "message": response.text} # Zwracamy status i raw text
    except requests.exceptions.RequestException as e:
        print(f"Error sending answers to report endpoint: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    print("Próbuję pobrać posortowane dane z API...")
    try:
        sorted_data = fetch_and_save_sorted_data()
        print("\nPosortowane dane zostały pobrane.")
        
        # Pobierz pytania
        questions = fetch_questions()
        print("\nPytania zostały pobrane.")
        
        # Przeanalizuj rozmowy i odpowiedz na pytania
        print("\nRozpoczynam analizę rozmów i odpowiadanie na pytania...")
        answers = analyze_conversations_and_answer_questions(sorted_data, questions)
        
        if answers:
            print("\nPreliminarnie odpowiedzi na pytania:")
            print(json.dumps(answers, ensure_ascii=False, indent=2))
            
            # Przetwórz odpowiedzi i wykonaj potrzebne akcje
            print("\nPrzetwarzam odpowiedzi i wykonuję potrzebne akcje...")
            final_answers = process_answers(answers, sorted_data, questions)
            
            print("\nFinalne odpowiedzi:")
            print(json.dumps(final_answers, ensure_ascii=False, indent=2))
            
            # Zapisz odpowiedzi do pliku
            with open('answers.json', 'w', encoding='utf-8') as f:
                json.dump(final_answers, f, ensure_ascii=False, indent=2)
            print("\nOdpowiedzi zostały zapisane do pliku answers.json")
            
            max_report_attempts = 10 # Zwiększono liczbę prób
            report_attempt_count = 0
            successful_report = False
            last_report_response = None
            incorrect_attempts_count = {} # Słownik do śledzenia liczby błędnych prób na pytanie
            incorrect_answers_history = {} # Słownik do przechowywania historii błędnych odpowiedzi

            while report_attempt_count < max_report_attempts and not successful_report:
                if report_attempt_count > 0:
                    print(f"\nRetrying report attempt {report_attempt_count + 1}/{max_report_attempts}...")
                    if last_report_response and last_report_response.get('code') != 0:
                        error_message = last_report_response.get("message", "")
                        match = re.search(r"question (\d+)", error_message)
                        if match:
                            incorrect_q_id = match.group(1)
                            incorrect_attempts_count[incorrect_q_id] = incorrect_attempts_count.get(incorrect_q_id, 0) + 1
                            print(f"Detected incorrect question: {incorrect_q_id}. Consecutive incorrect attempts: {incorrect_attempts_count[incorrect_q_id]}.")

                            # Dodaj bieżącą błędną odpowiedź do historii
                            if incorrect_q_id in final_answers and "answer" in final_answers[incorrect_q_id]:
                                if incorrect_q_id not in incorrect_answers_history:
                                    incorrect_answers_history[incorrect_q_id] = []
                                incorrect_answers_history[incorrect_q_id].append(final_answers[incorrect_q_id]["answer"])

                            reanalysis_context = {}
                            if incorrect_attempts_count[incorrect_q_id] >= 3:
                                print(f"Question {incorrect_q_id} failed 3 or more times. Adding facts to re-analysis context...")
                                facts = read_facts()
                                reanalysis_context["facts"] = facts
                            
                            if incorrect_q_id in incorrect_answers_history:
                                reanalysis_context["incorrect_answers_history"] = incorrect_answers_history[incorrect_q_id]

                            print(f"Original question for re-analysis ({incorrect_q_id}): {questions[incorrect_q_id]}")

                            temp_questions_for_llm = {incorrect_q_id: questions[incorrect_q_id]}
                            reanalyzed_raw_answers = analyze_conversations_and_answer_questions(sorted_data, temp_questions_for_llm, reanalysis_context)
                            print(f"Raw re-analyzed answers for {incorrect_q_id}: {reanalyzed_raw_answers}")

                            if reanalyzed_raw_answers:
                                reanalyzed_processed_answers = process_answers(reanalyzed_raw_answers, sorted_data, questions)
                                final_answers.update(reanalyzed_processed_answers)
                                print(f"Updated final answers after re-analysis: {final_answers}")
                                print(f"Updated answer for question {incorrect_q_id}.")
                                # Reset attempts if re-analysis is successful for this question
                                incorrect_attempts_count[incorrect_q_id] = 0
                                if incorrect_q_id in incorrect_answers_history:
                                    del incorrect_answers_history[incorrect_q_id]
                            else:
                                print(f"Failed to re-analyze question {incorrect_q_id}. Aborting retries for this question.")
                                # Do not break here, let the loop continue if other questions are fine
                        else:
                            print("Could not extract incorrect question ID from report error message. Aborting retries.")
                            break

                answers_for_report = extract_simple_answers(final_answers)
                
                print("\nWysyłam odpowiedzi do endpointu raportowania...")
                report_response = send_answers_to_report_endpoint(answers_for_report, AIDEVS_KEY)
                last_report_response = report_response
                
                if report_response is not None:
                    if report_response.get("code") == 0:
                        successful_report = True
                        print("\nAnswers successfully sent to report endpoint.")
                        # Reset all attempts on successful report
                        incorrect_attempts_count = {}
                        incorrect_answers_history = {}
                    else:
                        response_code = report_response.get('code', 'N/A')
                        response_message = report_response.get('message', 'N/A')
                        print(f"\nNie udało się wysłać odpowiedzi do endpointu raportowania. Kod błędu: {response_code}, Wiadomość: {response_message}")
                        report_attempt_count += 1
                        time.sleep(2 ** report_attempt_count)
                else:
                    print("\nNie udało się wysłać odpowiedzi do endpointu raportowania. Brak odpowiedzi z serwera.")
                    report_attempt_count += 1
                    time.sleep(2 ** report_attempt_count)

            if not successful_report:
                print("\nFailed to send answers to report endpoint after multiple attempts.")
            else:
                print("\nFinal answers successfully submitted.")
        
    except requests.exceptions.RequestException as e:
        print(f"\nNie udało się pobrać posortowanych danych z API: {str(e)}")
        print("Sprawdzam lokalny plik z posortowanymi danymi...")
        
        if os.path.exists('phone_data_sorted.json'):
            print("Znaleziono lokalny plik z posortowanymi danymi. Wczytuję...")
            with open('phone_data_sorted.json', 'r', encoding='utf-8') as f:
                sorted_data = json.load(f)
            
            # Pobierz pytania
            questions = fetch_questions()
            print("\nPytania zostały pobrane.")
            
            # Przeanalizuj rozmowy i odpowiedz na pytania
            print("\nRozpoczynam analizę rozmów i odpowiadanie na pytania...")
            answers = analyze_conversations_and_answer_questions(sorted_data, questions)
            
            if answers:
                print("\nPreliminarnie odpowiedzi na pytania:")
                print(json.dumps(answers, ensure_ascii=False, indent=2))
                
                # Przetwórz odpowiedzi i wykonaj potrzebne akcje
                print("\nPrzetwarzam odpowiedzi i wykonuję potrzebne akcje...")
                final_answers = process_answers(answers, sorted_data, questions)
                
                print("\nFinalne odpowiedzi:")
                print(json.dumps(final_answers, ensure_ascii=False, indent=2))
                
                # Zapisz odpowiedzi do pliku
                with open('answers.json', 'w', encoding='utf-8') as f:
                    json.dump(final_answers, f, ensure_ascii=False, indent=2)
                print("\nOdpowiedzi zostały zapisane do pliku answers.json")
                
                max_report_attempts = 5 # Zwiększono liczbę prób
                report_attempt_count = 0
                successful_report = False
                last_report_response = None
                incorrect_attempts_count = {}
                incorrect_answers_history = {}

                while report_attempt_count < max_report_attempts and not successful_report:
                    if report_attempt_count > 0:
                        print(f"\nRetrying report attempt {report_attempt_count + 1}/{max_report_attempts}...")
                        if last_report_response and last_report_response.get('code') != 0:
                            error_message = last_report_response.get("message", "")
                            match = re.search(r"question (\d+)", error_message)
                            if match:
                                incorrect_q_id = match.group(1)
                                incorrect_attempts_count[incorrect_q_id] = incorrect_attempts_count.get(incorrect_q_id, 0) + 1
                                print(f"Detected incorrect question: {incorrect_q_id}. Consecutive incorrect attempts: {incorrect_attempts_count[incorrect_q_id]}.")

                                # Dodaj bieżącą błędną odpowiedź do historii
                                if incorrect_q_id in final_answers and "answer" in final_answers[incorrect_q_id]:
                                    if incorrect_q_id not in incorrect_answers_history:
                                        incorrect_answers_history[incorrect_q_id] = []
                                    incorrect_answers_history[incorrect_q_id].append(final_answers[incorrect_q_id]["answer"])

                                reanalysis_context = {}
                                if incorrect_attempts_count[incorrect_q_id] >= 3:
                                    print(f"Question {incorrect_q_id} failed 3 or more times. Adding facts to re-analysis context...")
                                    facts = read_facts()
                                    reanalysis_context["facts"] = facts
                                
                                if incorrect_q_id in incorrect_answers_history:
                                    reanalysis_context["incorrect_answers_history"] = incorrect_answers_history[incorrect_q_id]

                                print(f"Original question for re-analysis ({incorrect_q_id}): {questions[incorrect_q_id]}")

                                temp_questions_for_llm = {incorrect_q_id: questions[incorrect_q_id]}
                                reanalyzed_raw_answers = analyze_conversations_and_answer_questions(sorted_data, temp_questions_for_llm, reanalysis_context)
                                print(f"Raw re-analyzed answers for {incorrect_q_id}: {reanalyzed_raw_answers}")

                                if reanalyzed_raw_answers:
                                    reanalyzed_processed_answers = process_answers(reanalyzed_raw_answers, sorted_data, questions)
                                    final_answers.update(reanalyzed_processed_answers)
                                    print(f"Updated final answers after re-analysis: {final_answers}")
                                    print(f"Updated answer for question {incorrect_q_id}.")
                                    # Reset attempts if re-analysis is successful for this question
                                    incorrect_attempts_count[incorrect_q_id] = 0
                                    if incorrect_q_id in incorrect_answers_history:
                                        del incorrect_answers_history[incorrect_q_id]
                                else:
                                    print(f"Failed to re-analyze question {incorrect_q_id}. Aborting retries for this question.")
                                    # Do not break here, let the loop continue if other questions are fine
                            else:
                                print("Could not extract incorrect question ID from report error message. Aborting retries.")
                                break

                    answers_for_report = extract_simple_answers(final_answers)
                    
                    print("\nWysyłam odpowiedzi do endpointu raportowania...")
                    print(f"Payload for report: {json.dumps(answers_for_report, ensure_ascii=False, indent=2)}")
                    report_response = send_answers_to_report_endpoint(answers_for_report, AIDEVS_KEY)
                    last_report_response = report_response
                    
                    if report_response is not None:
                        if report_response.get("code") == 0:
                            successful_report = True
                            print("\nAnswers successfully sent to report endpoint.")
                            # Reset all attempts on successful report
                            incorrect_attempts_count = {}
                            incorrect_answers_history = {}
                        else:
                            response_code = report_response.get('code', 'N/A')
                            response_message = report_response.get('message', 'N/A')
                            print(f"\nNie udało się wysłać odpowiedzi do endpointu raportowania. Kod błędu: {response_code}, Wiadomość: {response_message}")
                            report_attempt_count += 1
                            time.sleep(2 ** report_attempt_count)
                    else:
                        print("\nNie udało się wysłać odpowiedzi do endpointu raportowania. Brak odpowiedzi z serwera.")
                        report_attempt_count += 1
                        time.sleep(2 ** report_attempt_count)

                if not successful_report:
                    print("\nFailed to send answers to report endpoint after multiple attempts.")
                else:
                    print("\nFinal answers successfully submitted.")
        else:
            print("Nie znaleziono lokalnego pliku z posortowanymi danymi.")
            print("Rozpoczynam analizę rozmów przez LLM...")
            
            # Fetch and save phone data if not exists
            if not os.path.exists('phone_data.json'):
                fetch_and_save_phone_data()
            
            # Process conversations
            process_conversations()