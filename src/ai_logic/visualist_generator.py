import os
import json
import sqlite3
import requests
from dotenv import load_dotenv

# --- 1. SETUP & CONFIGURATION ---
load_dotenv()
ROOT_DIR = r"C:\Users\DELL\OneDrive\Desktop\auto--editor__AI"
JSON_PATH = os.path.join(ROOT_DIR, "adobe_screenplay.json")
DB_PATH = os.path.join(ROOT_DIR, "project_memory.db")
ASSET_FOLDER = os.path.join(ROOT_DIR, "assets", "ai_images")

# Ensure the visualist has a place to store its work
os.makedirs(ASSET_FOLDER, exist_ok=True)

def generate_and_store_free():
    print("\n🎨 [Visualist: FREE MODE] Starting Final Integration Test...")
    
    # --- 2. LOAD THE BRAIN'S PLAN ---
    if not os.path.exists(JSON_PATH):
        print(f"❌ Error: {JSON_PATH} not found. Please run the Director script first!")
        return

    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            screenplay = json.load(f)
    except Exception as e:
        print(f"❌ Error reading JSON file: {e}")
        return
    
    image_prompts = screenplay.get('image_prompts', [])
    if not image_prompts:
        print("ℹ️ No images found in the JSON file. Check your Director logic.")
        return

    # --- 3. CONNECT TO PROJECT MEMORY (SQLite) ---
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create the table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS generated_assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT,
            local_path TEXT,
            prompt_used TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    print(f"🔄 Processing {len(image_prompts)} visual assets...")

    for idx, item in enumerate(image_prompts):
        # --- FIX: ROBUST DATA HANDLING ---
        # If the AI gave us a dictionary, extract. If it's just a string, convert.
        if isinstance(item, dict):
            keyword = item.get('keyword', f'scene_{idx}').replace(" ", "_")
            prompt_text = item.get('prompt', 'Business presentation visual')
        else:
            prompt_text = str(item)
            keyword = f"scene_{idx}"

        # Clean the filename
        file_name = f"gen_{idx}_{keyword}.jpg"
        full_path = os.path.join(ASSET_FOLDER, file_name)

        # Skip if already downloaded to save time
        if os.path.exists(full_path):
            print(f"⏩ Skipping existing file: {file_name}")
            continue

        # --- 4. THE FREE GENERATION (Pollinations API) ---
        print(f"🚀 Generating Visual {idx+1}/{len(image_prompts)}: {keyword}...")
        
        # URL encode the prompt for the browser request
        clean_prompt = requests.utils.quote(prompt_text)
        free_url = f"https://image.pollinations.ai/prompt/{clean_prompt}?width=1024&height=1024&nologo=true&seed={idx}"

        try:
            # Download the image directly from the free cloud
            response = requests.get(free_url, timeout=45)
            
            if response.status_code == 200:
                # Save to Local Drive
                with open(full_path, 'wb') as handler:
                    handler.write(response.content)

                # --- 5. THE HANDSHAKE: LOG TO DATABASE ---
                cursor.execute("""
                    INSERT INTO generated_assets (keyword, local_path, prompt_used)
                    VALUES (?, ?, ?)
                """, (keyword, full_path, prompt_text))
                
                conn.commit()
                print(f"✅ SUCCESS: {file_name} saved and indexed in DB.")
            else:
                print(f"❌ API Rejected Request: Status {response.status_code}")

        except Exception as e:
            print(f"❌ Error during generation for '{keyword}': {e}")

    conn.close()
    print("\n✨ [INTEGRATION TEST COMPLETE]")
    print(f"📂 Check your folder: {ASSET_FOLDER}")
    print("📊 Your 'generated_assets' table is now synchronized with your cuts!")

if __name__ == "__main__":
    generate_and_store_free()