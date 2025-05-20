import base64
import tkinter as tk
from tkinter import filedialog
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PROMPT = 'Wykonaj OCR obrazu i zwróć tekst z obrazu. Uwzglednij akapity. Nie pomijaj ich. Są one kluczowe. Tekst ma być odwzorowany tak jak na obrazie.'

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
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.jfif")]
    )
    return file_paths

def analyze_maps_with_gpt4(image_base64_list):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    # Prepare content array with prompt and all images
    content = [{"type": "text", "text": PROMPT}]
    
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

def process_ocr_response(text):
    # Split text into paragraphs (split by double newlines)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    # Create numbered paragraphs
    numbered_paragraphs = []
    for i, paragraph in enumerate(paragraphs, 1):
        numbered_paragraphs.append(f"{i}. {paragraph}")
    
    return numbered_paragraphs

def extract_words_from_paragraphs(paragraphs):
    word_mapping = {}
    for i, paragraph in enumerate(paragraphs, 1):
        # Split paragraph into words and remove any empty strings
        words = [word.strip() for word in paragraph.split() if word.strip()]
        # Skip the first word if it's just a number with a dot (e.g., "1.")
        if words and words[0].replace(".", "").isdigit():
            words = words[1:]
        # Store words with their paragraph number and position
        for j, word in enumerate(words, 1):
            key = f"A{i}S{j}"
            word_mapping[key] = word
    return word_mapping

def save_word_mapping(word_mapping, filename="word_mapping.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for key, word in word_mapping.items():
            f.write(f"{key}: {word}\n")

def extract_specific_words(word_mapping):
    # Define the specific word references we want to extract
    word_references = [
        "A1S53", "A2S27", "A2S28", "A2S29",
        "A4S5", "A4S22", "A4S23",
        "A1S13", "A1S15", "A1S16", "A1S17", "A1S10", "A1S19",
        "A2S62", "A3S31", "A3S32", "A1S22", "A3S34",
        "A5S37", "A1S4"
    ]
    
    # Extract words and maintain the same grouping as in the references
    extracted_words = []
    current_group = []
    
    for ref in word_references:
        word = word_mapping.get(ref, f"[{ref} not found]")
        current_group.append(word)
        
        # Check if we should start a new group (based on the original grouping)
        if ref in ["A2S29", "A4S23", "A1S19", "A3S34", "A1S4"]:
            extracted_words.append(" ".join(current_group))
            current_group = []
    
    return extracted_words

if __name__ == "__main__":
    file_paths = select_files()
    
    if file_paths:  # Check if files were selected
        try:
            # Check if analysis_result.txt exists
            if os.path.exists("analysis_result.txt"):
                print("\nFound existing analysis_result.txt, using it instead of making a new request...")
                with open("analysis_result.txt", "r", encoding="utf-8") as f:
                    numbered_paragraphs = f.read().splitlines()
            else:
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
                
                # Process the OCR result into numbered paragraphs
                numbered_paragraphs = process_ocr_response(analysis_result)
                
                # Save analysis result with numbered paragraphs
                with open("analysis_result.txt", "w", encoding="utf-8") as out_file:
                    out_file.write("\n".join(numbered_paragraphs))
            
            # Extract words and create mapping
            word_mapping = extract_words_from_paragraphs(numbered_paragraphs)
            
            # Extract specific words based on references
            specific_words = extract_specific_words(word_mapping)
            
            # Save word mapping
            save_word_mapping(word_mapping)
            
            # Save specific words
            with open("specific_words.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(specific_words))
            
            print("\nAnalysis complete! Results saved to analysis_result.txt")
            print("\nWord mapping saved to word_mapping.txt")
            print("\nSpecific words saved to specific_words.txt")
            print("\nExtracted specific words:")
            for group in specific_words:
                print(group)
            
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("No files were selected.") 