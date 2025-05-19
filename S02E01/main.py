import os
import openai
import tkinter as tk
from tkinter import filedialog
from dotenv import load_dotenv
import json
import requests

# Load environment variables from .env file
load_dotenv()

# Set API keys from environment variables
api_key = os.getenv("OPENAI_API_KEY")
aidevs_key = os.getenv("AIDEVS_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please check your .env file.")
if not aidevs_key:
    raise ValueError("AIDEVS_KEY not found in environment variables. Please check your .env file.")

openai.api_key = api_key

SYSTEM_PROMPT = """You are an intelligent investigator assisting in analyzing transcripts of witness interrogations.

Your task is to determine **on which street professor Andrzej Maj teaches**. The transcripts contain statements of witnesses suspected of having connections with the professor.

Be aware that:
- Witnesses may contradict each other.
- Some statements may be incorrect or misleading.
- Some testimonies may be vague, humorous, chaotic, or evasive.
- The exact name of the street **does not appear directly in the transcripts**.

You must analyze the statements holistically, look for contextual clues, evaluate credibility, and **use your internal knowledge about professor Andrzej Maj** to infer the most likely street.

Return only the **name of the street**, without extra commentary or justification.
If you're not sure, return your best possible guess based on reasoning and internal knowledge.

<example>
{
"street": "Warszawska"
}
</example>"""

def select_audio_files():
    root = tk.Tk()
    root.withdraw()

    file_paths = filedialog.askopenfilenames(
        title="Select audio files",
        filetypes=[("M4a Files", "*.m4a")]
    )

    return list(file_paths)

def transcribe_audio(file_path):
    print(f"Transcribing: {os.path.basename(file_path)}")
    with open(file_path, "rb") as audio_file:
        transcript = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"  # You can also use 'json', 'srt', etc.
        )
    return transcript

def create_combined_context(transcriptions):
    combined_text = "\n\n=== New transcription ===\n\n".join(transcriptions)
    return combined_text

def analyze_transcripts(combined_text):
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": combined_text}
            ],
            temperature=0.7
        )
        
        # Extract the response content
        result = response.choices[0].message.content
        
        # Try to parse as JSON
        try:
            result_json = json.loads(result)
            return result_json.get("street", "The street was not found")
        except json.JSONDecodeError:
            return result.strip()
            
    except Exception as e:
        print(f"Error during GPT analysis: {e}")
        return "Error"

def send_result_to_endpoint(result):
    endpoint = "https://centrala.ag3nts.org/report"
    payload = {
        "task": "mp3",
        "apikey": aidevs_key,
        "answer": result
    }
    
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        print(f"\nResponse from server: {response.text}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending result to endpoint: {e}")
        return None

if __name__ == "__main__":
    selected_files = select_audio_files()

    if not selected_files:
        print("No files selected.")
        exit()

    # Array to store all transcriptions
    all_transcriptions = []

    for path in selected_files:
        try:
            text = transcribe_audio(path)
            print(f"\n--- {os.path.basename(path)} ---")
            print(text)
            all_transcriptions.append(text)
        except Exception as e:
            print(f"Error processing {path}: {e}")

    if all_transcriptions:
        print("\n=== Combined context from all transcriptions ===")
        combined_context = create_combined_context(all_transcriptions)
        print(combined_context)
        
        # Save combined context to a file
        output_file = "combined_transcriptions.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(combined_context)
        print(f"\nSaved combined context to file: {output_file}")
        
        # Analyze the transcripts using GPT-4
        print("\n=== Analysis of transcripts by GPT-4 ===")
        result = analyze_transcripts(combined_context)
        print(f"\nAnalysis result: {result}")
        
        # Send result to endpoint
        print("\n=== Sending result to endpoint ===")
        send_result_to_endpoint(result)
