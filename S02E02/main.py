import base64
import tkinter as tk
from tkinter import filedialog
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MAP_ANALYSIS_PROMPT = '''Twoim zadaniem jest zidentyfikowanie miasta, z którego pochodzą fragmenty mapy przedstawione na czterech oddzielnych obrazach. Zwróć nazwę miasta jako pojedyncze słowo – nazwę miejscowości, z której pochodzą mapy.

Uwaga: jeden z fragmentów może być błędny i pochodzić z innego miasta – uwzględnij to w analizie.

W swojej analizie:

Wypisz rozpoznane nazwy ulic, charakterystyczne obiekty (np. cmentarze, szkoły, sklepy, itd.) i ważne punkty orientacyjne, które mogą pomóc w identyfikacji lokalizacji.

Zwróć uwagę na układ urbanistyczny (np. ulice prostopadłe, układ dzielnic, tory kolejowe).

Upewnij się, że ulice i obiekty znajdują się rzeczywiście w mieście, które planujesz podać jako końcową odpowiedź.

Jeśli któryś z fragmentów wyraźnie nie pasuje do reszty, zignoruj go przy określaniu miasta, ale wskaż, który to i dlaczego.

Jeśli uznasz, że potrzebna jest dodatkowa weryfikacja, zrób to przed udzieleniem odpowiedzi.

Format odpowiedzi:
{
  "_thinking": [
    "Let me think...",
    "Fragment 1 contains Warszawska street, which is common but prominent in Białystok.",
    "Fragment 2 shows a school named 'Szkoła Podstawowa nr 8' which also appears in Białystok.",
    "Fragment 3 has a river with two bridges — looks like the layout of the Biała river.",
    "Fragment 4 contains street names unrelated to previous ones, possibly a false clue.",
    "Most consistent elements point to Białystok."
  ],
  "city": "Białystok"
}'''

def convert_file_to_base64(file_path):
    with open(file_path, "rb") as f:
        encoded_bytes = base64.b64encode(f.read())
        encoded_str = encoded_bytes.decode("utf-8")
        return encoded_str

def select_files():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_paths = filedialog.askopenfilenames(
        title="Select map images to analyze",
        filetypes=[("Image files", "*.jpg *.jpeg *.png")]
    )
    return file_paths

def analyze_maps_with_gpt4(image_base64_list):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    # Prepare content array with prompt and all images
    content = [{"type": "text", "text": MAP_ANALYSIS_PROMPT}]
    
    # Add each image to the content array
    for base64_image in image_base64_list:
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
        })
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ],
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error during API call: {str(e)}"

if __name__ == "__main__":
    file_paths = select_files()
    
    if file_paths:  # Check if files were selected
        try:
            # Convert all images to base64
            base64_images = []
            for file_path in file_paths:
                base64_output = convert_file_to_base64(file_path)
                base64_images.append(base64_output)
            
            # Save base64 to file for reference
            with open("output_base64.txt", "w") as out_file:
                for i, base64_str in enumerate(base64_images, 1):
                    out_file.write(f"Image {i}:\n{base64_str}\n\n")
            
            print(f"Converted {len(base64_images)} images to Base64 and saved as output_base64.txt")
            
            # Analyze with GPT-4
            print("\nAnalyzing images with GPT-4...")
            analysis_result = analyze_maps_with_gpt4(base64_images)
            
            # Save analysis result
            with open("analysis_result.txt", "w", encoding="utf-8") as out_file:
                out_file.write(analysis_result)
            
            print("\nAnalysis complete! Results saved to analysis_result.txt")
            print("\nAnalysis result:")
            print(analysis_result)
            
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("No files were selected.") 