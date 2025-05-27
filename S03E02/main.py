from dotenv import load_dotenv
import os
import uuid
import glob
import requests
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from qdrant_client.http.models import VectorParams, Distance
import tiktoken
import re
from datetime import datetime

# === KONFIGURACJA ===
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
AIDEVS_API_KEY = os.getenv("AIDEVS_API_KEY")
QDRANT_URL = "https://eeb8095a-b791-4de1-9318-86138a58594d.eu-central-1-0.aws.cloud.qdrant.io/"
COLLECTION_NAME = "reports"
EMBEDDING_MODEL = "text-embedding-3-large"
CHUNK_SIZE = 500  # liczba tokenów
VECTOR_SIZE = 3072  # wymiar wektora dla text-embedding-3-large

openai = OpenAI(api_key=OPENAI_API_KEY)
qdrant = QdrantClient(QDRANT_URL, api_key=QDRANT_API_KEY, check_compatibility=False)

# Test połączenia z Qdrant i utworzenie kolekcji jeśli nie istnieje
try:
    collections = qdrant.get_collections()
    collection_names = [collection.name for collection in collections.collections]
    
    if COLLECTION_NAME not in collection_names:
        print(f"📦 Tworzenie kolekcji {COLLECTION_NAME}...")
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
        )
        print(f"✅ Kolekcja {COLLECTION_NAME} została utworzona")
    else:
        print(f"✅ Kolekcja {COLLECTION_NAME} już istnieje")
except Exception as e:
    print(f"❌ Błąd połączenia z Qdrant: {str(e)}")
    exit(1)

# === POMOCNICZE FUNKCJE ===
def split_text(text, max_tokens=CHUNK_SIZE):
    tokenizer = tiktoken.encoding_for_model("gpt-4")
    tokens = tokenizer.encode(text)
    chunks = [tokens[i:i+max_tokens] for i in range(0, len(tokens), max_tokens)]
    return [tokenizer.decode(chunk) for chunk in chunks]

def embed_text(texts: list[str]) -> list[list[float]]:
    response = openai.embeddings.create(
        input=texts,
        model=EMBEDDING_MODEL
    )
    return [e.embedding for e in response.data]

def extract_date_from_filename(filename: str) -> str:
    # Extract date from filename (formats: YYYY-MM-DD or YYYY_MM_DD)
    date_pattern = r'(\d{4})[-_](\d{2})[-_](\d{2})'
    match = re.search(date_pattern, filename)
    if match:
        year, month, day = match.groups()
        return f"{year}-{month}-{day}"
    return None

def search_reports(question: str, limit: int = 1):
    # Generowanie embeddingu dla pytania
    question_embedding = embed_text([question])[0]
    
    # Wyszukiwanie w bazie
    search_result = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query_vector=question_embedding,
        limit=limit
    )
    
    # Wyświetlanie wyników
    for result in search_result:
        print(f"\n📅 Data raportu: {result.payload['date']}")
        print(f"📄 Plik: {result.payload['filename']}")
        print(f"📝 Fragment tekstu: {result.payload['text']}")
        print(f"🎯 Dopasowanie: {result.score:.2%}")

def check_file_exists_in_collection(filename: str) -> bool:
    """Sprawdza czy plik już istnieje w kolekcji"""
    search_result = qdrant.scroll(
        collection_name=COLLECTION_NAME,
        query_filter={"must": [{"key": "filename", "match": {"value": filename}}]},
        limit=1
    )
    return len(search_result[0]) > 0

def send_answer(date: str):
    """Wysyła odpowiedź do API"""
    url = "https://centrala.ag3nts.org/reportFormat"
    payload = {
        "task": "wektory",
        "apikey": AIDEVS_API_KEY,
        "answer": date
    }
    
    response = requests.post(url, json=payload)
    print(f"\n📤 Odpowiedź z API: {response.text}")
    return response.json()

# === WCZYTYWANIE I PRZETWARZANIE ===
def process_and_upload_reports(path="./reports/"):
    files = glob.glob(os.path.join(path, "*.md")) + glob.glob(os.path.join(path, "*.txt"))
    for file_path in files:
        filename = os.path.basename(file_path)
        
        # Sprawdź czy plik już istnieje w kolekcji
        if check_file_exists_in_collection(filename):
            print(f"⏭️  Pomijam {filename} - już istnieje w kolekcji")
            continue
            
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
            
        date = extract_date_from_filename(filename)
        if not date:
            print(f"⚠️ Nie znaleziono daty w nazwie pliku: {filename}")
            continue
            
        chunks = split_text(content)
        print(f"📄 Przetwarzanie: {filename} → {len(chunks)} fragmentów")
        embeddings = embed_text(chunks)

        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vec,
                payload={
                    "filename": filename,
                    "date": date,
                    "chunk": i,
                    "text": chunk
                }
            )
            for i, (chunk, vec) in enumerate(zip(chunks, embeddings))
        ]

        qdrant.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
        print(f"✅ Załadowano do Qdrant: {filename}")

# === URUCHOM ===
if __name__ == "__main__":
    # Sprawdź czy kolekcja ma jakieś dane
    collection_info = qdrant.get_collection(COLLECTION_NAME)
    points_count = collection_info.points_count
    
    if points_count > 0:
        print(f"📊 Kolekcja {COLLECTION_NAME} zawiera {points_count} punktów")
        question = "W raporcie, z którego dnia znajduje się wzmianka o kradzieży prototypu broni?"
        print(f"\n❓ Pytanie: {question}")
        
        # Wyszukaj odpowiedź i wyślij datę do API
        search_result = qdrant.query_points(
            collection_name=COLLECTION_NAME,
            query=embed_text([question])[0],
            limit=1
        )
        
        if search_result.points:
            best_match = search_result.points[0]
            print(f"\n📅 Data raportu: {best_match.payload['date']}")
            print(f"📄 Plik: {best_match.payload['filename']}")
            print(f"📝 Fragment tekstu: {best_match.payload['text']}")
            print(f"🎯 Dopasowanie: {best_match.score:.2%}")
            
            # Wyślij odpowiedź do API
            send_answer(best_match.payload['date'])
        else:
            print("❌ Nie znaleziono odpowiedzi")
    else:
        print("📥 Kolekcja jest pusta, rozpoczynam indeksowanie plików...")
        process_and_upload_reports()



