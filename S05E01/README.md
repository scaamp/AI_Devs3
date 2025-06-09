# S04E05

## 🇬🇧 Task Name
Notes Analysis System

## Task Summary
The goal of this task was to analyze a cryptic and metaphor-rich notebook written by Rafał. The notebook consisted of text pages (1–18) and a scanned image (page 19). Using OCR and language models, we had to answer 5 questions about the notebook's content. The answers were not always explicit, and the system had to infer them from vague references and context.

## 🔍 My Approach
1. Downloaded the PDF file and extracted text from pages 1–18 using `PyMuPDF`.
2. Processed page 19 (image) by converting it into a high-resolution PNG and sending it to GPT-4V for visual analysis (OCR-like).
3. Combined all extracted content into a single context.
4. Created an iterative loop that:
   - Sends the context to GPT-4.1 for analysis.
   - Submits the result to the API endpoint.
   - On failure, re-prompts GPT with feedback (hints, wrong answers, etc.).
   - Locks correct answers to avoid overwriting them in the next iterations.
5. The process continues until all 5 answers are accepted by the server.

## ⚠️ Challenges
- Answers were often not stated directly — required inference and logic.
- Page 19 required careful OCR processing; text was scattered and slightly distorted.
- Ensuring that correct answers persist across retries without being overridden.

## 🧰 Tools & Libraries
- Python 3.11
- `fitz` (PyMuPDF) – PDF parsing
- `PIL`, `base64` – image processing
- `openai` – GPT-4.1 and GPT-4V integration
- `dotenv` – secret management
- `requests`, `json`

## 🎓 What I Learned
- How to orchestrate iterative question-answer refinement with feedback loop.
- How to stabilize and lock correct LLM answers in multi-step workflows.
- How to leverage GPT-4V for OCR-style extraction from images.
- Importance of context-aware prompting for ambiguous or metaphorical text.

---

## 🇵🇱 Nazwa zadania
System analizy notatnika

## Opis zadania
Zadanie polegało na analizie osobliwego, pełnego metafor notatnika autorstwa Rafała. Notatnik składał się z 18 stron tekstu i jednej strony obrazowej (strona 19). Na podstawie tej zawartości należało odpowiedzieć na 5 pytań. Odpowiedzi często nie były podane wprost – trzeba było je wywnioskować z kontekstu i aluzji.

## 🔍 Moje podejście
1. Pobrałem plik PDF i wyciągnąłem tekst ze stron 1–18 za pomocą biblioteki `PyMuPDF`.
2. Stronę 19 (obraz) przetworzyłem na obraz PNG w wysokiej rozdzielczości i przekazałem do GPT-4V w celu analizy wizualnej (OCR).
3. Połączyłem cały kontekst w jeden tekst.
4. Zbudowałem pętlę iteracyjną, która:
   - Wysyła kontekst do GPT-4.1 celem analizy.
   - Przesyła odpowiedzi do API.
   - W razie niepowodzenia dodaje informację zwrotną (hint, debug) do promptu.
   - Blokuje poprawne odpowiedzi, by nie zostały nadpisane.
5. Pętla kończy się, gdy wszystkie odpowiedzi są zaakceptowane przez centralę.

## ⚠️ Problemy i wyzwania
- Odpowiedzi często nie były dosłowne – wymagały wnioskowania.
- OCR strony 19 był trudny – tekst był fragmentaryczny i zniekształcony.
- Trzeba było dbać, by prawidłowe odpowiedzi nie były przypadkowo zmieniane przez LLM.

## 🧰 Użyte biblioteki
- Python 3.11
- `fitz` (PyMuPDF) – analiza PDF
- `PIL`, `base64` – przetwarzanie obrazów
- `openai` – integracja z GPT-4.1 i GPT-4V
- `dotenv` – zarządzanie danymi poufnymi
- `requests`, `json`

## 🎓 Czego się nauczyłem
- Jak stworzyć system iteracyjnej poprawy odpowiedzi na pytania na podstawie feedbacku.
- Jak utrwalać poprawne odpowiedzi i unikać ich przypadkowego nadpisania.
- Jak wykorzystać GPT-4V do OCR obrazów.
- Jak konstruować prompt do analizy niejednoznacznych i metaforycznych tekstów.
