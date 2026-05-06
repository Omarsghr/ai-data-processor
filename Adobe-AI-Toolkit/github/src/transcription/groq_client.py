import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load the keys from your .env file
load_dotenv()

# 1. Create the list of your 10 current keys
# This will look for GROQ_KEY_1 up to GROQ_KEY_10
API_KEYS = [os.getenv(f"GROQ_KEY_{i}") for i in range(
    1, 11) if os.getenv(f"GROQ_KEY_{i}")]


def transcribe_with_groq(audio_file_path, output_json="map.json"):
    """
    High-speed cloud transcription using Groq's LPU inference.
    Uses a bank of 10 keys to prevent Rate Limit errors.
    """
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(
            f"audio file not found at path:{audio_file_path}")

    print(f" Uploading to Groq Cloud...: {audio_file_path}")

    # 2. START OF THE LOOP: Try each key in your bank
    for index, key in enumerate(API_KEYS):
        try:
            # Initialize the client with the current key
            client = Groq(api_key=key)

            with open(audio_file_path, "rb") as file:
                multi_lang_prompt = (
                    "السلام عليكم، اليوم غادي نهضرو على coding و AI. "
                    "إزاي تعمل edit للفيديو بتاعك professionally وبطريقة سهلة. "
                    "Let's get started with this tutorial."
                )

                # API Call to Groq
                transcripation = client.audio.transcriptions.create(
                    file=(audio_file_path, file.read()),
                    model="whisper-large-v3",
                    prompt=multi_lang_prompt,
                    response_format="verbose_json",
                )

                # Required to get segments and timestamps
                segments = transcripation.segments

                # Save results to JSON file
                with open(output_json, "w", encoding="utf-8") as f:
                    json.dump(segments, f, ensure_ascii=False, indent=4)
                    print(
                        f"Success! Transcription saved to :{output_json} using Key #{index + 1}")
                    return True

        except Exception as e:
            # If the error is a Rate Limit (429), we switch keys
            if "429" in str(e):
                print(f"Key #{index + 1} is blocked. Switching to next key...")
                continue
            else:
                print(
                    f"Error during Groq transcription with Key #{index + 1}: {e}")
                # If we have more keys, we try the next one anyway
                continue

    # If we get here, it means all 10 keys failed
    return False


if __name__ == "__main__":
    # Test execution
    try:
        transcribe_with_groq("tips on de.mp3")
    except Exception:
        pass
