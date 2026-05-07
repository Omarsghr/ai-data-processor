import sqlite3
from pydub import AudioSegment, silence

class AdobeToolkitDB:
    """The 'Memory' of the Service: Updated to handle Signal Data too."""
    def __init__(self, db_name="project_memory.db"):
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        # 1. AI Logic Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_intelligence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT, ai_prompt TEXT, action_type TEXT, status TEXT DEFAULT 'PENDING'
            )
        ''')
        # 2. NEW: Signal Analysis Table for Houssam's data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signal_cuts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time REAL NOT NULL,
                end_time REAL NOT NULL,
                duration REAL,
                is_processed INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()

    def insert_silence_gaps(self, cut_list):
        """Pushes detected silence ranges into the database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        for cut in cut_list:
            cursor.execute('''
                INSERT INTO signal_cuts (start_time, end_time, duration)
                VALUES (?, ?, ?)
            ''', (cut['start'], cut['end'], cut['duration']))
        conn.commit()
        conn.close()
        print(f"✅ {len(cut_list)} silence gaps saved to SQLite.")


def detect_silence_gaps(audio_file_path, silence_thresh=-50, min_silence_len=1000):
    """Scans audio for gaps and stores them in the database."""
    db = AdobeToolkitDB() # Connect to memory
    
    try:
        audio = AudioSegment.from_file(audio_file_path)
        silent_ranges = silence.detect_silence(
            audio, 
            min_silence_len=min_silence_len,
            silence_thresh=silence_thresh
        )

        formatted_cuts = []
        for start, end in silent_ranges:
            formatted_cuts.append({
                "start": start / 1000,
                "end": end / 1000,
                "duration": (end - start) / 1000
            })

        # THE CONNECTION: Save to DB
        if formatted_cuts:
            db.insert_silence_gaps(formatted_cuts)
            
        return formatted_cuts

    except Exception as e:
        print(f"Error processing audio: {e}")
        return []

if __name__ == "__main__":
    test_file = "assets/raw_audio.mp3"
    print("--- 🎙️ Signal Analysis Service Starting ---")
    
    cuts = detect_silence_gaps(test_file)
    
    for cut in cuts:
        print(f"Detected Gap: {cut['start']}s to {cut['end']}s")