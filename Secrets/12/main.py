import os
import librosa
import soundfile as sf
import numpy as np
from pydub import AudioSegment
import datetime
import whisper

def load_audio(input_path, sr=16000):
    audio, _ = librosa.load(input_path, sr=sr)
    return audio, sr

def cut_silence(audio, sr, top_db=30):
    intervals = librosa.effects.split(audio, top_db=top_db)
    non_silent_audio = np.concatenate([audio[start:end] for start, end in intervals])
    return non_silent_audio

def slow_down_audio(audio, rate):
    return librosa.effects.time_stretch(y=audio, rate=rate)

def reverse_audio(audio):
    return audio[::-1]

def save_audio(audio, sr, output_path):
    sf.write(output_path, audio, sr)

def transcribe_audio_whisper(audio_path, model_size="base"):
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path)
    return result["text"]

def main(input_file):
    timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    os.makedirs("processed_audio", exist_ok=True)

    print(f"[INFO] Loading audio file: {input_file}")
    audio, sr = load_audio(input_file)

    print("[INFO] Cutting silence...")
    audio_no_silence = cut_silence(audio, sr)
    cut_path = f"processed_audio/cut_silent_{timestamp}.wav"
    save_audio(audio_no_silence, sr, cut_path)

    for factor in [0.5, 0.33]:  # slowdown 2x and 3x
        print(f"[INFO] Processing slowdown factor: {1/factor:.1f}x")
        slowed_audio = slow_down_audio(audio_no_silence, factor)
        reversed_slowed = reverse_audio(slowed_audio)

        version = "2x" if factor == 0.5 else "3x"
        output_path = f"processed_audio/reverted_cut_silent_{timestamp}_slow_{version}.wav"
        save_audio(reversed_slowed, sr, output_path)

        print(f"[INFO] Saved: {output_path}")
        print("[INFO] Transcribing with Whisper...")
        transcript = transcribe_audio_whisper(output_path)
        print(f"\nTranscript ({version}):\n{transcript}\n")

if __name__ == "__main__":
    input_file = "Konstruktorska-4.mp3"  # Change this to your input path if needed
    main(input_file)
