import base64

def xor_decrypt_base64_string(base64_encoded: str, key: str) -> str:
    """
    1. Dekoduje ciąg zakodowany Base64 do bajtów.
    2. XORuje każdy bajt z kluczem (cyklicznie).
    3. Zwraca odszyfrowany tekst jako string.
    """
    try:
        # Krok 1: Dekoduj Base64 do bajtów
        data = base64.b64decode(base64_encoded)

        # Krok 2: XOR z kluczem
        decrypted = ''.join(
            chr(byte ^ ord(key[i % len(key)])) for i, byte in enumerate(data)
        )

        return decrypted
    except Exception as e:
        return f"Error during decryption: {e}"

# 🔐 Zaszyfrowany tekst (bez spacji)
ciphertext = "GhUiPj1fKTM3NCY1KSUmNxkP"
key = "Andrzej"

# 🔓 Odszyfrowanie
plaintext = xor_decrypt_base64_string(ciphertext, key)
print("Odszyfrowana wiadomość:", plaintext)
