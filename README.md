# AI Video-to-Data Processor

This project extracts audio from video files and uses AI to transcribe the content into structured JSON data.

## Features

- **Audio Extraction:** Uses MoviePy to pull audio from `.mp4`.
- **AI Transcription:** Uses OpenAI Whisper to convert speech to text.
- **Data Export:** Saves timestamps and words into a JSON file for easy sharing.

## How to use

1. Add your video as `video.mp4`.
2. Run `python audio_processor.py`.
3. Run `python transcriber.py`.
