from dotenv import load_dotenv
import os
import requests
import json
import re
import base64
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Read the API keys
openai_api_key = os.getenv('OPENAI_API_KEY')
aidevs_api_key = os.getenv('AIDEVS_API_KEY')

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# Print the keys (in a secure way, showing only first few characters)
if openai_api_key == None:
    print("OPENAI_API_KEY not found")

if aidevs_api_key == None:
    print("AIDEVS_API_KEY not found") 
    
# Prepare the payload
payload = {
    "task": "photos",
    "apikey": aidevs_api_key,
    "answer": "START"
}

# Send POST request to the endpoint
response = requests.post('https://centrala.ag3nts.org/report', json=payload)

# Print the response in a readable format
print(f"Status Code: {response.status_code}")
response_data = response.json()
print("\nResponse:")
print(f"Code: {response_data['code']}")
print(f"Message: {response_data['message']}")

# Create a directory for downloaded images if it doesn't exist
download_dir = "downloaded_images"
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Extract image filenames using regex
images = re.findall(r'IMG_\d+(?:_[A-Z0-9]+)?\.PNG', response_data['message'])
print("\nFound images:", images)

base_url = "https://centrala.ag3nts.org/dane/barbara/"

# System prompt for image analysis
SYSTEM_PROMPT = """Jesteś ekspertem w analizie zdjęć i tworzeniu rysopisów. Twoim zadaniem jest obiektywny opis wyglądu osoby. Twoim zadaniem jest szczegółowo przeanalizować załączone zdjęcie i dobrać jedną z poniższych akcji, która poprawi jego jakość. Możliwe opcje to:

- "REPAIR NAZWA_PLIKU" – jeśli na zdjęciu widoczne są zakłócenia, szumy, glitche, artefakty lub problemy z renderowaniem.
- "DARKEN NAZWA_PLIKU" – jeśli zdjęcie jest zbyt jasne lub przepalone, przez co utracone są szczegóły.
- "BRIGHTEN NAZWA_PLIKU" – jeśli zdjęcie jest zbyt ciemne i trudno dostrzec szczegóły.
- "NONE" – jeśli zdjęcie jest dobrej jakości i nie wymaga obróbki.

Zwróć wynik w formacie JSON, zawierający dwa pola:

- `"action"` – wartość z powyższych opcji (np. "REPAIR IMG_001.PNG")
- `"justification"` – jednozdaniowe uzasadnienie Twojej decyzji (w języku angielskim)"""

DESCRIPTION_PROMPT = """Twoim zadaniem jest przeanalizowanie załączonego zdjęcia przedstawiającego postać oraz stworzenie bardzo dokładnego rysopisu w języku polskim. Uwzględnij jak najwięcej cech charakterystycznych: płeć, wiek, rysy twarzy, kolor i długość włosów, oczy, brwi, karnację, wzrost (jeśli możliwy do oszacowania), styl ubioru, dodatki, tatuaże, postawę ciała, mimikę, oraz inne nietypowe szczegóły. 

Nie spekuluj, nie oceniaj charakteru osoby. Skup się na tym, co jest fizycznie widoczne. Rysopis ma być możliwie obiektywny, precyzyjny i szczegółowy.

Zwróć wynik w formacie JSON:

```json
{
  "answer": "Tu wstaw dokładny rysopis postaci w języku polskim jako jeden ciągły tekst."
}
```"""

def extract_images_from_message(message):
    """Extract image filenames from a message using regex"""
    return re.findall(r'IMG_\d+(?:_[A-Z0-9]+)?\.PNG', message)

def download_image(image_name):
    """Download an image if it doesn't exist and return its path"""
    file_path = os.path.join(download_dir, image_name)
    
    if os.path.exists(file_path):
        print(f"Image already exists, skipping download: {image_name}")
        return file_path
        
    image_url = base_url + image_name
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Successfully downloaded: {image_name}")
        return file_path
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {image_name}: {e}")
        return None

def analyze_image(image_name):
    """Analyze an image using OpenAI and return the analysis"""
    file_path = os.path.join(download_dir, image_name)
    
    try:
        with open(file_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Analyze this image: {image_name}"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )

        analysis = json.loads(response.choices[0].message.content)
        print(f"\nAnalysis for {image_name}:")
        print(f"Action: {analysis['action']}")
        print(f"Justification: {analysis['justification']}")
        return analysis

    except Exception as e:
        print(f"Error analyzing {image_name}: {e}")
        return None

def generate_person_description(image_name):
    """Generate a detailed description of the person in the image"""
    file_path = os.path.join(download_dir, image_name)
    
    try:
        with open(file_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "system",
                    "content": DESCRIPTION_PROMPT
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Describe the person in this image: {image_name}"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500,
            response_format={ "type": "json_object" }
        )

        try:
            description = json.loads(response.choices[0].message.content)
            if 'answer' not in description:
                print(f"Warning: Response missing 'answer' field: {response.choices[0].message.content}")
                description = {"answer": response.choices[0].message.content}
        except json.JSONDecodeError as e:
            print(f"Warning: Invalid JSON response: {response.choices[0].message.content}")
            description = {"answer": response.choices[0].message.content}

        print(f"\nPerson description for {image_name}:")
        print(f"Answer: {description['answer']}")
        return description

    except Exception as e:
        print(f"Error generating person description for {image_name}: {e}")
        return None

def send_action_to_endpoint(action_or_description, is_description=False):
    """Send the action or description to the endpoint and return the response"""
    action_payload = {
        "apikey": aidevs_api_key,
        "answer": action_or_description,
        "task": "photos"
    }
    
    try:
        action_response = requests.post('https://centrala.ag3nts.org/report', json=action_payload)
        print(f"\nAction Response:")
        print(f"Status Code: {action_response.status_code}")
        print(f"Response: {action_response.text}")
        
        response_data = action_response.json()
        if 'message' in response_data:
            # Check for flag pattern in message
            flag_match = re.search(r'\{\{FLG:([^}]+)\}\}', response_data['message'])
            if flag_match:
                flag = flag_match.group(1)
                print(f"\n!!! FLAG FOUND: {flag} !!!")
                print("Stopping program execution...")
                exit(0)
                
        return response_data
    except Exception as e:
        print(f"Error sending {'description' if is_description else 'action'} to endpoint: {e}")
        return None

# Process initial images
processed_images = set()
images_to_process = set(images)

while images_to_process:
    current_image = images_to_process.pop()
    if current_image in processed_images:
        continue
        
    # Download the image
    file_path = download_image(current_image)
    if not file_path:
        continue
        
    # Analyze the image
    analysis = analyze_image(current_image)
    if not analysis:
        continue
        
    # Handle based on the action
    if analysis['action'] != "NONE":
        response = send_action_to_endpoint(analysis['action'])
        if response:
            # Extract new images from the response message
            new_images = extract_images_from_message(response['message'])
            for new_image in new_images:
                if new_image not in processed_images and new_image not in images_to_process:
                    print(f"Found new image in response: {new_image}")
                    images_to_process.add(new_image)
    else:
        # For NONE action, generate person description and send it
        description = generate_person_description(current_image)
        if description:
            response = send_action_to_endpoint(description['answer'], is_description=True)
            if response:
                # Extract new images from the response message
                new_images = extract_images_from_message(response['message'])
                for new_image in new_images:
                    if new_image not in processed_images and new_image not in images_to_process:
                        print(f"Found new image in response: {new_image}")
                        images_to_process.add(new_image)
    
    processed_images.add(current_image) 