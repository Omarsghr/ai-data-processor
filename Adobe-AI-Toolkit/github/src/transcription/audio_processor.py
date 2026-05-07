from moviepy import VideoFileClip
import os


def extract_audio(video_input, audio_output="temp_audio.mp3"):
    # Converts video to mp3 to prepare for AI transcription.
    try:
        if not os.path.exists(video_input):
            print(f"Error: {video_input} not found.")
            print(f"Current working directory: {os.getcwd()}")
            return None

        print(f"--- Processing: {video_input} ---")

        # Use 'with' statement to ensure the file is closed correctly
        with VideoFileClip(video_input) as video:

            if video.audio is None:
                print("هذا الفيديو لا يحتوي على صوت.")
                return None

            print("Extracting audio track...")

            # Write the audio file
            video.audio.write_audiofile(audio_output, bitrate="192k")

        print(f"Audio extracted successfully: {audio_output}")
        return audio_output

    except Exception as e:
        print(f"Error processing {video_input}: {e}")
        return None


class AudioProcessor:
    def process_video(self, video_path):
        audio_file = extract_audio(video_path)
        if audio_file:
            # Placeholder for transcription logic
            return "Transcription placeholder text."
        return None


if __name__ == "__main__":
    # Test it with your file
    extract_audio("video.mp4")

    processor = AudioProcessor()
    
    # 1. Automatically find any .mp4 file in the current folder
    video_files = [f for f in os.listdir('.') if f.endswith('.mp4')]
    
    if video_files:
        target_video = video_files[0] # Pick the first video found
        print(f"🚀 Auto-Detected: {target_video}")
        
        # 2. Run the full pipeline
        result = processor.process_video(target_video)
        
        if result:
            print(f"--- 🎯 Transcription Complete for {target_video} ---")
            print(f"Preview: {result[:100]}...")
    else:
        print("❌ No .mp4 files found in the directory. Drop a video here to test!")