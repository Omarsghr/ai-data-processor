import os
import sqlite3
import librosa
import numpy as np

def analyze_silence(audio_path, db_path):
    print(f"📉 Analyzing audio waves for: {os.path.basename(audio_path)}")
    
    try:
        # Load audio file
        y, sr = librosa.load(audio_path, sr=None)
        
        # Detect non-silent intervals (top_db=30 is usually good for voice)
        intervals = librosa.effects.split(y, top_db=30)
        
        # Calculate silent segments
        silences = []
        last_end = 0
        for start, end in intervals:
            if start > last_end:
                silences.append((last_end / sr, start / sr))
            last_end = end
        
        # Add final silence if it exists
        duration = librosa.get_duration(y=y, sr=sr)
        if last_end / sr < duration:
            silences.append((last_end / sr, duration))

        # Save to the CENTRAL Database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # CRITICAL: Create table if missing, but DO NOT drop 'transcript'
        cursor.execute("CREATE TABLE IF NOT EXISTS silence_map (start REAL, end REAL)")
        cursor.execute("DELETE FROM silence_map") # Clear old silence data only
        
        for start, end in silences:
            cursor.execute("INSERT INTO silence_map (start, end) VALUES (?, ?)", (start, end))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Found {len(silences)} silent segments.")
        print(f"💾 Silence map saved to: {db_path}")

    except Exception as e:
        print(f"❌ Silence Analysis Error: {e}")

if __name__ == "__main__":
    # ARCHITECT PATHS
    root_dir = r"C:\Users\DELL\OneDrive\Desktop\auto--editor__AI"
    db_path = os.path.join(root_dir, "project_memory.db")
    
    # Find the audio file
    audio_file = os.path.join(root_dir, "temp_audio.mp3")
    
    if os.path.exists(audio_file):
        analyze_silence(audio_file, db_path)
    else:
        print(f"❌ Error: Could not find {audio_file}")