from dotenv import load_dotenv
import os
import requests
import openai

load_dotenv()

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
AIDEVS_API_KEY=os.getenv("AIDEVS_API_KEY")

# Verify API keys are loaded
if not AIDEVS_API_KEY:
    raise ValueError("AIDEVS_API_KEY not found in environment variables")

# Endpointy
BASE_URL = "https://centrala.ag3nts.org"

QUESTIONS_URL=f"{BASE_URL}/data/{AIDEVS_API_KEY}/gps_question.json"
DATA_URL=f"{BASE_URL}/data/{AIDEVS_API_KEY}/gps.txt"

PEOPLE_URL = f"{BASE_URL}/people"
PLACES_URL = f"{BASE_URL}/places"
DB_URL = f"{BASE_URL}/apidb"
GPS_URL = f"{BASE_URL}/gps"
REPORT_URL = f"{BASE_URL}/report"

# Configure OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def get_questions():
    """Fetch questions from the JSON endpoint."""
    url = QUESTIONS_URL.format(AIDEVS_API_KEY=AIDEVS_API_KEY)
    print(f"\nTrying to fetch questions from: {url}")
    
    try:
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            return None
            
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def get_gps_data():
    """Fetch GPS data from the text endpoint."""
    url = DATA_URL.format(AIDEVS_API_KEY=AIDEVS_API_KEY)
    print(f"\nTrying to fetch GPS data from: {url}")
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            return None
            
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Szukane miasto
TARGET_CITY = "Lubawa"

# Krok 1: Pobierz osoby z Lubawy
def get_people_from_city(city):
    response = requests.post(PLACES_URL, json={
        "apikey": AIDEVS_API_KEY,
        "query": city
    })
    print(f"\nDatabase get_people query for {city}:")
    print(f"Response: {response.text}")
    return response.json()["message"].split()


# Krok 2: Pobierz ID użytkownika z bazy danych
def get_user_id(name):
    sql = f"SELECT id FROM users WHERE username = '{name}'"
    response = requests.post(DB_URL, json={
        "task": "database",
        "apikey": AIDEVS_API_KEY,
        "query": sql
    })
    print(f"\nDatabase query for {name}:")
    print(f"SQL: {sql}")
    print(f"Response: {response.text}")
    
    try:
        data = response.json()
        if "reply" in data and data["reply"]:
            return data["reply"][0]["id"]
        return None
    except (KeyError, IndexError, ValueError) as e:
        print(f"Error processing response for {name}: {e}")
        return None

# Krok 3: Pobierz współrzędne GPS po ID
def get_gps_coordinates(user_id):
    response = requests.post(GPS_URL, json={
        "apikey": AIDEVS_API_KEY,
        "userID": user_id
    })
    return response.json()

def get_all_users_gps():
    """Fetch GPS data for all users."""
    all_gps_data = {}
    
    # Get all people from the city
    people = get_people_from_city(TARGET_CITY)
    print(f"\nFound {len(people)} people in {TARGET_CITY}")
    
    for person in people:
        if person.lower() == "barbara":
            continue
            
        user_id = get_user_id(person)
        if user_id is not None:
            print(f"\nFetching GPS data for {person} (ID: {user_id})")
            try:
                response = requests.post(GPS_URL, json={
                    "apikey": AIDEVS_API_KEY,
                    "userID": str(user_id)  # Convert user_id to string
                })
                
                if response.status_code == 200:
                    gps_data = response.json()
                    print(f"Response for {person}: {gps_data}")  # Debug print
                    
                    if gps_data.get("code") == 0 and "message" in gps_data:
                        coords = gps_data["message"]
                        if "lat" in coords and "lon" in coords:
                            all_gps_data[person] = {
                                "lat": coords["lat"],
                                "lon": coords["lon"]
                            }
                            print(f"Successfully got GPS data for {person}")
                        else:
                            print(f"No GPS coordinates found in message for {person}")
                    else:
                        print(f"Invalid response format for {person}: {gps_data}")
                else:
                    print(f"Failed to get GPS data for {person}. Status code: {response.status_code}")
            except Exception as e:
                print(f"Error getting GPS data for {person}: {e}")
    
    return all_gps_data

def send_result_request(results):
    response = requests.post(REPORT_URL, json={
    "task": "gps",
    "apikey": AIDEVS_API_KEY,
    "answer": results
    })

    if response.status_code == 200:
        result_data = response.json()
        print(result_data)

        
# Główna logika agenta
def run_agent():
    # Print the data
    print("=== Questions ===")
    questions = get_questions()
    if questions:
        print("\nParsed Questions:")
        print(questions)
    else:
        print("\nFailed to get questions data")

    print("\n=== GPS Data ===")
    gps_data = get_gps_data()
    if gps_data:
        print("\nGPS Data:")
        print(gps_data)
    else:
        print("\nFailed to get GPS data")

    # Get GPS data for all users
    print("\n=== Fetching GPS data for all users ===")
    results = get_all_users_gps()
    
    print("\nFinal Results:")
    print(results)

    send_result_request(results)
    return results

def download_and_save_gps_data():
    """Download GPS data and save it to a file."""
    try:
        response = requests.get(DATA_URL)
        if response.status_code == 200:
            with open('gps_data.txt', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("GPS data saved to gps_data.txt")
            return True
        else:
            print(f"Failed to download GPS data. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error downloading GPS data: {e}")
        return False

def analyze_gps_data_with_gpt():
    """Analyze GPS data using GPT-4."""
    analysis_file = 'gps_analysis.txt'
    
    # Check if analysis already exists
    if os.path.exists(analysis_file):
        print(f"\nAnalysis file {analysis_file} already exists. Reading existing analysis...")
        with open(analysis_file, 'r', encoding='utf-8') as f:
            print("\nExisting Analysis:")
            print(f.read())
        return

    try:
        # Read the GPS data file
        with open('gps_data.txt', 'r', encoding='utf-8') as f:
            gps_data = f.read()

        # Prepare the prompt for GPT-4
        prompt = f"""Analyze the following GPS data and answer the question: "What was the agent's purpose?"
        
GPS Data:
{gps_data}

Please provide a detailed analysis of the agent's purpose based on this data."""

        # Call GPT-4
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant analyzing GPS data to determine an agent's purpose."},
                {"role": "user", "content": prompt}
            ]
        )

        # Get the analysis
        analysis = response.choices[0].message.content

        # Save analysis to file
        with open(analysis_file, 'w', encoding='utf-8') as f:
            f.write(analysis)

        # Print the analysis
        print("\nGPT-4 Analysis:")
        print(analysis)
        print(f"\nAnalysis saved to {analysis_file}")

    except Exception as e:
        print(f"Error analyzing GPS data: {e}")

# Download and analyze GPS data
if download_and_save_gps_data():
    analyze_gps_data_with_gpt()
    
# Uruchom agenta i wyślij dane do Centrali
final_result = run_agent()