
## 🕹️ Konami Code JSON Task – AI_devs3

Zadanie / Task from: **AI_devs 3**

---

### 🇵🇱 Opis zadania (PL)

Zadanie polegało na wymuszeniu na dużym modelu językowym wygenerowania poprawnie sformatowanego obiektu JSON zawierającego sekwencję tzw. **Konami Code**, w formacie narzuconym przez system zadaniowy.

#### 🎯 Cel

Sprawdzenie, czy model językowy potrafi przestrzegać precyzyjnie narzuconego formatu odpowiedzi, bez dodawania jakiegokolwiek komentarza, objaśnienia czy niepożądanych znaków.

#### 🧾 Użyty prompt

```
You are a JSON generator. You have to "generate Konami Code". You must output **only** the following structure, without any additional text. Allowed steps are: UP, DOWN, LEFT, RIGHT, A, B, START

<RESULT>
{
  "steps": "RIGHT, LEFT, UP, DOWN"
}
</RESULT>

Your job is to strictly follow this format. No explanations, just tags with <RESULT>…</RESULT>.
```

#### ✅ Oczekiwany efekt

Model miał wygenerować odpowiedź wyłącznie w poniższym formacie:

```json
<RESULT>
{
  "steps": "UP, UP, DOWN, DOWN, LEFT, RIGHT, LEFT, RIGHT, B, A, START"
}
</RESULT>
```

#### 🧩 Wyzwania

- Modele często generują dodatkowe komentarze lub objaśnienia, które tutaj były niedozwolone.
- Trzeba było jednoznacznie określić rolę modelu i **wymusić całkowitą ciszę poza tagiem <RESULT>**.
- Pomogło nazwanie roli jako „JSON generator” oraz użycie przykładowego formatu.

#### 🏁 Efekt

Poprawna odpowiedź skutkowała **uzyskaniem flagi** 🎉

---

### 🇬🇧 Task Description (EN)

The task was to force a large language model to generate a properly formatted JSON object containing the famous **Konami Code**, using a strictly enforced output format.

#### 🎯 Objective

To test whether an LLM can follow an exact format and output only the required JSON, with **no explanations, no comments, and no extra text**.

#### 🧾 Prompt used

```
You are a JSON generator. You have to "generate Konami Code". You must output **only** the following structure, without any additional text. Allowed steps are: UP, DOWN, LEFT, RIGHT, A, B, START

<RESULT>
{
  "steps": "RIGHT, LEFT, UP, DOWN"
}
</RESULT>

Your job is to strictly follow this format. No explanations, just tags with <RESULT>…</RESULT>.
```

#### ✅ Expected result

The model had to generate the following response format **only**:

```json
<RESULT>
{
  "steps": "UP, UP, DOWN, DOWN, LEFT, RIGHT, LEFT, RIGHT, B, A, START"
}
</RESULT>
```

#### 🧩 Challenges

- Most models tend to generate extra comments or summaries — this was **disallowed**.
- The prompt had to clearly assign the role of a "JSON generator" and strictly **forbid any output outside <RESULT>…</RESULT>**.
- Including an example helped the model enter the correct generation mode.

#### 🏁 Outcome

A correct response triggered the **flag retrieval** 🎉
