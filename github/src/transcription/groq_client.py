import os
import json
from groq import Groq
# Initialize the Groq client
# Tip: It's best to set your API Key as an environment variable for security
# For now, you can replace 'YOUR_GROQ_API_KEY' with your actual key
client = Groq(
    api_key="GROQ_API_KEY")


def transcribe_with_groq(audio_file_path, output_json="map.json"):
    """
    High-speed cloud transcription using Groq's LPU inference.
    Uses Whisper-Large-V3 for maximum accuracy across multiple languages/dialects.
    """
    # Check if the audio file exists
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(
            f"audio file not found at path:{audio_file_path}")
    print(f" Uploading to Groq Cloud...: {audio_file_path}")
    try:
        with open(audio_file_path, "rb") as file:
            # Multi-language prompt to improve context for Moroccan/Egyptian/Tech speech
            multi_lang_prompt = (
                "السلام عليكم، اليوم غادي نهضرو على coding و AI. "
                "إزاي تعمل edit للفيديو بتاعك professionally وبطريقة سهلة. "
                "Let's get started with this tutorial."
            )
            # API Call to Groq
            transcripation = client.audio.transcriptions.create(file=(audio_file_path, file.read(
            )), model="whisper-large-v3", prompt=multi_lang_prompt, response_format="verbose_json", )
            # Required to get segments and timestamps
            segments = transcripation.segments
            # Save results to JSON file
            with open(output_json, "w", encoding="utf-8") as f:
                json.dump(segments, f, ensure_ascii=False, indent=4)
                print(f"transcripation saved to :{output_json}")
                return True
    except Exception as e:
        print(f"error during Groq transcription :{e}")
        # We raise the exception so the transcription_manager.py can catch it and switch to local
        raise e


if __name__ == "__main__":
    # Test execution
    try:
        transcribe_with_groq("tips on de.mp3")
    except Exception:
        pass
