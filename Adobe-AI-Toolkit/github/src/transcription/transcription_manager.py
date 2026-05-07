import os
import json
import sqlite3
from pydub import AudioSegment
from groq_client import transcribe_with_groq


class TranscriptionManager:
    def __init__(self, db_name="project_memory.db"):
        self.db_name = db_name

    def compress_audio(self, input_path):
        """Reduces audio quality to speed up upload and stay under Groq's 25MB limit."""
        target_path = "compressed_temp.mp3"
        print(f"📉 Compressing audio for Groq (Downsampling to 100kbps)...")

        audio = AudioSegment.from_file(input_path)
        # Convert to Mono and 16000Hz (Perfect for Voice AI)
        audio = audio.set_frame_rate(16000).set_channels(1)

        # Export at 96k or 100k bitrate
        audio.export(target_path, format="mp3", bitrate="96k")
        return target_path

    def _save_to_database(self, json_file):
        """Infects the database with the transcript text."""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            full_text = data.get("text", "")
            if full_text:
                conn = sqlite3.connect(self.db_name)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM transcript")
                cursor.execute(
                    "INSERT INTO transcript (full_text) VALUES (?)", (full_text,))
                conn.commit()
                conn.close()
                print("✨ [DATABASE] Transcript saved successfully.")
        except Exception as e:
            print(f"❌ [DB ERROR] {e}")

    def run_workflow(self, audio_file):
        """The Main Engine: Compress -> Transcribe -> Save."""
        print(f"\n--- 🚀 GROQ-ONLY WORKFLOW: {audio_file} ---")

        # 1. COMPRESS (Shrinks 50MB -> ~5MB)
        compressed_file = self.compress_audio(audio_file)
        output_json = "map.json"

        # 2. TRANSCRIBE (High Speed)
        try:
            print("☁️ Sending to Groq Cloud...")
            transcribe_with_groq(compressed_file, output_json)
            print("✅ Success: Transcribed in seconds.")

            # 3. SAVE
            self._save_to_database(output_json)

        except Exception as e:
            print(f"❌ Groq Error: {e}")
        finally:
            # Clean up the temp file to keep your workspace clean
            if os.path.exists(compressed_file):
                os.remove(compressed_file)


if __name__ == "__main__":
    manager = TranscriptionManager()
    manager.run_workflow("tips on de.mp3")
