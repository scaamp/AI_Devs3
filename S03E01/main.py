import tkinter as tk
from tkinter import filedialog
import os
import json
from typing import Dict, List, Set
import openai
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Configure OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")
aidevs_key = os.getenv("AIDEVS_KEY")

def wybierz_pliki_faktow() -> Dict[str, str]:
    """
    Wybiera pliki TXT z faktami i zwraca słownik {nazwa_pliku: zawartość}
    """
    root = tk.Tk()
    root.withdraw()
    pliki = filedialog.askopenfilenames(
        title="Wybierz pliki .txt z faktami",
        filetypes=[("Pliki tekstowe", "*.txt")]
    )
    zawartosci = {}
    for sciezka in pliki:
        with open(sciezka, 'r', encoding='utf-8') as f:
            zawartosc = f.read()
            nazwa = os.path.basename(sciezka)
            zawartosci[nazwa] = zawartosc
    return zawartosci

def wczytaj_fakty_z_pliku(nazwa_pliku: str = "przetworzone_fakty.json") -> Dict[str, Dict]:
    """
    Wczytuje przetworzone fakty z pliku JSON.
    """
    try:
        with open(nazwa_pliku, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"Błąd podczas wczytywania pliku {nazwa_pliku}: {str(e)}")
        return {}

def przetworz_fakty(pliki_faktow: Dict[str, str]) -> Dict[str, Dict]:
    """
    Przetwarza pliki z faktami i tworzy słownik z informacjami o osobach i ich atrybutach.
    """
    # Najpierw sprawdź czy istnieje plik z przetworzonymi faktami
    fakty = wczytaj_fakty_z_pliku()
    
    # Znajdź pliki, które nie zostały jeszcze przetworzone
    nieprzetworzone_pliki = {
        nazwa: tresc for nazwa, tresc in pliki_faktow.items() 
        if nazwa not in fakty
    }
    
    if not nieprzetworzone_pliki:
        print("Wszystkie pliki zostały już przetworzone wcześniej.")
        return fakty
    
    print(f"Przetwarzanie {len(nieprzetworzone_pliki)} nowych plików...")
    
    for nazwa_pliku, tresc in nieprzetworzone_pliki.items():
        # Przygotuj prompt dla GPT-4
        prompt = f"""
        Przeanalizuj poniższy tekst z faktami i wyodrębnij kluczowe informacje w formacie JSON:
        - osoby (imiona i nazwiska)
        - ich zawody
        - specjalne umiejętności
        - inne istotne atrybuty

        Pamiętaj o zasadach:
        - Słowa kluczowe muszą być w języku polskim
        - Słowa kluczowe muszą być krótkie, zwięzłe i konkretne
        - W mianowniku
        - Oddzielone przecinkami bez spacji
        - Jeżeli imie i nazwisko nie jest znane, nie dodawaj takiego rekordu do faktów
        
        Tekst do analizy:
        {tresc}

        Zwróć wynik w formacie JSON z następującą strukturą:
        {{
            "osoby": [
                {{
                    "imie_nazwisko": "string",
                    "slowa_kluczowe": "string"
                }}
            ],
            "sektory": [
                {{
                    "nazwa": "string",
                    "slowa_kluczowe": "string"
                }}
            ]
        }}

        WAŻNE: Odpowiedź musi być poprawnym JSON-em, bez żadnego dodatkowego tekstu przed lub po JSON-ie.
        """
        
        try:
            response = openai.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": tresc}
                ],
                temperature=0.3
            )
            
            # Pobierz odpowiedź i usuń ewentualne białe znaki
            odpowiedz = response.choices[0].message.content.strip()
            
            try:
                # Parsuj odpowiedź JSON
                wynik = json.loads(odpowiedz)
                fakty[nazwa_pliku] = wynik
            except json.JSONDecodeError as je:
                print(f"Błąd parsowania JSON dla pliku {nazwa_pliku}: {str(je)}")
                print(f"Otrzymana odpowiedź: {odpowiedz}")
                fakty[nazwa_pliku] = {"error": "Nieprawidłowy format JSON", "raw_response": odpowiedz}
            
        except Exception as e:
            print(f"Błąd podczas przetwarzania pliku {nazwa_pliku}: {str(e)}")
            fakty[nazwa_pliku] = {"error": str(e)}
    
    # Zapisz zaktualizowane fakty do pliku
    zapisz_fakty_do_pliku(fakty)
    return fakty

