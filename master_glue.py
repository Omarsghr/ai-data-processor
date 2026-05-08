import subprocess
import os

def find_file(filename, search_path):
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None

def main():
    python_exe = r"C:\Users\DELL\AppData\Local\Python\pythoncore-3.14-64\python.exe"
    
    # Get current directory
    current_dir = os.getcwd()
    
    # List of files we need, in order
    pipeline_files = [
        ("AUDIO EXTRACTION", "audio_processor.py"),
        ("AI TRANSCRIPTION", "transcription_manager.py"),
        ("SILENCE ANALYSIS", "signal_processor.py"),
        ("DIRECTOR LOGIC", "keyword_director.py")
    ]

    print("🚀 ADOBE-AI-TOOLKIT: AUTO-LOCATING PIPELINE COMPONENTS")

    for step_name, filename in pipeline_files:
        print(f"\n▶️ {step_name}...")
        file_path = find_file(filename, current_dir)
        
        if file_path:
            print(f"✅ Found: {file_path}")
            try:
                # Run script in its own folder to avoid import errors
                subprocess.run([python_exe, file_path], cwd=os.path.dirname(file_path), check=True)
            except Exception as e:
                print(f"⚠️ Error in {step_name}: {e}")
                break
        else:
            print(f"❌ FAILED: Could not find {filename} anywhere in {current_dir}")

if __name__ == "__main__":
    main()