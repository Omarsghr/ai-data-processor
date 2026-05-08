import sqlite3
import os
import json
import sys
from groq import Groq
from dotenv import load_dotenv

# --- ARCHITECT CONFIGURATION ---
# This loads your 15 keys from the .env file in your root folder
load_dotenv() 

ROOT_DIR = r"C:\Users\DELL\OneDrive\Desktop\auto--editor__AI"
DB_PATH = os.path.join(ROOT_DIR, "project_memory.db")
JSON_BACKUP = os.path.join(ROOT_DIR, "src", "transcription", "map.json")
OUTPUT_JSON = os.path.join(ROOT_DIR, "adobe_screenplay.json")

def initialize_and_verify_db():
    """Ensures the database exists and contains the transcript data."""
    if not os.path.exists(DB_PATH):
        print(f"⚠️ [System] Database not found at {DB_PATH}.")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("CREATE TABLE IF NOT EXISTS transcript (full_text TEXT, method_used TEXT)")
    conn.commit()

    cursor.execute("SELECT full_text FROM transcript LIMIT 1")
    row = cursor.fetchone()

    if not (row and row[0]):
        print("⚠️ [Director] Database empty. Attempting Self-Heal from map.json...")
        if os.path.exists(JSON_BACKUP):
            with open(JSON_BACKUP, 'r', encoding='utf-8') as f:
                data = json.load(f)
                text_content = data.get('text', '')
                if text_content:
                    cursor.execute("INSERT INTO transcript (full_text, method_used) VALUES (?, ?)", 
                                 (text_content, 'HROQ_AUTO_RECOVERY'))
                    conn.commit()
                    print("🚀 [Director] Success: Database repaired using map.json!")
        else:
            print(f"❌ [Director] Critical: map.json not found at {JSON_BACKUP}")
    
    return conn

def generate_screenplay(video_mode="Business"):
    print(f"\n--- 🚀 HROQ Intelligence Service Starting: {video_mode} Mode ---")
    
    conn = initialize_and_verify_db()
    cursor = conn.cursor()

    # --- MODES & PERSONALITY ---
    modes = {
        "Education": "Focus on clarity. Detect School names, definitions, and technical terms. Action: ZOOM on definitions, GEN_IMAGE for entities.",
        "Vlog": "Focus on personality. Detect emotions, funny moments, and locations. Action: SHAKE for funny parts, WARM_FILTER for stories.",
        "Cinematic": "Focus on visuals. Detect descriptive adjectives (e.g., 'huge', 'dark', 'epic'). Action: SLOW_MO and CINEMATIC_LUT.",
        "Marketing": "Focus on CTA (Call to Action). Detect product names and prices. Action: TEXT_OVERLAY for features.",
        "Business": "Focus on professionalism and clarity. Detect company names, financial terms, and key metrics ($/%). Action: LOWER_THIRD for names, DATA_CHART for metrics.",
        "Real_Estate": "Atmosphere focus. Detect room names and luxury terms. Action: WIDE_LENS_CROP, GEN_IMAGE for floorplans.",
        "Social_Media": "Retention focus. Detect hooks and trends. Action: KINETIC_SUBTITLES, FAST_ZOOM, GLITCH_TRANSITIONS."
    }

    selected_instruction = modes.get(video_mode, modes["Education"])

    try:
        # 1. Fetch Data
        cursor.execute("SELECT full_text FROM transcript")
        transcript_res = cursor.fetchone()
        cursor.execute("SELECT start, end FROM silence_map")
        silences = cursor.fetchall()

        if not transcript_res or not silences:
            print("❌ Error: Missing data in DB. Ensure transcription and silence analysis ran first.")
            return

        transcript = transcript_res[0]

        # 2. Initialize Groq (Pulling from your .env)
        # Change "GROQ_API_KEY_1" to match exactly what is in your .env file
        api_key = os.getenv("GROQ_API_KEY_1") 
        
        if not api_key:
            print("❌ Error: GROQ_API_KEY_1 not found in .env! Check your variable names.")
            return

        client = Groq(api_key=api_key)

        # 3. Request AI Direction
        system_prompt = f"""
        You are an Expert AI Video Director for Adobe Premiere Pro. 
        Video Style: {video_mode}.
        Instruction: {selected_instruction}

        Analyze the transcript and output ONLY a JSON object with:
        1. 'commands': List of objects (word, action, style, sfx).
        2. 'image_prompts': List of visual descriptions for GEN_IMAGE actions.
        3. 'settings': {{'music': str, 'lut': str, 'font': str}}.
        """

        print("🧠 HROQ is analyzing keywords and creating the screenplay...")
        
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Transcript: {transcript}"}
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )

        screenplay = json.loads(response.choices[0].message.content)

        # 4. Sync Silence Timing
        screenplay['timing_data'] = {
            "silence_intervals": [{"start": s[0], "end": s[1]} for s in silences]
        }

        # 5. Save Final Export
        with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
            json.dump(screenplay, f, indent=4)
        
        print(f"✨ SUCCESS: Screenplay generated for {len(silences)} segments.")
        print(f"📂 Saved to: {OUTPUT_JSON}")

    except Exception as e:
        print(f"❌ System Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Change the mode here to test different styles
    generate_screenplay(video_mode="Business")