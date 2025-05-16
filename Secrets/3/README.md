## 🏠 Dom Zygfryda – AI_devs 3

Zadanie / Task from: **AI_devs 3**

---

### 🇵🇱 Opis zadania (PL)

W tym zadaniu należało połączyć się z przypisanym serwerem zdalnym (SSH), zalogować jako agent i odnaleźć **ukrytą flagę**. Flaga była zaszyta w jednym z katalogów serwera, a podpowiedź brzmiała: _"Flaga znajduje się w domu Zygfryda."_

#### 🎯 Cel

Sprawdzenie umiejętności poruszania się po zdalnym systemie Linux, wykorzystania uprawnień oraz rozwiązywania zagadek logiczno-programistycznych z ograniczonym dostępem.

#### 🧠 Analiza

- Po połączeniu z serwerem agent otrzymywał indywidualny port aplikacji.
- Główna wskazówka sugerowała, że "dom Zygfryda" to **`/home/zygfryd`**.
- Użytkownik `agentXXXX` nie miał uprawnień do bezpośredniego przeglądania katalogu `/home`.

#### 🔍 Strategia

1. Zidentyfikowanie domniemanego folderu zygfryda:
   ```bash
   ls -ld /home/*
   ```
2. Próba odczytu zawartości:
   ```bash
   find /home/zygfryd -type f -exec grep "{{FLG:" {} \; 2>/dev/null
   ```
   lub
   ```bash
   find /home/zygfryd -type f -exec strings {} \; 2>/dev/null | grep "{{FLG:"
   ```

3. Ostatecznie udało się odnaleźć flagę o wzorze `{{FLG:...}}` w pliku zlokalizowanym w katalogu `/home/zygfryd`.

#### 🧩 Wyzwania

- Brak dostępu do katalogów innych użytkowników.
- Flaga nie była możliwa do wykrycia prostym `grep -r`, bo ukryta była w nieprzeglądanym domyślnie folderze.
- Konieczność obchodzenia ograniczeń uprawnień poprzez szukanie plików z globalnym dostępem do odczytu.

#### 🏁 Efekt

Odnalezienie flagi zakończyło zadanie sukcesem 🎉

---

### 🇬🇧 Task Description (EN)

In this task, the goal was to connect to a remote SSH server as an assigned agent and **find a hidden flag**. A clue was given: _"The flag is in Zygfryd’s home."_

#### 🎯 Objective

To test the ability to explore a Linux system remotely with limited permissions and use logic to locate a hidden flag.

#### 🧠 Analysis

- Each participant logged into a personal SSH session.
- The clue indicated that the flag was located in `/home/zygfryd`.
- Direct access to `/home` or `/home/zygfryd` was restricted by default.

#### 🔍 Strategy

1. Listing available home directories:
   ```bash
   ls -ld /home/*
   ```

2. Searching for the flag in readable files:
   ```bash
   find /home/zygfryd -type f -exec grep "{{FLG:" {} \; 2>/dev/null
   ```

   or using `strings`:
   ```bash
   find /home/zygfryd -type f -exec strings {} \; 2>/dev/null | grep "{{FLG:"
   ```

3. The flag was eventually found inside a readable file under `/home/zygfryd`.

#### 🧩 Challenges

- No permission to list directories directly.
- Flag not visible through naive search (`grep -r`).
- Required reasoning and use of system-level commands to bypass access limits indirectly.

#### 🏁 Outcome

Successfully retrieved the hidden flag 🎉