def przetworz_raport(nazwa_pliku: str, tresc: str, fakty: Dict[str, Dict]) -> Dict:
    """
    Przetwarza pojedynczy raport, uwzględniając powiązane fakty.
    """
    # Pierwszy request - analiza raportu i wyciągnięcie osób i sektorów
    prompt_analiza = f"""
    Przeanalizuj poniższy raport i wyodrębnij:
    1. Wszystkie osoby (imiona i nazwiska)
    2. Sektory (na podstawie treści i nazwy pliku)

    Nazwa pliku raportu: {nazwa_pliku}
    Treść raportu:
    {tresc}

    Zwróć wynik w formacie JSON:
    {{
        "osoby": ["string"],
        "sektory": ["string"]
    }}

    WAŻNE: 
    - Odpowiedź musi być poprawnym JSON-em
    - Uwzględnij sektory zarówno z treści jak i z nazwy pliku
    - Osoby powinny być w formacie "Imię Nazwisko"
    """
    
    try:
        # Pierwszy request - analiza raportu
        response_analiza = openai.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "Jesteś asystentem analizującym tekst i wyodrębniającym osoby i sektory. Zawsze zwracaj poprawny JSON."},
                {"role": "user", "content": prompt_analiza}
            ],
            temperature=0.3
        )
        
        # Parsuj wynik pierwszej analizy
        analiza_wynik = json.loads(response_analiza.choices[0].message.content.strip())
        print(analiza_wynik)

        # Wczytaj przekształcone fakty
        try:
            with open("przeksztalcone_fakty.json", 'r', encoding='utf-8') as f:
                przeksztalcone_fakty = json.load(f)
        except FileNotFoundError:
            print("Nie znaleziono pliku przeksztalcone_fakty.json")
            przeksztalcone_fakty = {"osoby": [], "sektory": []}
        except Exception as e:
            print(f"Błąd podczas wczytywania przeksztalcone_fakty.json: {str(e)}")
            przeksztalcone_fakty = {"osoby": [], "sektory": []}

        # Znajdź powiązane dane dla znalezionych osób i sektorów
        powiazane_dane = {
            "osoby": [],
            "sektory": []
        }

        # Znajdź dane dla osób
        for znaleziona_osoba in analiza_wynik["osoby"]:
            for osoba in przeksztalcone_fakty["osoby"]:
                if osoba["imie_nazwisko"].lower() == znaleziona_osoba.lower():
                    powiazane_dane["osoby"].append(osoba)
                    break

        # Znajdź dane dla sektorów
        for znaleziony_sektor in analiza_wynik["sektory"]:
            for sektor in przeksztalcone_fakty["sektory"]:
                if sektor["nazwa"].lower() == znaleziony_sektor.lower():
                    powiazane_dane["sektory"].append(sektor)
                    break
                
        # Drugi request - generowanie słów kluczowych na podstawie analizy i powiązanych faktów
        prompt_slowa_kluczowe = f"""
        Na podstawie poniższych informacji wygeneruj listę słów kluczowych:

        Nazwa pliku: {nazwa_pliku}
        Znalezione osoby: {json.dumps(analiza_wynik['osoby'], ensure_ascii=False)}
        Znalezione sektory: {json.dumps(analiza_wynik['sektory'], ensure_ascii=False)}
        Powiązane dane o osobach: {json.dumps(powiazane_dane['osoby'], ensure_ascii=False, indent=2)}
        Powiązane dane o sektorach: {json.dumps(powiazane_dane['sektory'], ensure_ascii=False, indent=2)}

        Zwróć wynik w formacie JSON:
        {{
            "nazwa_pliku": "{nazwa_pliku}",
            "slowa_kluczowe": "słowo1,słowo2,słowo3,..."
        }}

        Pamiętaj o zasadach:
        - Słowa kluczowe muszą być w języku polskim
        - Słowa kluczowe muszą być krótkie, zwięzłe i konkretne
        - W mianowniku
        - Oddzielone przecinkami bez spacji
        - Uwzględnij imiona i nazwiska jeśli są istotne
        - Uwzględnij słowa kluczowe z powiązanych danych o osobach i sektorach
        """
        
        response_slowa_kluczowe = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Jesteś asystentem generującym słowa kluczowe na podstawie analizy tekstu i powiązanych faktów. Zawsze zwracaj poprawny JSON."},
                {"role": "user", "content": prompt_slowa_kluczowe}
            ],
            temperature=0.3
        )
        
        # Parsuj wynik drugiej analizy
        wynik = json.loads(response_slowa_kluczowe.choices[0].message.content.strip())
        
        print("Ostateczny wynik: ", wynik)
        return wynik
        
    except json.JSONDecodeError as je:
        print(f"Błąd parsowania JSON dla raportu {nazwa_pliku}: {str(je)}")
        return {
            "nazwa_pliku": nazwa_pliku,
            "error": "Nieprawidłowy format JSON",
            "raw_response": str(je)
        }
    except Exception as e:
        print(f"Błąd podczas przetwarzania raportu {nazwa_pliku}: {str(e)}")
        return {
            "nazwa_pliku": nazwa_pliku,
            "error": str(e)
        }

