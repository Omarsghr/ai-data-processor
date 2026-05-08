import os
import subprocess
import sys

# Configuration
ROOT_DIR = r"C:\Users\DELL\OneDrive\Desktop\auto--editor__AI"
PYTHON_EXE = sys.executable 

def run_script(script_path, args=None):
    """Helper to run a sub-script with optional arguments."""
    print(f"--- Running: {os.path.basename(script_path)} ---")
    
    # We add args so we can pass the audio filename to the sub-scripts
    command = [PYTHON_EXE, script_path]
    if args:
        command.extend(args)
        
    result = subprocess.run(command, capture_output=False)
    if result.returncode != 0:
        print(f"❌ Error in {script_path}. Stopping pipeline.")
        return False
    return True

def run_master_pipeline(target_audio=None):
    """
    The main engine. If target_audio is provided (from Server), 
    it processes that specific file.
    """
    print("\n🎬 === STARTING AUTO-EDITOR AI MASTER GLUE === 🎬\n")
    
    # Prepare arguments for sub-scripts (like the filename)
    args = [target_audio] if target_audio else []

    # 1. THE EYE (Signal Analysis)
    eye_script = os.path.join(ROOT_DIR, "src", "signal_analysis", "signal_processor.py")
    if not run_script(eye_script, args): return

    # 2. THE BRAIN (Director)
    brain_script = os.path.join(ROOT_DIR, "src", "ai_logic", "keyword_director.py")
    if not run_script(brain_script, args): return

    # 3. THE VISUALIST (Image Generation)
    visualist_script = os.path.join(ROOT_DIR, "src", "ai_logic", "visualist_generator.py")
    if not run_script(visualist_script, args): return

    print("="*50)
    print("🚀 MASTER PIPELINE COMPLETE")
    print("="*50)
    return "adobe_screenplay.json" # Return the final result for the server

if __name__ == "__main__":
    # If you run it manually:
    run_master_pipeline()