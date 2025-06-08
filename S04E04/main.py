from dotenv import load_dotenv
import os
import requests
import openai
from flask import Flask, request, jsonify
import re
import json

app = Flask(__name__)

load_dotenv()
AIDEVS_KEY = os.getenv("AIDEVS_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Map description - 4x4 grid, starting from top-left (0,0)
MAP = {
    (0,0): "punkt startowy",  # Location marker
    (0,1): "trawa",           # Grass
    (0,2): "drzewo",          # Tree
    (0,3): "dom",             # House
    (1,0): "trawa",           # Grass
    (1,1): "wiatrak",         # Windmill
    (1,2): "trawa",           # Grass
    (1,3): "trawa",           # Grass
    (2,0): "trawa",           # Grass
    (2,1): "trawa",           # Grass
    (2,2): "skały",           # Rocks
    (2,3): "drzewa",          # Trees
    (3,0): "góry",            # Mountains
    (3,1): "góry",            # Mountains
    (3,2): "samochód",        # Car
    (3,3): "Jaskinia"         # Cave
}

def parse_instruction(instruction):
    """Parse natural language instruction using GPT-4 to determine movement"""
    
    # Initialize OpenAI client
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    system_prompt = """Jesteś analizatorem instrukcji nawigacyjnych dla drona na mapie 4x4.

    Dron zawsze startuje z pozycji (0,0) w lewym górnym rogu mapy.
    Mapa ma wymiary 4x4 (wiersze 0-3, kolumny 0-3).

    Kierunki:
    - "prawo" = zwiększ kolumnę (+y) 
    - "lewo" = zmniejsz kolumnę (-y)
    - "dół" = zwiększ wiersz (+x)
    - "góra"/"w górę" = zmniejsz wiersz (-x)

    Przeanalizuj instrukcję i zwróć JSON z liczbą kroków w każdym kierunku:
    {
    "right": liczba_kroków_w_prawo,
    "left": liczba_kroków_w_lewo, 
    "down": liczba_kroków_w_dół,
    "up": liczba_kroków_w_górę
    }

    Przykłady:
    - "poleciałem jedno pole w prawo" -> {"right": 1, "left": 0, "down": 0, "up": 0}
    - "2 pola w dół, 1 pole w lewo" -> {"right": 0, "left": 1, "down": 2, "up": 0}
    - "na sam dół" -> {"right": 0, "left": 0, "down": 3, "up": 0}
    - "skrajnie na prawo" -> {"right": 3, "left": 0, "down": 0, "up": 0}

    Uwagi:
    - Słowa liczbowe: jedno/jeden=1, dwa=2, trzy=3, cztery=4
    - Jeśli nie ma wyraźnej liczby, przyjmij 1 krok
    - Zwracaj tylko JSON, bez dodatkowego tekstu"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": instruction}
            ],
            temperature=0,
            max_tokens=150
        )
        
        # Parse the JSON response
        movement_json = response.choices[0].message.content.strip()
        print(f"GPT-4 response: {movement_json}")
        
        movement = json.loads(movement_json)
        
        # Calculate final position
        x = 0 + movement.get('down', 0) - movement.get('up', 0)
        y = 0 + movement.get('right', 0) - movement.get('left', 0)
        
        # Clamp to map boundaries (0-3 for both x and y)
        x = max(0, min(3, x))
        y = max(0, min(3, y))
        
        print(f"Calculated position: ({x}, {y})")
        return x, y
        
    except Exception as e:
        print(f"Error parsing instruction with GPT-4: {e}")
        # Fallback to starting position
        return 0, 0

@app.route('/drone', methods=['POST'])
def drone_navigation():
    try:
        # Get instruction from request
        data = request.get_json()
        
        if not data or 'instruction' not in data:
            return jsonify({"description": "błąd"}), 400
        
        instruction = data['instruction']
        
        # Log the instruction for debugging
        print(f"Received instruction: {instruction}")
        
        # Parse instruction to get final position
        x, y = parse_instruction(instruction)
        
        print(f"Final position: ({x}, {y})")
        
        # Get description for this position
        description = MAP.get((x, y), "nieznane")
        
        print(f"Description: {description}")
        
        # Return response
        response = {"description": description}
        return jsonify(response), 200
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"description": "błąd"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    print("Starting drone navigation API with GPT-4 instruction parsing...")
    
    # Check if OpenAI API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  Warning: OPENAI_API_KEY environment variable is not set!")
        print("   Set it with: export OPENAI_API_KEY='your-api-key'")
    
    print("Map layout:")
    for i in range(4):
        row = []
        for j in range(4):
            row.append(f"({i},{j}):{MAP[(i,j)]}")
        print(" | ".join(row))
    
    app.run(host='0.0.0.0', port=54236, debug=True)




