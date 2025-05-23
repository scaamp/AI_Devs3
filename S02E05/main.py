import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
from pprint import pprint
import json
import openai
import dotenv
import base64

dotenv.load_dotenv()

os.makedirs("pobrane", exist_ok=True)
openai.api_key = os.getenv("OPENAI_API_KEY")
aidevs_key = os.getenv("AIDEVS_KEY")
# Adres URL do pliku HTML
url = "https://centrala.ag3nts.org/dane/arxiv-draft.html"

def zapisz(url, folder="pobrane/"):
    try:
        r = requests.get(url)
        r.raise_for_status()
        nazwa = url.split("/")[-1]
        with open(os.path.join(folder, nazwa), "wb") as f:
            f.write(r.content)
        print(f"✔️ Zapisano: {nazwa}")
    except Exception as e:
        print(f"❌ Błąd przy {url}: {e}")

def zindexuj_html(html):
    soup = BeautifulSoup(html, "html.parser")
    result = []

    # Przejście po elementach w kolejności DOM
    for elem in soup.body.descendants:
        if elem.name == "img":
            src = elem.get("src")
            if src:  # Only process if src exists
                result.append({
                    "type": "image",
                    "src": os.path.join("pobrane", src.split("/")[-1])
                })
        elif elem.name == "audio":
            src = elem.get("src")
            if src:  # Only process if src exists
                result.append({
                    "type": "audio",
                    "src": os.path.join("pobrane", src.split("/")[-1])
                })
        elif elem.name == "source" and elem.get("type") == "audio/mpeg":
            src = elem.get("src")
            if src:  # Only process if src exists
                result.append({
                    "type": "audio",
                    "src": os.path.join("pobrane", src.split("/")[-1])
                })
        elif elem.string and elem.string.strip():
            result.append({
                "type": "text",
                "content": elem.string.strip()
            })

    return result

def to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Pobierz stronę
response = requests.get(url)
html = response.text

# Parsowanie HTML
soup = BeautifulSoup(html, "html.parser")

# --- OBRAZY ---
obrazy = [img.get("src") for img in soup.find_all("img")]
print("\n🖼️ Obrazy:", obrazy)

# --- MP3 ---
mp3ki = []
for audio in soup.find_all("audio"):
    src = audio.get("src")
    if src:
        mp3ki.append(src)
for source in soup.find_all("source"):
    if source.get("type") == "audio/mpeg":
        mp3ki.append(source.get("src"))
print("\n🎵 MP3:", mp3ki)

# Pobierz wszystkie obrazki i mp3 (upewnij się, że mają pełne URL-e)
for link in obrazy + mp3ki:
    pelny_link = urljoin(url, link)
    zapisz(pelny_link)

# Indeksowanie zawartości
zindeksowane = zindexuj_html(html)

# Zapisz zindeksowane do pliku JSON
with open("zindeksowane.json", "w", encoding="utf-8") as f:
    json.dump(zindeksowane, f, ensure_ascii=False, indent=2)

# Budowa multimodalnego inputu
content = []

for item in zindeksowane:
    if item["type"] == "text":
        content.append({"type": "text", "text": item["content"]})
    elif item["type"] == "image":
        b64 = to_base64(item["src"])
        content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}})
    elif item["type"] == "audio":
        with open(item["src"], "rb") as audio_file:
            transcription = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            ).text
        content.append({"type": "text", "text": f"Transkrypcja audio: {transcription}"})
        
# Dodaj pytania
content.append({
    "type": "text",
    "text": (
        "Odpowiedz na poniższe pytania w bardzo krótkiej formie (jedno zdanie), w formacie JSON. Nie zwracaj nic poza odpowiedzią.\n"
        # "Klucz ma byc identyczny jak w podanym przykładzie czyli 'ID-pytania-01:' itd.\n"
        "01=jakiego owocu użyto podczas pierwszej próby transmisji materii w czasie?\n"
        "02=Na rynku którego miasta wykonano testową fotografię użytą podczas testu przesyłania multimediów?\n"
        "03=Co Bomba chciał znaleźć w Grudziądzu?\n"
        "04=Resztki jakiego dania zostały pozostawione przez Rafała?\n"
        "05=Od czego pochodzą litery BNW w nazwie nowego modelu językowego?\n\n"
        "Format:\n"
        "{\n"
        '    "01": "krótka odpowiedź",\n'
        '    "02": "krótka odpowiedź",\n'
        '    "03": "krótka odpowiedź",\n'
        '    "04": "krótka odpowiedź",\n'
        '    "05": "krótka odpowiedź"\n'
        "}"
    )
})

# Wyślij do GPT-4o
response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": content}
    ],
    temperature=0.2
)

answer = response.choices[0].message.content

print(answer)      

# Parsowanie odpowiedzi JSON
try:
    # Usuń ewentualne znaki nowej linii i spacje z początku i końca
    answer = answer.strip()
    # Usuń markery bloku kodu JSON
    answer = answer.replace("```json", "").replace("```", "").strip()
    # Jeśli odpowiedź jest w formacie JSON string, parsuj ją
    if answer.startswith('{') and answer.endswith('}'):
        parsed_answer = json.loads(answer)
    else:
        print("Odpowiedź nie jest w formacie JSON")
        parsed_answer = {}
except json.JSONDecodeError as e:
    print(f"Błąd parsowania JSON: {e}")
    parsed_answer = {}
    
print("Wysyłana odpowiedź:", parsed_answer)   

# Wysyłanie odpowiedzi do API
post_payload = {
    "task": "arxiv",
    "apikey": aidevs_key,
    "answer": parsed_answer
}

response = requests.post("https://centrala.ag3nts.org/report", json=post_payload)
print("\nOdpowiedź z API:", response.json())      
    
