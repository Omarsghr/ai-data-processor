import whisper
import json
import os
import imageio_ffmpeg


def transcribe_local_small(audio_file, output_file):
    """
    Offline transcription using OpenAI Whisper 'small' model.
    Acts as a local fallback for the Auto-Editor pipeline.
    """

    # 1. Locate the FFmpeg executable installed via imageio-ffmpeg
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

    # 2. Set environment variable so Whisper can find the FFmpeg binary
    os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path

    # Check if the input file exists before starting
    if not os.path.exists(audio_file):
        print(f"Error: The file '{audio_file}' was not found.")
        return

    try:
        print("--- Local Transcription Started ---")
        print(f"System: Using FFmpeg binary at {ffmpeg_path}")

        # Load the 'small' model (Better accuracy for dialects like Darija/Egyptian)
        print("Model: Loading Whisper 'small' model to memory...")
        model = whisper.load_model("small")

        print(f"Status: Processing audio file '{audio_file}'...")

        # Multi-language prompt to guide the AI for Moroccan/Egyptian/English/French contexts
        multi_lang_prompt = (
            "السلام عليكم، اليوم غادي نهضرو على coding و AI. "
            "إزاي تعمل edit للفيديو بتاعك professionally وبطريقة سهلة. "
            "Let's get started with this tutorial."
        )

        # Execute transcription
        # fp16=False: Required for CPU processing
        # best_of/beam_size: Higher values improve accuracy for complex speech
        result = model.transcribe(
            audio_file,
            fp16=False,
            initial_prompt=multi_lang_prompt,
            best_of=5,
            beam_size=5
        )

        # Save the segments (text + timestamps) to a JSON file
        with open(output_file, "w", encoding="UTF-8") as f:
            json.dump(result['segments'], f, ensure_ascii=False, indent=4)

        print("-" * 30)
        print(f"Success! Data map exported to: {output_file}")
        print("-" * 30)

    except Exception as e:
        print(f"Critical Error during local transcription: {e}")


if __name__ == "__main__":
    # Standard entry point for the script
    transcribe_local_small("tips on de.mp3", "map.json")
