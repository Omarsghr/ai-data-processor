import subprocess
import sys
import os

def main():
    print("🚀 INITIALIZING ADOBE-AI-TOOLKIT MASTER PIPELINE")
    
    # Paths to sub-scripts
    base = "Adobe-AI-Toolkit/github/src/transcription"
    
    # Step 1: Extract
    print("\n--- [1/3] EXTRACTING AUDIO ---")
    subprocess.run([sys.executable, f"{base}/audio_processor.py"])
    
    # Step 2: Transcribe
    print("\n--- [2/3] AI TRANSCRIPTION (GROQ BANK) ---")
    subprocess.run([sys.executable, f"{base}/transcription_manager.py"])
    
    # Step 3: Database Verification
    print("\n--- [3/3] FINALIZING DATABASE ---")
    print("✨ Task complete. Open project_memory.db to see your results.")

if __name__ == "__main__":
    main()