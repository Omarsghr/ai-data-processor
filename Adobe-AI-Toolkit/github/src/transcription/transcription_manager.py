import os
import sqlite3
import json
from groq_client import transcribe_with_groq
from local_whisper import transcribe_local_small

class TranscriptionManager:
    def __init__(self, db_name="project_memory.db"):
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        """Ensures the transcript table is ready for data."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transcript (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_text TEXT,
                method_used TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def _save_to_memory(self, text, method):
        """Pushes the final text into the SQLite database."""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            # We wipe the old one to keep the 'Current Project' clean
            cursor.execute("DELETE FROM transcript") 
            cursor.execute("INSERT INTO transcript (full_text, method_used) VALUES (?, ?)", (text, method))
            conn.commit()
            conn.close()
            print(f"✅ Transcription saved to DB Memory via {method}.")
        except Exception as e:
            print(f"❌ Database Error: {e}")

    def get_transcription(self, audio_file, output_file="map.json"):
        """Orchestrates the failover logic: Cloud -> Local."""
        print(f"--- Starting Transcription Workflow for: {audio_file} ---")

        # Attempt 1: Groq Cloud
        try:
            print("Attempting Cloud Transcription (Groq API)...")
            # We assume your function returns the text or writes to output_file
            transcribe_with_groq(audio_file, output_file)
            
            # Read the result from the JSON file to save to DB
            with open(output_file, 'r') as f:
                data = json.load(f)
                text = data.get("text", "") # Adjust key based on your Groq output format
            
            self._save_to_memory(text, "GROQ_CLOUD")
            print("Success: Processed via Groq Cloud.")

        except Exception as e:
            # Fallback: Local Whisper
            print(f"Cloud Error: {e} | Switching to Local Fallback...")

            try:
                transcribe_local_small(audio_file, output_file)
                
                with open(output_file, 'r') as f:
                    data = json.load(f)
                    text = data.get("text", "")
                
                self._save_to_memory(text, "LOCAL_WHISPER")
                print("Success: Processed locally.")
                
            except Exception as local_e:
                print(f"Critical Failure: Both methods failed. {local_e}")

if __name__ == "__main__":
    # Test run
    manager = TranscriptionManager()
    manager.get_transcription("tips on de.mp3")
