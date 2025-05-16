import os
from dotenv import load_dotenv
import requests

load_dotenv()

klucz = os.getenv("AIDEVS_KEY")
model = "gemma3:latest"
url = f"https://centrala.ag3nts.org/data/{klucz}/cenzura.txt"
response = requests.get(url)
tekst = response.text
print(tekst)

prompt = f"""You are a censoring agent. Your task is to replace personal data in the following text with the word "CENZURA".

Follow these rules strictly:
- Replace first name and last name with "CENZURA"
- Replace age with "CENZURA"
- Replace city name with "CENZURA""
- Replace street and house number (BOTH!) with "CENZURA"
- Replace any personal data with "CENZURA"
- DO NOT change any other characters, punctuation, or text
- Return only the censored text

<example>
Oryginał: Osoba podejrzana to Andrzej Mazur. Adres: Gdańsk, ul. Długa 8. Wiek: 29 lat.  
Wynik: Osoba podejrzana to CENZURA. Adres: CENZURA, ul. CENZURA. Wiek: CENZURA.
</example>
Text to censor:
{tekst}"""

# Send request to the local API
api_url = "http://localhost:11434/api/generate"
payload = {
    "model": model,
    "prompt": prompt,
    "stream": False
}

response = requests.post(api_url, json=payload)
result = response.json()
censored_text = result.get('response', '')
print("Censored text:", censored_text)

# Send the result to the final endpoint
final_url = "https://centrala.ag3nts.org/report"
final_payload = {
    "task": "CENZURA",
    "apikey": klucz,
    "answer": censored_text
}

headers = {
    'Content-Type': 'application/json'
}
final_response = requests.post(final_url, json=final_payload, headers=headers)
print("Final response:", final_response.text)


