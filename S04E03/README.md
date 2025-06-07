# S04E03

## 🇬🇧 Task Name
Autonomous Website Navigation – SoftoAI

## Task Summary
The goal of the task was to answer 3 questions about the SoftoAI company by visiting their website. Each answer had to be retrieved programmatically by recursively exploring the website and selecting the correct pages. The logic had to avoid traps like infinite loops or misleading links.

## 🔍 My Approach
1. Downloaded the 3 questions from the central API.
2. Built a recursive search mechanism in Python to explore the SoftoAI website.
3. Used BeautifulSoup to extract text and links from each page.
4. Passed page content and available links to GPT-4 to:
   - Check if the answer was on the current page.
   - Suggest the most relevant link if not.
5. Resolved relative/absolute links and prevented revisiting pages.
6. Collected all answers and submitted them to `/report`.

## ⚠️ Challenges
- GPT sometimes returned malformed JSON or ambiguous answers.
- Some links led to misleading or looping pages.
- Had to handle various edge cases (e.g., fallback if GPT returned `none`, duplicate links).

## 🧰 Tools & Libraries
- Python 3.11  
- `requests` – HTTP requests  
- `beautifulsoup4` – HTML parsing  
- `openai` – GPT-4 integration  
- `dotenv` – environment variable handling  
- `urllib.parse.urljoin` – safe link resolution

## 🎓 What I Learned
- How to safely explore websites programmatically with a language model as a decision-maker.
- Techniques for avoiding infinite loops and bad link traversal.
- How to integrate GPT-4 for intelligent page crawling.
- JSON parsing, fallback handling, and recursive page exploration with memory.

---

## 🇵🇱 Nazwa zadania
Autonomiczna nawigacja po stronie – SoftoAI

## Opis zadania
Celem było odpowiedzenie na 3 pytania dotyczące firmy SoftoAI. Odpowiedzi należało znaleźć na stronie internetowej firmy, eksplorując ją automatycznie. Trzeba było unikać pułapek, zapętleń i błędnych stron – system miał działać samodzielnie i skutecznie.

## 🔍 Moje podejście
1. Pobrałem pytania z API centrali.
2. Zbudowałem rekurencyjny mechanizm do przeszukiwania strony.
3. Za pomocą BeautifulSoup analizowałem tekst i linki na każdej podstronie.
4. Wysyłałem treść strony i linki do GPT-4, który:
   - Wskazywał odpowiedź, jeśli znajdowała się na stronie,
   - Albo wybierał kolejny najlepszy link.
5. Rozwiązywałem ścieżki linków (relatywne i absolutne) i unikałem powtórzeń.
6. Zebrałem wszystkie odpowiedzi i wysłałem je do `/report`.

## ⚠️ Problemy i wyzwania
- GPT czasem zwracał niepoprawny JSON lub niejednoznaczne odpowiedzi.
- Niektóre linki prowadziły do zapętleń lub były mylące.
- Musiałem obsłużyć wiele przypadków brzegowych (np. fallback przy `none`, duplikaty linków).

## 🧰 Użyte biblioteki
- Python 3.11  
- `requests` – obsługa zapytań HTTP  
- `beautifulsoup4` – parsowanie HTML  
- `openai` – integracja z GPT-4  
- `dotenv` – obsługa zmiennych środowiskowych  
- `urllib.parse.urljoin` – bezpieczne przetwarzanie ścieżek

## 🎓 Czego się nauczyłem
- Jak bezpiecznie eksplorować strony internetowe z użyciem LLM jako nawigatora.
- Techniki unikania zapętleń i błędnych linków.
- Jak używać GPT-4 do inteligentnego sterowania przeglądaniem stron.
- Parsowanie JSON, fallbacki i rekurencyjna eksploracja stron z pamięcią.

