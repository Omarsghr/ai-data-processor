import sqlite3

def init_complete_db():
    conn = sqlite3.connect('project_memory.db')
    cursor = conn.cursor()

    # 1. AI Intelligence Table (Your Step 1)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_intelligence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL,
            ai_prompt TEXT,          -- The instructions for image/video gen
            timestamp_sec REAL,
            action_type TEXT,        -- 'IMAGE_GEN', 'VIDEO_GEN', 'ZOOM'
            asset_path TEXT,         
            status TEXT DEFAULT 'PENDING'
        )
    ''')

    # 2. Signal Analysis Table (Houssam's Step 2)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS signal_cuts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time REAL NOT NULL,
            end_time REAL NOT NULL,
            duration REAL,
            cut_type TEXT DEFAULT 'jump_cut',
            is_processed INTEGER DEFAULT 0 -- 0 for pending, 1 for done
        )
    ''')

    # Add this to your init_db function
    cursor.execute('''
       CREATE TABLE IF NOT EXISTS transcript (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_text TEXT,
            language TEXT DEFAULT 'en',
             processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Full Database Schema Initialized: AI & Signal tables are ready.")

if __name__ == "__main__":
    init_complete_db()