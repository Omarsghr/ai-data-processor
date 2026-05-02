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
      # 2. Use 'with' statement to ensure the file is closed correctly after
        with VideoFileClip(video_input) as video:
            print("Extracting audio track...")
            # 3. Write the audio file
            video.audio.write_audiofile(audio_output, bitrate="192k")
        print(f"audio extracted successfully: {audio_output}")
        return audio_output
    except Exception as e:
        print(f"error processing {video_input}: {e}")


if __name__ == "__main__":
    # Test it with your file
    extract_audio("video.mp4")
