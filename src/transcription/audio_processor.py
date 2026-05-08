import os
import subprocess

def extract_audio(video_path, output_audio_path):
    """Uses FFmpeg to extract high-quality mp3 from video."""
    print(f"🎬 Processing: {os.path.basename(video_path)}")
    
    # Absolute path to ffmpeg.exe (adjust if your ffmpeg is in a different spot)
    ffmpeg_exe = r"C:\Users\DELL\OneDrive\Desktop\auto--editor__AI\ffmpeg.exe"
    
    # FFmpeg command: -i (input), -q:a 0 (best quality), -map a (audio only)
    command = [
        ffmpeg_exe, "-i", video_path,
        "-q:a", "0", "-map", "a",
        "-y", output_audio_path # -y forces overwrite
    ]

    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        print(f"✅ Audio Extraction Successful: {output_audio_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg Error: {e}")
        return False

if __name__ == "__main__":
    # --- ARCHITECT PATHS ---
    # We force the root to be the auto--editor__AI folder
    root_dir = r"C:\Users\DELL\OneDrive\Desktop\auto--editor__AI"
    output_audio = os.path.join(root_dir, "temp_audio.mp3")

    # Find ANY video file in the root folder to process
    video_files = [f for f in os.listdir(root_dir) if f.endswith(('.mp4', '.mkv', '.mov'))]

    if video_files:
        target_video = os.path.join(root_dir, video_files[0]) # Picks the first video found
        extract_audio(target_video, output_audio)
    else:
        print(f"❌ Error: No video files (.mp4, .mkv, .mov) found in {root_dir}")