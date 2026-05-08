import os
import subprocess
import sys

# Configuration
ROOT_DIR = r"C:\Users\DELL\OneDrive\Desktop\auto--editor__AI"
PYTHON_EXE = sys.executable  # Uses the Python from your (venv) automatically

def run_script(script_path):
    """Helper to run a sub-script and wait for it to finish."""
    print(f"--- Running: {os.path.basename(script_path)} ---")
    result = subprocess.run([PYTHON_EXE, script_path], capture_output=False)
    if result.returncode != 0:
        print(f"❌ Error in {script_path}. Stopping pipeline.")
        sys.exit(1)
    print(f"✅ Finished: {os.path.basename(script_path)}\n")

def run_master_pipeline():
    print("🎬 === STARTING AUTO-EDITOR AI MASTER GLUE === 🎬\n")
    
    # 1. THE EYE (Signal Analysis)
    # This creates the 600 silence segments in the DB
    eye_script = os.path.join(ROOT_DIR, "src", "signal_analysis", "signal_processor.py")
    run_script(eye_script)

    # 2. THE BRAIN (Director)
    # This creates the JSON screenplay based on keywords
    brain_script = os.path.join(ROOT_DIR, "src", "ai_logic", "keyword_director.py")
    run_script(brain_script)

    # 3. THE VISUALIST (Image Generation)
    # This downloads the free images and indexes them in the DB
    visualist_script = os.path.join(ROOT_DIR, "src", "ai_logic", "visualist_generator.py")
    run_script(visualist_script)

    print("="*50)
    print("🚀 MASTER PIPELINE COMPLETE")
    print("📊 Project Memory DB is now fully populated.")
    print("="*50)

if __name__ == "__main__":
    run_master_pipeline()