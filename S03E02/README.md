# S03E02 — Semantic Search with Qdrant

## 🇬🇧 Task Name  
**Indexing and Semantic Retrieval of Weapon Reports**

## Description  
The goal was to create a semantic search engine that indexes weapon test reports and allows querying them by meaning. The user was expected to identify the report mentioning the theft of a weapon prototype and return the correct report date via API.

## My Approach  
1. I configured a local script using `OpenAI` for embeddings and `Qdrant Cloud` as the vector database.
2. I parsed each `.txt` or `.md` report file from the `/reports` directory and extracted the date from the filename (e.g. `2024-02-21_XR-5_report.txt` → `2024-02-21`).
3. I split the report content into 500-token chunks and embedded each chunk using `text-embedding-3-large`.
4. Each embedded chunk was saved to the Qdrant collection `reports`, with metadata including `date`, `filename`, `chunk`, and `text`.
5. To answer the question: *"Which report mentions the theft of a weapon prototype?"*, I embedded the query and searched Qdrant for the most similar entry (limit=1).
6. I submitted the date of the best-matching report to the AIDevs API.

## Challenges  
- Matching file naming patterns and extracting valid ISO dates.
- Avoiding redundant uploads: I implemented a check to prevent duplicate files from being indexed.
- Ensuring Qdrant collection existence and compatibility.
- Handling Qdrant Cloud API authentication (`api-key` header instead of localhost).

## Tools and Libraries  
- Python 3  
- `openai` – embedding generation  
- `qdrant-client` – vector database interface  
- `tiktoken` – token counting  
- `uuid`, `dotenv`, `glob`, `requests`, `re`

## What I Learned  
This task solidified my understanding of:
- Working with vector databases (Qdrant)
- Efficient document chunking and metadata handling
- Embedding semantic queries and scoring results
- Using AI to build practical search tools with real business use cases

---

## 🇵🇱 Nazwa zadania  
**Indeksowanie i wyszukiwanie semantyczne raportów o broni**

## Opis  
Celem było stworzenie silnika wyszukiwania semantycznego, który indeksuje raporty testowe broni i pozwala je przeszukiwać na podstawie znaczenia. Należało odnaleźć raport zawierający wzmiankę o kradzieży prototypu broni i przesłać jego datę do API.

## Moje podejście  
1. Skonfigurowałem skrypt lokalny używając `OpenAI` do generowania embeddingów oraz `Qdrant Cloud` jako bazy wektorowej.
2. Dla każdego pliku `.txt` lub `.md` w folderze `/reports` odczytałem nazwę i wydobyłem datę (np. `2024-02-21_XR-5_report.txt` → `2024-02-21`).
3. Treść raportu została podzielona na fragmenty po 500 tokenów i każdy z nich został embedowany za pomocą `text-embedding-3-large`.
4. Każdy fragment został zapisany w kolekcji `reports` w Qdrant, z metadanymi takimi jak `date`, `filename`, `chunk` i `text`.
5. Aby odpowiedzieć na pytanie: *"W raporcie, z którego dnia znajduje się wzmianka o kradzieży prototypu broni?"*, embedowałem pytanie i przeszukałem bazę (limit=1).
6. Najtrafniejszy wynik został przesłany do API AIDevs jako odpowiedź.

## Problemy i wyzwania  
- Wydobycie poprawnej daty z nazw plików (różne formaty).
- Ochrona przed duplikacją danych w Qdrant – dodałem warunek sprawdzający, czy plik już istnieje.
- Obsługa autoryzacji i łączenia z Qdrant Cloud (nagłówek `api-key` zamiast `localhost`).
- Zachowanie zgodności wymiaru embeddingu z konfiguracją kolekcji (3072 dla `text-embedding-3-large`).

## Użyte biblioteki  
- Python 3  
- `openai` – generowanie embeddingów  
- `qdrant-client` – integracja z bazą wektorową  
- `tiktoken` – tokenizacja  
- `uuid`, `dotenv`, `glob`, `requests`, `re`

## Czego się nauczyłem  
To zadanie utrwaliło moją wiedzę na temat:
- Pracy z wektorową bazą danych Qdrant
- Segmentacji dokumentów i obsługi metadanych
- Praktycznego zastosowania embeddingów do semantycznego wyszukiwania
- Wdrażania rozwiązania AI opartego o rzeczywiste potrzeby biznesowe
