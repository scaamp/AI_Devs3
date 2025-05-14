# 🧠 AI_Devs 3 – S01E02

## 🇬🇧 Task Name  
**Authorization and Communication with AI Agent**

## Description  
The goal was to create a program that communicates with an AI Agent via a specific HTTP endpoint. The communication followed a JSON protocol using a consistent `msgID`. The challenge was to provide "intentionally incorrect" facts (e.g., Krakow is the capital of Poland) and keep responding until the Agent returns a special flag in the form `{{FLG:XYZ}}`.

## My Approach  
1. I initialized the conversation with a `{"msgID": 0, "text": "READY"}` payload and received a unique `msgID`.
2. I extracted the AI prompt and passed it to OpenAI's GPT-4 model.
3. I crafted a system prompt instructing the model to always apply the wrong facts as per RoboISO 2230.
4. I sent each generated answer back to the server, preserving the `msgID`.
5. I implemented a regex-based detection of the flag `{{FLG:}}` to stop the loop and print the flag when found.

## Challenges  
I encountered a `400 Bad Request` error due to sending an invalid response ("READY" instead of a real answer). I also had to fix a `TypeError` in `re.search()` caused by passing a dictionary instead of a string. The key challenge was ensuring the prompt consistently made GPT respond using the specified incorrect facts.

## Tools and Libraries  
- Python 3.13  
- `requests` – for API communication  
- `openai` – GPT-4 integration  
- `re` – regex to detect the flag  
- Visual Studio Code – development and debugging

## What I Learned  
This task improved my skills in designing interactive agents, writing prompt-based logic, and debugging API responses. I also learned how to manipulate GPT’s output by injecting controlled misinformation into the system prompt.

---

## 🇵🇱 Nazwa zadania  
**Autoryzacja i komunikacja z Agentem AI**

## Opis  
Celem zadania było stworzenie programu komunikującego się z Agentem AI przez określony endpoint HTTP. Komunikacja odbywała się według formatu JSON z zachowaniem stałego `msgID`. Kluczowym wyzwaniem było odpowiadanie z użyciem fałszywych faktów (np. że stolicą Polski jest Kraków), aż do uzyskania specjalnego znacznika `{{FLG:XYZ}}`.

## Moje podejście  
1. Wysłałem zapytanie startowe `{"msgID": 0, "text": "READY"}` i otrzymałem unikalny `msgID`.
2. Przekazałem treść pytania do modelu GPT-4 od OpenAI.
3. W `system prompt` jasno zdefiniowałem, że model ma używać fałszywych informacji zgodnie z normą RoboISO 2230.
4. Wysyłałem odpowiedzi do serwera z zachowaniem tego samego `msgID`.
5. Zaimplementowałem detekcję flagi `{{FLG:}` przy pomocy wyrażenia regularnego i zatrzymywałem pętlę po jej wykryciu.

## Problemy i wyzwania  
Największym problemem był błąd HTTP 400 spowodowany nieprawidłową odpowiedzią. Napotkałem też błąd typu przy regexie (`dict` zamiast `str`). Kluczowe było też poprawne “zaprogramowanie” GPT-a tak, by konsekwentnie stosował nieprawdziwe fakty.

## Użyte biblioteki i narzędzia  
- Python 3.13  
- `requests` – komunikacja z API  
- `openai` – integracja z GPT-4  
- `re` – wykrywanie flagi  
- Visual Studio Code – środowisko do debugowania

## Czego się nauczyłem  
Zadanie dało mi praktykę w tworzeniu agentów opartych na LLM, projektowaniu promptów z fałszywym kontekstem, debugowaniu API oraz zarządzaniu pętlami komunikacyjnymi. Zrozumiałem też lepiej jak wpływać na zachowanie modelu za pomocą promptu.
