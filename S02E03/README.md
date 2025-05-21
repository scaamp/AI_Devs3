# S02E03

## 🇬🇧 Task Name  
**Robot Visualizer via GPT-4 and DALL·E**

## Description  
The goal of this task was to generate an image of a robot based on a technical JSON description fetched from a public API. The robot description was often vague or too raw for direct image generation. Therefore, a GPT-4 model was used to transform it into a vivid, visually-detailed English description, which was then sent to DALL·E 3 to generate the final image. The generated image URL was submitted as the final answer.

## My Approach  
1. Loaded `OPENAI_API_KEY` and `AIDEVS_KEY` from a `.env` file.
2. Downloaded the original robot description from `https://c3ntrala.ag3nts.org/data/{AIDEVS_KEY}/robotid.json`.
3. Sent the raw description to GPT-4 with a carefully designed system prompt, requesting a visually clear, English-only version.
4. Sent the output to OpenAI's DALL·E 3 API to generate an image based on the transformed prompt.
5. Posted the image URL to the `/report` endpoint to complete the task.

## Challenges  
- The original robot description was sometimes inconsistent or sparse — hence the GPT-4 transformation was crucial.
- Ensured that the GPT output strictly followed an image-friendly structure (avoiding behavioral descriptions).
- Managed token limits and API structure between `chat/completions` and `images/generations`.

## Tools and Libraries  
- Node.js  
- `dotenv` – environment variable loading  
- `axios` – HTTP client  
- OpenAI API – GPT-4 + DALL·E 3  

## What I Learned  
This task improved my ability to orchestrate multiple AI services into one pipeline. I practiced prompt design, chaining GPT and DALL·E APIs, and handling image generation requests with precision. I also refined techniques for JSON-to-natural-language transformation using GPT-4 in real-world use cases.

---

## 🇵🇱 Nazwa zadania  
**Wizualizacja robota przez GPT-4 i DALL·E**

## Opis  
Celem było wygenerowanie obrazu robota na podstawie opisu pobranego z API. Opis ten był często chaotyczny i niejasny, dlatego musiał zostać przekształcony na dokładny opis wizualny. Użyliśmy GPT-4 do konwersji opisu na angielski prompt przyjazny dla DALL·E 3, który wygenerował finalny obrazek. Następnie przesłaliśmy URL obrazka jako odpowiedź.

## Moje podejście  
1. Załadowałem klucze z pliku `.env`.
2. Pobrałem dane robota z API `robotid.json`.
3. Wysłałem opis do GPT-4 z promptem proszącym o jego wizualne przekształcenie.
4. Wygenerowałem obraz przez DALL·E 3 na podstawie nowego promptu.
5. Przesłałem wygenerowany URL jako odpowiedź końcową.

## Problemy i wyzwania  
- Surowe opisy robotów były niedokładne, więc przekształcenie ich było kluczowe.
- Trzeba było dopilnować, aby odpowiedź GPT nie zawierała funkcjonalnych opisów, a tylko cechy fizyczne.
- Obsługa błędów między różnymi API (GPT-4 i DALL·E) wymagała uważności.

## Użyte biblioteki i narzędzia  
- Node.js  
- `dotenv` – zmienne środowiskowe  
- `axios` – obsługa HTTP  
- OpenAI API – GPT-4 + DALL·E 3  

## Czego się nauczyłem  
Zadanie pozwoliło mi lepiej zrozumieć jak łączyć różne modele AI w jeden spójny pipeline. Przećwiczyłem projektowanie promptów, łączenie GPT-4 z DALL·E oraz przekształcanie danych technicznych w naturalny język opisowy.

