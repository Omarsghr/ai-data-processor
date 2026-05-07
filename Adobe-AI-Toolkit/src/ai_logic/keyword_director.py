import os
import json
import random
import sqlite3
from groq import Groq
from dotenv import load_dotenv

# 1. FOUNDATION: Load keys and environment
load_dotenv()

class AdobeToolkitDB:
    """The 'Memory' of the Service: Handles all SQLite operations."""
    def __init__(self, db_name="project_memory.db"):
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        # Create AI Intelligence table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_intelligence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT,
                ai_prompt TEXT,
                action_type TEXT,
                status TEXT DEFAULT 'PENDING'
            )
        ''')
        conn.commit()
        conn.close()

    def insert_screenplay(self, screenplay_list):
        """Injects AI instructions into the database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        for item in screenplay_list:
            cursor.execute('''
                INSERT INTO ai_intelligence (keyword, ai_prompt, action_type)
                VALUES (?, ?, ?)
            ''', (
                item.get('word'), 
                f"Asset: {item.get('asset_suggestion')} | Mood: {item.get('mood')}", 
                item.get('action')
            ))
        conn.commit()
        conn.close()
        print(f"✅ {len(screenplay_list)} items stored in SQLite.")


class HROQEngine:
    """The 'Brain' of the Service: Handles AI analysis using Groq."""
    def __init__(self):
        self.db = AdobeToolkitDB() # Connect the brain to the memory

    def _get_client(self):
        # Dynamically picks one of your 15 API keys
        key_index = random.randint(1, 15)
        api_key = os.getenv(f"GROQ_API_KEY_{key_index}")
        return Groq(api_key=api_key)

    def analyze_content(self, transcription_text, video_type="educational"):
        contexts = {
            "educational": "focus on technical terms, definitions, and complex formulas.",
            "marketing": "focus on product names, emotional hooks, and call-to-actions.",
            "vlog": "focus on names of places, funny moments, and personal stories."
        }
        selected_context = contexts.get(video_type, "focus on high-impact keywords.")

        system_instruction = (
            f"You are a Professional Video Editing Director. {selected_context} "
            "Analyze the user's text and identify triggers for: "
            "1. zoom (technical emphasis), 2. image/b-roll (visual support), 3. bg_music. "
            "Return ONLY a JSON object with a list 'screenplay' containing: "
            "'word', 'action', 'asset_suggestion', 'mood', and 'style_rules'."
        )

        try:
            client = self._get_client()
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": transcription_text}
                ],
                model="llama-3.3-70b-versatile",
                response_format={"type": "json_object"}
            )
            
            # Parse result
            result_json = json.loads(response.choices[0].message.content)
            
            # THE CONNECTION: Save to DB automatically
            self.db.insert_screenplay(result_json.get('screenplay', []))
            
            return result_json
        except Exception as e:
            return {"error": str(e), "status": "failed"}


# --- EXECUTION ---
if __name__ == "__main__":
    print("--- 🚀 HROQ Intelligence Service Starting ---")
    engine = HROQEngine()
    
    sample_text = "In Paris, the Eiffel Tower is amazing. You should buy our travel guide for only $10."
    
    # This now analyzes AND saves to the database in one move
    final_output = engine.analyze_content(sample_text, video_type="marketing")
    
    print("\n--- Final JSON for Reference ---")
    print(json.dumps(final_output, indent=4))