def wybierz_raporty_txt() -> Dict[str, str]:
    """
    Wybiera pliki TXT z raportami i zwraca słownik {nazwa_pliku: zawartość}
    """
    root = tk.Tk()
    root.withdraw()
    pliki = filedialog.askopenfilenames(
        title="Wybierz pliki .txt z raportami",
        filetypes=[("Pliki tekstowe", "*.txt")]
    )
    zawartosci = {}
    for sciezka in pliki:
        with open(sciezka, 'r', encoding='utf-8') as f:
            zawartosc = f.read()
            nazwa = os.path.basename(sciezka)
            zawartosci[nazwa] = zawartosc
    return zawartosci

def zapisz_fakty_do_pliku(fakty: Dict[str, Dict], nazwa_pliku: str = "przetworzone_fakty.json"):
    """
    Zapisuje przetworzone fakty do pliku JSON.
    """
    try:
        with open(nazwa_pliku, 'w', encoding='utf-8') as f:
            json.dump(fakty, f, ensure_ascii=False, indent=2)
        print(f"\nZapisano przetworzone fakty do pliku: {nazwa_pliku}")
    except Exception as e:
        print(f"Błąd podczas zapisywania pliku {nazwa_pliku}: {str(e)}")

def zapisz_wyniki_do_pliku(wyniki: List[Dict], nazwa_pliku: str = "wyniki_analizy.json"):
    """
    Zapisuje wyniki analizy raportów do pliku JSON.
    """
    try:
        with open(nazwa_pliku, 'w', encoding='utf-8') as f:
            json.dump(wyniki, f, ensure_ascii=False, indent=2)
        print(f"\nZapisano wyniki analizy do pliku: {nazwa_pliku}")
    except Exception as e:
        print(f"Błąd podczas zapisywania pliku {nazwa_pliku}: {str(e)}")

def przeksztalc_fakty(fakty: Dict[str, Dict]) -> Dict:
    """
    Przekształca fakty do nowego formatu, łącząc wszystkie osoby i sektory w jedną listę.
    """
    nowy_format = {
        "osoby": [],
        "sektory": []
    }
    
    # Słowniki do śledzenia unikalnych osób i sektorów
    unikalne_osoby = {}  # klucz: imie_nazwisko, wartość: słowa_kluczowe
    unikalne_sektory = {}  # klucz: nazwa, wartość: słowa_kluczowe
    
    # Przetwórz wszystkie fakty
    for plik, dane in fakty.items():
        # Przetwórz osoby
        for osoba in dane.get("osoby", []):
            imie_nazwisko = osoba.get("imie_nazwisko")
            if imie_nazwisko:
                if imie_nazwisko not in unikalne_osoby:
                    unikalne_osoby[imie_nazwisko] = osoba.get("slowa_kluczowe", "")
                else:
                    # Połącz słowa kluczowe jeśli ta sama osoba pojawia się w różnych plikach
                    obecne_slowa = unikalne_osoby[imie_nazwisko]
                    nowe_slowa = osoba.get("slowa_kluczowe", "")
                    if obecne_slowa and nowe_slowa:
                        unikalne_osoby[imie_nazwisko] = f"{obecne_slowa},{nowe_slowa}"
        
        # Przetwórz sektory
        for sektor in dane.get("sektory", []):
            nazwa = sektor.get("nazwa")
            if nazwa:
                if nazwa not in unikalne_sektory:
                    unikalne_sektory[nazwa] = sektor.get("slowa_kluczowe", "")
                else:
                    # Połącz słowa kluczowe jeśli ten sam sektor pojawia się w różnych plikach
                    obecne_slowa = unikalne_sektory[nazwa]
                    nowe_slowa = sektor.get("slowa_kluczowe", "")
                    if obecne_slowa and nowe_slowa:
                        unikalne_sektory[nazwa] = f"{obecne_slowa},{nowe_slowa}"
    
    # Konwertuj słowniki na listy w nowym formacie
    nowy_format["osoby"] = [
        {"imie_nazwisko": imie, "slowa_kluczowe": slowa}
        for imie, slowa in unikalne_osoby.items()
    ]
    
    nowy_format["sektory"] = [
        {"nazwa": nazwa, "slowa_kluczowe": slowa}
        for nazwa, slowa in unikalne_sektory.items()
    ]
    
    return nowy_format

