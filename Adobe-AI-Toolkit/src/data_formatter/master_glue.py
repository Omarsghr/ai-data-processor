import sqlite3
import json

class master_glue:
    def __init__(self, db_name='project_memory.db'):
       self.db_name = db_name

    def fetch_data(self):
        """pulls everything from the database tables"""
        conn = sqlite3.connect(self.db_name)
        # Line 11: CRITICAL! This tells Python to return data as a Dictionary (key:value) 
        # instead of a list of numbers. This makes the JSON readable.
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        # --- STEP 1: Grab AI Instructions ---
        # Line 16: We select the columns we need for the Adobe Extension
        cursor.execute("SELECT keyword, ai_prompt, action_type FROM ai_intelligence")
        # Line 18: Convert the rows into a clean list of dictionaries
        ai_instructions = [dict(row) for row in cursor.fetchall()]
       # --- STEP 2: Grab Signal Analysis Cuts ---
        # Line 21: We grab the start/end times found by Houssam's code
        cursor.execute("SELECT start_time, end_time, duration FROM signal_cuts")
        silence_cuts = [dict(row) for row in cursor.fetchall()]

        conn.close() # Line 24: Close connection to save Gamer PC memory
        return ai_instructions, silence_cuts
    def create_screenplay_json(self, output_file='screenplay.json'):
        """ formats the raw data into a structured json 'plate' for the adobe extension """
        ai_data, cut_data = self.fetch_data()
        # The 'Master Glue' Logic - Updated for Adobe-AI-Toolkit
        screenplay = {
            "version": "1.0",
            "app_name": "Adobe-AI-Toolkit",
            "engine": "HROQ-Signal-Sync",
            "workflow_data": {
                "edit_cuts": cut_data,       # Silence gaps for the timeline
                "ai_visuals": ai_data        # AI-generated prompts for assets
            },
            "system_status": "Ready for Extension Injection"
        }
        # Line 41: Open the file and write the JSON
        with open(output_file, 'w') as f:
            # indent=4 makes the file look 'pretty' and easy for you to read
            json.dump(screenplay, f, indent=4) 
        
        print(f"✅ {output_file} generated! The bridge is built.")