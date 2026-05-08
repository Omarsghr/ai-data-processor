import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load the keys from your .env file
load_dotenv()

# Match the naming in your .env: GROQ_API_KEY_1 to GROQ_API_KEY_15
API_KEYS = [os.getenv(f"GROQ_API_KEY_{i}") for i in range(1, 16) if os.getenv(f"GROQ_API_KEY_{i}")]

def transcribe_with_groq(audio_file_path, output_json="map.json"):
    """
    High-speed cloud transcription using a bank of 15 keys.
    """
    if not API_KEYS:
        print("❌ Error: No API keys found in .env (Checked for GROQ_API_KEY_1 to 15)")
        return None

    if not os.path.exists(audio_file_path):
        print(f"❌ Error: Audio file not found at {audio_file_path}")
        return None

    print(f"☁️ Sending to Groq Cloud: {os.path.basename(audio_file_path)}")

    for index, key in enumerate(API_KEYS):
        try:
            client = Groq(api_key=key)

            with open(audio_file_path, "rb") as file:
                # Multi-lang prompt to guide the AI for Moroccan/Arabic context
                multi_lang_prompt = (
                    "السلام عليكم، اليوم غادي نهضرو على coding و AI. "
                    "إزاي تعمل edit للفيديو بتاعك professionally وبطريقة سهلة. "
                )

                transcription = client.audio.transcriptions.create(
                    file=(audio_file_path, file.read()),
                    model="whisper-large-v3",
                    prompt=multi_lang_prompt,
                    response_format="verbose_json",
                )

                # Prepare the data dictionary
                output_data = {
                    "text": transcription.text,
                    "segments": transcription.segments
                }

                # Save results to JSON file
                with open(output_json, "w", encoding="utf-8") as f:
                    json.dump(output_data, f, ensure_ascii=False, indent=4)
                
                print(f"✅ Success! Transcription saved using Key #{index + 1}")
                
                # Return the text so the Manager can save it to DB immediately
                return transcription.text

        except Exception as e:
            if "429" in str(e):
                print(f"⚠️ Key #{index + 1} Rate Limited. Switching to next...")
                continue
            else:
                print(f"❌ Error with Key #{index + 1}: {e}")
                continue

    print("🚫 All 15 keys failed or were rate limited.")
    return None