def zapisz_przeksztalcone_fakty(fakty: Dict, nazwa_pliku: str = "przeksztalcone_fakty.json"):
    """
    Zapisuje przekształcone fakty do pliku JSON.
    """
    try:
        with open(nazwa_pliku, 'w', encoding='utf-8') as f:
            json.dump(fakty, f, ensure_ascii=False, indent=2)
        print(f"\nZapisano przekształcone fakty do pliku: {nazwa_pliku}")
    except Exception as e:
        print(f"Błąd podczas zapisywania pliku {nazwa_pliku}: {str(e)}")

def wczytaj_wyniki_analizy(nazwa_pliku: str = "wyniki_analizy.json") -> List[Dict]:
    """
    Wczytuje wyniki analizy z pliku JSON.
    """
    try:
        with open(nazwa_pliku, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Błąd podczas wczytywania pliku {nazwa_pliku}: {str(e)}")
        return []

def wyslij_wyniki_na_endpoint(wyniki: List[Dict]) -> None:
    """
    Wysyła wyniki analizy na endpoint.
    """
    # Przekształć listę wyników do wymaganego formatu
    odpowiedz = {
        "task": "dokumenty",
        "apikey": aidevs_key,
        "answer": {}
    }
    
    for wynik in wyniki:
        if "nazwa_pliku" in wynik and "slowa_kluczowe" in wynik:
            odpowiedz["answer"][wynik["nazwa_pliku"]] = wynik["slowa_kluczowe"]
    
    # Wyślij dane na endpoint
    try:
        response = requests.post("https://centrala.ag3nts.org/report", json=odpowiedz)
        response.raise_for_status()
        print("\nWynik wysłania na endpoint:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except requests.exceptions.RequestException as e:
        print(f"\nBłąd podczas wysyłania na endpoint: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"Odpowiedź serwera: {e.response.text}")

def main():
    # Sprawdź czy istnieją już wyniki analizy
    wyniki = wczytaj_wyniki_analizy()
    if wyniki:
        print("\nZnaleziono istniejące wyniki analizy.")
        print(f"Liczba przetworzonych raportów: {len(wyniki)}")
        # Wyślij istniejące wyniki na endpoint
        wyslij_wyniki_na_endpoint(wyniki)
        return
    
    # Wybierz pliki z faktami
    print("Wybierz pliki z faktami...")
    pliki_faktow = wybierz_pliki_faktow()
    if not pliki_faktow:
        print("Nie wybrano żadnych plików z faktami!")
        return

    # Przetwórz fakty (lub wczytaj z pliku jeśli istnieją)
    print("Sprawdzanie i przetwarzanie faktów...")
    fakty = przetworz_fakty(pliki_faktow)
    print(f"Łącznie dostępnych {len(fakty)} przetworzonych plików z faktami.")
    
    # Przekształć fakty do nowego formatu
    print("\nPrzekształcanie faktów do nowego formatu...")
    przeksztalcone_fakty = przeksztalc_fakty(fakty)
    
    # Zapisz przekształcone fakty
    zapisz_przeksztalcone_fakty(przeksztalcone_fakty)

    # Wybierz i przetwórz raporty
    print("\nWybierz pliki z raportami...")
    raporty = wybierz_raporty_txt()
    if not raporty:
        print("Nie wybrano żadnych raportów!")
        return
        
    # Przetwórz każdy raport osobno
    wyniki = []
    for nazwa, tresc in raporty.items():
        print(f"\nPrzetwarzanie raportu: {nazwa}")
        wynik = przetworz_raport(nazwa, tresc, fakty)
        wyniki.append(wynik)
        print(f"Wynik: {json.dumps(wynik, indent=2, ensure_ascii=False)}")
        
    # Zapisz wyniki do pliku    
    zapisz_wyniki_do_pliku(wyniki)
    
    # Wyślij wyniki na endpoint
    wyslij_wyniki_na_endpoint(wyniki)

if __name__ == "__main__":
    main()
