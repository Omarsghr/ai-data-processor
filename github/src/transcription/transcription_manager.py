import os
# Importing your specific modules (make sure the filenames match)
from groq_client import transcribe_with_groq
from local_whisper import transcribe_local_small


def get_transcription(audio_file, output_file="map.json"):
    """
    Orchestrates the transcription process. 
    Tries the high-speed Groq API first, then falls back to local Whisper.
    """
    print(f"--- Starting Transcription Workflow for: {audio_file} ---")

    try:
        # Attempt 1: High-Speed Cloud Transcription
        print("Attempting Cloud Transcription (Groq API)...")
        transcribe_with_groq(audio_file, output_file)
        print("Success: Processed via Groq Cloud.")

    except Exception as e:
        # Fallback: Local Processing
        print(f"Cloud Error: {e}")
        print("Switching to Local Fallback (Whisper Small)...")

        try:
            transcribe_local_small(audio_file, output_file)
            print("Success: Processed locally.")
        except Exception as local_e:
            print(
                f"Critical Failure: Both Cloud and Local methods failed. {local_e}")


if __name__ == "__main__":
    # Test run
    get_transcription("tips on de.mp3")
