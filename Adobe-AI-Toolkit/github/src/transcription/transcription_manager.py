import os
import sqlite3
import json
import time
from groq_client import transcribe_with_groq
from local_whisper import transcribe_local_small

class TranscriptionManager:
    def __init__(self, db_name="project_memory.db"):
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
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
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM transcript") 
            cursor.execute("INSERT INTO transcript (full_text, method_used) VALUES (?, ?)", (text, method))
            conn.commit()
            conn.close()
            print(f"✅ [MEMORY] Transcript saved via {method}.")
        except Exception as e:
            print(f"❌ [DB ERROR] {e}")

    def _extract_text_from_json(self, file_path):
        """Intelligently parses JSON whether it's a list or a dict."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # If it's a dictionary (Groq style)
        if isinstance(data, dict):
            return data.get("text", "")
        
        # If it's a list (Local Whisper segments style)
        if isinstance(data, list):
            # Join all 'text' fields from each segment
            return " ".join([segment.get("text", "") for segment in data])
        
        return str(data)

    def get_transcription(self, audio_file, output_file="map.json"):
        print(f"\n--- 🧠 STARTING BRAIN PROCESS: {audio_file} ---")

        if os.path.exists(output_file):
            os.remove(output_file)

        # Attempt 1: Groq Cloud
        try:
            print("🚀 Attempting Groq Cloud...")
            transcribe_with_groq(audio_file, output_file)
            time.sleep(1) 

            if os.path.exists(output_file):
                text = self._extract_text_from_json(output_file)
                if text:
                    self._save_to_memory(text, "GROQ_CLOUD")
                    print("✨ Success: Groq Cloud finished!")
                    return text
            raise FileNotFoundError("Groq output missing")

        except Exception as e:
            print(f"⚠️ Cloud Failed: {e}. Switching to NVIDIA GPU...")
            
            try:
                # Attempt 2: Local NVIDIA GPU
                transcribe_local_small(audio_file, output_file)
                
                if os.path.exists(output_file):
                    text = self._extract_text_from_json(output_file)
                    self._save_to_memory(text, "LOCAL_WHISPER")
                    print("✅ Success: Processed locally on NVIDIA GPU.")
                    return text
                
            except Exception as local_e:
                print(f"❌ CRITICAL FAILURE: {local_e}")
                return None

if __name__ == "__main__":
    manager = TranscriptionManager()
    target_audio = "temp_audio.mp3"
    
    if os.path.exists(target_audio):
        manager.get_transcription(target_audio)
    else:
        print("❌ Run 'audio_processor.py' first!")