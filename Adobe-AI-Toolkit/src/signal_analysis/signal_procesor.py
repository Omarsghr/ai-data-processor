import sys
import os

# --- PYTHON 3.13 COMPATIBILITY PATCH ---
# We manually map 'audioop-lts' to the name 'audioop' so pydub doesn't crash.
try:
    import audioop
except ImportError:
    try:
        import importlib
        audioop = importlib.import_module("audioop_lts")
        sys.modules["audioop"] = audioop
        print("🛠️ Python 3.13 Patch Applied: audioop-lts linked.")
    except ImportError:
        print("❌ Error: Please run 'pip install audioop-lts' in your venv first.")
        sys.exit(1)

from pydub import AudioSegment, silence
import sqlite3

class SignalProcessor:
    def __init__(self, db_name="project_memory.db"):
        # Ensure path to DB is correct relative to the script
        self.db_path = os.path.join(os.getcwd(), db_name)
        self._init_db()

    def _init_db(self):
        """Creates the signals table to store silence/volume data."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signal_map (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_ms INTEGER,
                end_ms INTEGER,
                type TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def analyze_audio(self, file_path):
        """Scans for silence and important audio segments."""
        if not os.path.exists(file_path):
            print(f"❌ Audio file not found: {file_path}")
            return

        print(f"📉 Analyzing signal for: {file_path}...")
        audio = AudioSegment.from_file(file_path)
        
        # Detect silence (minimum 1 second of silence, below -40dBFS)
        # You can adjust 'silence_thresh' if it's too sensitive
        silent_ranges = silence.detect_silence(
            audio, 
            min_silence_len=1000, 
            silence_thresh=-40
        )

        print(f"✅ Found {len(silent_ranges)} silent segments.")
        self._save_signals(silent_ranges, "SILENCE")

    def _save_signals(self, ranges, sig_type):
        """Saves the detected ranges to SQLite."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Wipe old signal data for this new test
        cursor.execute("DELETE FROM signal_map")
        
        for start, end in ranges:
            cursor.execute(
                "INSERT INTO signal_map (start_ms, end_ms, type) VALUES (?, ?, ?)",
                (start, end, sig_type)
            )
        
        conn.commit()
        conn.close()
        print(f"💾 Signals saved to DB: {self.db_path}")

# --- EXECUTION BLOCK ---
if __name__ == "__main__":
    processor = SignalProcessor()
    
    # Target the file your i7 created
    target = "temp_audio.mp3"
    
    if os.path.exists(target):
        processor.analyze_audio(target)
    else:
        print("❌ temp_audio.mp3 not found. Run audio_processor.py first!")