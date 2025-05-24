# Sekretna Flaga – XOR z Andrzejem

## 🇬🇧 Task Name  
**Decrypting the Secret Flag using XOR and the Key "Andrzej"**

## Description  
A hidden message was embedded as a base64-encoded string:  
`GhUiPj1fKTM3NCY1KSUmNxkP`  

A note found in the task ("Klucz do wszystkiego") suggested that the key to uncovering the mystery is **Andrzej**. Based on that, I assumed the encrypted string was XORed with the word `"Andrzej"` and encoded with Base64.

## My Approach  
1. I removed whitespace and decoded the string from Base64 to raw bytes.
2. I XORed each byte with the corresponding character of `"Andrzej"` (repeating).
3. The decrypted result was the flag

## Tools Used  
- Python 3.11  
- `base64` module  
- Custom XOR decryption function

## What I Learned  
This was a logic-based steganography challenge where narrative clues guided toward the correct decryption method. It combined cryptography, string manipulation, and story-based reasoning.

---

## 🇵🇱 Nazwa zadania  
**Odszyfrowanie sekretnej flagi przy pomocy XOR i klucza "Andrzej"**

## Opis  
Ukryta wiadomość została przedstawiona jako ciąg zakodowany Base64:  
`GhUiPj1fKTM3NCY1KSUmNxkP`  

W notatce zatytułowanej "Klucz do wszystkiego" pojawiła się wskazówka, że to **Andrzej** jest kluczem do rozwiązania. Założyłem, że wiadomość była zakodowana przez XOR z `"Andrzej"` i następnie zakodowana w Base64.

## Moje podejście  
1. Usunąłem spację i zdekodowałem ciąg z Base64 do bajtów.
2. Wykonałem XOR każdego bajtu z odpowiadającym znakiem klucza `"Andrzej"` (cyklicznie).
3. Wynikiem była sekretna flaga!

## Użyte narzędzia  
- Python 3.11  
- Moduł `base64`  
- Własna funkcja do deszyfrowania XOR

## Czego się nauczyłem  
Zadanie pokazało, jak fabularna narracja może prowadzić do logicznej techniki deszyfrowania. Wymagało połączenia storytellingu, podstaw kryptografii i kodowania tekstowego.

---
