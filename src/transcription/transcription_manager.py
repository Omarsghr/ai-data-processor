import os
import sys
import sqlite3
import glob
from dotenv import load_dotenv

# --- PATH INJECTOR ---
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from groq_clients import transcribe_with_groq
except ImportError:
    from .groq_clients import transcribe_with_groq

class TranscriptionManager:
    def __init__(self):
        # 1. SET PROJECT PATHS
        self.root_dir = r"C:\Users\DELL\OneDrive\Desktop\auto--editor__AI"
        self.toolkit_dir = os.path.join(self.root_dir, "Adobe-AI-Toolkit")
        self.db_path = os.path.join(self.root_dir, "project_memory.db")
        
        # 2. KEY-FINDER LOGIC (Checks root and toolkit folder)
        env_locations = [
            os.path.join(self.root_dir, ".env"),
            os.path.join(self.toolkit_dir, ".env")
        ]
        
        for path in env_locations:
            if os.path.exists(path):
                load_dotenv(dotenv_path=path)
                print(f"🔑 [System] Loaded .env from: {path}")
                break

    def find_latest_audio(self):
        """Finds any .mp3 file in the project or desktop."""
        search_locations = [self.root_dir, r"C:\Users\DELL\OneDrive\Desktop"]
        for location in search_locations:
            audio_files = glob.glob(os.path.join(location, "*.mp3"))
            if audio_files:
                audio_files.sort(key=os.path.getmtime, reverse=True)
                return audio_files[0]
        return None

    def _save_to_db(self, text):
        """Saves transcript to the central database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS transcript (full_text TEXT, method_used TEXT)")
        cursor.execute("DELETE FROM transcript") 
        cursor.execute("INSERT INTO transcript (full_text, method_used) VALUES (?, ?)", (text, "HROQ_15_NODE_BANK"))
        conn.commit()
        conn.close()
        print(f"💾 [DB] Data saved to {self.db_path}")

    def run(self):
        print("🔍 Searching for audio source...")
        audio_source = self.find_latest_audio()

        if not audio_source:
            print("❌ Error: No .mp3 audio file found!")
            return

        print(f"🎬 Processing: {os.path.basename(audio_source)}")
        output_json = os.path.join(current_dir, "map.json")
        
        # Call the 15-node Groq bank
        result_text = transcribe_with_groq(audio_source, output_json)
        
        if result_text:
            self._save_to_db(result_text)
            print("✅ AI TRANSCRIPTION Success.")
        else:
            print("⚠️ Groq Bank returned empty text. Check API Keys in .env")

if __name__ == "__main__":
    manager = TranscriptionManager()
    manager.run()